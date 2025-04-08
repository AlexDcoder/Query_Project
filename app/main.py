import streamlit as st
from time import time
import os
from models.db.connector import DBConnector
from models.query.maneger import QueryManeger
from models.query.parser import QueryParser


st.set_page_config('Trabalho Consultas', page_icon='👨‍💻', layout='wide')
st.title('Envio e Otimização de Consultas')

with st.form('Formulário de Envio de consultas'):
    # A string com a consulta SQL é entrada na interface gráfica 
    user_query = st.text_area(
        'Campo de consultas', placeholder='Digite sua consulta aqui.')
    submit = st.form_submit_button('Enviar')
if submit:
    with st.spinner('Iniciando conexão com o Banco...', show_time=True):
        # connector = DBConnector(
        #     os.environ['HOST'], os.environ['USER'], os.environ['PASSWORD'], 
        #     os.environ['DATABASE']
        # )
        # connector.start_connection()
        print('aqui')
    st.write(
        f'''
        **Requisição executada**
        ```
        {user_query}
        ```
        ''')
    # query_result = connector.execute_query(user_query)
    # TODO A string é parseada e o comando SQL é validado além de validar se as tabelas existem e se 
    
    # TODO os campos informados no select existem nas tabelas 
    
    # TODO O comando SQL é convertido para álgebra relacional 
    
    # TODO Mostrar na Interface a conversão do SQL para álgebra relacional 
    
    # TODO A álgebra relacional é otimizada conforme as heurísticas solicitadas (ver item 5) 
    
    # TODO O grafo de operadores é construído em memória 
    
    # TODO O grafo de operadores deve ser mostrado na Interface gráfica 
    
    # TODO O resultado da consulta mostrando cada operação e a ordem que será executada, é exibido 
    # na interface gráfica (plano de execução) 
