import pandas as pd
import duckdb as dk
import streamlit as st



if st.session_state.get('file') is not None:
    dcb = st.session_state['file']

else:
    st.warning("Nenhum arquivo carregado. Por favor, carregue um arquivo na primeira página.")

# Conecta ao banco de dados DuckDB
con = dk.connect()

# Registra o DataFrame como uma tabela temporária
con.register("dcb003", dcb)

vcl = con.sql(
f"""
    SELECT
        CAST(item AS TEXT) AS Item,
        "Desc Item" AS Descrição,
        UPPER(Dep) AS Depósito,
        Quantidade,
        CURRENT_DATE - CAST("Data Ult. Transf." AS DATE) AS "Dias sem Giro",
    FROM dcb003
    WHERE Depósito LIKE '%VCL%'
"""
).df()

con.register("tabela_vcl", vcl)

vcl_periodos = con.sql(
"""
    SELECT
        Item,
        Descrição,

    CASE 

        WHEN "Dias sem Giro" > 0 AND "Dias sem Giro" <= 30 THEN '0 a 30 dias'
        WHEN "Dias sem Giro" > 30 AND "Dias sem Giro" <= 60 THEN '30 a 60 dias'
        WHEN "Dias sem Giro" > 60 AND "Dias sem Giro" <= 90 THEN '60 a 90 dias'
        WHEN "Dias sem Giro" > 90 AND "Dias sem Giro" <= 180 THEN '90 a 180 dias'
        WHEN "Dias sem Giro" >= 180 THEN 'Acima de 180 dias'
        END Permanência, "Dias sem Giro"
    FROM    
        tabela_vcl
    GROUP BY
        Item, Descrição, "Dias sem Giro"
    ORDER BY
        "Dias sem Giro" DESC
    
""").df()

# Dataframe com Quantidade de Itens sem giro por Período
vcl_metrics = vcl_periodos.drop(['Dias sem Giro'], axis=1)
vcl_metrics = vcl_metrics.drop_duplicates()

con.register("metrics_vcl", vcl_metrics)

metricsvcl = con.sql(
"""
    SELECT
        Permanência,
        COUNT(Permanência) AS Total
    FROM
        metrics_vcl
    GROUP BY 
        Permanência
    ORDER BY
        Permanência
"""
).df()