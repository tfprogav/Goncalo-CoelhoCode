from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

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

    # Título da página
    label = Label(content_frame, text='Gestão de Pagamentos', font=('Arial', 24, 'bold'))
    label.place(x=340, y=1)

    # Frame para os selects à esquerda
    select_frame = Frame(content_frame)
    select_frame.place(x=50, y=50)

    # Selects para selecionar o curso, turma e aluno
    label_curso = Label(select_frame, text='Selecionar curso:', font=('Arial', 14))
    label_curso.grid(row=0, column=0, sticky='w', pady=10)

    select_curso = ttk.Combobox(select_frame, values=['Curso 1', 'Curso 2', 'Curso 3'], font=('Arial', 12))
    select_curso.grid(row=0, column=1, padx=5, pady=5)

    label_turma = Label(select_frame, text='Selecionar turma:', font=('Arial', 14))
    label_turma.grid(row=1, column=0, sticky='w', pady=10)

    select_turma = ttk.Combobox(select_frame, values=['Turma 1', 'Turma 2', 'Turma 3'], font=('Arial', 12))
    select_turma.grid(row=1, column=1, padx=5, pady=5)

    label_aluno = Label(select_frame, text='Selecionar aluno:', font=('Arial', 14))
    label_aluno.grid(row=2, column=0, sticky='w', pady=10)

    select_aluno = ttk.Combobox(select_frame, values=['Aluno 1', 'Aluno 2', 'Aluno 3'], font=('Arial', 12))
    select_aluno.grid(row=2, column=1, padx=5, pady=5)

    # Botão de pesquisa
    button_procurar = ttk.Button(select_frame, text='Procurar', style='RoundedButton.TButton')
    button_procurar.grid(row=3, columnspan=2, pady=10)

    # Frame para pagar a fatura à direita
    pagar_frame = Frame(content_frame)
    pagar_frame.place(x=500, y=50)

    # Label para mostrar as informações do aluno selecionado
    label_info_aluno = Label(pagar_frame, text='Informações do Aluno:', font=('Arial', 16, 'bold'))
    label_info_aluno.grid(row=0, column=0, columnspan=2, pady=20)

    # Selects para selecionar o mês e o método de pagamento
    label_mes = Label(pagar_frame, text='Selecionar mês:', font=('Arial', 14))
    label_mes.grid(row=1, column=0, sticky='w', pady=(0, 10))

    select_mes = ttk.Combobox(pagar_frame, values=['Janeiro', 'Fevereiro', 'Março'], font=('Arial', 12))
    select_mes.grid(row=1, column=1, pady=(0, 10))

    label_pagamento = Label(pagar_frame, text='Selecionar método de pagamento:', font=('Arial', 14))
    label_pagamento.grid(row=2, column=0, sticky='w', pady=(0, 10))

    select_pagamento = ttk.Combobox(pagar_frame, values=['Cartão de crédito', 'Transferência bancária'],
                                    font=('Arial', 12))
    select_pagamento.grid(row=2, column=1, pady=(0, 10))

    # Botão para pagar a fatura
    button_pagar = ttk.Button(pagar_frame, text='Pagar Fatura', style='RoundedButton.TButton')
    button_pagar.grid(row=4, column=0, columnspan=2, pady=10)

    # Definição do estilo para os botões com bordas arredondadas
    style = ttk.Style()
    style.configure('RoundedButton.TButton', borderwidth=0, relief='flat', background='#383838', foreground='white',
                    font=('Arial', 12))
    style.map('RoundedButton.TButton', background=[('active', '#4C4C4C')], foreground=[('active', 'white')])

    # Tabela de faturas
    table_frame = Frame(content_frame)
    table_frame.place(x=50, y=270)

    table = ttk.Treeview(table_frame, columns=('Fatura', 'Valor', 'Status'), show='headings')
    table.column('Fatura', width=150)
    table.column('Valor', width=100)
    table.column('Status', width=100)
    table.heading('Fatura', text='Fatura')
    table.heading('Valor', text='Valor')
    table.heading('Status', text='Status')

    # Exemplo de dados da tabela (substitua com seus próprios dados)
    table.insert('', 'end', values=('Fatura 1', 'R$100', 'Pendente'))
    table.insert('', 'end', values=('Fatura 2', 'R$150', 'Pago'))
    table.insert('', 'end', values=('Fatura 3', 'R$200', 'Pendente'))
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