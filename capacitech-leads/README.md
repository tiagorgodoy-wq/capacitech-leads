# ⚡ CAPACITECH | Painel de Inteligência Comercial B2B (WEG)

Sistema de prospecção, qualificação e inteligência comercial de lojas de materiais elétricos e revendas técnicas em um raio de até **200 km de Ribeirão Preto/SP**, estruturado em **3 anéis radiais de prioridade**.

---

## 📊 Resumo da Base Mapeada

- **Total de Leads Qualificados**: 1.094 revendas e lojas elétricas
- **Anel 1 (0 a 40 km - Imediato)**: 220 estabelecimentos (57.7% com WhatsApp validado)
- **Anel 2 (41 a 100 km - Regional)**: 394 estabelecimentos (41.9% com WhatsApp validado)
- **Anel 3 (101 a 200 km - Expandido)**: 480 estabelecimentos (49.0% com WhatsApp validado)

Arquivo consolidado gerado: `leads_eletrica_capacitech_200km.csv` (formato padrão com delimitador `;` e codificação UTF-8 BOM).

---

## 🔒 Acesso e Credenciais Padrão

Por padrão, a tela de autenticação do painel solicita:
- **Usuário**: `admin`
- **Senha**: `capacitech2026`

> **Como alterar a senha**:
> Você pode alterar diretamente as variáveis `AUTH_USER` e `AUTH_PASSWORD` no arquivo `app.py` ou configurar com segurança máxima nas configurações de segredos (*Secrets*) do Streamlit Cloud.

---

## 🚀 Como Hospedar Gratuitamente na Nuvem (Acesso de Qualquer Computador / Celular)

A melhor opção 100% gratuita, estável e mantida pela comunidade oficial é o **Streamlit Community Cloud**.

### Passo a Passo (Leva menos de 3 minutos):

1. **Crie um repositório no seu GitHub**:
   - Acesse [github.com/new](https://github.com/new) e crie um repositório (pode ser **Público** ou **Privado**), por exemplo: `capacitech-leads`.

2. **Envie os arquivos para o repositório**:
   No terminal desta pasta, execute:
   ```bash
   git init
   git add .
   git commit -m "Painel de Inteligência Comercial Capacitech"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/capacitech-leads.git
   git push -u origin main
   ```

3. **Conecte no Streamlit Community Cloud**:
   - Acesse [share.streamlit.io](https://share.streamlit.io/) e faça login com sua conta do GitHub.
   - Clique em **"New app"**.
   - Selecione o repositório `capacitech-leads`, branch `main`, e o arquivo principal `app.py`.
   - Clique em **"Deploy"**!

4. **Pronto!**
   - Em cerca de 1 a 2 minutos, sua aplicação estará online com um link seguro HTTPS (exemplo: `https://capacitech-leads.streamlit.app`).
   - Qualquer pessoa que acessar esse link precisará do seu **login e senha** para ver os dados.
   - Você pode acessar pelo celular, notebook, tablet ou de qualquer lugar do mundo.

---

## 💻 Como Rodar Localmente

Caso queira abrir o painel na sua própria máquina:

```bash
pip install -r requirements.txt
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

---

## 🛠️ Funcionalidades do Painel

- **Filtro Radial Dinâmico**: Seleção por Anel 1, Anel 2 e Anel 3.
- **Filtro por Cidades**: Seleção múltipla entre os 35 municípios atendidos.
- **Busca Textual Instantânea**: Pesquise por razão social, nome fantasia, rua ou telefone.
- **Ações Rápidas**: Links diretos com um clique para abrir conversa no WhatsApp (`wa.me`) e ficha no Google Maps.
- **Exportação Multiformato**: Download dos leads filtrados em **CSV** ou **Planilha Excel (.xlsx)** formatada.
- **Gráficos e Indicadores**: Distribuição geográfica, cobertura de WhatsApp e ranking de porte estimado por avaliações.
