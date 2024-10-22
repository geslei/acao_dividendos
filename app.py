import yfinance as yf
import streamlit as st
import datetime
import pandas as pd
import quantstats as qs

qs.extend_pandas()

st.set_page_config(
    page_title='DASHBOARD FINANCEIRO - AÇÕES',
    layout='wide')

st.header("Cotação de Ações e Dividendos")

# Verifica se o ticker foi inserido
col_1, col_2, col_3 = st.columns([1, 0.5, 0.5])
with col_1:
    ticker = st.text_input('Digite o ticker da ação', 'VALE3')
with col_2:
    data_inicio = st.date_input("De", value=datetime.date.today() - datetime.timedelta(days=365))
with col_3:
    data_fim = st.date_input("Até", value=datetime.date.today())

# Converte as datas para string no formato 'YYYY-MM-DD'
start_date = data_inicio.strftime("%Y-%m-%d")
end_date = data_fim.strftime("%Y-%m-%d")

empresa = yf.Ticker(f"{ticker}.SA")
tickerDF = empresa.history(period='1d', start=start_date, end=end_date)

# Calcule o índice de Sharpe
retornos = tickerDF['Close'].pct_change().dropna()
indice_sharpe = qs.stats.sharpe(retornos) * 100  # Convertendo para porcentagem

# Calcular a volatilidade
volatilidade = qs.stats.volatility(retornos) * 100  # Convertendo para porcentagem

col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
if ticker:
    with col1:
        st.write(f"Nome da empresa: {empresa.info['longName']}")
    with col2:
        st.write(f"Cotação Atual: {empresa.info['currentPrice']} BRL")
    with col3:
        st.write(f"Índice de Sharpe: {indice_sharpe:.2f}%")  # Exibindo o índice de Sharpe em porcentagem
    with col4:
        st.write(f"Volatilidade: {volatilidade:.2f}%")  # Exibindo a volatilidade em porcentagem
    with col5:
        st.write(f"Setor: {empresa.info['industry']}")  # Exibindo a indústria do ativo

st.line_chart(tickerDF.Close)
st.bar_chart(tickerDF.Dividends)
st.dataframe(tickerDF)
