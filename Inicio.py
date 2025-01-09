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