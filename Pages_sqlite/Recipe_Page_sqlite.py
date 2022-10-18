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


class RecipeSuggestions(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master)
        self.controller = controller

    # Steps to create a scrollable window/page:
        # 1 Create a main frame
        main_frame = customtkinter.CTkFrame(self)
        main_frame.pack(fill = BOTH, expand = 1)

        # 2 Create a Canvas inside the main frame
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side = LEFT, fill = BOTH, expand = 1)

        # 3 Add a scrollbar to the Canvas
        my_scrollbar = customtkinter.CTkScrollbar(main_frame, command = my_canvas.yview)
        my_scrollbar.pack(side = RIGHT, fill = Y)

        # 4 Configure the Canvas
        my_canvas.config(yscrollcommand = my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.config(scrollregion = my_canvas.bbox("all")))

        # 5 Create anotehr frame inside the Canvas (Content Frame)
        content_frame = customtkinter.CTkFrame(my_canvas)

        # 6 Add that new frame to a window in the Canvas
        my_canvas.create_window((0, 0), window = content_frame, anchor = "nw")


        ############################### Frame for the top bar containing title and logo ###################################
        top_frame = customtkinter.CTkFrame(self, width=1260, height=130)
        top_frame.place(x=0, y = 0)

        logo_img = ImageTk.PhotoImage(file="assets/images/WVU_Logo.png")
        logo_widget = customtkinter.CTkLabel(top_frame, image=logo_img )
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        customtkinter.CTkLabel(top_frame, text="Recipe Suggestions" , text_font=("TkMenutext_font", 40)).place(x=415, y = 40)
        ###################################################################################################################


        ############################### Frame for the bottom bar containing go back button #################################
        bottom_frame = customtkinter.CTkFrame(self, width=1260, height=100)
        bottom_frame.place(x=0, y = 650)

        customtkinter.CTkButton(bottom_frame, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")).place(x=1100, y=10)
        ###################################################################################################################


        # this is just to sit a width for the canvas
        customtkinter.CTkLabel(content_frame, text="" , text_font=("", 1000), width = 5000).grid(row=0, column=0, pady=150, padx=10)

        # Content
        recipe1_label = customtkinter.CTkLabel(content_frame, text="Recipe 1", text_font=("TkMenuFont", 20))
        recipe1_label.place(x=100, y = 150)
        recipe1_img = ImageTk.PhotoImage(file="assets/images/recipe1.png")
        recipe1_widget = customtkinter.CTkLabel(content_frame, image=recipe1_img)
        recipe1_widget.image = recipe1_img
        recipe1_widget.place(x=100, y = 200)
        recipe11_img = ImageTk.PhotoImage(file="assets/images/recipe11.png")
        recipe11_widget = customtkinter.CTkLabel(content_frame, image=recipe11_img)
        recipe11_widget.image = recipe11_img
        recipe11_widget.place(x=100, y = 435)

        recipe2_label = customtkinter.CTkLabel(content_frame, text="Recipe 2", text_font=("TkMenuFont", 20))
        recipe2_label.place(x=500, y = 150)
        recipe2_img = ImageTk.PhotoImage(file="assets/images/recipe2.png")
        recipe2_widget = customtkinter.CTkLabel(content_frame, image=recipe2_img)
        recipe2_widget.image = recipe2_img
        recipe2_widget.place(x=500, y = 200)
        recipe22_img = ImageTk.PhotoImage(file="assets/images/recipe22.png")
        recipe22_widget = customtkinter.CTkLabel(content_frame, image=recipe22_img)
        recipe22_widget.image = recipe22_img
        recipe22_widget.place(x=500, y = 435)

        recipe3_label = customtkinter.CTkLabel(content_frame, text="Recipe 3", text_font=("TkMenuFont", 20))
        recipe3_label.place(x=900, y = 150)
        recipe3_img = ImageTk.PhotoImage(file="assets/images/recipe3.png")
        recipe3_widget = customtkinter.CTkLabel(content_frame, image=recipe3_img)
        recipe3_widget.image = recipe3_img
        recipe3_widget.place(x=900, y = 200)
        recipe33_img = ImageTk.PhotoImage(file="assets/images/recipe33.png")
        recipe33_widget = customtkinter.CTkLabel(content_frame, image=recipe33_img)
        recipe33_widget.image = recipe33_img
        recipe33_widget.place(x=900, y = 435)
