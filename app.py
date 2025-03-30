
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URL da planilha oficial
csv_url = "https://docs.google.com/spreadsheets/d/1OaLfhcQheje1b7T2eBvF6pWAyYAZ8yhIdUO2swe1enQ/export?format=csv"

st.set_page_config(page_title="Investidor Nato", layout="wide")
st.title("📊 Painel Inteligente - Investidor Nato")

# Carregar dados da planilha
df = pd.read_csv(csv_url)

# Filtros interativos
st.sidebar.header("🔎 Filtros")
tipo_filtrado = st.sidebar.multiselect("Tipo de Ativo", options=df["Tipo"].unique(), default=list(df["Tipo"].unique()))
setor_filtrado = st.sidebar.multiselect("Setor", options=df["Setor"].dropna().unique(), default=list(df["Setor"].dropna().unique()))

# Aplicar filtros
df_filtrado = df[(df["Tipo"].isin(tipo_filtrado)) & (df["Setor"].isin(setor_filtrado))]

# Calcular renda se colunas existirem
if "Aporte (R$)" in df_filtrado.columns and "Dividend Yield" in df_filtrado.columns:
    df_filtrado["Renda Anual Estimada (R$)"] = df_filtrado["Aporte (R$)"] * (df_filtrado["Dividend Yield"] / 100)
    df_filtrado["Renda Mensal Estimada (R$)"] = df_filtrado["Renda Anual Estimada (R$)"] / 12

    st.subheader("💰 Renda Passiva Estimada (após filtro)")
    st.metric("Renda Mensal", f"R$ {df_filtrado['Renda Mensal Estimada (R$)'].sum():,.2f}")
    st.metric("Renda Anual", f"R$ {df_filtrado['Renda Anual Estimada (R$)'].sum():,.2f}")

# Tabela com destaque visual
st.subheader("📋 Carteira Filtrada com Destaques")
def cor_dy(val):
    media = df_filtrado["Dividend Yield"].mean()
    if val > media:
        return 'background-color: #d4edda'  # verde claro
    elif val < media:
        return 'background-color: #f8d7da'  # vermelho claro
    return ''

st.dataframe(df_filtrado.style.applymap(cor_dy, subset=["Dividend Yield"]))

# Gráfico de alocação por ativo
if "Aporte (R$)" in df_filtrado.columns:
    st.subheader("📈 Distribuição por Ativo")
    fig1, ax1 = plt.subplots()
    ax1.pie(df_filtrado["Aporte (R$)"], labels=df_filtrado["Ticker/Código"], autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

# Gráfico de distribuição por Tipo
st.subheader("🧱 Distribuição por Tipo de Ativo")
fig2, ax2 = plt.subplots()
df_tipo = df_filtrado.groupby("Tipo")["Aporte (R$)"].sum()
ax2.pie(df_tipo, labels=df_tipo.index, autopct="%1.1f%%", startangle=90)
ax2.axis("equal")
st.pyplot(fig2)

# IA com sugestões de perguntas
st.subheader("🤖 Assistente de Investimentos (IA)")
st.markdown("Sugestões de perguntas:")
st.markdown("- Qual meu ativo com maior DY?")
st.markdown("- Qual a média de dividendos da carteira?")
st.markdown("- Quanto posso receber por mês se reinvestir os proventos?")

pergunta = st.text_input("Digite sua pergunta para a IA:")
if pergunta:
    st.info("⚙️ Integração com IA será ativada com sua chave da OpenAI via `st.secrets`.")
