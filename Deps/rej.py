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

rej = con.sql(
f"""
    SELECT
        CAST(item AS TEXT) AS Item,
        "Desc Item" AS Descrição,
        UPPER(Dep) AS Depósito,
        Quantidade,
        CURRENT_DATE - CAST("Data Ult. Transf." AS DATE) AS "Dias sem Giro",
    FROM dcb003
    WHERE Depósito LIKE '%REJ%'
"""
).df()

con.register("tabela_rej", rej)

rej_periodos = con.sql(
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
        tabela_rej
    GROUP BY
        Item, Descrição, "Dias sem Giro"
    ORDER BY
        "Dias sem Giro" DESC
    
""").df()

# Dataframe com Quantidade de Itens sem giro por Período
rej_metrics = rej_periodos.drop(['Dias sem Giro'], axis=1)
rej_metrics = rej_metrics.drop_duplicates()

con.register("metrics_rej", rej_metrics)

metricsrej = con.sql(
"""
    SELECT
        Permanência,
        COUNT(Permanência) AS Total
    FROM
        metrics_rej
    GROUP BY 
        Permanência
    ORDER BY
        Permanência
"""
).df()