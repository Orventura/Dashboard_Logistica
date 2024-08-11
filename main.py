import streamlit as st
from vcl import vcl, vcl_periodos
from rej import rej, rej_periodos


dep = st.sidebar.radio(
    "Selecione o Depósito:",
    ["PL3", "DCL", "REJ", "VCL"],
    index=1,
)
# Título da aplicação
deposito = dep
st.title('Acompanhamento de Depósitos')
st.header(f':red[{deposito}]', divider='rainbow')



st.subheader('Quantidade de Códigos')
col1, col2, col3, col4 = st.columns(4)
col1.metric("0 a 30 dias", "25")
col2.metric("30 a 60 dias", "30")
col3.metric("60 a 90 dias", "35")
col4.metric("acima de 180 dias", "5")
st.subheader('', divider='rainbow')




# Slider de seleção de intervalo de dias
start_day, end_day = st.sidebar.select_slider(
    "Selecione o período em dias",
    options=[0, 30, 60, 90, 180, '> 180'],
    value=(0, '> 180'))



# Lógica de filtragem
if dep == "PL3":
    pass
elif dep == "DCL":
    pass
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
        

