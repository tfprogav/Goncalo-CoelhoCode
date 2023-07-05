from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry
from fpdf import FPDF

def executar_query(query):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tf_prog_av"
    )
    cursor = mydb.cursor()
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    mydb.commit()
    mydb.close()
    return resultados


def show_gestao_utilizadores():
    clear_content_frame()
    label = Label(content_frame, text='Informações de Gestão de Utilizadores', font=('Arial', 14))
    label.pack(pady=20)

def show_gestao_alunos():
    clear_content_frame()
    label = Label(content_frame, text='Informações de Gestão de Alunos', font=('Arial', 14))
    label.pack(pady=20)

def show_gestao_aulas_horarios():
    clear_content_frame()
    label = Label(content_frame, text='Informações de Gestão de Aulas e Horários', font=('Arial', 14))
    label.pack(pady=20)

def show_gestao_pagamentos():

    clear_content_frame() # limpa a frama para aparecer a nova pagina

    def get_cursos(): #Funçao para ir buscar o nome dos cursos que serve para ambas as paginas
        query = "SELECT curso_desc FROM q_cursos"
        resultados = executar_query(query)
        cursos = [resultado[0] for resultado in resultados]  # Obtém o valor concatenado do curso
        return cursos

    def abrir_gestao_pagamentos():
        clear_content_frame()
        show_gestao_pagamentos()


    ######################################################################
    #############------ PAGINA EDITAR FATURAS(ADMIN) ------###############
    ######################################################################

    def abrir_editar_faturas():
        clear_content_frame()

        def login():
            email = entry_email.get()
            password= entry_password.get()

            #verifica se é utilizador com cargo de administrador
            query = f"SELECT utilizador_nome FROM q_utilizadores " \
                    f"WHERE utilizador_email = '{email}' AND utilizador_senha = '{password}' AND utilizador_perfil = 3"

            executar_query(query)

            #caso seja administrador
            if executar_query(query):
                clear_content_frame()

                #vai buscar os dados das faturas que ainda nao foram pagas
                query_tabela = f"SELECT pagamento_id, pagamento_data, pagamento_aluno_id, pagamento_curso_id, pagamento_valor FROM q_pagamentos " \
                               f"WHERE pagamento_pagou = 0"
                resultados = executar_query(query_tabela)


                ############################################
                ##------- TABELA FATURAS POR PAGAR -------##
                ############################################

                label_contexto = Label(content_frame, text='Ediçao da Tabela Faturas', font=('Arial', 16, 'bold'))
                label_contexto.place(relx=0.5, rely=0, anchor='n')

                # Conteúdo da tabela
                table_frame2 = Frame(content_frame)
                table_frame2.place(x=10, y=50)

                table_fatura = ttk.Treeview(table_frame2, columns=('ID', 'Data', 'Aluno ID', 'Curso', 'Valor'), show='headings')
                table_fatura.column('ID', width=100)
                table_fatura.column('Data', width=100)
                table_fatura.column('Aluno ID', width=100)
                table_fatura.column('Curso', width=100)
                table_fatura.column('Valor', width=100)
                table_fatura.heading('ID', text='ID')
                table_fatura.heading('Data', text='Data')
                table_fatura.heading('Aluno ID', text='Aluno ID')
                table_fatura.heading('Curso', text='Curso')
                table_fatura.heading('Valor', text='Valor')

                table_fatura.pack()

                #mostra os resultados da query na tabela
                for resultado in resultados:
                    table_fatura.insert('', 'end', values=(resultado))

                def apagar_linha():
                    item_selecionado = table_fatura.selection()  # Obter item selecionado
                    if item_selecionado:
                        linha_selecionada = table_fatura.item(item_selecionado)['values']  # Obter valores da linha selecionada
                        pagamento_id = linha_selecionada[0]  # Pagamento ID está na primeira coluna (índice 0)

                        #apagar a linha com base na linha que foi selecionada
                        query_apagar = f"DELETE FROM q_pagamentos WHERE pagamento_id = {pagamento_id}"
                        executar_query(query_apagar)

                        # Remover a linha selecionada da tabela
                        table_fatura.delete(item_selecionado)

                        messagebox.showinfo("Sucesso", "Fatura apagada com sucesso!")
                    else:
                        messagebox.showwarning("Aviso", "Nenhuma linha selecionada.")

                #botao para apagar a fatura selecionada
                button_apagar_linha = Button(content_frame, text='Apagar fatura selecionada', bg='#d43f3f', command=apagar_linha)
                button_apagar_linha.place(x=550, y=80)

                #####################################
                ##--- FRAME PARA EDITAR FATURAS ---##
                #####################################
                def editar_fatura():
                    item_selecionado = table_fatura.selection()  # Obter item selecionado
                    if item_selecionado:
                        linha_selecionada = table_fatura.item(item_selecionado)['values']  # Obter valores da linha selecionada
                        pagamento_id = linha_selecionada[0]  # Pagamento ID está na primeira coluna (índice 0)

                        # Obter os dados da fatura a ser editada com base no pagamento_id
                        query_fatura = f"SELECT pagamento_data, pagamento_aluno_id, pagamento_curso_id, pagamento_valor " \
                                       f"FROM q_pagamentos WHERE pagamento_id = {pagamento_id}"
                        resultado = executar_query(query_fatura)


                        if resultado:
                            def get_curso_id3():
                                nome_curso = select_curso3.get()
                                query = f"SELECT curso_id FROM q_cursos WHERE curso_desc = '{nome_curso}'"
                                resultados = executar_query(query)

                                if resultados:  # Verifica se há resultados antes de acessar o índice
                                    return resultados[0][0]
                                return None

                            def atualizar_aluno3():
                                curso_id = get_curso_id3()  # Obtém o id do curso selecionado
                                query = f"SELECT q_utilizadores.utilizador_nome FROM q_utilizadores INNER JOIN q_alunos_cursos ON q_utilizadores.utilizador_id = q_alunos_cursos.aluno_id INNER JOIN q_cursos ON q_alunos_cursos.curso_id = q_cursos.curso_id WHERE q_cursos.curso_id = '{curso_id}'"
                                resultados = executar_query(query)
                                alunos = [resultado[0] for resultado in resultados]  # coloca os nomes numa lista
                                select_aluno3['values'] = alunos  # atribui os valores da lista ao select_aluno
                                select_aluno3.set('')  # Limpa o conteúdo do select_aluno quando atualiza o curso

                            def get_alunos3():
                                return alunos_selecionados

                            def get_aluno_id3():
                                aluno_nome = select_aluno3.get()
                                query = f"SELECT utilizador_id FROM q_utilizadores WHERE utilizador_nome = '{aluno_nome}'"
                                resultados = executar_query(query)
                                if resultados:  # Verifica se há resultados antes de acessar o índice
                                    return resultados[0][0]
                                return None

                            def get_valor2():
                                curso_nome = select_curso3.get()
                                query = f"SELECT curso_preco FROM q_cursos WHERE curso_desc = '{curso_nome}'"
                                resultados = executar_query(query)
                                valor = resultados[0][0]  # Obtém o valor concatenado do curso
                                return valor


                            update_frame = Frame(content_frame) #frame update
                            update_frame.place(x=550, y=200)

                            label_curso3 = Label(update_frame, text='Selecionar curso:', font=('Arial', 14))
                            label_curso3.grid(row=0, column=0, sticky='w', pady=10)

                            # Atribui os cursos a uma variável para ser mostrado como valores no select_curso
                            cursos2 = get_cursos()
                            select_curso3 = ttk.Combobox(update_frame, values=cursos2, font=('Arial', 12))
                            select_curso3.grid(row=0, column=1, padx=5, pady=5)

                            button_atualizar_aluno3 = ttk.Button(update_frame, text='Atualizar alunos',
                                                                 style='RoundedButton.TButton',
                                                                 command=atualizar_aluno3)
                            button_atualizar_aluno3.grid(row=1, column=1, pady=10)

                            # Label e combobox para selecionar o aluno
                            label_aluno3 = Label(update_frame, text='Selecionar aluno:', font=('Arial', 14))
                            label_aluno3.grid(row=2, column=0, sticky='w', pady=10)

                            aluno3 = get_alunos3()
                            select_aluno3 = ttk.Combobox(update_frame, values=aluno3, font=('Arial', 12))
                            select_aluno3.grid(row=2, column=1, padx=5, pady=5)

                            label_mes3 = Label(update_frame, text='Selecionar mês:', font=('Arial', 14))
                            label_mes3.grid(row=3, column=0, sticky='w', pady=(0, 10))

                            entry_data = DateEntry(update_frame, select_mode='day', font=('Arial', 12))
                            entry_data.grid(row=3, column=1, pady=(0, 10))

                            data =resultado[0][0] #passa o valor da data para uma variavel

                            entry_data.set_date(data) #passa o valor selecionado na linha para o widget da data

                            def guardar_alteracoes():
                                # Receber os novos valores que estao no widgets para posteriormente dar update
                                nova_data = entry_data.get_date()
                                nova_data_formato = nova_data.strftime("%Y-%m-%d")
                                novo_aluno_id = get_aluno_id3()
                                novo_curso_id = get_curso_id3()
                                novo_valor = get_valor2()

                                # Executar a query de atualização na tabela de faturas
                                query_atualizar = f"UPDATE q_pagamentos SET " \
                                                  f"pagamento_data = '{nova_data_formato}', " \
                                                  f"pagamento_aluno_id = {novo_aluno_id}, " \
                                                  f"pagamento_curso_id = {novo_curso_id}, " \
                                                  f"pagamento_valor = {novo_valor} " \
                                                  f"WHERE pagamento_id = {pagamento_id}"
                                executar_query(query_atualizar)

                                # Exibir mensagem de sucesso
                                messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")

                            # Botão para guardar as alterações
                            button_guardar = ttk.Button(update_frame, text="Salvar Alterações", style='RoundedButton.TButton',command=guardar_alteracoes)
                            button_guardar.grid(row=4, column=1)

                        else:
                            messagebox.showwarning("Aviso", "Fatura não encontrada.")
                    else:
                       messagebox.showwarning("Aviso", "Nenhuma linha selecionada.")

                # botao para apagar a fatura selecionada
                button_editar_linha = ttk.Button(content_frame, text='Editar fatura selecionada',style='RoundedButton.TButton',command=editar_fatura)
                button_editar_linha.place(x=550, y=130)

        # Título da página
        label = Label(content_frame, text='Login Administrador', font=('Arial', 24, 'bold'))
        label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Labels e entradas
        label_email = Label(content_frame, text='Email:', font=('Arial', 14))
        label_email.grid(row=1, column=0, sticky='e', pady=10)

        entry_email = Entry(content_frame)
        entry_email.grid(row=1, column=1, pady=10)

        label_password = Label(content_frame, text='Password:', font=('Arial', 14))
        label_password.grid(row=2, column=0, sticky='e', pady=10)

        entry_password = Entry(content_frame)
        entry_password.grid(row=2, column=1, pady=10)

        button_login = ttk.Button(content_frame, text='Login', style='RoundedButton.TButton', command=login)
        button_login.grid(row=3, column=1, pady=10)

# --------------------------------------------------------------------------------------------------------------------------------------------------#
    ###################################################################
    #################------ PAGINA CRIAR FATURAS ------################
    ###################################################################

    def pagina_criar_faturas():
        clear_content_frame()

        def get_curso_id2():
            nome_curso = select_curso2.get()
            query = f"SELECT curso_id FROM q_cursos WHERE curso_desc = '{nome_curso}'"
            resultados = executar_query(query)

            if resultados:  # Verifica se há resultados antes de acessar o índice
                return resultados[0][0]
            return None

        def atualizar_aluno2():
            curso_id = get_curso_id2()  # Obtém o id do curso selecionado
            query = f"SELECT q_utilizadores.utilizador_nome FROM q_utilizadores INNER JOIN q_alunos_cursos ON q_utilizadores.utilizador_id = q_alunos_cursos.aluno_id INNER JOIN q_cursos ON q_alunos_cursos.curso_id = q_cursos.curso_id WHERE q_cursos.curso_id = '{curso_id}'"
            resultados = executar_query(query)
            alunos = [resultado[0] for resultado in resultados]  # coloca os nomes numa lista
            select_aluno2['values'] = alunos  # atribui os valores da lista ao select_aluno
            select_aluno2.set('')  # Limpa o conteúdo do select_aluno quando atualiza o curso

        def get_alunos2():
            return alunos_selecionados

        def get_aluno_id2():
            aluno_nome = select_aluno2.get()
            query = f"SELECT utilizador_id FROM q_utilizadores WHERE utilizador_nome = '{aluno_nome}'"
            resultados = executar_query(query)
            if resultados:  # Verifica se há resultados antes de acessar o índice
                return resultados[0][0]
            return None
        def get_valor():
            curso_nome = select_curso2.get()
            query = f"SELECT curso_preco FROM q_cursos WHERE curso_desc = '{curso_nome}'"
            resultados = executar_query(query)
            valor = resultados[0][0] # Obtém o valor concatenado do curso
            return valor

        def on_criar_fatura_click():

            data = select_data2.get_date() #Recebe o valor do date picker
            data_formato = data.strftime("%Y-%m-%d") #Muda esse valor para o formato de data que está na base de dados

            #recebe os valores selecionados
            aluno_id = get_aluno_id2()
            curso_id = get_curso_id2()
            valor = get_valor()

            #tenta executar a query se conseguir mostra sucesso
            try:
                query_update = f"INSERT INTO q_pagamentos (pagamento_data, pagamento_aluno_id, pagamento_curso_id, pagamento_valor, pagamento_pagou) " \
                               f"VALUES ('{data_formato}',{aluno_id},{curso_id}, {valor}, 0)"
                executar_query(query_update)

                messagebox.showinfo("Sucesso","A fatura foi criada!")

            #se nao conseguir mostra a mensagem de erro
            except IndexError:  # caso a query nao seja executada com sucesso
                messagebox.showinfo("Aviso","A fatura nao foi paga, verifique se selecionou corretamente todos os campos")

        # Título da página
        label = Label(content_frame, text='Criar faturas', font=('Arial', 24, 'bold'))
        label.place(relx=0.5, rely=0, anchor='n')


        ###################################################
        ##-------- MENU SECUNDARIO CRIAR FATURAS --------##
        ###################################################

        menu_opcoes = Frame(content_frame, bg='#b3b5b4', width=150, height=50)
        menu_opcoes.pack(anchor='ne', expand=True)

        # Estilo dos botões do menu secundário
        button_styles_mini_menu = {
            'bg': '#008080',
            'fg': 'white',
            'activebackground': '#383838',
            'activeforeground': 'white',
            'font': FONT,
            'borderwidth': 0,
            'highlightthickness': 0,
            'relief': 'flat',
            'cursor': 'hand2',
        }

        # Botões do menu secundario
        button1_2 = Button(menu_opcoes, text='Criar faturas', **button_styles_mini_menu, command=pagina_criar_faturas)
        button1_2.pack(pady=10, padx=10, fill='x')

        button2_2 = Button(menu_opcoes, text='Gestão de pagamentos', **button_styles_mini_menu,
                         command=abrir_gestao_pagamentos)
        button2_2.pack(pady=10, padx=10, fill='x')

        button3_3 = Button(menu_opcoes, text='Editar Faturas', **button_styles_mini_menu,
                           command=abrir_gestao_pagamentos)
        button3_3.pack(pady=10, padx=10, fill='x')


        ##########################################
        ##--------- FRAME CRIAR FATURAS --------##
        ##########################################

        criarFatura_frame = Frame(content_frame)
        criarFatura_frame.place(relx=0.5, rely=0.3, anchor='center')

        # Label e combobox para selecionar o curso
        label_curso2 = Label(criarFatura_frame, text='Selecionar curso:', font=('Arial', 14))
        label_curso2.grid(row=0, column=0, sticky='w', pady=10)

        # Atribui os cursos a uma variável para ser mostrado como valores no select_curso
        cursos2 = get_cursos()
        select_curso2 = ttk.Combobox(criarFatura_frame, values=cursos2, font=('Arial', 12))
        select_curso2.grid(row=0, column=1, padx=5, pady=5)

        button_atualizar_aluno2 = ttk.Button(criarFatura_frame, text='Atualizar alunos', style='RoundedButton.TButton',
                                            command=atualizar_aluno2)
        button_atualizar_aluno2.grid(row=1, column=1, pady=10)

        # Label e combobox para selecionar o aluno
        label_aluno2 = Label(criarFatura_frame, text='Selecionar aluno:', font=('Arial', 14))
        label_aluno2.grid(row=2, column=0, sticky='w', pady=10)

        aluno2 = get_alunos2()
        select_aluno2 = ttk.Combobox(criarFatura_frame, values=aluno2, font=('Arial', 12))
        select_aluno2.grid(row=2, column=1, padx=5, pady=5)

        label_mes2 = Label(criarFatura_frame, text='Selecionar mês:', font=('Arial', 14))
        label_mes2.grid(row=3, column=0, sticky='w', pady=(0, 10))

        select_data2 = DateEntry(criarFatura_frame, select_mode='day', font=('Arial', 12))
        select_data2.grid(row=3, column=1, pady=(0, 10))

        button_criar = ttk.Button(criarFatura_frame, text='Criar Fatura', style='RoundedButton.TButton', command=on_criar_fatura_click)
        button_criar.grid(row=4, column=1, columnspan=2, pady=10)

#--------------------------------------------------------------------------------------------------------------------------------------------------#

    ######################################################################
    #############------ PAGINA GESTÃO DE PAGAMENTOS ------################
    ######################################################################

    alunos_selecionados = [] # variavel global


    #####################################################
    ##------- FUNÇOES ASSOCIADAS AS QUERIES SQL -------##
    #####################################################

    def get_curso_id():
        nome_curso = select_curso.get()
        query = f"SELECT curso_id FROM q_cursos WHERE curso_desc = '{nome_curso}'"
        resultados = executar_query(query)

        if resultados:  # Verifica se há resultados antes de acessar o índice
            return resultados[0][0]
        return None

    def atualizar_aluno():
        curso_id = get_curso_id()  # Obtém o id do curso selecionado
        query = f"SELECT q_utilizadores.utilizador_nome FROM q_utilizadores INNER JOIN q_alunos_cursos ON q_utilizadores.utilizador_id = q_alunos_cursos.aluno_id INNER JOIN q_cursos ON q_alunos_cursos.curso_id = q_cursos.curso_id WHERE q_cursos.curso_id = '{curso_id}'"
        resultados = executar_query(query)
        alunos = [resultado[0] for resultado in resultados]  # coloca os nomes numa lista
        select_aluno['values'] = alunos  # atribui os valores da lista ao select_aluno
        select_aluno.set('')  # Limpa o conteúdo do select_aluno quando atualiza o curso

    def get_alunos():
        return alunos_selecionados

    def get_aluno_id():
        aluno_nome = select_aluno.get()
        query = f"SELECT utilizador_id FROM q_utilizadores WHERE utilizador_nome = '{aluno_nome}'"
        resultados = executar_query(query)
        if resultados:  # Verifica se há resultados antes de acessar o índice
            return resultados[0][0]
        return None

    def row_pagamento_id():
        aluno_id = get_aluno_id() # Obtém o ID do aluno

        # seleciona a linha que corresponde a fatura nao paga de um determinado aluno
        query = f"SELECT pagamento_id FROM q_pagamentos WHERE pagamento_aluno_id = '{aluno_id}' AND pagamento_pagou = '0'"

        resultados = executar_query(query)

        pagamento_id = resultados[0][0] #passa o valor da linha para a variavel

        # Verifica se o pagamento_id é um número inteiro porque a tabela devolvia o numero (I001) em vez de (1)
        if isinstance(pagamento_id, int):
            return pagamento_id
        else:
            # Caso contrário, assume-se que o pagamento_id começa com um "I" seguido de um número, remove o "I" inicial e converte o restante em um número inteiro
            return int(pagamento_id[1:])

    def on_procurar_click():
        aluno_id = get_aluno_id()
        # Mostra apenas as faturas que ainda não foram pagas
        query = f"SELECT pagamento_id, pagamento_data, pagamento_curso_id, pagamento_valor FROM q_pagamentos WHERE pagamento_aluno_id = '{aluno_id}' AND pagamento_pagou = '0'"
        resultados = executar_query(query)

        try: #estrutura para verificar se existem resultados a ser mostrados

            #se existir passa os valores da lista para as variaveis
            pagamento_id = row_pagamento_id()
            data = resultados[0][1]
            curso_id = resultados[0][2]
            valor = resultados[0][3]

            #coloca os valores na tabela
            table.insert('', 'end', values=(pagamento_id, data, curso_id, valor))

        #se não houver faturas para esse determinado aluno mostra uma mensagem de erro
        except IndexError:
            messagebox.showinfo("Aviso", "Não há faturas por pagar para o aluno selecionado.")

    def on_pagar_fatura_click():

        data = select_data.get_date()# Recebe o valor do date picker

        data_formato = data.strftime("%Y-%m-%d") # Muda esse valor para o formato de data que está na base de dados


        row_id = row_pagamento_id()
        metodo_pagamento = select_pagamento.get()

        try:
            query_update = f"UPDATE q_pagamentos SET pagamento_data = '{data_formato}', pagamento_metodo = '{metodo_pagamento}', pagamento_pagou = 1 WHERE pagamento_id = {row_id}"
            executar_query(query_update)

            messagebox.showinfo("Sucesso", "A fatura foi paga com sucesso!")

        except IndexError: #caso a query nao seja executada com sucesso
            messagebox.showinfo("Aviso", "A fatura nao foi paga, verifique se selecionou corretamente todos os campos")


    def gerar_pdf():
        pagamento_id = row_pagamento_id()

        # junçao das tabelas q_pagamentos e q_utilizadores para ir buscar o valor e o nome do aluno a que se esta a pagar a fatura
        query = f"SELECT q_pagamentos.pagamento_valor, q_utilizadores.utilizador_nome " \
                f"FROM q_pagamentos " \
                f"JOIN q_utilizadores ON q_pagamentos.pagamento_aluno_id = q_utilizadores.utilizador_id " \
                f"WHERE q_pagamentos.pagamento_id = '{pagamento_id}' AND q_pagamentos.pagamento_pagou = '0'"

        resultados = executar_query(query)

        # variaveis a receber valores
        valor = resultados[0][0]
        nome_aluno = resultados[0][1]
        data = select_data.get_date()
        data_formato = data.strftime("%Y-%m-%d")
        curso_nome = select_curso.get()
        metodo_pagamento = select_pagamento.get()

        pdf = FPDF()  # Cria um novo objeto PDF

        pdf.add_page()  # Adiciona uma página ao PDF

        pdf.image("imagens/template_ipt.png", w=200, h=30)  # Adicionar a imagem do cabeçalho

        pdf.set_font("Arial", size=12)  # Define a fonte e o tamanho do texto

        # Adiciona os detalhes do pagamento ao PDF
        pdf.cell(0, 10, f"Nome do aluno: {nome_aluno}", ln=1)
        pdf.cell(0, 10, f"Nome curso: {curso_nome}", ln=1)
        pdf.cell(0, 10, f"Data: {data_formato}", ln=1)
        pdf.cell(0, 10, f"Valor: {valor}€", ln=1)
        pdf.cell(0, 10, f"Método de Pagamento: {metodo_pagamento}", ln=1)

        nome_arquivo = "detalhes_pagamento_" + str(pagamento_id) + ".pdf"
        caminho_arquivo = "pdfs_recibos/" + nome_arquivo  # Define o caminho completo do arquivo
        try:
            pdf.output(caminho_arquivo)  # Tenta salvar o PDF em um arquivo
            messagebox.showinfo("Sucesso", "O pdf foi criado com sucesso na pasta pdfs_recibos")
        except IndexError:
            messagebox.showinfo("Aviso", "O pdf tem que ser gerado antes da fatura ser paga!")

    # titulo da página
    label = Label(content_frame, text='Gestão de Pagamentos', font=('Arial', 24, 'bold'))
    label.place(x=340, y=0)

    ######################################################
    ##------- FRAME DA ESQUERDA GESTÃO PAGAMENTOS ------##
    ######################################################

    select_frame = Frame(content_frame)
    select_frame.place(x=50, y=100)

    # Label e combobox para selecionar o curso
    label_curso = Label(select_frame, text='Selecionar curso:', font=('Arial', 14))
    label_curso.grid(row=0, column=0, sticky='w', pady=10)

    # Atribui os cursos a uma variável para ser mostrado como valores no select_curso
    cursos = get_cursos()
    select_curso = ttk.Combobox(select_frame, values=cursos, font=('Arial', 12))
    select_curso.grid(row=0, column=1, padx=5, pady=5)

    button_atualizar_aluno = ttk.Button(select_frame, text='Atualizar alunos', style='RoundedButton.TButton',command=atualizar_aluno)
    button_atualizar_aluno.grid(row=1, column=1, pady=10)

    # Label e combobox para selecionar o aluno
    label_aluno = Label(select_frame, text='Selecionar aluno:', font=('Arial', 14))
    label_aluno.grid(row=2, column=0, sticky='w', pady=10)

    aluno = get_alunos()
    select_aluno = ttk.Combobox(select_frame, values=aluno, font=('Arial', 12))
    select_aluno.grid(row=2, column=1, padx=5, pady=5)

    button_procurar_faturas = ttk.Button(select_frame, text='Procurar faturas', style='RoundedButton.TButton',
                                         command=on_procurar_click)
    button_procurar_faturas.grid(row=3, column=1, pady=10)


    ########################################################
    ##------- FRAME DA DIREITA GESTÃO DE PAGAMENTOS-------##
    ########################################################

    pagar_frame = Frame(content_frame)
    pagar_frame.place(x=500, y=150)

    # Label, comboboxes e botão para realizar o pagamento
    label_info_aluno = Label(pagar_frame, text='Informações do Aluno:', font=('Arial', 16, 'bold'))
    label_info_aluno.grid(row=0, column=0, columnspan=2, pady=20)

    label_mes = Label(pagar_frame, text='Selecionar mês:', font=('Arial', 14))
    label_mes.grid(row=1, column=0, sticky='w', pady=(0, 10))

    select_data = DateEntry( pagar_frame, select_mode='day', font=('Arial', 12))
    select_data.grid(row=1, column=1, pady=(0, 10))

    label_pagamento = Label(pagar_frame, text='Selecionar método de pagamento:', font=('Arial', 14))
    label_pagamento.grid(row=2, column=0, sticky='w', pady=(0, 10))

    select_pagamento = ttk.Combobox(pagar_frame, values=['Credit Card', 'Bank Transfer', 'PayPal', 'Cash'], font=('Arial', 12))
    select_pagamento.grid(row=2, column=1, pady=(0, 10))

    button_gerar_pdf = ttk.Button(pagar_frame, text="Gerar PDF", style='RoundedButton.TButton', command=gerar_pdf)
    button_gerar_pdf.grid(row=4, column=0, columnspan=2, pady=15)

    button_pagar = ttk.Button(pagar_frame, text='Pagar Fatura', style='RoundedButton.TButton', command=on_pagar_fatura_click)
    button_pagar.grid(row=5, column=0, columnspan=2, pady=10)


    # Estilo dos botões
    style = ttk.Style()
    style.configure('RoundedButton.TButton', borderwidth=0, relief='flat', background='#383838', foreground='white',
                    font=('Arial', 12))
    style.map('RoundedButton.TButton', background=[('active', '#4C4C4C')], foreground=[('active', 'white')])

    ############################################
    ##------- TABELA FATURAS POR PAGAR -------##
    ############################################

    label_contexto = Label(content_frame, text='Tabela Faturas', font=('Arial', 16, 'bold'))
    label_contexto.place(x=50, y=300)

    # Conteúdo da tabela
    table_frame = Frame(content_frame)
    table_frame.place(x=50, y=340)

    table = ttk.Treeview(table_frame, columns=('ID', 'Data', 'Curso', 'Valor'), show='headings')
    table.column('ID', width=100)
    table.column('Data', width=100)
    table.column('Curso', width=100)
    table.column('Valor', width=100)
    table.heading('ID', text='ID')
    table.heading('Data', text='Data')
    table.heading('Curso', text='Curso')
    table.heading('Valor', text='Valor')

    table.pack()


    #########################################################
    ##-------- MENU SECUNDARIO GESTÃO DE PAGAMENTOS--------##
    #########################################################

    menu_opcoes = Frame(content_frame, bg='#b3b5b4', width=150, height=50)
    menu_opcoes.pack(anchor='ne', expand=True)

    # Estilo dos botões do menu secundário
    button_styles_mini_menu = {
        'bg': '#008080',
        'fg': 'white',
        'activebackground': '#383838',
        'activeforeground': 'white',
        'font': FONT,
        'borderwidth': 0,
        'highlightthickness': 0,
        'relief': 'flat',
        'cursor': 'hand2',
    }

    # Botões do menu secundario
    button1 = Button(menu_opcoes, text='Criar faturas', **button_styles_mini_menu, command=pagina_criar_faturas)
    button1.pack(pady=10, padx=10, fill='x')

    button2 = Button(menu_opcoes, text='Gestão de pagamentos', **button_styles_mini_menu,
                     command=abrir_gestao_pagamentos)
    button2.pack(pady=10, padx=10, fill='x')

    button3 = Button(menu_opcoes, text='Editar Faturas', **button_styles_mini_menu,
                       command=abrir_editar_faturas)
    button3.pack(pady=10, padx=10, fill='x')


def show_performance_alunos():
    clear_content_frame()
    label = Label(content_frame, text='Informações de Performance de Alunos', font=('Arial', 14))
    label.pack(pady=20)

def clear_content_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()


root = Tk()
root.title('Centro de formação')
root.geometry('1280x640+280+150')
root.resizable(False, False) #janela nao pode ser redimensionada

FONT = ('Arial', 12)

main_frame = Frame(root, width=1280, height=720, bg='#F5F5F5')
main_frame.pack(fill='both', expand=True)

menu_frame = Frame(main_frame, bg='#383838', width=200, height=720)
menu_frame.pack(side='left', fill='y')

content_frame = Frame(main_frame, bg='white', width=1080, height=720)
content_frame.pack(side='left', fill='both', expand=True)

button_styles = {
    'bg': '#008080',
    'fg': 'white',
    'activebackground': '#4C4C4C',
    'activeforeground': 'white',
    'font': FONT,
    'borderwidth': 0,
    'highlightthickness': 0,
    'relief': 'flat',
    'cursor': 'hand2',
}

button1 = Button(menu_frame, text='Gestão de Utilizadores', **button_styles, command=show_gestao_utilizadores)
button1.pack(pady=10, padx=20, fill='x')

button2 = Button(menu_frame, text='Gestão de Alunos', **button_styles, command=show_gestao_alunos)
button2.pack(pady=10, padx=20, fill='x')

button3 = Button(menu_frame, text='Gestão de Aulas e Horários', **button_styles, command=show_gestao_aulas_horarios)
button3.pack(pady=10, padx=20, fill='x')

button4 = Button(menu_frame, text='Gestão de Pagamentos', **button_styles, command=show_gestao_pagamentos)
button4.pack(pady=10, padx=20, fill='x')

button5 = Button(menu_frame, text='Performance de Alunos', **button_styles, command=show_performance_alunos)
button5.pack(pady=10, padx=20, fill='x')

root.mainloop()