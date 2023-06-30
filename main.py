from tkinter import *
from tkinter import ttk
import mysql.connector
from tkcalendar import DateEntry
from tkinter import messagebox
from PIL import Image
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
    # limpa a frama para aparecer a nova pagina
    clear_content_frame()
    # variavel global
    alunos_selecionados = []

    ##------- FUNÇOES ASSOCIADAS AS QUERIES SQL -------##
    def get_cursos():
        query = "SELECT curso_id, curso_desc, CONCAT(curso_id, ' - ', curso_desc) AS courses FROM q_cursos"
        resultados = executar_query(query)
        cursos = [resultado[1] for resultado in resultados]  # Obtém o valor concatenado do curso
        return cursos

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

    def row_pagamento_id(): #funçao para ir buscar o id como numero inteiro sem o I incial
        aluno_id = get_aluno_id()
        # mostra apenas as faturas que ainda nao foram pagas
        query = f"SELECT pagamento_id FROM q_pagamentos WHERE pagamento_aluno_id = '{aluno_id}' AND pagamento_pagou = '0'"
        resultados = executar_query(query)
        pagamento_id = resultados[0][0]
        if isinstance(pagamento_id, int):
            return pagamento_id
        else:
            return int(pagamento_id[1:])

    def on_procurar_click():
        aluno_id = get_aluno_id()
        # Mostra apenas as faturas que ainda não foram pagas
        query = f"SELECT pagamento_id, pagamento_data, pagamento_curso_id, pagamento_valor FROM q_pagamentos WHERE pagamento_aluno_id = '{aluno_id}' AND pagamento_pagou = '0'"
        resultados = executar_query(query)

        try: #estrutura para verificar se existem resultados a ser mostrados
            pagamento_id = row_pagamento_id()
            data = resultados[0][1]
            curso_id = resultados[0][2]
            valor = resultados[0][3]

            print(pagamento_id, data, curso_id, valor)

            table.delete(*table.get_children())
            table.insert('', 'end', values=(pagamento_id, data, curso_id, valor))

        except IndexError: #caso nao haja resultados mostra o erro
            messagebox.showinfo("Aviso", "Não há faturas por pagar para o aluno selecionado.")

    def on_pagar_fatura_click():
        # Recebe o valor do date picker
        data = select_data.get_date()

        # Muda esse valor para o formato de data que está na base de dados
        data_formato = data.strftime("%Y-%m-%d")

        row_id = row_pagamento_id()
        metodo_pagamento = select_pagamento.get()

        try:
            query_update = f"UPDATE q_pagamentos SET pagamento_data = '{data_formato}', pagamento_metodo = '{metodo_pagamento}', pagamento_pagou = 1 WHERE pagamento_id = {row_id}"
            executar_query(query_update)

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

        data = select_data.get_date()
        data_formato = data.strftime("%Y-%m-%d")

        curso_id = get_curso_id()

        valor = resultados[0][0]
        nome_aluno = resultados[0][1] #nome

        metodo_pagamento = select_pagamento.get()

        pdf = FPDF() # Cria um novo objeto PDF

        pdf.add_page() # Adiciona uma página ao PDF

        pdf.image("imagens/template_ipt.png", w= 200, h= 30 ) # Adicionar a imagem do cabeçalho

        pdf.set_font("Arial", size=12) # Define a fonte e o tamanho do texto

        # Adiciona os detalhes do pagamento ao PDF
        pdf.cell(0, 10, f"Nome do aluno: {nome_aluno}", ln=1)
        pdf.cell(0, 10, f"Data: {data_formato}", ln=1)
        pdf.cell(0, 10, f"Curso ID: {curso_id}", ln=1)
        pdf.cell(0, 10, f"Valor: {valor}", ln=1)
        pdf.cell(0, 10, f"Método de Pagamento: {metodo_pagamento}", ln=1)

        # Salva o PDF em um arquivo
        pdf.output("detalhes_pagamento.pdf")


    def pagina_criar_faturas():
        clear_content_frame()

        #titulo da pagina
        label = Label(content_frame, text='Criar faturas', font=('Arial', 24, 'bold'))
        label.place(x=340, y=0)

        #####################################
        ##-------- MENU SECUNDARIO --------##
        #####################################

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


    def abrir_gestao_pagamentos():
        clear_content_frame()
        show_gestao_pagamentos()



    #####################################
    ##-------- MENU SECUNDARIO --------##
    #####################################

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
    #Botões do menu secundario
    button1 = Button(menu_opcoes, text='Criar faturas', **button_styles_mini_menu, command=pagina_criar_faturas)
    button1.pack(pady=10, padx=10, fill='x')

    button2 = Button(menu_opcoes, text='Gestão de pagamentos', **button_styles_mini_menu, command=abrir_gestao_pagamentos)
    button2.pack(pady=10, padx=10, fill='x')

    # titulo da página
    label = Label(content_frame, text='Gestão de Pagamentos', font=('Arial', 24, 'bold'))
    label.place(x=340, y=0)

    #####################################
    ##------- FRAME DA ESQUERDA -------##
    #####################################

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

    #####################################
    ##------- TABELA FATURAS -------##
    #####################################

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

    #####################################
    ##------- FRAME DA DIREITA -------##
    #####################################

    pagar_frame = Frame(content_frame)
    pagar_frame.place(x=500, y=100)

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

    button_pagar = ttk.Button(pagar_frame, text='Pagar Fatura', style='RoundedButton.TButton', command=on_pagar_fatura_click)
    button_pagar.grid(row=4, column=0, columnspan=2, pady=10)

    btn_gerar_pdf = ttk.Button(pagar_frame, text="Gerar PDF", command=gerar_pdf)
    btn_gerar_pdf.grid(row=5, column=0, columnspan=2, pady=15)

    # Estilo dos botões
    style = ttk.Style()
    style.configure('RoundedButton.TButton', borderwidth=0, relief='flat', background='#383838', foreground='white',
                    font=('Arial', 12))
    style.map('RoundedButton.TButton', background=[('active', '#4C4C4C')], foreground=[('active', 'white')])

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
root.resizable(0, 0)

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