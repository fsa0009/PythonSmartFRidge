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

# Login Page Class
class Login(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        global username_verify
        global password_verify
        global username_entry1
        global password_entry1

        username_verify = StringVar()
        password_verify = StringVar()

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
                              borderwidth=0, activebackground='#ebac00', cursor='hand2').place(x=810, y=175)
        login_line = Canvas(self, width=60, height=5, bg='#ebac00').place(x=810, y=203)

        # Tap Signup button
        SignUp_button = Button(self, text='Sign up', fg="white", font=("yu gothic ui bold", 12), bg="#001532",
                              command=lambda: controller.show_frame("Register"), borderwidth=0, activebackground='#ebac00', cursor='hand2')
        SignUp_button.place(x=1000, y=175)

        # Username Entry
        customtkinter.CTkLabel(right_frame, text='• Username', text_font=("yu gothic ui", 11, 'bold')).place(x=140, y=230)
        username_entry1 = Entry(right_frame, textvariable = username_verify, font=("yu gothic ui semibold", 12))
        username_entry1.place(x=174, y=260, width=256, height=34)
        username_entry1.bind('<FocusIn>', controller.entry_callback)
        # Password Entry
        customtkinter.CTkLabel(right_frame, text='• Password', text_font=("yu gothic ui", 11, 'bold')).place(x=140, y=310)
        password_entry1 = Entry(right_frame, textvariable = password_verify, font=("yu gothic ui semibold", 12), show = "•")
        password_entry1.place(x=174, y=340, width=256, height=34)
        password_entry1.bind('<FocusIn>', controller.entry_callback)
        # checkbutton for hiding and showing password
        checkButton = customtkinter.CTkCheckBox(right_frame, text='show password', command = password_command1)
        checkButton.place(x=174, y=390)



        def login_user(): # Login Process
            username_info1 = username_verify.get()
            password_info1 = password_verify.get()
            username_entry1.delete(0, END)
            password_entry1.delete(0, END)

            list_of_files = os.listdir()
            if username_info1 in list_of_files:
                file1 = open(username_info1, "r")
                verify = file1.read().splitlines()
                if password_info1 in verify:
                     messagebox.showinfo ("", "Login Success")
                     command = controller.show_frame("MainMenu")
                else:
                    messagebox.showerror("", "Verification Failed")
            else:
                messagebox.showerror("", "User not found")

        # Proceed Login button
        loginBtn1 = customtkinter.CTkButton(right_frame, text='Login', text_font=("yu gothic ui bold", 15),
                           cursor='hand2', command = login_user)
        loginBtn1.place(x=175, y=430, width=256, height=50)


def password_command1(): # show/passowrd for login
    if password_entry1.cget('show') == '•':
        password_entry1.config(show='')
    else:
        password_entry1.config(show='•')
