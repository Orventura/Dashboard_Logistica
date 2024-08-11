import pandas as pd
import duckdb as dk



local_excel = r"H:\EXPEDICAO\00 Painel de Controle\Programação\DCB003\DCB003.xlsx"
# Carrega o arquivo CSV
#caminho = 'DCB 20240304.csv'
#dcb = pd.read_csv(caminho, sep=';', encoding='ANSI')

dcb = pd.read_excel(local_excel, decimal=',')

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
WHEN "Dias sem Giro" > 90 AND "Dias sem Giro" <= 180 THEN 'Acima de 90 dias'
WHEN "Dias sem Giro" >= 180 THEN 'Acima de 180 dias'
END Permanência, "Dias sem Giro"
FROM    
    tabela_vcl
ORDER BY
    "Dias sem Giro" DESC
    
    
""").df()