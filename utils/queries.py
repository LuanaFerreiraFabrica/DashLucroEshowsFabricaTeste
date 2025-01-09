import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import mysql.connector


LOGGER = get_logger(__name__)

def mysql_connection(empresa):
  if empresa == "fabrica":
    mysql_config = st.secrets["mysql_fabrica"]
  else:
    mysql_config = st.secrets["mysql_eshows"]
  conn = mysql.connector.connect(
    host=mysql_config['host'],
    port=mysql_config['port'],
    database=mysql_config['database'],
    user=mysql_config['username'],
    password=mysql_config['password']
  )    
  return conn

def execute_query(query, empresa):
  conn = mysql_connection(empresa)
  cursor = conn.cursor()
  cursor.execute(query)
  # Obter nomes das colunas
  column_names = [col[0] for col in cursor.description]
  # Obter resultados
  result = cursor.fetchall()
  cursor.close()
  return result, column_names



def dataframe_query(query, empresa):
  resultado, nomeColunas = execute_query(query, empresa)
  dataframe = pd.DataFrame(resultado, columns=nomeColunas)
  return dataframe



@st.cache_data
def GET_FATURAMENTO_COUVERT():
  return dataframe_query(''' 
  SELECT
    te.NOME_FANTASIA AS 'Loja',
    cast(tiv.EVENT_DATE as date) AS 'Data Evento',
    SUM(tiv.UNIT_VALUE * tiv.COUNT) AS 'Valor Bruto',
    SUM(tiv.DISCOUNT_VALUE) AS Desconto,
    SUM((tiv.UNIT_VALUE * tiv.COUNT) - tiv.DISCOUNT_VALUE) AS 'Valor Liquido'
  FROM T_ITENS_VENDIDOS tiv
  LEFT JOIN T_ITENS_VENDIDOS_CADASTROS tivc ON tiv.PRODUCT_ID = tivc.ID_ZIGPAY
  LEFT JOIN T_ITENS_VENDIDOS_CATEGORIAS tivc2 ON tivc.FK_CATEGORIA = tivc2.ID
  LEFT JOIN T_ITENS_VENDIDOS_TIPOS tivt ON tivc.FK_TIPO = tivt.ID
  LEFT JOIN T_EMPRESAS te ON tiv.LOJA_ID = te.ID_ZIGPAY
  WHERE tivc2.DESCRICAO = 'Couvert'
  	AND te.ID = 148
  GROUP BY tiv.EVENT_DATE
  ORDER BY tiv.EVENT_DATE
  ''', "fabrica")

@st.cache_data
def GET_GASTOS_ESHOWS():
  return dataframe_query('''
  SELECT 
    CAST(P.DATA_INICIO AS DATE) AS 'Data Evento',
    SUM(P.VALOR_BRUTO) AS 'Valor Gasto'
  FROM T_PROPOSTAS P
  LEFT JOIN T_COMPANIES C ON P.FK_CONTRANTE = C.ID
  WHERE C.ID = '1504'
    AND P.FK_STATUS_PROPOSTA IS NOT NULL
    AND P.FK_STATUS_PROPOSTA NOT IN ('102')
  GROUP BY YEAR(P.DATA_INICIO), MONTH(P.DATA_INICIO), DAY(P.DATA_INICIO)
  ORDER BY YEAR(P.DATA_INICIO), MONTH(P.DATA_INICIO), DAY(P.DATA_INICIO)
  ''', "eshows")