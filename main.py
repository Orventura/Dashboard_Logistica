import streamlit as st
from vcl import vcl, vcl_periodos
from rej import rej, rej_periodos
from dcl import dcl, dcl_periodos, metricsdcl
from pl3 import pl3, pl3_periodos, metricspl3


dep = st.sidebar.radio(
    "Selecione o Depósito:",
    ["PL3", "DCL", "REJ", "VCL"],
    index=1,
)
# Título da aplicação
deposito = dep
st.title('Acompanhamento de Depósitos')
st.header(f':red[{deposito}]', divider='rainbow')


if dep == 'PL3':

    st.subheader('Quantidade de Códigos sem Giro')
    col1, col2, col3, col4, col5 = st.columns(5)
    cont_0_30 = metricspl3['Total'].get(0, 0)
    cont_30_60 = metricspl3['Total'].get(1, 0)
    cont_60_90 = metricspl3['Total'].get(2, 0)
    cont_90_180 = metricspl3['Total'].get(3, 0)
    cont_maior_180 = metricspl3['Total'].get(4, 0)

    col1.metric("0 a 30 dias", f"{cont_0_30}")
    col2.metric("30 a 60 dias", f"{cont_30_60}")
    col3.metric("60 a 90 dias", f"{cont_60_90}")
    col4.metric("90 a 180 dias", f"{cont_90_180}")
    col5.metric("acima de 180 dias", f"{cont_maior_180}")
    st.subheader('', divider='rainbow')

elif dep == "DCL":
    st.subheader('Quantidade de Códigos sem Giro')
    col1, col2, col3, col4, col5 = st.columns(5)
    cont_0_30 = metricsdcl[metricsdcl['Permanência'] == '0 a 30 dias']['Total'].sum()
    cont_30_60 = metricsdcl[metricsdcl['Permanência'] == '30 a 60 dias']['Total'].sum()
    cont_60_90 = metricsdcl[metricsdcl['Permanência'] == '60 a 90 dias']['Total'].sum()
    cont_90_180 = metricsdcl[metricsdcl['Permanência'] == '90 a 180 dias']['Total'].sum()
    cont_maior_180 = metricsdcl[metricsdcl['Permanência'] == 'Acima de 180 dias']['Total'].sum()

    col1.metric("0 a 30 dias", f"{cont_0_30}")
    col2.metric("30 a 60 dias", f"{cont_30_60}")
    col3.metric("60 a 90 dias", f"{cont_60_90}")
    col4.metric("90 a 180 dias", f"{cont_90_180}")
    col5.metric("acima de 180 dias", f"{cont_maior_180}")
    st.subheader('', divider='rainbow')



# Slider de seleção de intervalo de dias
start_day, end_day = st.sidebar.select_slider(
    "Selecione o período em dias",
    options=[0, 30, 60, 90, 180, '> 180'],
    value=(0, '> 180'))



# Lógica de filtragem
if dep == "PL3":
    if end_day == '> 180':

        filtered_pl3 = pl3_periodos[pl3_periodos["Dias sem Giro"] > start_day]
        st.subheader(f"Produtos de {start_day} a {end_day} dias sem giro")
        filtered_pl3 = filtered_pl3.drop(['Dias sem Giro'], axis=1)
        st.dataframe(filtered_pl3.drop_duplicates(), hide_index=True, use_container_width=True)
    else:
        filtered_pl3 = pl3_periodos[(pl3_periodos["Dias sem Giro"] > start_day) & (pl3_periodos["Dias sem Giro"] <= end_day)]
        st.subheader(f"Produtos de {start_day} a {end_day} dias sem giro")
        filtered_pl3 = filtered_pl3.drop(['Dias sem Giro'], axis=1)
        st.dataframe(filtered_pl3.drop_duplicates(), hide_index=True, use_container_width=True)
elif dep == "DCL":
    if end_day == '> 180':

        filtered_dcl = dcl_periodos[dcl_periodos["Dias sem Giro"] > start_day]
        st.subheader(f"Produtos de {start_day} a {end_day} dias sem giro")
        filtered_dcl = filtered_dcl.drop(['Dias sem Giro'], axis=1)
        st.dataframe(filtered_dcl.drop_duplicates(), hide_index=True, use_container_width=True)
    else:
        filtered_dcl = dcl_periodos[(dcl_periodos["Dias sem Giro"] > start_day) & (dcl_periodos["Dias sem Giro"] <= end_day)]
        st.subheader(f"Produtos de {start_day} a {end_day} dias sem giro")
        filtered_dcl = filtered_dcl.drop(['Dias sem Giro'], axis=1)
        st.dataframe(filtered_dcl.drop_duplicates(), hide_index=True, use_container_width=True)

elif dep == "REJ":
    deposito = "REJ"
    if end_day == '> 180':

        filtered_rej = rej_periodos[rej_periodos["Dias sem Giro"] > start_day]
        st.subheader(f"Produtos de {start_day} a {end_day} dias sem giro")
        st.dataframe(filtered_rej.drop(["Dias sem Giro"], axis=1), hide_index=True, use_container_width=True )
    else:
        filtered_rej = rej_periodos[(rej_periodos["Dias sem Giro"] > start_day) & (rej_periodos["Dias sem Giro"] <= end_day)]
        st.subheader(f"Produtos de {start_day} a {end_day} dias sem giro")
        st.dataframe(filtered_rej.drop(["Dias sem Giro"], axis=1), hide_index=True, use_container_width=True)


else:
    if end_day == '> 180':

        filtered_vcl = vcl_periodos[vcl_periodos["Dias sem Giro"] > start_day]
        st.subheader(f"Produtos de {start_day} a {end_day} dias sem giro")
        st.dataframe(filtered_vcl.drop(["Dias sem Giro"], axis=1), hide_index=True, use_container_width=True )
    else:
        filtered_vcl = vcl_periodos[(vcl_periodos["Dias sem Giro"] > start_day) & (vcl_periodos["Dias sem Giro"] <= end_day)]
        st.subheader(f"Produtos de {start_day} a {end_day} dias sem giro")
        st.dataframe(filtered_vcl.drop(["Dias sem Giro"], axis=1), hide_index=True, use_container_width=True)
        

