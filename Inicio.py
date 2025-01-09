import streamlit as st
from utils.queries import *


st.set_page_config(
  initial_sidebar_state="collapsed",
  page_title="Início",
  page_icon=":money_with_wings:",
  layout="wide",
)


st.title("Análise Couvert Artístico")

lucro_couvert = GET_FATURAMENTO_COUVERT()
gastos_eshows = GET_GASTOS_ESHOWS()

merged_df = lucro_couvert.merge(gastos_eshows, on='Data Evento', how='outer')
merged_df.fillna(0, inplace=True)
merged_df['Lucro'] = merged_df['Valor Liquido'] - merged_df['Valor Gasto']

total_lucro = merged_df['Lucro'].sum()
total_lucro = f"{total_lucro:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

row = st.columns([3, 6, 3])
with row[1]:
  st.dataframe(merged_df, hide_index=True)
  row2 = st.columns([1, 6, 1])
  with row2[1]:
    with st.container(border=True): 
      st.write(f"Total de lucro: R${total_lucro}")

st.title('Shows dos dias selecionados')
row3 = st.columns([7, 3])
with row3[0]:
    days = st.multiselect("Escolha a data:", (merged_df['Data Evento']), placeholder="Selecione a Data", default=None)
row = st.columns([3, 5, 3])
with row[1]:
  shows = GET_SHOWS()
  # Converta a coluna 'DATA EVENTO' para datetime (se necessário)
  shows['Data Evento'] = pd.to_datetime(shows['Data Evento'], format='%Y-%m-%d')
  if days:
    # Converte as datas selecionadas para o mesmo tipo de 'DATA EVENTO'
    days = pd.to_datetime(days, format='%Y-%m-%d')
    shows = shows[shows['Data Evento'].isin(days)]
  shows['Data Evento'] = shows['Data Evento'].dt.date
  st.dataframe(shows, hide_index=True)
