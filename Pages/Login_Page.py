from tkinter import *
from tkinter import ttk
import tkinter
from PIL import ImageTk, Image
from tkinter import messagebox
# from tkinter import ttk as objTTK
from functools import partial
import tkinter as tk
import subprocess
import os
import tkinter as objTK
import datetime as objDateTime
import customtkinter
import pyrebase

global test_token

class FirebaseConfig:
    def __init__(self):
        self.firebaseConfig = {
              "apiKey": "AIzaSyDEB5qdpI_D371iICJlHKfU67Op1e5JVeA",
              "authDomain": "smartfridgeapp-wvu.firebaseapp.com",
              "databaseURL": "https://smartfridgeapp-wvu-default-rtdb.firebaseio.com/my-info/cn9uHd7h4FOuX1fr9wOXw8JZwkz1",
              "projectId": "smartfridgeapp-wvu",
              "storageBucket": "smartfridgeapp-wvu.appspot.com",
              "messagingSenderId": "21386787655",
              "appId": "1:21386787655:web:cb406f9a8c8ffbaf5faa62",
              "measurementId": "G-YFLKE7K46T" }

        self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.auth = self.firebase.auth()
        self.storage = self.firebase.storage()
        self.pushdb()
    def register(self, username, password):
        try:
            user = self.auth.create_user_with_email_and_password(username, password)
            self.auth.send_email_verification(user['idToken'])
            return True
        except:
            return False

    def login(self, username, password):
        try:
            login = self.auth.sign_in_with_email_and_password(username, password)
            return login
        except:
            return False

    def reset_password(self, username_reset):
        try:
            self.auth.send_password_reset_email(username_reset)
            return
        except:
             return False

    def pushdb(self):
        data = {"name": "test 'test' test"}
        db = self.firebase.database()
        db.child("my-info").child("cn9uHd7h4FOuX1fr9wOXw8JZwkz1").child("Name")
        db.child("Name").update(data)

# Login Page Class
class Login(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        global username
        global password
        global username_entry
        global password_entry

        username = StringVar()
        password = StringVar()

        # Slicing the page
        frame = customtkinter.CTkFrame(master=self, width=1280, height=720, corner_radius=0)
        frame.place(relx=0, rely=0)

        left_frame = customtkinter.CTkFrame(master=self, width=640, height=720, corner_radius=0)
        left_frame.place(relx=0.5, rely=0.5, anchor=tkinter.E)

        right_frame = customtkinter.CTkFrame(master=self, width=640, height=720, corner_radius=0)
        right_frame.place(relx=1, rely=0.5, anchor=tkinter.E)

        # Corner Picture (logo)
        logo_img = ImageTk.PhotoImage(file="assets/images/WVU_Logo.png")
        logo_widget = customtkinter.CTkLabel(left_frame, image=logo_img )
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        # Picture on left side
        Welcome_img = ImageTk.PhotoImage(file="assets/images/WVU_Welcome.png")
        Welcome_widget = customtkinter.CTkLabel(left_frame, image=Welcome_img )
        Welcome_widget.image = Welcome_img
        Welcome_widget.place(relx=1, rely=0.5, anchor=tkinter.E)

        label_1 = customtkinter.CTkLabel(right_frame, text='Smart Fridge GUI', text_font=('Arial', 20, 'bold'))
        label_1.place(relx=0.44, rely=0.2, anchor=tkinter.CENTER)

        # Tap Login button
        login_button = customtkinter.CTkButton(self, text='Login', text_font=("yu gothic ui bold", 12), borderwidth=0,
                                                fg_color= ("#001532", "gray20"),  cursor='hand2', width = 2)
        login_button.place(x=810, y=175)
        login_line = Canvas(self, width=60, height=5, bg='#ebac00')
        login_line.place(x=810, y=203)

        # Tap Signup button
        SignUp_button = customtkinter.CTkButton(self, text='Sign up', text_font=("yu gothic ui bold", 12), fg_color= ("#001532", "gray20"), #2a2d2e
                              borderwidth=0, cursor='hand2', width = 2,  command=lambda: controller.show_frame("Register"))
        SignUp_button.place(x=1000, y=175)

        # Username Entry
        username_label = customtkinter.CTkLabel(right_frame, text='• Email', text_font=("yu gothic ui", 11, 'bold'))
        username_label.place(x=127, y=230)
        username_entry = Entry(right_frame, textvariable=username, font=("yu gothic ui", 15))
        username_entry.place(x=174, y=260, width=256, height=34)
        username_entry.bind('<FocusIn>', controller.entry_callback)
        # Password Entry
        password_label = customtkinter.CTkLabel(right_frame, text='• Password', text_font=("yu gothic ui", 11, 'bold'))
        password_label.place(x=140, y=310)
        password_entry = Entry(right_frame, textvariable=password, font=("yu gothic ui", 15), show = "•")
        password_entry.place(x=174, y=340, width=256, height=34)
        password_entry.bind('<FocusIn>', controller.entry_callback)
        # checkbutton for hiding and showing password
        checkButton = customtkinter.CTkCheckBox(right_frame, text='show password', command = password_command)
        checkButton.place(x=174, y=390)


        def login_user(): # Login Process

            if (username_entry.get() == '') or (password_entry.get() == ''):
                messagebox.showerror("","Email/Password cannot be empty!")
            else:
                response = FirebaseConfig().login(username_entry.get(), password_entry.get())
                if response:
                    tok = response['idToken']

                    complete_account_info = FirebaseConfig().auth.get_account_info(tok)
                    email_verified = complete_account_info['users'][0]['emailVerified']
                    if email_verified:
                        controller.app_login_cred['email'].set(response['email'])
                        controller.app_login_cred['idToken'].set(response['idToken'])
                        messagebox.showinfo ("", "Login Success")
                        username_entry.delete(0, END)
                        password_entry.delete(0, END)
                        command = controller.show_frame("MainMenu")
                    else:
                         messagebox.showerror("", "User not found")
                else:
                    messagebox.showerror("", "Verification Failed")

        # Proceed Login button
        loginBtn1 = customtkinter.CTkButton(right_frame, text='Login', text_font=("yu gothic ui bold", 15),
                           cursor='hand2', command = login_user)
        loginBtn1.place(x=175, y=430, width=256, height=50)

        def pwd_reset(): # add item pop up
            pop = customtkinter.CTkToplevel()
            pop.title("Reset Password")
            pop.geometry("830x130")
            username_reset = StringVar()
            ########################## positioning pop up in the center ##############################
            # Gets the requested values of the height and widht.
            windowWidth = self.winfo_reqwidth()
            windowHeight = self.winfo_reqheight()
            # Gets both half the screen width/height and window width/height
            positionRight = int(self.winfo_screenwidth()/3.1 - windowWidth/2.5)
            positionDown = int(self.winfo_screenheight()/2 - windowHeight/2)
            # Positions the window in the center of the page.
            pop.geometry("+{}+{}".format(positionRight, positionDown))
            # pop.attributes('-topmost', 1)
            ##########################################################################################
            def call_reset_pwd():
                response = FirebaseConfig().reset_password(reset_pwd_entry.get())
                if response is None:
                    messagebox.showinfo ("", "Password reset email sent successfully!")
                    pop.destroy()
                else:
                    messagebox.showerror("", "User not found")

            customtkinter.CTkLabel(pop, text = "Email:", text_font=("yu gothic ui", 15, 'bold')).place(x=250, y=68, anchor=tkinter.E)

            #Entry Boxe fo reset

            reset_pwd_entry = Entry(pop, textvariable=username_reset, font=("yu gothic ui", 15), width = 30)
            reset_pwd_entry.bind('<FocusIn>', controller.entry_callback)
            reset_pwd_entry.place(x=400, y=68, anchor=tkinter.CENTER)


            customtkinter.CTkButton(pop, text="Confirm", text_font=("TkHeadingtext_font", 19) , cursor="hand2",
                    command = call_reset_pwd).place(x=720, y=68, anchor=tkinter.CENTER)

        # reset_pwd_label = Label(right_frame, text="Forgot Password?", cursor="hand2", bg="#001532", fg="white")
        reset_pwd_button = customtkinter.CTkButton(right_frame, text='Forgot Password?', fg_color= ("#001532", "gray20"),
                                borderwidth=0, cursor='hand2', width = 2,  command=pwd_reset)
        reset_pwd_button.place(x=310, y=388)


def password_command(): # show/password for login
    if password_entry.cget('show') == '•':
        password_entry.config(show='')
    else:
        password_entry.config(show='•')
