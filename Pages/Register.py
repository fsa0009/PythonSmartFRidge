from Pages import *


class Register(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        name = StringVar()
        username = StringVar()
        password = StringVar()
        verify_password = StringVar()

        # Slicing the page
        left_frame = customtkinter.CTkFrame(master=self, corner_radius=0)#, fg_color = "red")
        left_frame.grid(row = 0, column = 0, sticky = "nesw")

        right_frame = customtkinter.CTkFrame(master=self, corner_radius=0)#,  fg_color = "green")
        right_frame.grid(row = 0, column = 1, sticky = "nesw")

        # Picture on left side
        Welcome_img = Image.open("assets/images/WVU.png")
        Welcome_img = Welcome_img.resize((500, 500), Image.ANTIALIAS)
        Welcome_img = ImageTk.PhotoImage(Welcome_img)
        Welcome_widget = customtkinter.CTkLabel(left_frame, image=Welcome_img)
        Welcome_widget.image = Welcome_img
        Welcome_widget.pack(pady = (120, 0) ,anchor = "center")

        label_1 = customtkinter.CTkLabel(right_frame, text='Smart Fridge GUI', text_font=("TkMenutext_font", 25, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        label_1.pack(pady = (100, 0))

        tab_frame = customtkinter.CTkFrame(right_frame, corner_radius=0, width=260, height=40)#, fg_color = "green")
        tab_frame.pack(pady = 20)

        # Tab Login button
        login_button = customtkinter.CTkButton(tab_frame, text='Login', text_font=("yu gothic ui bold", 12), fg_color= ("#ebe7e4", "#122e54"), hover_color= ("#c6baba", "#1e3d6d"),
                                               text_color = ("#1e3d6d", "#ebe7e4"), borderwidth=0, cursor='hand2', width = 2, command=lambda: controller.show_frame("Login"))
        login_button.place(anchor = "nw")

        # Tab Signup button
        SignUp_button = customtkinter.CTkButton(tab_frame, text='Sign up', text_font=("yu gothic ui bold", 12), borderwidth=0, text_color = ("#1e3d6d", "#ebe7e4"),
                                fg_color= ("#ebe7e4", "#122e54"), hover_color= ("#c6baba", "#1e3d6d"),  cursor='hand2', width = 2)
        SignUp_button.place(relx = 0.86, anchor= "n")
        SignUp_line = Canvas(tab_frame, width=60, height=5, bg='#ebac00')
        SignUp_line.place(relx = 0.75, rely = 0.7)

        # Username Entry
        name_label = customtkinter.CTkLabel(right_frame, text='• Name', text_font=("yu gothic ui", 11, 'bold'), text_color = ("#1e3d6d", "#ebe7e4"))
        name_label.pack(padx = (0, 212))
        name_entry = Entry(right_frame, textvariable= name, font=("yu gothic ui", 15), width=23)
        name_entry.pack(pady = (0, 20))
        name_entry.bind('<FocusIn>', controller.entry_callback)

        # Username Entry
        username_label = customtkinter.CTkLabel(right_frame, text='• Email', text_font=("yu gothic ui", 11, 'bold'), text_color = ("#1e3d6d", "#ebe7e4"))
        username_label.pack(padx = (0, 212))
        username_entry = Entry(right_frame, textvariable=username, font=("yu gothic ui", 15), width=23)
        username_entry.pack(pady = (0, 20))
        username_entry.bind('<FocusIn>', controller.entry_callback)

        # Password Entry
        password_label = customtkinter.CTkLabel(right_frame, text='• Password'  , text_font=("yu gothic ui", 11, 'bold'), text_color = ("#1e3d6d", "#ebe7e4"))
        password_label.pack(padx = (0, 185))
        password_entry = Entry(right_frame, textvariable=password, font=("yu gothic ui", 15), show='•', width=23)
        password_entry.pack(pady = (0, 20))
        password_entry.bind('<FocusIn>', controller.entry_callback)

        # Verify password
        verify_password_label = customtkinter.CTkLabel(right_frame, text='• Verify Password', text_font=("yu gothic ui", 11, 'bold'), text_color = ("#1e3d6d", "#ebe7e4"))
        verify_password_label.pack(padx = (0, 140))
        verify_password_entry = Entry(right_frame, textvariable=verify_password, font=("yu gothic ui", 15), show='•', width=23)
        verify_password_entry.pack()
        verify_password_entry.bind('<FocusIn>', controller.entry_callback)

        # checkbutton for hiding and showing password
        checkButton = customtkinter.CTkCheckBox(right_frame, text='show password', text_color = ("#1e3d6d", "#ebe7e4"), hover_color= ("#c6baba", "#1e3d6d"),
                                                command=lambda:[password_command0(), password_command()])
        checkButton.pack(padx = (0, 140), pady = 15)

        def register_user(): # Signup Process

            if (name_entry.get() == '') or (username_entry.get() == '') or (password_entry.get() == '') or (verify_password_entry.get() == ''):
                messagebox.showerror("","Please enter all the required information!")
            else:
                if password.get() != verify_password.get():
                    messagebox.showerror("","Password doesn't match")
                elif len(password_entry.get()) < 6:
                    messagebox.showerror("","Make sure your password is at lest 6 characters")

                else:
                    response = FirebaseConfig().register(username_entry.get(), password_entry.get(), name_entry.get())
                    if response:
                        messagebox.showinfo ("","Registration Successful.\nPlease Verify you email before signing in.")
                        controller.show_frame("Login")
                        name_entry.delete(0, END)
                        username_entry.delete(0, END)
                        password_entry.delete(0, END)
                        verify_password_entry.delete(0, END)
                    else:
                        messagebox.showerror("","Invalid Email Address")
                        controller.show_frame("Register")

        # Proceed Signup customtkinter.CTkButtons
        SignUp_button1 = customtkinter.CTkButton(right_frame, text='Sign Up', text_font=("yu gothic ui bold", 15),
                           cursor='hand2', command=register_user, width=256, height=50)
        SignUp_button1.pack()

        def password_command(): # show/passowrd for signup
            if password_entry.cget('show') == '•':
                password_entry.configure(show='')
            else:
                password_entry.configure(show='•')

        def password_command0(): # show/passowrd for signup (verify password)
            if verify_password_entry.cget('show') == '•':
                verify_password_entry.configure(show='')
            else:
                verify_password_entry.configure(show='•')
