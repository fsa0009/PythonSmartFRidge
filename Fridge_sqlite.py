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

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
#customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue", "sweetkind"
customtkinter.set_default_color_theme("assets/themes/wvu-dark.json")

class SmartFridgeApp(customtkinter.CTk):    # Main Class
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)
        window = customtkinter.CTkFrame(self)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, Register, MainMenu, ItemsList, AddItems, RecipeSuggestions, SuggestedShopping, Settings):
            page_name = F.__name__
            global frame
            frame = F(master=window, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

        # Styling the treeviews
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("", 15), background="#2a2d2e", foreground="white", rowheight=35, fieldbackground="#343638", bordercolor="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", font=('Arial', 15, 'bold'), background="#565b5e",
                                                    foreground="white", relief="flat",  rowheight=35, fieldbackground="#343638", bordercolor="#343638", borderwidth=0)
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    def entry_callback(self, event): # Call Matchbox keyboard automatically
        os.popen('matchbox-keyboard','r',4096)

    # Functions for Login and Register Pages
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
            self.show_frame("Register")
        else:
            if password_info == password1_info:
                    file = open(username_info, "w")
                    file.write(username_info+"\n")
                    file.write(password_info)
                    file.close()
                    messagebox.showinfo ("","Registration Successful. Please Login.")
                    self.show_frame("Login")
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
                 messagebox.showinfo ("", "Login Success")
                 self.show_frame("MainMenu")
            else:
                messagebox.showerror("", "Verification Failed")
        else:
            messagebox.showerror("", "User not found")
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

    # Functions for ItemsList Page
    def List_delete_one(self): # Delete one selected ITEM
        List_selected = List.selection()
        if List.selection()==():
            messagebox.showerror("", "Please Select an Item to Delete")
        else:
            choice = messagebox.askquestion("Delete Item", "Are you sure you want to delete the selected item?")
            if choice == 'yes':

                ############## Delete item from  Database ##############
                conn = sqlite3.connect('items_list.db')
                c = conn.cursor()
                # Delete item from the table

                c.execute("DELETE from items WHERE oid =" + oid_entry.get())

                # clear entries
                self.clear_entries()
                # Commit changes
                conn.commit()
                # Close our connection
                conn.close()
                #########################################################
                # Clear the Treeview
                List.delete(*List.get_children())
                # Requiry
                self.query_database()
                messagebox.showinfo ("", "Item Deleted!")
    def List_delete_selected(self): # Delete multiple selected ITEMS
        List_selected = List.selection()
        # Create List of ID's
        ids_to_delete = []
        # Add selections to ids_to_delete list
        for record in List_selected:
                ids_to_delete.append(List.item(record, "values")[4])
        if List.selection()==():
            messagebox.showerror("", "Please Select an Item to Delete")
        else:

            choice = messagebox.askquestion("Delete Item", "Are you sure you want to delete the selected item?")
            if choice == 'yes':

                ##################### Delete selected from the Database ######################
                conn = sqlite3.connect('items_list.db')
                c = conn.cursor()
                # Delete selected items from the table
                c.executemany("DELETE FROM items WHERE rowid = ?", [(a,) for a in ids_to_delete])
                # clear entries
                self.clear_entries()
                # Commit changes
                conn.commit()
                # Close our connection
                conn.close()
                #############################################################################
                # Clear the Treeview
                List.delete(*List.get_children())
                # Requiry
                self.query_database()
                messagebox.showinfo ("", "Item/s Deleted!")
    def List_delete_all(self): # Delets all items

        choice = messagebox.askquestion("Delete All Items", "Are you sure you want to delete ALL items?")

        if choice == 'yes':
            ############## Delete everything from the Database ##############
            conn = sqlite3.connect('items_list.db')
            c = conn.cursor()
            # Delete everything from the table

            c.execute("DROP TABLE items ")

            # clear entries
            self.clear_entries()
            # Commit changes
            conn.commit()
            # Close our connection
            conn.close()

            ##################################################################
            # Clear the Treeview
            List.delete(*List.get_children())
            # Recreate the Table
            self.create_after_drop()
            messagebox.showinfo ("", "Items Deleted!")
    def create_after_drop(self):
        conn = sqlite3.connect('items_list.db')
        # Create a cursor instance
        c = conn.cursor()

        # Create table
        c.execute("""CREATE TABLE if not exists items(
            item_name text,
            brand_name text,
            expiration_date date,
            remaining_amount integer
            )
            """)

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()
    def fake_database(self):
        List_data =[
            ["A", "C", "12-04-2022", "40%"],
            ["B", "A", "12-06-2022", "60%"],
            ["C", "D", "12-01-2022", "20%"],
            ["D", "B", "12-02-2022", "30%"],
            ["E", "F", "12-05-2022", "50%"],
            ["F", "E", "12-03-2022", "100%"]
            ]

        for record in range(len(List_header)):
            strHdr = List_header[record]
            List.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            List.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])

        for record in range(len(List_data)):
            List.insert("", "end", values=List_data[record])

        conn = sqlite3.connect('items_list.db')
        # Create a cursor instance
        c = conn.cursor()

        # Create table
        c.execute("""CREATE TABLE if not exists items(
            item_name text,
            brand_name text,
            expiration_date date,
            remaining_amount integer
            )
            """)


        for record in List_data:
            c.execute("INSERT INTO items VALUES (:item_name, :brand_name, :expiration_date, :remaining_amount)",
                {
                'item_name': record[0],
                'brand_name': record[1],
                'expiration_date': record[2],
                'remaining_amount': record[3]
                }
                )

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()
    def select_record(self, e):
        # clear entry boxes
        name_entry.delete(0, END)
        brand_entry.delete(0, END)
        exdate_entry.delete(0, END)
        amount_entry.delete(0, END)
        oid_entry.delete(0, END)

        # Grab record number
        selected = List.focus()
        # Grab record VALUES
        values = List.item(selected, "values")
        # output to entry boxes
        name_entry.insert(0, values[0])
        brand_entry.insert(0, values[1])
        exdate_entry.insert(0, values[2])
        amount_entry.insert(0, values[3])
        oid_entry.insert(0, values[4])
    def clear_entries(self):
        name_entry.delete(0, END)
        brand_entry.delete(0, END)
        exdate_entry.delete(0, END)
        amount_entry.delete(0, END)
        oid_entry.delete(0, END)
    def update_record(self):
        # Grab the record number
        selected = List.focus()
        List.item(selected, text="", values=(name_entry.get(), brand_entry.get(), exdate_entry.get(), amount_entry.get(), oid_entry.get()))

        self.clear_entries()

    # Functions for AddItems Page
    def List_add_record(self): # adds the data to the table (List)
        # List.insert("", "end", values=(name_entry.get(), brand_entry.get(), exdate_entry.get(), amount_entry.get()))

        if name_entry.get()=="":
            messagebox.showerror("", "Item's data needed")
        else:
            ############## Add to the Database ##############
            conn = sqlite3.connect('items_list.db')
            c = conn.cursor()

            c.execute("INSERT INTO items VALUES (:item_name, :brand_name, :expiration_date, :remaining_amount)",
                {
                    'item_name': name_entry.get(),
                    'brand_name': brand_entry.get(),
                    'expiration_date': exdate_entry.get(),
                    'remaining_amount': amount_entry.get(),
                })

            # Commit changes
            conn.commit()
            # Close our connection
            conn.close()
            #################################################
            # Clear the Treeview
            List.delete(*List.get_children())
            # Requiry
            self.query_database()

            name_entry.delete(0, END)
            brand_entry.delete(0, END)
            exdate_entry.delete(0, END)
            amount_entry.delete(0,END)
    def query_database(self):
        conn = sqlite3.connect('items_list.db')
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM items")
        records = c.fetchall()
        # print(records)
        # for record in records:
        #     print(record)
        global record
        for record in range(len(List_header)):
            strHdr = List_header[record]
            List.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            List.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])
        count = 0
        for record in records:
            List.insert(parent='', index='end', iid=count, text=count+1, values= (record[1], record[2], record[3], record[4], record[0]) )
            count += 1

        # for record in range(len(List_data)):
        #     List.insert("", "end", values=List_data[record])


        # for record in records:
        #     if count % 2 == 0:
        #         List.insert(parent='', index='end', iid=count, text=count+1, values=(record[1], record[2], record[3], record[4]), tags=('evenrow',))
        #     else:
        #         List.insert(parent='', index='end', iid=count, text=count+1, values=(record[1], record[2], record[3], record[4]), tags=('oddrow',))
        #     count += 1

        # Commit changes
        conn.commit()
        # Close our connection
        conn.close()

    # Functions for ShoppingList Page
    def ShoppingList_delete_all(self): # Delets all items
        for values in ShoppingList.get_children():
            ShoppingList.delete(values)
    def ShoppingList_delete_selected(self): # Delete multiple selected ITEMS
        ShoppingList_delete_selected = ShoppingList.selection()
        for values in ShoppingList_delete_selected:
            ShoppingList.delete(values)
    def ShoppingList_add_popup (self): # add item pop up
        global name_entry1
        global brand_entry1
        global root
        pop = customtkinter.CTkToplevel(self)
        pop.title("Add items to your Shopping list")
        pop.geometry("830x130")

        ########################## Ignore This ##############################
        # Gets the requested values of the height and widht.
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        print("Width",windowWidth,"Height",windowHeight)
        # Gets both half the screen width/height and window width/height
        positionRight = int(root.winfo_screenwidth()/2.7 - windowWidth/2.5)
        positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
        # Positions the window in the center of the page.
        pop.geometry("+{}+{}".format(positionRight, positionDown))
        ####################################################################

        customtkinter.CTkLabel(pop, text = "Name:", text_font=("yu gothic ui", 15, 'bold')).place(x=163, y=30, anchor=tkinter.E)
        customtkinter.CTkLabel(pop, text = "Brand:", text_font=("yu gothic ui", 15, 'bold')).place(x=463, y=30, anchor=tkinter.E)

        #Entry Boxes
        name_entry1 = customtkinter.CTkEntry(pop, text_font=("yu gothic ui", 15), width = 280)
        name_entry1.bind('<FocusIn>', self.entry_callback)
        name_entry1.place(x=200, y=68, anchor=tkinter.CENTER)

        brand_entry1 = customtkinter.CTkEntry(pop, text_font=("yu gothic ui", 15), width = 280)
        brand_entry1.bind('<FocusIn>', self.entry_callback)
        brand_entry1.place(x=500, y=68, anchor=tkinter.CENTER)

        customtkinter.CTkButton(pop, text="Confirm", text_font=("TkHeadingtext_font", 19) , cursor="hand2",
                command = self.ShoppingList_add_record).place(x=720, y=68, anchor=tkinter.CENTER)
    def ShoppingList_add_record(self): # adds the data to the table (ShoppingList)
        ShoppingList.insert("", "end", values=(name_entry1.get(), brand_entry1.get()))
        # clear the entry boxes
        name_entry1.delete(0, END)
        brand_entry1.delete(0, END)

    # Functions for Settings Page
    def Reset_prompt(self): # Popup confirming reset
        choice = messagebox.askquestion("Reset", "Are you sure you want to reset? \n Proceeding will sign you out")
        if choice == 'yes':
            self.show_frame("Login")
    def Shutdown_prompt(self): # Popup confirming shutdown
        choice = messagebox.askquestion("Shutdown", "Are you sure you want to shutdown the system?")
        if choice == 'yes':
            subprocess.call(['sudo', 'shutdown', '-h', '-t 5', 'now'])
    def Restart_prompt(self): # Popup confirming restart
        choice = messagebox.askquestion("Reboot", "Are you sure you want to reboot the system?")
        if choice == 'yes':
            subprocess.call(['sudo', 'shutdown', '-r', '-t 5', 'now'])
    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


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
        checkButton = customtkinter.CTkCheckBox(right_frame, text='show password', command=controller.password_command1)
        checkButton.place(x=174, y=390)

        # Proceed Login button
        loginBtn1 = customtkinter.CTkButton(right_frame, text='Login', text_font=("yu gothic ui bold", 15),
                           cursor='hand2', command=controller.login_user)
        loginBtn1.place(x=175, y=430, width=256, height=50)


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
        command=lambda:[controller.password_command0(), controller.password_command()])
        checkButton.place(x=174, y=470)

        # Proceed Signup customtkinter.CTkButtons
        SignUp_button1 = customtkinter.CTkButton(right_frame, text='Sign Up', text_font=("yu gothic ui bold", 15),
                           cursor='hand2', command=controller.register_user)
        SignUp_button1.place(x=174, y=510, width=256, height=50)


class MainMenu(customtkinter.CTkFrame):
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

        label_1 = customtkinter.CTkLabel(right_frame, text='Main Menu', text_font=("TkMenutext_font", 50))
        label_1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        button_1 = customtkinter.CTkButton(right_frame, text="List of Items", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=lambda:controller.show_frame("ItemsList"))
        button_1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        button_2 = customtkinter.CTkButton(right_frame, text="Recipe Suggestions", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=lambda:controller.show_frame("RecipeSuggestions"))
        button_2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        button_3 = customtkinter.CTkButton(right_frame, text="Shopping List", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=lambda:controller.show_frame("SuggestedShopping"))
        button_3.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        button_4 = customtkinter.CTkButton(right_frame, text="Settings", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=lambda:controller.show_frame("Settings"))
        button_4.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)


class ItemsList(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        class MyTreeview(objTTK.Treeview):
                def heading(self, column, sort_by=None, **kwargs):
                    if sort_by and not hasattr(kwargs, 'command'):
                        func = getattr(self, f"_sort_by_{sort_by}", None)
                        if func:
                            kwargs['command'] = partial(func, column, False)
                        # End of if
                    # End of if
                    return super().heading(column, **kwargs)
                # End of heading()

                def _sort(self, column, reverse, data_type, callback):
                    l = [(self.set(k, column), k) for k in self.get_children('')]
                    l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
                    for index, (_, k) in enumerate(l):
                        self.move(k, '', index)
                    # End of for loop
                    self.heading(column, command=partial(callback, column, not reverse))
                # End of _sort()

                def _sort_by_num(self, column, reverse):
                    self._sort(column, reverse, int, self._sort_by_num)
                # End of _sort_by_num()

                def _sort_by_name(self, column, reverse):
                    self._sort(column, reverse, str, self._sort_by_name)
                # End of _sort_by_num()

                def _sort_by_date(self, column, reverse):
                    def _str_to_datetime(string):
                        return objDateTime.datetime.strptime(string, "%m-%d-%Y")
                    # End of _str_to_datetime()

                    self._sort(column, reverse, _str_to_datetime, self._sort_by_date)
                # End of _sort_by_num()

                def _sort_by_multidecimal(self, column, reverse):
                    def _multidecimal_to_str(string):
                        arrString = string.split(".")
                        strNum = ""
                        for iValue in arrString:
                            strValue = f"{int(iValue):02}"
                            strNum = "".join([strNum, str(strValue)])
                        # End of for loop
                        strNum = "".join([strNum, "0000000"])
                        return int(strNum[:8])
                    # End of _multidecimal_to_str()

                    self._sort(column, reverse, _multidecimal_to_str, self._sort_by_multidecimal)
                # End of _sort_by_num()

                def _sort_by_percentage(self, column, reverse):
                    def _percentage_to_num(string):
                        return int(string.replace("%", ""))
                    # End of _percentage_to_num()

                    self._sort(column, reverse, _percentage_to_num, self._sort_by_percentage)
                # End of _sort_by_num()

                def _sort_by_numcomma(self, column, reverse):
                    def _numcomma_to_num(string):
                        return int(string.replace(",", ""))
                    # End of _numcomma_to_num()

                    self._sort(column, reverse, _numcomma_to_num, self._sort_by_numcomma)
                # End of _sort_by_num()

        global List
        global List_header
        global List_SortType
        global List_ColWidth
        global List_ColAlignment
        global name_entry
        global brand_entry
        global exdate_entry
        global amount_entry
        global oid_entry

        logo_img = ImageTk.PhotoImage(file="assets/images/WVU_Logo.png")
        logo_widget = customtkinter.CTkLabel(self, image=logo_img )
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        customtkinter.CTkLabel(self, text="List of Items" , text_font=("TkMenutext_font", 40)).place(x=493, y = 40)


        table_frame = customtkinter.CTkFrame(self,  highlightthickness=0, borderwidth=0, width=800, height=500)
        table_frame.place(relx=0.525, rely=0.53, anchor=tkinter.CENTER)

        List_header = ["Name", "Brand", "Expiration Date", "Remaining"]

        # Creating Treeview List
        List = MyTreeview(table_frame, columns=List_header, show="headings")
        # positioning the Treeview List
        List.place(x=0, y=0, width = 735, height=390)
        # Tree View Scrollbar
        tree_Scroll = customtkinter.CTkScrollbar(table_frame, command=List.yview)
        tree_Scroll.place(x=737, y=0, height=420)
        List.configure(yscrollcommand=tree_Scroll.set)

        List_ColWidth = [57, 53, 85, 69]
        List_ColAlignment = ["center", "center", "center", "center"]
        List_SortType = ["name", "name", "date", "percentage"]

        ## uncomment this to inser fake Database
        controller.fake_database()
        # controller.query_database()
#########################################################################################################################################

        # Delete one Items Button
        delete_one_button = customtkinter.CTkButton(self, text= "Delete", command = controller.List_delete_one, text_font=("TkHeadingtext_font", 20))
        delete_one_button.place(x=1260, y=150, anchor="e")

        # Delete Selected Items Button
        delete_selected_button = customtkinter.CTkButton(self, text= "Del multi", command = controller.List_delete_selected, text_font=("TkHeadingtext_font", 20))
        delete_selected_button.place(x=1260, y=210, anchor="e")

        # Delete all Items Button
        delete_all_button = customtkinter.CTkButton(self, text = "Delete All", command=controller.List_delete_all, text_font=("TkHeadingtext_font", 20))
        delete_all_button.place(x=1260, y=270, anchor="e")

        # Clear all Entry Boxes Button
        clear_button = customtkinter.CTkButton(self, text = "Clear Entry", command=controller.clear_entries, text_font=("TkHeadingtext_font", 20), width = 180)
        clear_button.place(x=1260, y=550, anchor="e")

        # Update Items Button
        update_button = customtkinter.CTkButton(self, text = "Update Item", command=controller.update_record, text_font=("TkHeadingtext_font", 20), width = 180)
        update_button.place(x=1260, y=600, anchor="e")

        oid_label = customtkinter.CTkLabel(self, text = "ID:", text_font=("TkHeadingtext_font", 20))
        oid_label.place(x=120, y=210, anchor="e")
        oid_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20))
        oid_entry.place(x=220, y=210, anchor="e")

        name_label = customtkinter.CTkLabel(self, text = "Name:", text_font=("TkHeadingtext_font", 18))
        name_label.place(x=380, y=550, anchor="e")
        name_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        name_entry.place(x=600, y=550, anchor="e")

        brand_label = customtkinter.CTkLabel(self, text = "Brand:", text_font=("TkHeadingtext_font", 18))
        brand_label.place(x=825, y=550, anchor="e")
        brand_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        brand_entry.place(x=1007, y=550, anchor="e")

        exdate_label = customtkinter.CTkLabel(self, text = "Exp. Date: ", text_font=("TkHeadingtext_font", 18))
        exdate_label.place(x=404, y=600, anchor="e")
        exdate_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        exdate_entry.place(x=600, y=600, anchor="e")

        amount_label = customtkinter.CTkLabel(self, text = "Amount: ", text_font=("TkHeadingtext_font", 18))
        amount_label.place(x=825, y=600, anchor="e")
        amount_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        amount_entry.place(x=1007, y=600, anchor="e")

        # AddItems Page customtkinter.CTkButton
        AddItems_page_button = customtkinter.CTkButton(self, text= "Add Items",text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                width =310, command=controller.List_add_record)
        AddItems_page_button.place(x=475, y=655)

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")

        # Bind the treeview
        List.bind("<ButtonRelease-1>", controller.select_record)


class AddItems(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        global List
        global count
        # global name_entry
        # global brand_entry
        # global exdate_entry
        # global amount_entry

        logo_img = ImageTk.PhotoImage(file="assets/images/WVU_Logo.png")
        logo_widget = customtkinter.CTkLabel(self, image=logo_img )
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        customtkinter.CTkLabel(self, text="Add Items"  , text_font=("TkMenutext_font", 40)).place(x=517, y = 40)
        customtkinter.CTkLabel(self, text="Scan or manually add item info:"  , text_font=("TkMenutext_font", 20)).place(x=180, y = 120)
        customtkinter.CTkLabel(self, text="Choose Item location:"  , text_font=("TkMenutext_font", 20)).place(x=180, y = 230)

        # Frame to put the entry boxes in it
        Design_frame1 = customtkinter.CTkFrame(self, width=100, height=33, highlightthickness=0, borderwidth=0)
        Design_frame1.place(x=310, y = 160)
        # customtkinter.CTkLabel for adding data entry boxes
        customtkinter.CTkLabel(Design_frame1, text = "Item Name", text_font=("yu gothic ui", 15, 'bold') ).grid(row=0, column=0)
        customtkinter.CTkLabel(Design_frame1, text = "Item Brand", text_font=("yu gothic ui", 15, 'bold') ).grid(row=0, column=1)
        customtkinter.CTkLabel(Design_frame1, text = "Expiration Date*", text_font=("yu gothic ui", 15, 'bold') ).grid(row=0, column=2)
        # customtkinter.CTkLabel(Design_frame1, text = "% Remaining", text_font=("yu gothic ui", 15, 'bold') ).grid(row=0, column=3)

        #Entry Boxes
        name_entry = Entry(Design_frame1, font=("yu gothic ui", 15))
        name_entry.grid(row=1, column=0)
        name_entry.bind('<FocusIn>', controller.entry_callback)

        brand_entry = Entry(Design_frame1, font=("yu gothic ui", 15))
        brand_entry.grid(row=1, column=1)
        brand_entry.bind('<FocusIn>', controller.entry_callback)

        exdate_entry = Entry(Design_frame1, font=("yu gothic ui", 15))
        exdate_entry.grid(row=1, column=2)
        exdate_entry.bind('<FocusIn>', controller.entry_callback)

        amount_entry = customtkinter.CTkEntry(Design_frame1, text_font=("yu gothic ui", 15))
        amount_entry.grid(row=1, column=3, padx =20)
        amount_entry.bind('<FocusIn>', controller.entry_callback)

        # Label for choosing the sensor
        Design_frame2 = customtkinter.CTkFrame(self , height=33, highlightthickness=0, borderwidth=0)
        Design_frame2.place(x=350, y = 280)

        # 1
        SensorBtn1 = customtkinter.CTkButton(Design_frame2, text= "Sensor #1", text_font=("TkHeadingtext_font", 25)  , cursor="hand2",
                height= 130)
        SensorBtn1.grid(row=0, column=1, pady=[0,30], padx = [0,30])
        # 2
        SensorBtn2 = customtkinter.CTkButton(Design_frame2, text= "Sensor #2", text_font=("TkHeadingtext_font", 25)  , cursor="hand2",
                height= 130)
        SensorBtn2.grid(row=0, column=2, pady=[0,30])
        # 3
        SensorBtn3 = customtkinter.CTkButton(Design_frame2, text= "Sensor #3", text_font=("TkHeadingtext_font", 25)  , cursor="hand2",
                height= 130)
        SensorBtn3.grid(row=0, column=3, pady=[0,30], padx = [30,0])
        # 4
        SensorBtn4 = customtkinter.CTkButton(Design_frame2, text= "Sensor #4", text_font=("TkHeadingtext_font", 25)  , cursor="hand2",
                height= 130)
        SensorBtn4.grid(row=1, column=1, padx = [0,30])
        # 5
        SensorBtn5 = customtkinter.CTkButton(Design_frame2, text= "Sensor #5", text_font=("TkHeadingtext_font", 25)  , cursor="hand2",
                height= 130)
        SensorBtn5.grid(row=1, column=2)
        # 6
        SensorBtn6 = customtkinter.CTkButton(Design_frame2, text= "Sensor #6", text_font=("TkHeadingtext_font", 25)  , cursor="hand2",
                height= 130)
        SensorBtn6.grid(row=1, column=3, padx = [30,0])

        # The Add Button
        add_record = customtkinter.CTkButton(self, text= "Add",text_font=("TkHeadingtext_font", 25) ,  cursor="hand2",
                width =310, command=controller.List_add_record)
        add_record.place(x=475, y=655)
        # The Back Button
        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20)  , cursor="hand2",
                command=lambda:controller.show_frame("ItemsList")
            ).place(x=1260, y=700, anchor="se")


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


class SuggestedShopping(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller
        class MyTreeview(objTTK.Treeview):
                def heading(self, column, sort_by=None, **kwargs):
                    if sort_by and not hasattr(kwargs, 'command'):
                        func = getattr(self, f"_sort_by_{sort_by}", None)
                        if func:
                            kwargs['command'] = partial(func, column, False)
                        # End of if
                    # End of if
                    return super().heading(column, **kwargs)
                # End of heading()

                def _sort(self, column, reverse, data_type, callback):
                    l = [(self.set(k, column), k) for k in self.get_children('')]
                    l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
                    for index, (_, k) in enumerate(l):
                        self.move(k, '', index)
                    # End of for loop
                    self.heading(column, command=partial(callback, column, not reverse))
                # End of _sort()

                def _sort_by_num(self, column, reverse):
                    self._sort(column, reverse, int, self._sort_by_num)
                # End of _sort_by_num()

                def _sort_by_name(self, column, reverse):
                    self._sort(column, reverse, str, self._sort_by_name)
                # End of _sort_by_num()

                def _sort_by_date(self, column, reverse):
                    def _str_to_datetime(string):
                        return objDateTime.datetime.strptime(string, "%m-%d-%Y")
                    # End of _str_to_datetime()

                    self._sort(column, reverse, _str_to_datetime, self._sort_by_date)
                # End of _sort_by_num()

                def _sort_by_multidecimal(self, column, reverse):
                    def _multidecimal_to_str(string):
                        arrString = string.split(".")
                        strNum = ""
                        for iValue in arrString:
                            strValue = f"{int(iValue):02}"
                            strNum = "".join([strNum, str(strValue)])
                        # End of for loop
                        strNum = "".join([strNum, "0000000"])
                        return int(strNum[:8])
                    # End of _multidecimal_to_str()

                    self._sort(column, reverse, _multidecimal_to_str, self._sort_by_multidecimal)
                # End of _sort_by_num()

                def _sort_by_percentage(self, column, reverse):
                    def _percentage_to_num(string):
                        return int(string.replace("%", ""))
                    # End of _percentage_to_num()

                    self._sort(column, reverse, _percentage_to_num, self._sort_by_percentage)
                # End of _sort_by_num()
                def _sort_by_numcomma(self, column, reverse):
                    def _numcomma_to_num(string):
                        return int(string.replace(",", ""))
                    # End of _numcomma_to_num()

                    self._sort(column, reverse, _numcomma_to_num, self._sort_by_numcomma)
                # End of _sort_by_num()

        global ShoppingList
        global count1

        logo_img = ImageTk.PhotoImage(file="assets/images/WVU_Logo.png")
        logo_widget = customtkinter.CTkLabel(self, image=logo_img )
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        customtkinter.CTkLabel(self, text="Suggested Shopping List" , text_font=("TkMenutext_font", 40)).place(x=345, y = 40)

        # Add Style
        style = ttk.Style()
        # style.theme_use("clam") # pick a theme (ugly)

        # Creat a frame to put the list and scrollbar in
        table_frame = customtkinter.CTkFrame(self,  highlightthickness=0, borderwidth=0, width=800, height=510)
        table_frame.place(relx=0.525, rely=0.53, anchor=tkinter.CENTER)

        # Define Columns
        arrlbHeader = ["Name", "Brand"]

        # Creating Treeview List
        ShoppingList = MyTreeview(table_frame, columns=arrlbHeader, show="headings")
        # positioning the Treeview List
        ShoppingList.place(x=0, y=0, width = 735, height=420)
        # Tree View Scrollbar
        tree_Scroll = customtkinter.CTkScrollbar(table_frame, command=ShoppingList.yview)
        tree_Scroll.place(x=737, y=0, height=420)
        ShoppingList.configure(yscrollcommand=tree_Scroll.set)

        # Inputing Data
        arrRows = [
            ["Rice", "Brand #1"],
            ["Milk", "Brand #2"],
            ["Pasta", "Brand #3"],
            ["Orange Juice", "Brand #4"],
            ["Potato", "Brand #5"],
            ["Rice", "Brand #6"],
            ["Milk", "Brand #7"],
            ["Pasta", "Brand #8"],
            ["Orange Juice", "Brand #9"],
            ["Potato", "Brand #10"],
            ["Rice", "Brand #11"],
            ["Potato", "Brand #12"],
            ["Rice", "Brand #13"],
            ["Milk", "Brand #14"],
            ["Pasta", "Brand #15"],
            ["Orange Juice", "Brand #16"],
            ["Potato", "Brand #17"],
            ["Rice", "Brand #18"]
            ]

        arrColWidth = [57, 53]
        arrColAlignment = ["center", "center"]
        arrSortType = ["name", "name"]

        for iCount in range(len(arrlbHeader)):
            strHdr = arrlbHeader[iCount]
            ShoppingList.heading(strHdr, text=strHdr.title(), sort_by=arrSortType[iCount])
            ShoppingList.column(arrlbHeader[iCount], width=arrColWidth[iCount], stretch=True, anchor=arrColAlignment[iCount])
        # End of for loop

        for iCount in range(len(arrRows)):
            ShoppingList.insert("", "end", values=arrRows[iCount])

        # Delete Selected Items customtkinter.CTkButton
        delete_selected_button = customtkinter.CTkButton(self, text= "Delete", command = controller.ShoppingList_delete_selected, text_font=("TkHeadingtext_font", 20))
        delete_selected_button.place(x=1260, y=150, anchor="e")

        # Delete all Items customtkinter.CTkButton
        delete_all_button = customtkinter.CTkButton(self, text = "Delete All", command=controller.ShoppingList_delete_all, text_font=("TkHeadingtext_font", 20))
        delete_all_button.place(x=1260, y=210, anchor="e")

        # The Add customtkinter.CTkButton
        shopping_add = customtkinter.CTkButton(self, text= "Add",text_font=("TkHeadingtext_font", 25) ,  cursor="hand2",
                width =310, command=controller.ShoppingList_add_popup)
        shopping_add.place(x=475, y=655)

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")


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

        optionmenu = customtkinter.CTkOptionMenu(right_frame, values=["Light", "Dark"], text_font=("TkHeadingtext_font", 15),
                                            width = 200, height = 30, command=controller.change_appearance_mode)
        optionmenu.place(relx=0.59, rely=0.8, anchor=tkinter.CENTER)


        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")


#class PageName(customtkinter.CTkFrame):
    #def __init__(self, master, controller):
        #customtkinter.CTkFrame.__init__(self, master )
        #self.controller = controller

############ Initiallize app ############
if __name__ == "__main__":
    root = SmartFridgeApp()
    root.title("Smart Fridge 1.8")
    root.geometry("1280x720")
    root.resizable(0, 0)
    root.attributes('-topmost', 0)

    ########################## Ignore This ###############################
    # Gets the requested values of the height and widht.
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    print("Width",windowWidth,"Height",windowHeight)
    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth()/3.5 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/3.5 - windowHeight/2)
    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionRight, positionDown))
    ####################################################################


    #root.attributes('-fullscreen', 1)
    root.mainloop()
