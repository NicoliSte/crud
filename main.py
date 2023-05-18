import streamlit as st
import Controllers.ClienteController as ClienteController
import models.Cliente as cliente
import pandas as pd

# Variável de estado para controlar a exibição dos formulários
state = st.session_state.get("state", "cadastro")

# Função para exibir a tela de cadastro de usuário
def mostrar_tela_cadastro():
    # TITULO 
    st.markdown("<h1 style='text-align: center;'>Cadastrar Usuário</h1>", unsafe_allow_html=True)

    # CRIANDO FORMULARIO
    with st.form(key="include_usuario"):
        input_name = st.text_input(label="Nome")
        input_age = st.number_input(label="Idade", format="%d",step=1)
        input_sex = st.selectbox("Qual foi o sexo atribuído no seu nascimento?", ["Feminino", "Masculino"])
        input_senha = st.text_input(label="Crie uma senha", type='password')
        col1, col2 = st.columns(2)

        if col1.form_submit_button("Cadastrar"):
            # Lógica para cadastrar o usuário
            cliente.nome= input_name
            cliente.idade = input_age
            cliente.sexo = input_sex 
            cliente.senha = input_senha

            ClienteController.incluir(cliente)
            st.success("Usuário cadastrado com sucesso!")

            # Altera o estado para exibir a tela de login
            st.session_state.state = "login"

        if col2.form_submit_button("Ja possui conta? Faça login"):
            # Altera o estado para exibir a tela de login
            st.session_state.state = "login"
            st.experimental_rerun()

# Função para exibir a tela de login
def mostrar_tela_login():
    # TITULO 
    st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)

    # CRIANDO FORMULARIO
    with st.form(key="login_usuario"):
        input_name = st.text_input(label="Nome")
        input_senha = st.text_input(label="Senha", type='password')
        col1, col2 = st.columns(2)

     # Lógica para login do usuário
        if col1.form_submit_button("Fazer login"):
            logged_in_user = ClienteController.login(input_name, input_senha)
            if logged_in_user:
               
                st.session_state.logged_in_user = logged_in_user  # Armazena o usuário logado na sessão
                st.session_state.state = "dashboard"  # Altera o estado para exibir o dashboard
                st.experimental_rerun()
            else:
                st.error("Nome de usuário ou senha incorretos!")
           
        if col2.form_submit_button("Cadastre-se"):
            # Altera o estado para exibir a tela de cadastro
            st.session_state.state = "cadastro"
            st.experimental_rerun()

# Função para exibir o dashboard
def mostrar_dashboard():
    # Verifica se o usuário está logado
    if 'logged_in_user' in st.session_state:
        logged_in_user = st.session_state.logged_in_user
        user_id = logged_in_user[0]  # Obtém o ID do usuário logado
        user_name = logged_in_user[1]  # Obtém o nome do usuário logado

        # Exibe o nome do usuário logado
        st.subheader(f"Bem-vindo {user_name}!")

        # Exibe a seção "Adicionar Treino"
        adicionar_treino(user_id)

        if st.button("Sair"):
            st.session_state.clear()  # Limpa a sessão
            st.experimental_rerun()  # Reinicia a aplicação

    else:
        st.error("Usuário não logado!")

st.sidebar.title('Menu')
Page_treino =st.sidebar.selectbox('Treino', ['Criar', 'Consultar'])

# Função para adicionar treino
def adicionar_treino(user_id):
    treinos_salvos = []  # Inicializa a variável como uma lista vazia    
    
    

    if Page_treino == 'Criar': 
        st.experimental_set_query_params() 
        # CRIANDO FORMULARIO
        st.markdown("<h1 style='text-align: center;'>Cadastrar Trenio</h1>", unsafe_allow_html=True)
        with st.form(key="adicionar_treino"):
            input_day = st.selectbox("Dia da semana", ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"])
            input_muscle_group = st.text_input("Grupo Muscular")
            input_cliente_id = st.text_input("Cliente ID", value=user_id, disabled=True)
            exercise_list = []

            exercise_input = st.text_area("Exercícios (separe por vírgula)")
            series_input = st.text_area("Séries (separe por vírgula)")
            repetitions_input = st.text_area("Repetições (separe por vírgula)")

            exercises = exercise_input.split(",")
            series = series_input.split(",")
            repetitions = repetitions_input.split(",")

            if len(exercises) != len(series) or len(exercises) != len(repetitions):
                st.error("O número de exercícios, séries e repetições deve ser o mesmo.")
                return

            for exercise, series, repetitions in zip(exercises, series, repetitions):
                exercise = exercise.strip()
                series = series.strip()
                repetitions = repetitions.strip()

             # Ignorar valores vazios ou não numéricos
                if not exercise or not series or not repetitions:
                    continue

                try:
                    series = int(series)
                    repetitions = int(repetitions)
                except ValueError:
                    st.error("As séries e repetições devem ser números inteiros.")
                    return

                exercise_data = {
                    "exercicio": exercise,
                    "series": series,
                    "repeticoes": repetitions
                }
                exercise_list.append(exercise_data)

            if st.form_submit_button("Salvar Treino"):
                # Lógica para adicionar o treino ao banco de dados
                for exercise in exercise_list:
                    ClienteController.adicionar_treino(input_day, input_muscle_group, exercise["exercicio"], exercise["series"], exercise["repeticoes"], input_cliente_id)

                st.success("Treino salvo com sucesso!")

        
    # CRIANDO FORMULÁRIO PARA LISTAR TREINOS SALVOS

    if Page_treino == 'Consultar':
       #caso get esteja vazio mostrar a pagina de listagem
       paramId = st.experimental_get_query_params()
       if paramId =={}:
        if paramId.get("id") == None:
            st.experimental_set_query_params() 
            

            treinos_salvos = ClienteController.listar_treinos_salvos(user_id)  # Obter a lista de treinos apenas uma vez

        if len(treinos_salvos) == 0:
                st.write("Nenhum treino salvo.")
        else:
            colms = st.columns((1, 2, 2, 2, 1, 1.65, 2, 2))
            campos = ['Id', 'Dia', 'Grupo Muscular', 'Exercício', 'Série', 'Repetição', 'Excluir', 'Alterar']
            
            for campo_nome, col in zip(campos, colms):
                col.write(campo_nome)
            
            for item in treinos_salvos:

            
                col1, col2, col3, col4, col5, col6, col7 , col8= st.columns((1, 2, 2, 2, 1, 1.65, 2, 2))
                col1.write(item[0])  # Acessa o elemento da tupla (id)
                col2.write(item[1])  # Acessa o elemento da tupla (dia)
                col3.write(item[2])  # Acessa o elemento da tupla (musculo)
                col4.write(item[3])  # Acessa o elemento da tupla (exercicio)
                col5.write(item[4])  # Acessa o elemento da tupla (serie)
                col6.write(item[5])  # Acessa o elemento da tupla (repeticao)
                button_space = col7.empty()
                on_Click_Excluir = button_space.button('Excluir', key='btnExcluir' + str(item[0]))  # Chave exclusiva com base no ID do item
                button_space_a = col8.empty()
                on_Click_Alterar = button_space_a.button('Alterar', key='btnAlterar' + str(item[0]))  # Chave exclusiva com base no ID do item

                if on_Click_Excluir:
                    ClienteController.Excluir(item[0])
                    st.experimental_rerun()
                #se clicar m alterar mudar set ai o get ja nao vai ta vazio e recarregar a pagina
                if on_Click_Alterar:
                    st.experimental_set_query_params(
                        id=[item[0]]
                    )
                    st.experimental_rerun()
                    
     #mostrar a pagina de alteracao pois o get nao vai ta vazio               
       else:
            on_Click_Voltar = st.button("voltar")
            if on_Click_Voltar:
                st.experimental_set_query_params()
                st.experimental_rerun()
            # CRIANDO A LÓGICA DE ALTERAR
            idAlterar = st.experimental_get_query_params()
            

            if idAlterar.get("id") != None:
                idAlterar = idAlterar.get("id")[0]
                treino = ClienteController.treinos_salvos(int(idAlterar))
                st.experimental_set_query_params(
                    id=[treino['id']]
                )
                 
                st.markdown("<h1 style='text-align: center;'>Alterar Treino</h1>", unsafe_allow_html=True)
                with st.form(key="alterar_treino"):
                    input_day = st.selectbox("Dia da semana", ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"])
                    input_muscle_group = st.text_input("Grupo Muscular", value=treino['musculo'])
                    input_cliente_id = st.text_input("Cliente ID", value=user_id, disabled=True)
                    exercise_input = st.text_area("Exercícios ", value=str(treino.get('exercicio', '')))
                    series_input = st.text_area("Séries ", value=int(treino.get('serie', '')))
                    repetitions_input = st.text_area("Repetições ", value=int(treino.get('repeticao', '')))

                  
                    if st.form_submit_button("Alterar Treino"):
                        st.experimental_set_query_params()
                        ClienteController.alterar_treino(input_day, input_muscle_group, exercise_input,  series_input, repetitions_input,input_cliente_id, idAlterar)

                        st.success("Treino alterado com sucesso!")
                                                                      

# Verifica o estado atual e exibe a tela correspondente
if state == "cadastro":
    mostrar_tela_cadastro()
elif state == "login":
    mostrar_tela_login()
elif state == "dashboard":
    mostrar_dashboard()

# Verifica os parâmetros de consulta para redirecionar para uma seção específica
if "section" in st.experimental_get_query_params():
    section = st.experimental_get_query_params()["section"]
    if section == "dashboard":
        st.session_state.state = "dashboard"
        