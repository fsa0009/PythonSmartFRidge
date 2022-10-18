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

# Settings Page Class
class Settings(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        # Slicing the page
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


        label_1 = customtkinter.CTkLabel(right_frame, text='Settings', text_font=("TkMenutext_font", 50))
        label_1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)


        button_1 = customtkinter.CTkButton(right_frame, text="Reset", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=controller.Reset_prompt)
        button_1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)


        button_2 = customtkinter.CTkButton(right_frame, text="Shutdown", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=controller.Shutdown_prompt)
        button_2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


        button_3 = customtkinter.CTkButton(right_frame, text="Reboot", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=controller.Restart_prompt)
        button_3.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)


        button_4 = customtkinter.CTkButton(right_frame, text="Exit Interface", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350,  command=controller.destroy)
        button_4.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)


        label_mode = customtkinter.CTkLabel(right_frame, text="Theme:", text_font=("TkHeadingtext_font", 20))
        label_mode.place(relx=0.33, rely=0.8, anchor=tkinter.CENTER)

        optionmenu = customtkinter.CTkOptionMenu(right_frame, values=["System", "Dark", "Light"], text_font=("TkHeadingtext_font", 15),
                                            width = 200, height = 30, command=controller.change_appearance_mode)
        optionmenu.place(relx=0.59, rely=0.8, anchor=tkinter.CENTER)


        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")
