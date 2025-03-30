
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import openai

# Configuração do título
st.set_page_config(page_title="Painel Investidor Nato", layout="wide")
st.title("📊 Painel Inteligente - Investidor Nato")

# Seção de upload ou dados simulados
st.subheader("📂 Sua Carteira")
if "carteira" not in st.session_state:
    st.session_state.carteira = pd.DataFrame({
        "Ativo": ["MXRF11", "HGLG11", "TAEE11"],
        "Tipo": ["FII", "FII", "Ação"],
        "Classe": ["Papel", "Tijolo", "Energia"],
        "Aporte (R$)": [20000, 30000, 50000],
        "DY Anual (%)": [11.5, 9.0, 12.0]
    })

df = st.session_state.carteira
df["Renda Anual Estimada (R$)"] = df["Aporte (R$)"] * (df["DY Anual (%)"] / 100)
df["Renda Mensal Estimada (R$)"] = df["Renda Anual Estimada (R$)"] / 12

st.dataframe(df)

# Gráfico de distribuição
st.subheader("📈 Gráfico de Distribuição da Carteira")
fig, ax = plt.subplots()
ax.pie(df["Aporte (R$)"], labels=df["Ativo"], autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)

# Simulador de Renda
st.subheader("💰 Renda Passiva Estimada")
st.metric(label="Total Mensal Estimado", value=f"R$ {df['Renda Mensal Estimada (R$)'].sum():,.2f}")
st.metric(label="Total Anual Estimado", value=f"R$ {df['Renda Anual Estimada (R$)'].sum():,.2f}")

# Integração com IA (simples)
st.subheader("🤖 Consultar IA")
pergunta = st.text_input("Digite uma pergunta para a IA sobre sua carteira:")
if pergunta and "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": pergunta}]
    )
    st.write(resposta.choices[0].message["content"])
elif pergunta:
    st.warning("Chave da API da OpenAI não configurada. Configure em st.secrets.")
