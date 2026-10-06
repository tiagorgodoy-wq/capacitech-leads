import os
import sys
import re
import io
import pandas as pd
import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA E TEMA (WEG / CAPACITECH)
# ==============================================================================
st.set_page_config(
    page_title="CAPACITECH | Inteligência Comercial WEG",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada (Cores WEG: Azul #00579E, Azul Marinho #003B6D, Ciano #00A3E0)
st.markdown("""
<style>
    /* Estilo geral */
    .main-header {
        background: linear-gradient(135deg, #003B6D 0%, #00579E 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        margin: 0;
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
    }
    .main-header p {
        margin: 5px 0 0 0;
        font-size: 14px;
        color: #E0F2FE;
    }
    /* Cards de métricas */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        text-align: center;
        border-top: 4px solid #00579E;
    }
    .metric-val {
        font-size: 28px;
        font-weight: 800;
        color: #0F172A;
    }
    .metric-lbl {
        font-size: 12px;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
    }
    /* Badges */
    .badge-anel1 {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    .badge-anel2 {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    .badge-anel3 {
        background-color: #F1F5F9;
        color: #475569;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    /* Botões de Ação Direta */
    .btn-zap {
        background-color: #25D366;
        color: white !important;
        text-decoration: none;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SISTEMA DE AUTENTICAÇÃO E LOGIN SEGURO
# ==============================================================================

# Credenciais padrão (podem ser substituídas por st.secrets ou variáveis de ambiente)
AUTH_USER = st.secrets.get("AUTH_USER", "admin")
AUTH_PASSWORD = st.secrets.get("AUTH_PASSWORD", "capacitech2026")

def check_login():
    """Valida o login e mantém o estado na sessão."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="background: white; padding: 32px; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.06); text-align: center;">
                <div style="font-size: 40px; margin-bottom: 8px;">⚡</div>
                <h2 style="color: #003B6D; margin: 0 0 8px 0;">CAPACITECH | WEG</h2>
                <p style="color: #64748B; font-size: 14px; margin-bottom: 24px;">Painel Restrito de Inteligência Comercial Radial B2B</p>
            """, unsafe_allow_html=True)

            username_input = st.text_input("Usuário", key="login_user", placeholder="Digite seu usuário")
            password_input = st.text_input("Senha", type="password", key="login_pass", placeholder="Digite sua senha")
            btn_login = st.button("Acessar Painel Comercial", use_container_width=True, type="primary")

            if btn_login:
                if username_input == AUTH_USER and password_input == AUTH_PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Credenciais inválidas. Verifique usuário e senha.")

            st.markdown("</div>", unsafe_allow_html=True)
        return False
    return True

if not check_login():
    st.stop()

# ==============================================================================
# CARREGAMENTO E TRATAMENTO DA BASE DE LEADS
# ==============================================================================

CSV_PATH = "leads_eletrica_capacitech_200km.csv"

@st.cache_data(ttl=60)
def load_leads_data():
    """Carrega a base de leads, suportando múltiplos arquivos se disponíveis."""
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8-sig", dtype=str)
    elif os.path.exists("leads_anel1.csv"):
        # Carrega arquivos particionados e combina
        dfs = []
        for p in ["leads_anel1.csv", "leads_anel2.csv", "leads_anel3.csv"]:
            if os.path.exists(p):
                dfs.append(pd.read_csv(p, sep=";", encoding="utf-8", dtype=str))
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
        else:
            return pd.DataFrame()
    else:
        return pd.DataFrame()

    # Preenchimento de nulos
    for col in df.columns:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # Conversão de Porte_Estimado para numérico para ordenação
    if "Porte_Estimado" in df.columns:
        df["Porte_Num"] = pd.to_numeric(df["Porte_Estimado"].str.replace(r'\D', '', regex=True), errors="coerce").fillna(0).astype(int)
    else:
        df["Porte_Num"] = 0

    return df

df_raw = load_leads_data()

# ==============================================================================
# BARRA LATERAL (FILTROS E AÇÕES)
# ==============================================================================

with st.sidebar:
    st.markdown("### ⚡ **CAPACITECH**")
    st.caption("Revenda Autorizada WEG")
    st.markdown("---")

    # Botão de Logout
    if st.button("🚪 Sair do Sistema"):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown("### 🔍 **Filtros de Prospecção**")

    # Filtro por Anel Radial
    aneis_disponiveis = ["Anel 1", "Anel 2", "Anel 3"]
    if not df_raw.empty and "Prioridade_Anel" in df_raw.columns:
        presentes = [a for a in aneis_disponiveis if a in df_raw["Prioridade_Anel"].unique()]
    else:
        presentes = aneis_disponiveis

    filtro_aneis = st.multiselect(
        "Prioridade Radial",
        options=aneis_disponiveis,
        default=presentes,
        help="Anel 1 (0-40km), Anel 2 (41-100km), Anel 3 (101-200km)"
    )

    # Filtro por Cidade
    if not df_raw.empty and "Cidade" in df_raw.columns:
        cidades_todas = sorted(df_raw[df_raw["Prioridade_Anel"].isin(filtro_aneis)]["Cidade"].unique())
    else:
        cidades_todas = []

    filtro_cidades = st.multiselect(
        "Cidades",
        options=cidades_todas,
        default=[],
        placeholder="Todas as cidades selecionadas"
    )

    # Filtro por Canais de Contato
    st.markdown("#### **Canais de Contato**")
    apenas_whatsapp = st.checkbox("Apenas com WhatsApp direto", value=False)
    apenas_email = st.checkbox("Apenas com E-mail corporativo", value=False)
    apenas_site = st.checkbox("Apenas com Site / Instagram", value=False)

    # Filtro por Porte
    min_avaliacoes = st.slider("Mínimo de Avaliações (Fluxo)", 0, 500, 0, step=10)

    st.markdown("---")
    st.caption("Desenvolvido para inteligência de vendas B2B da Capacitech.")

# ==============================================================================
# FILTRAGEM DOS DADOS
# ==============================================================================

if df_raw.empty:
    st.warning("Nenhum dado encontrado no arquivo CSV. O minerador pode estar inicializando.")
    st.stop()

df_filtered = df_raw.copy()

if filtro_aneis:
    df_filtered = df_filtered[df_filtered["Prioridade_Anel"].isin(filtro_aneis)]

if filtro_cidades:
    df_filtered = df_filtered[df_filtered["Cidade"].isin(filtro_cidades)]

if apenas_whatsapp:
    df_filtered = df_filtered[df_filtered["WhatsApp"].str.len() > 3]

if apenas_email:
    df_filtered = df_filtered[df_filtered["Email"].str.contains("@", na=False)]

if apenas_site:
    df_filtered = df_filtered[df_filtered["Website_Instagram"].str.len() > 3]

if min_avaliacoes > 0:
    df_filtered = df_filtered[df_filtered["Porte_Num"] >= min_avaliacoes]

# Campo de busca livre
busca_termo = st.text_input("🔎 Pesquisar por Razão Social, Nome Fantasia, Telefone ou E-mail:", placeholder="Ex: Broketto, automação, (16), vendas@...")
if busca_termo:
    b = busca_termo.lower()
    df_filtered = df_filtered[
        df_filtered["Nome_Empresa"].str.lower().str.contains(b, na=False) |
        df_filtered["Cidade"].str.lower().str.contains(b, na=False) |
        df_filtered["Telefone_Fixo"].str.contains(b, na=False) |
        df_filtered["WhatsApp"].str.contains(b, na=False) |
        df_filtered["Email"].str.lower().str.contains(b, na=False)
    ]

# Ordenação: Anel (1 -> 2 -> 3) depois Porte desc
ring_weights = {"Anel 1": 1, "Anel 2": 2, "Anel 3": 3}
df_filtered["Peso_Anel"] = df_filtered["Prioridade_Anel"].map(ring_weights).fillna(99)
df_filtered = df_filtered.sort_values(by=["Peso_Anel", "Porte_Num"], ascending=[True, False]).drop(columns=["Peso_Anel"])

# ==============================================================================
# HEADER PRINCIPAL & MÉTRICAS
# ==============================================================================

st.markdown("""
<div class="main-header">
    <h1>⚡ AGENTE DE INTELIGÊNCIA COMERCIAL: PROSPECÇÃO RADIAL B2B</h1>
    <p>CAPACITECH (Revenda Autorizada WEG) &bull; Mapeamento Qualificado no Raio de 200 km de Ribeirão Preto/SP</p>
</div>
""", unsafe_allow_html=True)

# KPIs em cards
tot_leads = len(df_filtered)
tot_zap = len(df_filtered[df_filtered["WhatsApp"].str.len() > 3])
tot_email = len(df_filtered[df_filtered["Email"].str.contains("@", na=False)])
tot_site = len(df_filtered[df_filtered["Website_Instagram"].str.len() > 3])

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val">{tot_leads:,}</div>
        <div class="metric-lbl">Total de Leads Mapeados</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    pct_zap = (tot_zap / max(1, tot_leads)) * 100
    st.markdown(f"""
    <div class="metric-card" style="border-top-color: #25D366;">
        <div class="metric-val">{tot_zap:,} <span style="font-size:16px; color:#16A34A;">({pct_zap:.1f}%)</span></div>
        <div class="metric-lbl">WhatsApp Direto Validado</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    pct_em = (tot_email / max(1, tot_leads)) * 100
    st.markdown(f"""
    <div class="metric-card" style="border-top-color: #0284C7;">
        <div class="metric-val">{tot_email:,} <span style="font-size:16px; color:#0284C7;">({pct_em:.1f}%)</span></div>
        <div class="metric-lbl">E-mails Comerciais/Compras</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    pct_site = (tot_site / max(1, tot_leads)) * 100
    st.markdown(f"""
    <div class="metric-card" style="border-top-color: #9333EA;">
        <div class="metric-val">{tot_site:,} <span style="font-size:16px; color:#9333EA;">({pct_site:.1f}%)</span></div>
        <div class="metric-lbl">Presença Web / Instagram</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# ABAS DE VISUALIZAÇÃO: TABELA & EXPORTAÇÃO
# ==============================================================================

tab_tabela, tab_export, tab_graficos = st.tabs(["📋 Lista de Leads Qualificados", "📥 Exportar Dados (CSV / Excel)", "📊 Análise de Cobertura"])

with tab_tabela:
    st.markdown(f"**Exibindo {len(df_filtered)} empresas qualificadas** de acordo com os filtros aplicados.")

    # Colunas para exibição na tabela interativa
    display_cols = [
        "Prioridade_Anel",
        "Cidade",
        "Nome_Empresa",
        "Telefone_Fixo",
        "WhatsApp",
        "Email",
        "Porte_Estimado",
        "Website_Instagram",
        "Link_GoogleMaps"
    ]
    
    # Renderiza tabela interativa com links clicáveis nativos do Streamlit
    st.dataframe(
        df_filtered[display_cols],
        column_config={
            "Prioridade_Anel": st.column_config.TextColumn("Anel Radial", width="medium"),
            "Cidade": st.column_config.TextColumn("Cidade", width="medium"),
            "Nome_Empresa": st.column_config.TextColumn("Empresa / Revenda", width="large"),
            "Telefone_Fixo": st.column_config.TextColumn("Fixo", width="medium"),
            "WhatsApp": st.column_config.TextColumn("WhatsApp", width="medium"),
            "Email": st.column_config.TextColumn("E-mail", width="large"),
            "Porte_Estimado": st.column_config.NumberColumn("Avaliações (Fluxo)", format="%d"),
            "Website_Instagram": st.column_config.LinkColumn("Site / Insta", width="medium"),
            "Link_GoogleMaps": st.column_config.LinkColumn("Ficha Google Maps", width="medium")
        },
        hide_index=True,
        use_container_width=True,
        height=550
    )

with tab_export:
    st.markdown("### 📥 **Download da Base Qualificada**")
    st.write("Baixe a lista completa ou a seleção atual filtrada para abastecer seu CRM, disparadores ou planilhas de SDR.")

    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        st.markdown("#### **Formato CSV (Excel UTF-8)**")
        csv_buffer = io.StringIO()
        df_filtered[[
            "Prioridade_Anel", "Cidade", "Nome_Empresa", "Telefone_Fixo",
            "WhatsApp", "Email", "Website_Instagram", "Link_GoogleMaps", "Porte_Estimado"
        ]].to_csv(csv_buffer, sep=";", index=False, encoding="utf-8-sig")

        st.download_button(
            label="📄 Baixar Base em CSV (;)",
            data=csv_buffer.getvalue().encode("utf-8-sig"),
            file_name="leads_eletrica_capacitech_200km.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True
        )

    with col_exp2:
        st.markdown("#### **Formato Microsoft Excel (.xlsx)**")
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df_filtered[[
                "Prioridade_Anel", "Cidade", "Nome_Empresa", "Telefone_Fixo",
                "WhatsApp", "Email", "Website_Instagram", "Link_GoogleMaps", "Porte_Estimado"
            ]].to_excel(writer, index=False, sheet_name="Leads_Capacitech")

        st.download_button(
            label="📊 Baixar Base em Excel (.xlsx)",
            data=excel_buffer.getvalue(),
            file_name="leads_eletrica_capacitech_200km.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

with tab_graficos:
    st.markdown("### 📊 **Distribuição Geográfica e Potencial Comercial**")
    cg1, cg2 = st.columns(2)

    with cg1:
        st.markdown("#### **Leads por Anel Radial**")
        anel_counts = df_filtered["Prioridade_Anel"].value_counts().reset_index()
        anel_counts.columns = ["Anel", "Quantidade"]
        st.bar_chart(data=anel_counts.set_index("Anel"))

    with cg2:
        st.markdown("#### **Top 10 Cidades com Maior Concentração de Lojas**")
        city_counts = df_filtered["Cidade"].value_counts().head(10).reset_index()
        city_counts.columns = ["Cidade", "Quantidade"]
        st.bar_chart(data=city_counts.set_index("Cidade"))
