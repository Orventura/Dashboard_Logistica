import streamlit as st
import pandas as pd

st.title("Carregar Arquivozzzzzzzzz")

# Verifica se o arquivo já está carregado
if 'file' not in st.session_state:
    st.session_state['file'] = None

# Carrega o arquivo
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=['xlsx'])

if uploaded_file is not None:
    # Lê o arquivo e o armazena no session_state
    if uploaded_file.name.endswith('csv'):
        st.session_state['file'] = pd.read_csv(uploaded_file, sep=';', decimal=",", encoding='ANSI',)
    else:
        st.session_state['file'] = pd.read_excel(uploaded_file, decimal=",")
    

