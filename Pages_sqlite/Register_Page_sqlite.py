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
import sqlite3


class Register(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

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
        login_button = Button(self, text='Login', fg="white", font=("yu gothic ui bold", 12), bg="#001532",
                              command=lambda: controller.show_frame("Login"), borderwidth=0, activebackground='#ebac00', cursor='hand2')
        login_button.place(x=810, y=175)

        # Tap Signup button
        SignUp_button = Button(self, text='Sign up', fg="white", font=("yu gothic ui bold", 12), bg="#001532", borderwidth=0, activebackground='#ebac00', cursor='hand2')
        SignUp_button.place(x=1000, y=175)
        SignUp_line = Canvas(self, width=60, height=5, bg='#ebac00')
        SignUp_line.place(x=1000, y=203)

        # Username Entry
        customtkinter.CTkLabel(right_frame, text='• Username', text_font=("yu gothic ui", 11, 'bold')).place(x=140, y=230)
        username_entry = Entry(right_frame, textvariable = username , font=("yu gothic ui semibold", 12))
        username_entry.place(x=174, y=260, width=256, height=34)
        username_entry.bind('<FocusIn>', controller.entry_callback)
        # Password Entry
        customtkinter.CTkLabel(right_frame, text='• Password'  , text_font=("yu gothic ui", 11, 'bold')).place(x=140, y=310)
        password_entry = Entry(right_frame, textvariable = password , font=("yu gothic ui semibold", 12), show='•')
        password_entry.place(x=174, y=340, width=256, height=34)
        password_entry.bind('<FocusIn>', controller.entry_callback)
        # Verify password
        customtkinter.CTkLabel(right_frame, text='• Verify Password', text_font=("yu gothic ui", 11, 'bold')).place(x=162, y=390)
        verify_password_entry= Entry(right_frame, textvariable = password1 , font=("yu gothic ui semibold", 12), show='•')
        verify_password_entry.place(x=174, y=420, width=256, height=34)
        verify_password_entry.bind('<FocusIn>', controller.entry_callback)
        # checkbutton for hiding and showing password
        checkButton = customtkinter.CTkCheckBox(right_frame, text='show password',
        command=lambda:[password_command0(), password_command()])
        checkButton.place(x=174, y=470)

        def register_user(): # Signup Process
            username_info = username.get()
            password_info = password.get()
            password1_info = password1.get()
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            verify_password_entry.delete(0, END)
            list_of_files = os.listdir()

            if username_info in list_of_files:
                messagebox.showerror("","Username must be unique")
                controller.show_frame("Register")
            else:
                if password_info == password1_info:
                        file = open(username_info, "w")
                        file.write(username_info+"\n")
                        file.write(password_info)
                        file.close()
                        messagebox.showinfo ("","Registration Successful. Please Login.")
                        controller.show_frame("Login")
                else:
                    messagebox.showerror("","Password doesn't match")

        # Proceed Signup customtkinter.CTkButtons
        SignUp_button1 = customtkinter.CTkButton(right_frame, text='Sign Up', text_font=("yu gothic ui bold", 15),
                           cursor='hand2', command=register_user)
        SignUp_button1.place(x=174, y=510, width=256, height=50)



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
