import pandas as pd
import duckdb as dk
import streamlit as st
import numpy as np


local_excel = r"H:\EXPEDICAO\00 Painel de Controle\Programação\DCB003\DCB003.xlsx"
# Carrega o arquivo CSV
#caminho = 'DCB 20240304.csv'
#dcb = pd.read_csv(caminho, sep=';', encoding='ANSI')

dcb = pd.read_excel(local_excel, decimal=',')

# Conecta ao banco de dados DuckDB
con = dk.connect()

# Registra o DataFrame como uma tabela temporária
con.register("dcb003", dcb)

# Executa a consulta SQL
rej = con.sql("""

    SELECT
        CAST(item AS TEXT) AS Item,
        "Desc Item" AS Descrição,
        UPPER(Dep) AS Depósito,
        Quantidade,
        CURRENT_DATE - CAST("Data Ult. Transf." AS DATE) AS "Dias sem Giro",
    FROM dcb003
    WHERE Depósito LIKE '%EXP%'"""
).show()
