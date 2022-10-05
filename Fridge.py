from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
import tkinter as tk
import subprocess
import os

bg_color = "#001532" # change background color

class SmartFridgeApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Login)        # First page

    def switch_frame(self, frame_class): # Destroys current frame and replaces it with a new one
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=0, sticky='nsew')

    def register_user(self): # Signup Process
        username_info = username.get()
        password_info = password.get()
        password1_info = password1.get()
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        verify_password_entry.delete(0, END)
        list_of_files = os.listdir()

        if username_info in list_of_files:
            messagebox.showerror("","Username must be unique")
            master.switch_frame(Register)
        else:
            if password_info == password1_info:
                    file = open(username_info, "w")
                    file.write(username_info+"\n")
                    file.write(password_info)
                    file.close()
                    messagebox.showinfo ("","Registration Successful. Please Login.")
                    self.switch_frame(Login)
            else:
                messagebox.showerror("","Password doesn't match")

    def login_user(self): # Login Process
        username_info1 = username_verify.get()
        password_info1 = password_verify.get()
        username_entry1.delete(0, END)
        password_entry1.delete(0, END)

        list_of_files = os.listdir()
        if username_info1 in list_of_files:
            file1 = open(username_info1, "r")
            verify = file1.read().splitlines()
            if password_info1 in verify:
                 messagebox.showinfo ("","Login Success") # Label(login, text = "Login Successful!", bg=bg_color, fg="Green", font=("TkMenuFont", 40)).pack(pady=20)
                 self.switch_frame(MainMenue)
            else:
                messagebox.showerror("","Verification Failed")
        else:
            messagebox.showerror("","User not found")

    def password_command(self): # show/passowrd for signup
        if password_entry.cget('show') == '•':
            password_entry.config(show='')
        else:
            password_entry.config(show='•')

    def password_command0(self): # show/passowrd for signup (verify password)
        if verify_password_entry.cget('show') == '•':
            verify_password_entry.config(show='')
        else:
            verify_password_entry.config(show='•')

    def password_command1(self): # show/passowrd for login
        if password_entry1.cget('show') == '•':
            password_entry1.config(show='')
        else:
            password_entry1.config(show='•')

    def clicker(self): # Popup confirming shutdown
        choice = messagebox.askquestion("Shutdown","Are you sure you want to shutdown the system?")
        if choice == 'yes':
            subprocess.call(['sudo', 'shutdown', '-h', '-t 5','now'])

    def clicker1(self): # Popup confirming restart
        choice1 = messagebox.askquestion("Reboot","Are you sure you want to reboot the system?")
        if choice1 == 'yes':
            subprocess.call(['sudo', 'restart', '-h', '-t 5','now'])

    def clicker2(self): # Popup confirming reset
        choice2 = messagebox.askquestion("Reset","Are you sure you want to reset? \n Proceeding will sign you out")
        if choice2 == 'yes':
            self.switch_frame(Login)


class Login(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = bg_color)

        global username_verify
        global password_verify
        global username_entry1
        global password_entry1
        username_verify = StringVar()
        password_verify = StringVar()

        # Slicing the page
        design_frame1 = Listbox(self, bg=bg_color, width=115, height=50, highlightthickness=0, borderwidth=0)
        design_frame1.place(x=0, y=0)
        design_frame2 = Listbox(self, bg=bg_color, width=115, height=50, highlightthickness=0, borderwidth=0)
        design_frame2.place(x=676, y=0)
        design_frame3 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame3.place(x=75, y=106)
        design_frame4 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame4.place(x=676, y=106)

        # Picture on left side
        Wekcome_img = ImageTk.PhotoImage(file="assets/WVU_Welcome.png")
        Wekcome_widget = tk.Label(design_frame3, image=Wekcome_img, bg=bg_color)
        Wekcome_widget.image = Wekcome_img
        Wekcome_widget.place(x=50, y=10)

        # Welcome title
        welcome_label = Label(design_frame4, text='Smart Fridge GUI', fg="white", font=('Arial', 20, 'bold'), bg=bg_color)
        welcome_label.place(x=130, y=15)

        # Tap Login button
        login_button = Button(self, text='Login', fg="white", font=("yu gothic ui bold", 12), bg=bg_color,
                              borderwidth=0, activebackground='#ebac00', cursor='hand2').place(x=810, y=175)
        login_line = Canvas(self, width=60, height=5, bg='#ebac00').place(x=810, y=203)

        # Tap Signup button
        SignUp_button = Button(self, text='Sign up', fg="white", font=("yu gothic ui bold", 12), bg=bg_color,
                              command=lambda: master.switch_frame(Register), borderwidth=0, activebackground='#ebac00', cursor='hand2')
        SignUp_button.place(x=1000, y=175)

        # Username Entry
        Label(design_frame4, text='• Username', fg="white", bg=bg_color, font=("yu gothic ui", 11, 'bold')).place(x=130, y=140)
        username_entry1 = Entry(design_frame4, textvariable = username_verify, fg="black", font=("yu gothic ui semibold", 12), highlightthickness=2)
        username_entry1.place(x=134, y=170, width=256, height=34)
        username_entry1.config(highlightbackground="black", highlightcolor="black")

        # Password Entry
        Label(design_frame4, text='• Password', fg="white", bg=bg_color, font=("yu gothic ui", 11, 'bold')).place(x=130, y=220)
        password_entry1 = Entry(design_frame4, textvariable = password_verify, fg="black", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2)
        password_entry1.place(x=134, y=250, width=256, height=34)
        password_entry1.config(highlightbackground="black", highlightcolor="black")

        # checkbutton for hiding and showing password
        checkButton = Checkbutton(design_frame4, fg = "#949494", bg=bg_color, text='show password', activebackground=bg_color, activeforeground="#949494",
                                    command=master.password_command1)
        checkButton.place(x=130, y=288)

        # Proceed Login button
        loginBtn1 = Button(design_frame4, fg='#f8f8f8', text='Login', bg='#ebac00', font=("yu gothic ui bold", 15),
                           cursor='hand2', activebackground='#bb9008', command=master.login_user)
        loginBtn1.place(x=133, y=340, width=256, height=50)


class Register(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = bg_color)

        global username
        global password
        global password1
        global username_entry
        global password_entry
        global verify_password_entry
        username = StringVar()
        password = StringVar()
        password1 = StringVar()

        # Slicing the page
        design_frame5 = Listbox(self, bg=bg_color, width=115, height=50, highlightthickness=0, borderwidth=0)
        design_frame5.place(x=0, y=0)
        design_frame6 = Listbox(self, bg=bg_color, width=115, height=50, highlightthickness=0, borderwidth=0)
        design_frame6.place(x=676, y=0)
        design_frame7 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame7.place(x=75, y=106)
        design_frame8 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame8.place(x=676, y=106)

        # Picture on left side
        Wekcome_img = ImageTk.PhotoImage(file="assets/WVU_Welcome.png")
        Wekcome_widget = tk.Label(design_frame7, image=Wekcome_img, bg=bg_color)
        Wekcome_widget.image = Wekcome_img
        Wekcome_widget.place(x=50, y=10)

        # Welcome title
        welcome_label = Label(design_frame8, text='Smart Fridge GUI', fg="white", font=('Arial', 20, 'bold'), bg=bg_color)
        welcome_label.place(x=130, y=15)

        # Tap Login button
        login_button = Button(self, text='Login', fg="white", font=("yu gothic ui bold", 12), bg=bg_color,
                              command=lambda: master.switch_frame(Login), borderwidth=0, activebackground='#ebac00', cursor='hand2')
        login_button.place(x=810, y=175)

        # Tap Signup button
        SignUp_button = Button(self, text='Sign up', fg="white", font=("yu gothic ui bold", 12), bg=bg_color,
                                borderwidth=0, activebackground='#ebac00', cursor='hand2')
        SignUp_button.place(x=1000, y=175)
        SignUp_line = Canvas(self, width=60, height=5, bg='#ebac00')
        SignUp_line.place(x=1000, y=203)

        # Username Entry
        Label(design_frame8, text='• Username', fg="white", bg=bg_color, font=("yu gothic ui", 11, 'bold')).place(x=130, y=120)
        username_entry = Entry(design_frame8, textvariable = username, fg="black", font=("yu gothic ui semibold", 12), highlightthickness=2)
        username_entry.place(x=134, y=150, width=256, height=34)
        username_entry.config(highlightbackground="black", highlightcolor="black")

        # Password Entry
        Label(design_frame8, text='• Password', fg="white", bg=bg_color, font=("yu gothic ui", 11, 'bold')).place(x=130, y=190)
        password_entry = Entry(design_frame8, textvariable = password, fg="black", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2)
        password_entry.place(x=134, y=220, width=256, height=34)
        password_entry.config(highlightbackground="black", highlightcolor="black")

        # Verify password
        Label(design_frame8, text='• Verify Password', fg="white", bg=bg_color, font=("yu gothic ui", 11, 'bold')).place(x=130, y=265)
        verify_password_entry= Entry(design_frame8, textvariable = password1, fg="black", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2)
        verify_password_entry.place(x=134, y=295, width=256, height=34)
        verify_password_entry.config(highlightbackground="black", highlightcolor="black")

        # checkbutton for hiding and showing password
        checkButton = Checkbutton(design_frame8, fg = "#949494", bg=bg_color, text='show password', activebackground=bg_color, activeforeground="#949494",
        command=lambda:[master.password_command0(), master.password_command()])
        checkButton.place(x=130, y=330)

        # Proceed Signup buttons
        SignUp_button1 = Button(design_frame8, fg='#f8f8f8', text='Sign Up', bg='#ebac00', font=("yu gothic ui bold", 15),
                           cursor='hand2', activebackground='#bb9008', command=master.register_user)
        SignUp_button1.place(x=135, y=370, width=256, height=50)


class MainMenue(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = bg_color)

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.pack(side="top", anchor="nw", pady=20)

        tk.Label(self, text="Main Menu", bg=bg_color, fg="white", font=("TkMenuFont", 40)).pack()

        tk.Button(self, text="List of Items", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:master.switch_frame(ItemsList)).pack(pady=20)

        tk.Button(self, text="Recipe Suggestions", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:master.switch_frame(RecipeSuggestions)).pack()

        tk.Button(self, text="Suggested Shopping List", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:master.switch_frame(SuggestedShopping)).pack(pady=20)

        tk.Button(self, text="Settings", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:master.switch_frame(Settings)).pack()


class ItemsList(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = bg_color)

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.pack(side="top", anchor="nw", pady=20)

        tk.Label(self, text="List of Items", bg=bg_color, fg="white", font=("TkMenuFont", 40)).pack()

        tk.Button(self, text="Go Back", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command=lambda:master.switch_frame(MainMenue)
            ).pack(side="bottom", anchor="se", pady=20, padx=20)


class RecipeSuggestions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = bg_color)

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.pack(side="top", anchor="nw", pady=20)

        tk.Label(self, text="Recipe Suggestions", bg=bg_color, fg="white", font=("TkMenuFont", 40)).pack()

        tk.Button(self, text="Go Back", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command=lambda:master.switch_frame(MainMenue)
            ).pack(side="bottom", anchor="se", pady=20, padx=20)


class SuggestedShopping(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = bg_color)

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.pack(side="top", anchor="nw", pady=20)

        tk.Label(self, text="Suggested Shopping List", bg=bg_color, fg="white", font=("TkMenuFont", 40)).pack()

        tk.Button(self, text="Go Back", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command=lambda:master.switch_frame(MainMenue)
            ).pack(side="bottom", anchor="se", pady=20, padx=20)


class Settings(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = bg_color)

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.pack(side="top", anchor="nw", pady=20)

        tk.Label(self, text="Settings", bg=bg_color, fg="white", font=("TkMenuFont", 40)).pack()

        tk.Button(self, text="Adjust Interface", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:master.switch_frame(AdustInterface)).pack(pady=20)

        tk.Button(self, text="Reset", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:master.clicker2()).pack()

        tk.Button(self, text="Shutdown", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:master.clicker()).pack(pady=20)

        tk.Button(self, text="Reboot", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:master.clicker1()).pack()

        tk.Button(self, text="Exit Interface", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=root.destroy).pack(pady=20)

        tk.Button(self, text="Go Back", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command=lambda:master.switch_frame(MainMenue)
            ).pack(side="bottom", anchor="se", pady=20, padx=20)


class AdustInterface(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = bg_color)


        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.pack(side="top", anchor="nw", pady=20)

        Label(self, text="Adjust Interface Theme", bg=bg_color, fg="white", font=("TkMenuFont", 40)).pack()

        tk.Button(self, fg='#f8f8f8', text='Default', bg='#ebac00', font=("yu gothic ui bold", 15),
                           cursor='hand2', activebackground='#bb9008', width = 10).pack(pady=20)  # command=lambda:master.themedark()

        tk.Button(self, fg='#f8f8f8', text='Dark', bg='#ebac00', font=("yu gothic ui bold", 15),
                           cursor='hand2', activebackground='#bb9008', width = 10).pack()  # command=lambda:master.themedark()

        tk.Button(self, fg='#f8f8f8', text='Light', bg='#ebac00', font=("yu gothic ui bold", 15),
                           cursor='hand2', activebackground='#bb9008', width = 10).pack(pady=20)  # command=lambda:master.themedark()

        tk.Button(self, text="Go Back", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command=lambda:master.switch_frame(MainMenue)
            ).pack(side="bottom", anchor="se", pady=20, padx=20)

#class PageName(tk.Frame):
    #def __init__(self, master):
        #tk.Frame.__init__(self, master, bg = bg_color)

############ Initiallize app ############
if __name__ == "__main__":
    root = SmartFridgeApp()
    root.title("Smart Fridge 1.5")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.resizable(0, 0)
    root.geometry("1280x720")   # resolution of the touchscreen 1280x720
    #root.attributes('-fullscreen', True)
    root.mainloop()
