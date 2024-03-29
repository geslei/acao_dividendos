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

ticker = st.text_input('Digite o ticker da ação', 'VALE3')

# Verifica se o ticker foi inserido


col_1 , col_2 = st.columns([1,1])
with col_1:
    data_inicio = st.date_input("De", value=datetime.date.today() - datetime.timedelta(days=365))
with col_2:
    data_fim = st.date_input("Até", value=datetime.date.today())

# # Converte as datas para string no formato 'YYYY-MM-DD'
start_date = data_inicio.strftime("%Y-%m-%d")
end_date = data_fim.strftime("%Y-%m-%d")


empresa = yf.Ticker(f"{ticker}.SA")
tickerDF = empresa.history(period='1d', start=start_date, end=end_date)
# Calcule o índice de Sharpe
retornos = tickerDF['Close'].pct_change().dropna()
indice_sharpe = qs.stats.sharpe(retornos)
volatilidade = qs.stats.volatility(retornos)


col1, col2, col3, col4 = st.columns([1,1,1,1])
if ticker:
    with col1:
        st.write(f" Nome da empresa: {empresa.info['longName']}")
    with col2:
        st.write(f"Cotação Atual: {empresa.info['currentPrice']} BRL")
    with col3:
        st.write(f"Índice de Sharpe: {indice_sharpe:.2f}")  
    with col4:
        st.write(f" Volatilidade:{volatilidade:.2f}")     
    
st.line_chart(tickerDF.Close)
st.bar_chart(tickerDF.Dividends)
st.dataframe(tickerDF)
