from tkinter import *
from tkinter import ttk
import tkinter
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk as objTTK
from functools import partial
import tkinter as tk
import subprocess
import os
import tkinter as objTK
import datetime as objDateTime
import customtkinter
import pyrebase
from Pages.Login_Page import FirebaseConfig

# Register Page Class
class Register(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        username = StringVar()
        password = StringVar()
        verify_password = StringVar()

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
        login_button = customtkinter.CTkButton(self, text='Login', text_font=("yu gothic ui bold", 12), fg_color= ("#001532", "#2a2d2e"),
                              borderwidth=0,   cursor='hand2', width = 2, command=lambda: controller.show_frame("Login"),)
        login_button.place(x=810, y=175)

        # Tap Signup button
        SignUp_button = customtkinter.CTkButton(self, text='Sign up', text_font=("yu gothic ui bold", 12), borderwidth=0, fg_color= ("#001532", "#2a2d2e"),  cursor='hand2', width = 2)
        SignUp_button.place(x=1000, y=175)
        SignUp_line = Canvas(self, width=60, height=5, bg='#ebac00')
        SignUp_line.place(x=1005, y=203)

        # Username Entry
        username_label = customtkinter.CTkLabel(right_frame, text='• Email', text_font=("yu gothic ui", 11, 'bold'))
        username_label.place(x=127, y=230)
        username_entry = Entry(right_frame, textvariable=username, font=("yu gothic ui", 15))
        username_entry.place(x=174, y=260, width=256, height=34)
        username_entry.bind('<FocusIn>', controller.entry_callback)

        # Password Entry
        password_label = customtkinter.CTkLabel(right_frame, text='• Password'  , text_font=("yu gothic ui", 11, 'bold'))
        password_label.place(x=140, y=310)
        password_entry = Entry(right_frame, textvariable=password, font=("yu gothic ui", 15), show='•')
        password_entry.place(x=174, y=340, width=256, height=34)
        password_entry.bind('<FocusIn>', controller.entry_callback)

        # Verify password
        verify_password_label = customtkinter.CTkLabel(right_frame, text='• Verify Password', text_font=("yu gothic ui", 11, 'bold'))
        verify_password_label.place(x=162, y=390)
        verify_password_entry = Entry(right_frame, textvariable=verify_password, font=("yu gothic ui", 15), show='•')
        verify_password_entry.place(x=174, y=420, width=256, height=34)
        verify_password_entry.bind('<FocusIn>', controller.entry_callback)

        # checkbutton for hiding and showing password
        checkButton = customtkinter.CTkCheckBox(right_frame, text='show password',
        command=lambda:[password_command0(), password_command()])
        checkButton.place(x=174, y=470)

        def register_user(): # Signup Process
            password_info = password.get()
            verify_password_info = verify_password.get()

            if (username_entry.get() == '') or (password_entry.get() == '') or (verify_password_entry.get() == ''):
                messagebox.showerror("","Email/Password cannot be empty!")
            else:
                if password_info != verify_password_info:
                    messagebox.showerror("","Password doesn't match")
                elif len(password_entry.get()) < 6:
                    messagebox.showerror("","Make sure your password is at lest 6 characters")

                else:
                    response = FirebaseConfig().register(username_entry.get(), password_entry.get())
                    if response:
                        messagebox.showinfo ("","Registration Successful. Please Verify you email before Login.")
                        controller.show_frame("Login")
                        username_entry.delete(0, END)
                        password_entry.delete(0, END)
                        verify_password_entry.delete(0, END)
                    else:
                        messagebox.showerror("","An account with this email already exist")
                        controller.show_frame("Register")


        # Proceed Signup customtkinter.CTkButtons
        SignUp_button1 = customtkinter.CTkButton(right_frame, text='Sign Up', text_font=("yu gothic ui bold", 15),
                           cursor='hand2', command=register_user)
        SignUp_button1.place(x=174, y=510, width=256, height=50)

        def change_mode():
            if switch.get() == 1:
                customtkinter.set_appearance_mode("dark")
            else:
                customtkinter.set_appearance_mode("light")

        switch = customtkinter.CTkSwitch(left_frame, text="Dark Mode", command = change_mode)
        switch.place(x=20, y=680)

        def password_command(): # show/passowrd for signup
            if password_entry.cget('show') == '•':
                password_entry.config(show='')
            else:
                password_entry.config(show='•')

        def password_command0(): # show/passowrd for signup (verify password)
            if verify_password_entry.cget('show') == '•':
                verify_password_entry.config(show='')
            else:
                verify_password_entry.config(show='•')
