from Pages import *
from Pages.Pantry import *
from Pages.NonPantry import *
from Pages.Shopping import *
from Pages.Recipes import *
from Pages.MainMenu import *


class Login(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        global username
        global password
        global username_entry
        global password_entry
        global user

        username = StringVar()
        password = StringVar()
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
        tab_frame.pack(pady = (20, 50))

        # Tab Login button
        login_button = customtkinter.CTkButton(tab_frame, text='Login', text_font=("yu gothic ui bold", 12), borderwidth=0, text_color = ("#1e3d6d", "#ebe7e4"),
                                               fg_color= ("#ebe7e4", "#122e54"), hover_color= ("#c6baba", "#1e3d6d"),  cursor='hand2', width = 2)
        login_button.place(anchor = "nw")
        login_line = Canvas(tab_frame, width=60, height=5, bg='#ebac00')
        login_line.place(relx = 0, rely = 0.7)

        # Tab Signup button
        SignUp_button = customtkinter.CTkButton(tab_frame, text='Sign up', text_font=("yu gothic ui bold", 12), borderwidth=0, text_color = ("#1e3d6d", "#ebe7e4"),
                                  fg_color= ("#ebe7e4", "#122e54"), hover_color= ("#c6baba", "#1e3d6d"),  cursor='hand2', width = 2, command=lambda: controller.show_frame("Register"))
        SignUp_button.place(relx = 0.86, anchor= "n")

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
        password_entry.pack(pady = (0, 15))
        password_entry.bind('<FocusIn>', controller.entry_callback)
        # checkbutton for hiding and showing password
        def password_command(): # show/password for login
            if password_entry.cget('show') == '•':
                password_entry.configure(show='')
            else:
                password_entry.configure(show='•')

        option_frame = customtkinter.CTkFrame(right_frame, corner_radius=0, width=260, height=40)#, fg_color = "green")
        option_frame.pack()

        checkButton = customtkinter.CTkCheckBox(option_frame, text='show password', command = password_command, text_color = ("#1e3d6d", "#ebe7e4"), hover_color= ("#c6baba", "#1e3d6d"),)
        checkButton.place(relx = 0, rely = 0.06)

        def pwd_reset(): # add item pop up
            pop = customtkinter.CTkToplevel()
            pop.title("Password Reset")
            pop.attributes('-topmost', 1)
            width = 830
            height = 130
            # Centering the app in the middle of the screen
            screen_width = pop.winfo_screenwidth()
            screen_height = pop.winfo_screenheight()
            x_cordinate = int((screen_width/2) - (width/2))
            y_cordinate = int((screen_height/2) - (height/2))
            pop.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))

            username_reset = StringVar()

            def call_reset_pwd():
                if reset_pwd_entry.get() == "":
                    pop.update()
                    pop.attributes("-topmost", 0)
                    messagebox.showerror("", "Email address cannot be empty")
                    pop.update()
                    pop.attributes("-topmost",1)
                else:
                    response = FirebaseConfig().reset_password(reset_pwd_entry.get())
                    if response is None:
                        pop.destroy()
                        messagebox.showinfo ("", "Password reset link was sent to your email.")
                    else:
                        pop.update()
                        pop.attributes("-topmost", 0)
                        messagebox.showerror("", "Account not found")
                        pop.update()
                        pop.attributes("-topmost",1)


            customtkinter.CTkLabel(pop, text = "Email:", text_font=("yu gothic ui", 15, 'bold'), text_color = ("#1e3d6d", "#ebe7e4")).place(x=250, y=68, anchor=tkinter.E)

            #Entry Boxe fo reset

            reset_pwd_entry = Entry(pop, textvariable=username_reset, font=("yu gothic ui", 15), width = 30)
            reset_pwd_entry.bind('<FocusIn>', controller.entry_callback)
            reset_pwd_entry.place(x=400, y=68, anchor=tkinter.CENTER)


            customtkinter.CTkButton(pop, text="Confirm", text_font=("TkHeadingtext_font", 19) , cursor="hand2",
                    command = call_reset_pwd).place(x=720, y=68, anchor=tkinter.CENTER)

        # reset_pwd_label = Label(right_frame, text="Forgot Password?", cursor="hand2", bg="#001532", fg="white")
        reset_pwd_button = customtkinter.CTkButton(option_frame, text='Forgot Password?', text_color = ("#1e3d6d", "#ebe7e4"),
                                    fg_color= ("#ebe7e4", "#122e54"), hover_color= ("#c6baba", "#1e3d6d"),  borderwidth=0, cursor='hand2', width = 2,  command=pwd_reset)
        reset_pwd_button.place(relx = 0.76, anchor= "n")


        def login_user(): # Login Process

            if (username_entry.get() == '') or (password_entry.get() == ''):
                messagebox.showerror("","Email/Password cannot be empty!")
            else:
                global user
                if username_entry.get() == "guest":
                    Email = 'fcbaraz.i@gmail.com'
                    response = FirebaseConfig().login(Email, password_entry.get())
                elif "@gmail.com" not in username_entry.get():
                    Email = f'{username_entry.get()}@gmail.com'
                    response = FirebaseConfig().login(Email, password_entry.get())
                else:
                    Email = username_entry.get()
                    response = FirebaseConfig().login(Email, password_entry.get())
                if response:
                    tok = response['idToken']
                    complete_account_info = FirebaseConfig().auth.get_account_info(tok)
                    user = FirebaseConfig().auth.sign_in_with_email_and_password(Email, password_entry.get())
                    email_verified = complete_account_info['users'][0]['emailVerified']

                    if email_verified:
                        controller.app_login_cred['email'].set(response['email'])
                        controller.app_login_cred['idToken'].set(response['idToken'])
                        controller.app_login_cred['localId'].set(user['localId'])
                        username_entry.delete(0, END)
                        password_entry.delete(0, END)
                        command = controller.show_frame("MainMenu")
                        accountid = user['localId']
                        db = FirebaseConfig().firebase.database()
                        info = db.child("my-info").child(user['localId']).get()
                        info_values = list(info.val().values())
                        global user_name
                        user_name = info_values[1]
                        welcome_label(user_name)
                        # Pulling Users Data
                        try:
                            threading.Thread(target = query_database_non(accountid))
                        except:
                            pass
                        try:
                            threading.Thread(target = generate_recipe(accountid))
                        except:
                            pass
                        try:
                            threading.Thread(target = query_database(accountid))
                        except:
                            pass
                else:
                    messagebox.showerror("", "Verification Failed")


        def login_skip(): # Login Process

            Email = "fcbaraz.i@gmail.com"
            password = "121212"
            response = FirebaseConfig().login(Email, password)
            if response:
                tok = response['idToken']
                complete_account_info = FirebaseConfig().auth.get_account_info(tok)
                user = FirebaseConfig().auth.sign_in_with_email_and_password(Email, password)
                email_verified = complete_account_info['users'][0]['emailVerified']

                if email_verified:
                    controller.app_login_cred['email'].set(response['email'])
                    controller.app_login_cred['idToken'].set(response['idToken'])
                    controller.app_login_cred['localId'].set(user['localId'])
                    accountid = user['localId']
                    username_entry.delete(0, END)
                    password_entry.delete(0, END)
                    db = FirebaseConfig().firebase.database()
                    info = db.child("my-info").child(user['localId']).get()
                    info_values = list(info.val().values())
                    global user_name
                    user_name = info_values[1]
                    welcome_label(user_name)
                    # Pulling Users Data
                    controller.show_frame("MainMenu")
                    try:
                        threading.Thread(target = query_database_non(accountid))
                    except:
                        pass
                    try:
                        threading.Thread(target = generate_recipe(accountid))
                    except:
                        pass
                    try:
                        threading.Thread(target = query_database(accountid))
                    except:
                        pass

        # Proceed Login button
        loginBtn1 = customtkinter.CTkButton(right_frame, text='Login', text_font=("yu gothic ui bold", 15), cursor='hand2', command = lambda : threading.Thread(target= login_user).start(), width=256, height=50)
        loginBtn1.pack()
        #lambda : threading.Thread(target= login_skip).start()
