from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

menu_x = 0

def gestao_alunos():

    root = Tk()
    root.title('Centro de formação')
    root.geometry('1280x720+280+150')
    root.resizable(0, 0)

    FONT = 'Roboto 12'



    def movemenu():
        global menu_x
        menu_x += 0.001
        menu_panel.place(relx=menu_x, rely=0.095)

        if menu_x < 0.1625:
            root.after(1, movemenu)
        hamburguer_button.configure(command=goback)
        hamburguer_button.configure(image=goBack_tk)

    def goback():
        global menu_x
        menu_x -= 0.001
        menu_panel.place(relx=menu_x, rely=0.095)

        if menu_x > -0.1625:
            root.after(1, goback)
        hamburguer_button.configure(command=movemenu)
        hamburguer_button.configure(image=hamburguer_tk)



    main_frame = Frame(root, width=800, height=800, bg='#595454')
    main_frame.pack(expand=True, fill='both')

    # menu
    menu_panel = Frame(main_frame, bg='#474343')
    menu_panel.place(x=-210, y=0.01)

    button1 = Button(menu_panel, text='Gestão de Utilizadores', takefocus=False, bg='#383434', borderwidth=0,
                     fg='white', anchor='w', font=FONT, cursor='hand2')
    button1.pack(pady=5, fill='both', anchor='e')

    button2 = Button(menu_panel, text='Gestão de alunos', takefocus=False, bg='#383434', borderwidth=0, fg='white',
                     anchor='w', font=FONT, cursor='hand2')
    button2.pack(pady=5, fill='both')

    button3 = Button(menu_panel, text='Gestão de aulas e horários', takefocus=False, bg='#383434', borderwidth=0,
                     fg='white', anchor='w', font=FONT, cursor='hand2')
    button3.pack(pady=5, fill='both')

    button4 = Button(menu_panel, text='Gestão de pagamentos', takefocus=False, bg='#383434', borderwidth=0, fg='white',
                     anchor='w', font=FONT, cursor='hand2')
    button4.pack(pady=5, fill='both')

    button5 = Button(menu_panel, text='Performance de alunos', takefocus=False, bg='#383434', borderwidth=0, fg='white',
                     anchor='w', font=FONT, cursor='hand2')
    button5.pack(pady=5, fill='both')

    # hambuerguer menu
    hamburguer_original = Image.open('imagens/menu_hamburguer.png').resize((35, 35))
    hamburguer_tk = ImageTk.PhotoImage(hamburguer_original)

    goBack_original = Image.open('imagens/go_back.png').resize((35, 35))
    goBack_tk = ImageTk.PhotoImage(goBack_original)

    hamburguer_button = Button(main_frame, image=hamburguer_tk, takefocus=False, bg='#595454',
                               activebackground='#595454',
                               borderwidth=0, cursor='hand2', command=movemenu)
    hamburguer_button.place(x=5, y=5, bordermode='ignore')

    root.mainloop()

gestao_alunos()

