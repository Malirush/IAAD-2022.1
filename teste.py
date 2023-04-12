import streamlit as st
import mysql.connector
import pandas as pd





# Função para criar uma conexão com o banco de dados
def create_connection():
    cnx = mysql.connector.connect(user='aulas', password='Felipelol22.',
                                   host='localhost', database='clinicasmedicas')
    return cnx

#exibir tabela
def show_table(table_name, cnx):
    cursor = cnx.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    data = cursor.fetchall()
    st.table(data)


# Função para criar uma tabela no banco de dados
import streamlit as st
import mysql.connector

def create_table(cnx):
    cursor = cnx.cursor()
    table_name = st.text_input('Digite o nome da tabela:')
    column_names = st.text_input('Digite o nome das colunas separadas por vírgula:')
    table = st.empty()
    if st.button('Salvar'):
        query = f"CREATE TABLE {table_name} ({column_names})"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        df = show_table(cnx, table_name)
        table.empty()
        table.dataframe(df)
        st.success(f"Tabela {table_name} criada com sucesso!")


# Função para inserir dados em uma tabela no banco de dados
def insert_data(table_name, cnx):
    cursor = cnx.cursor()
    col_names = st.text_input('Digite o nome das colunas separadas por vírgula:')
    values = st.text_input('Digite os valores a serem inseridos separados por vírgula:')
    show_table(cnx, table_name)
    if st.button('Salvar'):
        query = f"INSERT INTO {table_name} ({col_names}) VALUES ({values})"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        show_table(cnx, table_name)
        st.success(f"Dados inseridos na tabela {table_name} com sucesso!")


# Função para atualizar dados em uma tabela no banco de dados
def update_data(table_name, cnx):
    cursor = cnx.cursor()

    # Define as entradas do usuário como formulário
    with st.form(key='update_form'):
        column_name = st.text_input('Digite o nome da coluna a ser atualizada:')
        new_value = st.text_input('Digite o novo valor:')
        condition_column = st.text_input('Digite o nome da coluna da condição:')
        condition_value = st.text_input('Digite o valor da condição:')

        # Define o botão de submissão do formulário
        submitted = st.form_submit_button(label='Salvar')
    if st.button('voltar'):
            st.experimental_rerun
    # Verifica se o botão de submissão foi pressionado
    if submitted:
        query = f"UPDATE {table_name} SET {column_name}='{new_value}' WHERE {condition_column}='{condition_value}'"
        cursor.execute(query)
        show_table(cnx, table_name)
        st.success(f"Dados atualizados com sucesso!")
        cnx.commit()
        cursor.close()
        

# Função para excluir dados em uma tabela no banco de dados
def delete_data(table_name,cnx):
    cursor = cnx.cursor()
    condition_column = st.text_input('Digite o nome da coluna da condição:', value='')
    condition_value = st.text_input('Digite o valor da condição:', value='')
    show_table(cnx, table_name)
    if st.button('Salvar'):
        query = f"DELETE FROM {table_name} WHERE {condition_column} = '{condition_value}'"
        st.text(query)
        cursor.execute(query)
        show_table(cnx, table_name)
        st.success(f"Dados excluídos com sucesso!")
        cnx.commit()
        cursor.close()
        


def get_tables(cnx):
    cursor = cnx.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    return [table[0] for table in tables]
    
def select_table():
    table_list = get_tables(cnx) # chama a função get_tables para obter a lista de tabelas
    st.write('Selecione uma tabela:')
    for table in table_list:
        if st.button(table):
            return f'{table}'


# Função para selecionar dados de uma tabela no banco de dados

def select_data(table_name,cnx):
    cursor = cnx.cursor()
    show_table(cnx, table_name)
    if st.button('Buscar'):
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) == 0:
            st.warning('Nenhum registro encontrado!')
        else:
            df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
            st.dataframe(df)


# Cria uma conexão com o banco de dados
cnx = create_connection()

# Define o título da página
st.title('Operações CRUD em MySQL com Streamlit')

# Define o menu de seleção de operações
option = st.sidebar.selectbox('Selecione uma operação:',
                             ['Criar tabela', 'Inserir dados', 'Atualizar dados', 'Excluir dados', 'Selecionar dados'])

# Executa a operação selecionada
if option == 'Criar tabela':
    create_table(cnx)
elif option == 'Inserir dados':
    tabela=select_table()
    if tabela:
        insert_data(tabela,cnx)
elif option == 'Atualizar dados':
    tabela=select_table()
    if tabela:
        update_data(tabela,cnx)
elif option == 'Excluir dados':
    tabela=select_table()
    if tabela:
        delete_data(tabela,cnx)
elif option == 'Selecionar dados':
    tabela=select_table()
    if tabela:
        select_data(tabela,cnx)

# Fecha a conexão com o banco de dados
cnx.close()
