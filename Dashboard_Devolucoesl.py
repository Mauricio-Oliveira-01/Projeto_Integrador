import os
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Devoluções por Marketplace", layout="wide")
st.title("Controle de Devoluções por Marketplace")
st.caption("Use os filtros da barra lateral para consultar cada marketplace separadamente.")

ARQUIVOS = {
    "Mercado Livre": "MERCADO LIVRE.csv",
    "Amazon": "ARMAZON.csv",
    "KaBuM!": "KABUM.csv",
    "Shopee": "SHOOP.csv",
    "Magalu": "MAGALU.csv",
}

@st.cache_data
def ler_csv(caminho):
    try:
        df = pd.read_csv(caminho, sep=";", encoding="ISO-8859-1")
    except UnicodeDecodeError:
        df = pd.read_csv(caminho, sep=";", encoding="utf-8-sig")
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

def preparar(df):
    df = df.copy()
    if "DATA" in df.columns:
        df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")
        df["MES"] = df["DATA"].dt.strftime("%m-%Y")
    if "QUANTIDADE" in df.columns:
        df["QUANTIDADE"] = pd.to_numeric(df["QUANTIDADE"], errors="coerce").fillna(0)
    return df

dados = {}
for nome, arquivo in ARQUIVOS.items():
    if os.path.exists(arquivo):
        try:
            dados[nome] = preparar(ler_csv(arquivo))
        except Exception as erro:
            st.sidebar.error(f"Erro ao ler {arquivo}: {erro}")
    else:
        st.sidebar.warning(f"Arquivo não encontrado: {arquivo}")

st.sidebar.header("Filtros")
marketplace = st.sidebar.selectbox("Marketplace", list(ARQUIVOS.keys()))
if marketplace not in dados:
    st.error(f"Não foi possível carregar a planilha de {marketplace}. Verifique se o CSV está na mesma pasta do programa.")
    st.stop()

df = dados[marketplace]
meses = sorted(df["MES"].dropna().unique().tolist(),
               key=lambda x: pd.to_datetime(x, format="%m-%Y", errors="coerce")) if "MES" in df.columns else []
mes = st.sidebar.selectbox("Mês", ["Todos"] + meses, index=1 if meses else 0)
if mes != "Todos" and "MES" in df.columns:
    df = df[df["MES"] == mes]

if "DEFEITO" in df.columns:
    defeito = st.sidebar.selectbox("Defeito", ["Todos"] + sorted(df["DEFEITO"].dropna().astype(str).unique()))
    if defeito != "Todos":
        df = df[df["DEFEITO"].astype(str) == defeito]
if "STATOS" in df.columns:
    status = st.sidebar.selectbox("Status", ["Todos"] + sorted(df["STATOS"].dropna().astype(str).unique()))
    if status != "Todos":
        df = df[df["STATOS"].astype(str) == status]
if "SITUAÇÃO" in df.columns:
    situacao = st.sidebar.selectbox("Situação", ["Todas"] + sorted(df["SITUAÇÃO"].dropna().astype(str).unique()))
    if situacao != "Todas":
        df = df[df["SITUAÇÃO"].astype(str) == situacao]

st.header(f"Devoluções — {marketplace}")
st.caption(f"Arquivo de origem: {ARQUIVOS[marketplace]} · {len(df)} registros")
c1, c2, c3 = st.columns(3)
c1.metric("Registros", len(df))
c2.metric("Quantidade total", f"{df['QUANTIDADE'].sum():,.0f}".replace(",", ".") if "QUANTIDADE" in df.columns else "N/D")
c3.metric("Ordens de serviço", df["OS"].nunique() if "OS" in df.columns else "N/D")

col1, col2 = st.columns(2)
if "DATA" in df.columns and "QUANTIDADE" in df.columns:
    d = df.dropna(subset=["DATA"]).groupby("DATA", as_index=False)["QUANTIDADE"].sum()
    if not d.empty:
        col1.plotly_chart(px.bar(d, x="DATA", y="QUANTIDADE", title="Devoluções por data"), use_container_width=True)
if "PRODUTO" in df.columns and "QUANTIDADE" in df.columns:
    p = df.groupby("PRODUTO", as_index=False)["QUANTIDADE"].sum().sort_values("QUANTIDADE", ascending=False).head(15)
    if not p.empty:
        col2.plotly_chart(px.bar(p, x="QUANTIDADE", y="PRODUTO", orientation="h", title="Produtos que mais retornaram"), use_container_width=True)
if "SITUAÇÃO" in df.columns and "QUANTIDADE" in df.columns:
    s = df.groupby("SITUAÇÃO", as_index=False)["QUANTIDADE"].sum()
    if not s.empty:
        st.plotly_chart(px.pie(s, values="QUANTIDADE", names="SITUAÇÃO", title="Situação das devoluções"), use_container_width=True)

st.subheader(f"Produtos devolvidos — {marketplace}")
st.dataframe(df, use_container_width=True, hide_index=True)
csv = df.to_csv(index=False, sep=";", encoding="ISO-8859-1", date_format="%d/%m/%Y").encode("ISO-8859-1", errors="replace")
st.download_button("Baixar CSV filtrado", data=csv, file_name=f"Devolucoes_{marketplace.replace(' ', '_')}.csv", mime="text/csv")
