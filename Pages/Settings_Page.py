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

class Settings(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        
        # Slicing the page
        left_frame = customtkinter.CTkFrame(master=self, corner_radius=0)#, fg_color = "red")
        left_frame.grid(row = 0, column = 0, sticky = "nesw")

        right_frame = customtkinter.CTkFrame(master=self, corner_radius=0)#,  fg_color = "green")
        right_frame.grid(row = 0, column = 1, sticky = "nesw")

        # Picture on left side
        Welcome_img = Image.open("assets/images/WVU_Welcome.png")
        Welcome_img = Welcome_img.resize((500, 500), Image.ANTIALIAS)   
        Welcome_img = ImageTk.PhotoImage(Welcome_img)
        Welcome_widget = customtkinter.CTkLabel(left_frame, image=Welcome_img)
        Welcome_widget.image = Welcome_img
        Welcome_widget.pack(pady = (120, 0) ,anchor = "center")


        label_1 = customtkinter.CTkLabel(right_frame, text='Settings', text_font=("TkMenutext_font", 50), text_color = ("#1e3d6d", "#ebe7e4"))
        label_1.pack(pady = (110, 80))


        button_1 = customtkinter.CTkButton(right_frame, text="Reset", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=controller.Reset_prompt)
        button_1.pack(pady = (0,30))


        button_2 = customtkinter.CTkButton(right_frame, text="Shutdown", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=controller.Shutdown_prompt)
        button_2.pack()


        button_3 = customtkinter.CTkButton(right_frame, text="Reboot", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=controller.Restart_prompt)
        button_3.pack(pady = 30)


        button_4 = customtkinter.CTkButton(right_frame, text="Exit Interface", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350,  command=controller.destroy)
        button_4.pack()

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(relx=0.98, rely=0.97, anchor= "se")
