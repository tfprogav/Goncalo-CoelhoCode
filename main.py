from tkinter import *
from tkinter import ttk
import mysql.connector

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
    clear_content_frame()

    alunos_selecionados = []

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
        alunos = [resultado[0] for resultado in resultados]
        select_aluno['values'] = alunos
        alunos_selecionados.clear()  # Limpa a lista de alunos selecionados

    def get_alunos():
        return alunos_selecionados

    def get_faturas_aluno(aluno):
        query = f"SELECT fatura, valor, status FROM faturas WHERE aluno = '{aluno}'"
        resultados = executar_query(query)
        return resultados

    def on_procurar_click():
        aluno_selecionado = select_aluno.get()
        faturas = get_faturas_aluno(aluno_selecionado)

        table.delete(*table.get_children())

        for fatura in faturas:
            table.insert('', 'end', values=fatura)

    label = Label(content_frame, text='Gestão de Pagamentos', font=('Arial', 24, 'bold'))
    label.place(x=340, y=1)

    select_frame = Frame(content_frame)
    select_frame.place(x=50, y=50)

    label_curso = Label(select_frame, text='Selecionar curso:', font=('Arial', 14))
    label_curso.grid(row=0, column=0, sticky='w', pady=10)

    cursos = get_cursos()
    select_curso = ttk.Combobox(select_frame, values=cursos, font=('Arial', 12))
    select_curso.grid(row=0, column=1, padx=5, pady=5)

    button_atualizar_turma = ttk.Button(select_frame, text='Atualizar', style='RoundedButton.TButton', command=atualizar_aluno)
    button_atualizar_turma.grid(row=1, column=1, pady=10)

    label_aluno = Label(select_frame, text='Selecionar aluno:', font=('Arial', 14))
    label_aluno.grid(row=2, column=0, sticky='w', pady=10)

    aluno = get_alunos()
    select_aluno = ttk.Combobox(select_frame, values=aluno, font=('Arial', 12))
    select_aluno.grid(row=2, column=1, padx=5, pady=5)

    button_procurar = ttk.Button(select_frame, text='Procurar', style='RoundedButton.TButton', command=on_procurar_click)
    button_procurar.grid(row=3, columnspan=2, pady=10)

    pagar_frame = Frame(content_frame)
    pagar_frame.place(x=500, y=50)

    label_info_aluno = Label(pagar_frame, text='Informações do Aluno:', font=('Arial', 16, 'bold'))
    label_info_aluno.grid(row=0, column=0, columnspan=2, pady=20)

    label_mes = Label(pagar_frame, text='Selecionar mês:', font=('Arial', 14))
    label_mes.grid(row=1, column=0, sticky='w', pady=(0, 10))

    select_mes = ttk.Combobox(pagar_frame, values=['Janeiro', 'Fevereiro', 'Março'], font=('Arial', 12))
    select_mes.grid(row=1, column=1, pady=(0, 10))

    label_pagamento = Label(pagar_frame, text='Selecionar método de pagamento:', font=('Arial', 14))
    label_pagamento.grid(row=2, column=0, sticky='w', pady=(0, 10))

    select_pagamento = ttk.Combobox(pagar_frame, values=['Cartão de crédito', 'Transferência bancária'], font=('Arial', 12))
    select_pagamento.grid(row=2, column=1, pady=(0, 10))

    button_pagar = ttk.Button(pagar_frame, text='Pagar Fatura', style='RoundedButton.TButton')
    button_pagar.grid(row=4, column=0, columnspan=2, pady=10)

    style = ttk.Style()
    style.configure('RoundedButton.TButton', borderwidth=0, relief='flat', background='#383838', foreground='white',
                    font=('Arial', 12))
    style.map('RoundedButton.TButton', background=[('active', '#4C4C4C')], foreground=[('active', 'white')])

    table_frame = Frame(content_frame)
    table_frame.place(x=50, y=270)

    table = ttk.Treeview(table_frame, columns=('Fatura', 'Valor', 'Status'), show='headings')
    table.column('Fatura', width=150)
    table.column('Valor', width=100)
    table.column('Status', width=100)
    table.heading('Fatura', text='Fatura')
    table.heading('Valor', text='Valor')
    table.heading('Status', text='Status')

    button_atualizar_turma.invoke()
    table.pack()


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
