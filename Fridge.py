from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk as objTTK
from functools import partial

import tkinter as tk
import subprocess
import os
import tkinter as objTK
import datetime as objDateTime


bg_color = "#001532" # change background color

class SmartFridgeApp(tk.Tk):    # Main Class
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        window = tk.Frame(self)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, Register, MainMenu, ItemsList, AddItems, RecipeSuggestions,
                    SuggestedShopping, Settings, AdjustInterface):
            page_name = F.__name__
            global frame
            frame = F(master=window, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

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
                 messagebox.showinfo ("","Login Success") # Label(login, text = "Login Successful!", bg=bg_color, fg="Green", font=("TkMenuFont", 40)).pack(pady=20)
                 self.show_frame("MainMenu")
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

    # Functions for ItemsList Page
    def List_delete_all(self): # Delets all items
        for values in List.get_children():
            List.delete(values)
    def List_delete_selected(self): # Delete multiple selected ITEMS
        List_selected = List.selection()
        for values in List_selected:
            List.delete(values)

    # Functions for AddItems Page
    def add_record(self): # adds the data to the table (List)
        List.insert("", "end", values=(name_entry.get(), brand_entry.get(), exdate_entry.get(), remain_entry.get()))
        name_entry.delete(0, END)
        brand_entry.delete(0, END)
        exdate_entry.delete(0, END)
        remain_entry.delete(0, END)

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
        pop = Toplevel(self, bg = bg_color)
        pop.title("Add items to your Shpping list")
        pop.geometry("780x130")

        Label(pop, text = "Name:", font=("yu gothic ui", 15, 'bold'), fg = "white", bg = bg_color).grid(row=0, column=0, sticky=W, padx=(30,0))
        Label(pop, text = "Brand:", font=("yu gothic ui", 15, 'bold'), fg = "white", bg = bg_color).grid(row=0, column=1, sticky=W, padx=(5,0))
        #Entry Boxes
        name_entry1 = Entry(pop, font=("yu gothic ui", 20))
        name_entry1.grid(row=1, column=0, padx=(30,0))
        name_entry1.bind('<FocusIn>', self.entry_callback)

        brand_entry1 = Entry(pop, font=("yu gothic ui", 20))
        brand_entry1.grid(row=1, column=1, padx=(5,0))
        brand_entry1.bind('<FocusIn>', self.entry_callback)

        Button(pop, text="Confirm", font=("TkHeadingFont", 16), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command = self.ShoppingList_add_record).grid(row=1, column=3, padx=5)
    def ShoppingList_add_record(self): # adds the data to the table (ShoppingList)
        ShoppingList.insert("", "end", values=(name_entry1.get(), brand_entry1.get()))
        # clear the entry boxes
        name_entry1.delete(0, END)
        brand_entry1.delete(0, END)

    # Functions for Settings Page
    def Reset_prompt(self): # Popup confirming reset
        choice = messagebox.askquestion("Reset","Are you sure you want to reset? \n Proceeding will sign you out")
        if choice == 'yes':
            self.show_frame("Login")
    def Shutdown_prompt(self): # Popup confirming shutdown
        choice = messagebox.askquestion("Shutdown","Are you sure you want to shutdown the system?")
        if choice == 'yes':
            subprocess.call(['sudo', 'shutdown', '-h', '-t 5','now'])
    def Restart_prompt(self): # Popup confirming restart
        choice = messagebox.askquestion("Reboot","Are you sure you want to reboot the system?")
        if choice == 'yes':
            subprocess.call(['sudo', 'shutdown', '-r', '-t 5','now'])

    # Functions for AdjustInterface Page
    def Dark_Theme(self):
        # bg_color = "black"
        # frame.config(bg = bg_color)
        # title.config(fg = "white", bg = bg_color)
        # logo_widget.configure(bg=bg_color)
        pass
    def Light_Theme(self):
        # bg_color = "white"
        # frame.config(bg = bg_color)
        # title.config(fg = "black", bg = bg_color)
        # logo_widget.configure(bg=bg_color)
        pass
    def Default_Theme(self):
        # bg_color = "#001532"
        # frame.config(bg = bg_color)
        # title.config(fg = "white", bg = bg_color)
        # logo_widget.configure(bg=bg_color)
        pass


class Login(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg = bg_color)
        self.controller = controller

        global username_verify
        global password_verify
        global username_entry1
        global password_entry1
        username_verify = StringVar()
        password_verify = StringVar()

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        # Slicing the page
        design_frame1 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame1.place(x=75, y=120)
        design_frame2 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame2.place(x=676, y=106)

        # Picture on left side
        Welcome_img = ImageTk.PhotoImage(file="assets/WVU_Welcome.png")
        Welcome_widget = tk.Label(design_frame1, image=Welcome_img, bg=bg_color)
        Welcome_widget.image = Welcome_img
        Welcome_widget.place(x=50, y=10)

        # Welcome title
        welcome_label = Label(design_frame2, text='Smart Fridge GUI', fg="white", font=('Arial', 20, 'bold'), bg=bg_color)
        welcome_label.place(x=130, y=15)

        # Tap Login button
        login_button = Button(self, text='Login', fg="white", font=("yu gothic ui bold", 12), bg=bg_color,
                              borderwidth=0, activebackground='#ebac00', cursor='hand2').place(x=810, y=175)
        login_line = Canvas(self, width=60, height=5, bg='#ebac00').place(x=810, y=203)

        # Tap Signup button
        SignUp_button = Button(self, text='Sign up', fg="white", font=("yu gothic ui bold", 12), bg=bg_color,
                              command=lambda: controller.show_frame("Register"), borderwidth=0, activebackground='#ebac00', cursor='hand2')
        SignUp_button.place(x=1000, y=175)

        # Username Entry
        Label(design_frame2, text='• Username', fg="white", bg=bg_color, font=("yu gothic ui", 11, 'bold')).place(x=130, y=140)
        username_entry1 = Entry(design_frame2, textvariable = username_verify, fg="black", font=("yu gothic ui semibold", 12), highlightthickness=2)
        username_entry1.place(x=134, y=170, width=256, height=34)
        username_entry1.config(highlightbackground="black", highlightcolor="black")
        username_entry1.bind('<FocusIn>', controller.entry_callback)
        # Password Entry
        Label(design_frame2, text='• Password', fg="white", bg=bg_color, font=("yu gothic ui", 11, 'bold')).place(x=130, y=220)
        password_entry1 = Entry(design_frame2, textvariable = password_verify, fg="black", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2)
        password_entry1.place(x=134, y=250, width=256, height=34)
        password_entry1.config(highlightbackground="black", highlightcolor="black")
        password_entry1.bind('<FocusIn>', controller.entry_callback)
        # checkbutton for hiding and showing password
        checkButton = Checkbutton(design_frame2, fg = "#949494", bg=bg_color, text='show password', activebackground=bg_color, activeforeground="#949494",
                                    command=controller.password_command1)
        checkButton.place(x=130, y=288)

        # Proceed Login button
        loginBtn1 = Button(design_frame2, fg='#f8f8f8', text='Login', bg='#ebac00', font=("yu gothic ui bold", 15),
                           cursor='hand2', activebackground='#bb9008', command=controller.login_user)
        loginBtn1.place(x=133, y=340, width=256, height=50)


class Register(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg = bg_color)
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

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        # Slicing the page
        design_frame1 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame1.place(x=75, y=120)
        design_frame2 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame2.place(x=676, y=106)

        # Picture on left side
        Welcome_img = ImageTk.PhotoImage(file="assets/WVU_Welcome.png")
        Welcome_widget = tk.Label(design_frame1, image=Welcome_img, bg=bg_color)
        Welcome_widget.image = Welcome_img
        Welcome_widget.place(x=50, y=10)

        # Welcome title
        welcome_label = Label(design_frame2, text='Smart Fridge GUI', fg="white", font=('Arial', 20, 'bold'), bg=bg_color)
        welcome_label.place(x=130, y=15)

        # Tap Login button
        login_button = Button(self, text='Login', fg="white", font=("yu gothic ui bold", 12), bg=bg_color,
                              command=lambda: controller.show_frame("Login"), borderwidth=0, activebackground='#ebac00', cursor='hand2')
        login_button.place(x=810, y=175)

        # Tap Signup button
        SignUp_button = Button(self, text='Sign up', fg="white", font=("yu gothic ui bold", 12), bg=bg_color,
                                borderwidth=0, activebackground='#ebac00', cursor='hand2')
        SignUp_button.place(x=1000, y=175)
        SignUp_line = Canvas(self, width=60, height=5, bg='#ebac00')
        SignUp_line.place(x=1000, y=203)

        # Username Entry
        Label(design_frame2, text='• Username', fg="white", bg=bg_color, font=("yu gothic ui", 11, 'bold')).place(x=130, y=120)
        username_entry = Entry(design_frame2, textvariable = username, fg="black", font=("yu gothic ui semibold", 12), highlightthickness=2)
        username_entry.place(x=134, y=150, width=256, height=34)
        username_entry.config(highlightbackground="black", highlightcolor="black")
        username_entry.bind('<FocusIn>', controller.entry_callback)
        # Password Entry
        Label(design_frame2, text='• Password', fg="white", bg=bg_color, font=("yu gothic ui", 11, 'bold')).place(x=130, y=190)
        password_entry = Entry(design_frame2, textvariable = password, fg="black", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2)
        password_entry.place(x=134, y=220, width=256, height=34)
        password_entry.config(highlightbackground="black", highlightcolor="black")
        password_entry.bind('<FocusIn>', controller.entry_callback)
        # Verify password
        Label(design_frame2, text='• Verify Password', fg="white", bg=bg_color, font=("yu gothic ui", 11, 'bold')).place(x=130, y=265)
        verify_password_entry= Entry(design_frame2, textvariable = password1, fg="black", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2)
        verify_password_entry.place(x=134, y=295, width=256, height=34)
        verify_password_entry.config(highlightbackground="black", highlightcolor="black")
        verify_password_entry.bind('<FocusIn>', controller.entry_callback)
        # checkbutton for hiding and showing password
        checkButton = Checkbutton(design_frame2, fg = "#949494", bg=bg_color, text='show password', activebackground=bg_color, activeforeground="#949494",
        command=lambda:[controller.password_command0(), controller.password_command()])
        checkButton.place(x=130, y=330)

        # Proceed Signup buttons
        SignUp_button1 = Button(design_frame2, fg='#f8f8f8', text='Sign Up', bg='#ebac00', font=("yu gothic ui bold", 15),
                           cursor='hand2', activebackground='#bb9008', command=controller.register_user)
        SignUp_button1.place(x=135, y=370, width=256, height=50)


class MainMenu(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg = bg_color)
        self.controller = controller

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)


        # Slicing the page
        design_frame1 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame1.place(x=75, y=120)
        design_frame2 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame2.place(x=676, y=106)

        Label(design_frame2, text='Main Menu', fg="white", font=("TkMenuFont", 40), bg=bg_color).place(x=130, y=15)

        # Picture on left side
        Welcome_img = ImageTk.PhotoImage(file="assets/WVU_Welcome.png")
        Welcome_widget = tk.Label(design_frame1, image=Welcome_img, bg=bg_color)
        Welcome_widget.image = Welcome_img
        Welcome_widget.place(x=50, y=10)


        tk.Button(design_frame2, text="List of Items", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:controller.show_frame("ItemsList")).place(x=100, y = 155)

        tk.Button(design_frame2, text="Recipe Suggestions", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:controller.show_frame("RecipeSuggestions")).place(x=100, y = 230)

        tk.Button(design_frame2, text="Suggested Shopping List", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:controller.show_frame("SuggestedShopping")).place(x=100, y = 305)

        tk.Button(design_frame2, text="Settings", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:controller.show_frame("Settings")).place(x=100, y = 380)


class ItemsList(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg = bg_color)
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

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        tk.Label(self, text="List of Items", bg=bg_color, fg="white", font=("TkMenuFont", 40)).place(x=493, y = 40)
        # Creat a frame to put the list and scrollbar in
        Design_frame1 = Listbox(self, width=126, height=31, bg =bg_color, highlightthickness=0, borderwidth=0)
        Design_frame1.place(x=270, y = 130)

        arrlbHeader = ["Name", "Brand", "Expiration Date", "Remaining"]

        # Creating Treeview List
        List = MyTreeview(Design_frame1, columns=arrlbHeader, show="headings")
        # positioning the Treeview List
        List.place(x=0, y=0, width = 735, height=420)
        # Tree View Scrollbar
        tree_Scroll = ttk.Scrollbar(Design_frame1, orient="vertical", command=List.yview)
        tree_Scroll.place(x=737, y=0, height=420)
        List.configure(yscrollcommand=tree_Scroll.set)

        # configure Treeview
        # Add Style
        style = ttk.Style()
        ## pick a theme (ugly)
        # style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Arial', 15, 'bold'), rowheight=35)
        style.configure("Treeview", font=("", 15), rowheight=35)  #foreground="white"   #fieldbackground="Green"   #background="#bb9008"
        style.map('Treeview', background=[('selected', '#ebac00')]) # color when selected

        arrRows =[
            ["A", "C", "12-04-2022", "40%"],
            ["B", "A", "12-06-2022", "60%"],
            ["C", "D", "12-01-2022", "20%"],
            ["D", "B", "12-02-2022", "30%"],
            ["E", "F", "12-05-2022", "50%"],
            ["F", "E", "12-03-2022", "100%"]
            ]

        # arrRows =[
        #     ["Rice", "Food", "12-10-2022", "100%"],
        #     ["Milk", "Drink", "12-10-2022", "90%"],
        #     ["Pasta", "Food", "12-10-2022", "80%"],
        #     ["Orange Juice", "Drink", "08-31-2022", "40%"],
        #     ["Potato", "Food", "12-10-2022", "100%"],
        #     ["Tomato", "Food", "12-10-2022", "100%"]
        #     ]

        arrColWidth = [57, 53, 85, 69]
        arrColAlignment = ["center", "center", "center", "center", "center"]

        arrSortType = ["name", "name", "date", "percentage"]
        for iCount in range(len(arrlbHeader)):
            strHdr = arrlbHeader[iCount]
            List.heading(strHdr, text=strHdr.title(), sort_by=arrSortType[iCount])
            List.column(arrlbHeader[iCount], width=arrColWidth[iCount], stretch=True, anchor=arrColAlignment[iCount])
        # End of for loop

        for iCount in range(len(arrRows)):
            List.insert("", "end", values=arrRows[iCount])


        # End of for loop

        # List.tag_configure('oddrow', background = "white")
        # List.tag_configure('evenrow', background = "#C9C9C7")
        # iCount = 0
        # for iCount in range(len(arrRows)):
        #     if iCount % 2 == 0:
        #         List.insert("", "end", values=arrRows[iCount], tags=('evenrow',))
        #     else:
        #         List.insert("", "end", values=arrRows[iCount], tags=('oddrow',))
        #     iCount += 1

        # Delete Selected Items button
        delete_selected_button = Button(self, text= "Delete", command = controller.List_delete_selected, font=("", 15))
        delete_selected_button.place(x=1038, y=130, width = 150, height=48)

        # Delete all Items button
        delete_all_button = Button(self, text = "Delete All", command=controller.List_delete_all, font=("", 15))
        delete_all_button.place(x=1038, y=190, width = 150, height=48)

        # AddItems Page Button
        AddItems_page_button = Button(self, text= "Add Items",font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:controller.show_frame("AddItems"))
        AddItems_page_button.place(x=475, y=644)

        tk.Button(self, text="Go Back", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command=lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")


class AddItems(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg = bg_color)
        self.controller = controller

        global List
        global count
        global name_entry
        global brand_entry
        global exdate_entry
        global remain_entry

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        tk.Label(self, text="Add Items", bg=bg_color, fg="white", font=("TkMenuFont", 40)).place(x=517, y = 40)
        tk.Label(self, text="Scan or manually add items:", bg=bg_color, fg="white", font=("TkMenuFont", 20)).place(x=180, y = 120)
        tk.Label(self, text="Choose Item location:", bg=bg_color, fg="white", font=("TkMenuFont", 20)).place(x=180, y = 230)

        # Frame to put the entry boxes in it
        Design_frame1 = Listbox(self, width=100, height=33, highlightthickness=0, borderwidth=0)
        Design_frame1.place(x=180, y = 160)
        # Label for adding data entry boxes
        Label(Design_frame1, text = "Item Name", font=("yu gothic ui", 15, 'bold'), bg="white").grid(row=0, column=0)
        Label(Design_frame1, text = "Item Type", font=("yu gothic ui", 15, 'bold'), bg="white").grid(row=0, column=1)
        Label(Design_frame1, text = "Expiration Date", font=("yu gothic ui", 15, 'bold'), bg="white").grid(row=0, column=2)
        Label(Design_frame1, text = "% Remaining", font=("yu gothic ui", 15, 'bold'), bg="white").grid(row=0, column=3)
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

        remain_entry = Entry(Design_frame1, font=("yu gothic ui", 15))
        remain_entry.grid(row=1, column=3)
        # remain_entry.bind('<FocusIn>', controller.entry_callback)

        # Label for choosing the sensor
        Design_frame2 = Listbox(self, bg = bg_color, height=33, highlightthickness=0, borderwidth=0)
        Design_frame2.place(x=350, y = 280)

        # Sensor Buttons
        # 1
        # pic = PhotoImage(file = "assets/image.png")
        # SensorBtn1=Button(Design_frame2 , image = pic, font=("TkHeadingFont", 25))

        SensorBtn1 =Button(Design_frame2, text= "Sensor #1", font=("TkHeadingFont", 25), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", height= 3)
        SensorBtn1.grid(row=0, column=1, pady=[0,30], padx = [0,30])
        # 2
        SensorBtn2 =Button(Design_frame2, text= "Sensor #2", font=("TkHeadingFont", 25), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", height= 3)
        SensorBtn2.grid(row=0, column=2, pady=[0,30])

        # 3
        SensorBtn3 =Button(Design_frame2, text= "Sensor #3", font=("TkHeadingFont", 25), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", height= 3)
        SensorBtn3.grid(row=0, column=3, pady=[0,30], padx = [30,0])

        # 4
        SensorBtn4 =Button(Design_frame2, text= "Sensor #4", font=("TkHeadingFont", 25), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", height= 3)
        SensorBtn4.grid(row=1, column=1, padx = [0,30])

        # 5
        SensorBtn5 =Button(Design_frame2, text= "Sensor #5", font=("TkHeadingFont", 25), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", height= 3)
        SensorBtn5.grid(row=1, column=2)

        # 6
        SensorBtn6 =Button(Design_frame2, text= "Sensor #6", font=("TkHeadingFont", 25), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", height= 3)
        SensorBtn6.grid(row=1, column=3, padx = [30,0])



        # The Add button
        add_record =Button(self, text= "Add",font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=controller.add_record)
        add_record.place(x=475, y=644)
        # The Back button
        tk.Button(self, text="Go Back", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command=lambda:controller.show_frame("ItemsList")
            ).place(x=1260, y=700, anchor="se")


class RecipeSuggestions(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg = bg_color)
        self.controller = controller

        # Create Frame for X Scrollbar
        # Create A Canvas
        my_canvas = Canvas(self, bg=bg_color)
        my_canvas.pack(side=LEFT, fill=BOTH,expand=1)

        # Add A Scrollbars to Canvas
        # x_scrollbar = ttk.Scrollbar(desing_frame1, orient=HORIZONTAL, command=my_canvas.xview)
        # x_scrollbar.pack(side=BOTTOM, fill=X)
        y_scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=my_canvas.yview)
        y_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure the canvas
        # my_canvas.configure(xscrollcommand=x_scrollbar.set)
        my_canvas.configure(yscrollcommand=y_scrollbar.set)
        my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion=my_canvas.bbox(ALL)))

        # Create Another Frame INSIDE the Canvas
        desing_frame2 = Frame(my_canvas, bg=bg_color)
        # Add that New Frame a Window In The Canvas
        my_canvas.create_window((100,100), window=desing_frame2, anchor="nw")


        recipe1_label =tk.Label(desing_frame2, text="Recipe 1", font=("TkMenuFont", 20), bg=bg_color, fg="white")
        recipe1_label.grid(row=1, column =1, pady=[150,0])
        recipe1_img = ImageTk.PhotoImage(file="assets/recipe1.png")
        recipe1_widget = tk.Label(desing_frame2, image=recipe1_img)
        recipe1_widget.image = recipe1_img
        recipe1_widget.grid(row=2, column = 1)
        recipe11_img = ImageTk.PhotoImage(file="assets/recipe11.png")
        recipe11_widget = tk.Label(desing_frame2, image=recipe11_img)
        recipe11_widget.image = recipe11_img
        recipe11_widget.grid(row=4, column =1)


        recipe2_label =tk.Label(desing_frame2, text="Recipe 2", font=("TkMenuFont", 20), bg=bg_color, fg="white")
        recipe2_label.grid(row=1, column =2, pady=[150,0])
        recipe2_img = ImageTk.PhotoImage(file="assets/recipe2.png")
        recipe2_widget = tk.Label(desing_frame2, image=recipe2_img)
        recipe2_widget.image = recipe2_img
        recipe2_widget.grid(row=2, column = 2, padx=50)
        recipe22_img = ImageTk.PhotoImage(file="assets/recipe22.png")
        recipe22_widget = tk.Label(desing_frame2, image=recipe22_img)
        recipe22_widget.image = recipe22_img
        recipe22_widget.grid(row=4, column =2)

        recipe3_label =tk.Label(desing_frame2, text="Recipe 3", font=("TkMenuFont", 20), bg=bg_color, fg="white")
        recipe3_label.grid(row=1, column =3, pady=[150,0])
        recipe3_img = ImageTk.PhotoImage(file="assets/recipe3.png")
        recipe3_widget = tk.Label(desing_frame2, image=recipe3_img)
        recipe3_widget.image = recipe3_img
        recipe3_widget.grid(row=2, column = 3)
        recipe33_img = ImageTk.PhotoImage(file="assets/recipe33.png")
        recipe33_widget = tk.Label(desing_frame2, image=recipe33_img)
        recipe33_widget.image = recipe33_img
        recipe33_widget.grid(row=4, column =3)


        desing_frame3 = Frame(self, bg=bg_color, width=1260, height=130)
        desing_frame3.place(x=2, y = 0)

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(desing_frame3, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20, anchor="nw")

        tk.Label(desing_frame3, text="Recipe Suggestions", bg=bg_color, fg="white", font=("TkMenuFont", 40)
                ).place(x=650, y = 40, anchor="center")

        tk.Button(self, text="Go Back", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command=lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")


class SuggestedShopping(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg = bg_color)
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

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        tk.Label(self, text="Suggested Shopping List", bg=bg_color, fg="white", font=("TkMenuFont", 40)).place(x=345, y = 40)


        # Add Style
        style = ttk.Style()
        # style.theme_use("clam") # pick a theme (ugly)


        # Creat a frame to put the list and scrollbar in
        Design_frame1 = Listbox(self, width=126, height=31, bg =bg_color, highlightthickness=0, borderwidth=0)
        Design_frame1.place(x=270, y = 130)



        # Define Columns
        arrlbHeader = ["Name", "Type"] #ShoppingList['columns'] = ("Name", "Type")

        # Creating Treeview List
        ShoppingList = MyTreeview(Design_frame1, columns=arrlbHeader, show="headings")
        # positioning the Treeview List
        ShoppingList.place(x=0, y=0, width = 735, height=420)
        # Tree View Scrollbar
        tree_Scroll = ttk.Scrollbar(Design_frame1, orient="vertical", command=ShoppingList.yview)
        tree_Scroll.place(x=737, y=0, height=420)
        ShoppingList.configure(yscrollcommand=tree_Scroll.set)
        # configure Treeview
        style.configure("Treeview.Heading", font=('Arial', 15, 'bold'), rowheight=35)
        style.configure("Treeview", font=("", 15), rowheight=35)  #foreground="white"   #fieldbackground="Green"   #background="#bb9008"
        style.map('Treeview', background=[('selected', '#ebac00')]) # color when selected


        # # Formating columns (There will be a hidden column called "#0". Using that for "Item #")
        # ShoppingList.column("#0", anchor=W, width=45, minwidth=25) # "Hidden"
        # ShoppingList.column("Name", anchor=W, width=120, minwidth=90)
        # ShoppingList.column("Type", anchor=W, width=120, minwidth=60)
        # # Columns Headings
        # ShoppingList.heading("#0", text="     #", anchor=W)
        # ShoppingList.heading("Name", text="Item Name", anchor=W)
        # ShoppingList.heading("Type", text="Item Type", anchor=W)
        # Inputing Data
        arrRows = [
            ["Rice", "Food"],
            ["Milk", "Drink"],
            ["Pasta", "Food"],
            ["Orange Juice", "Drink"],
            ["Potato", "Food"],
            ["Rice", "Food"],
            ["Milk", "Drink"],
            ["Pasta", "Food"],
            ["Orange Juice", "Drink"],
            ["Potato", "Food"],
            ["Rice", "Food"],
            ["Potato", "Food"],
            ["Rice", "Food"],
            ["Milk", "Drink"],
            ["Pasta", "Food"],
            ["Orange Juice", "Drink"],
            ["Potato", "Food"],
            ["Rice", "Food"]
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


        #     # Creating striped rows
        # ShoppingList.tag_configure('oddrow', background = "white")
        # ShoppingList.tag_configure('evenrow', background = "#C9C9C7")
        # count1 = 0
        # for record in Shopping_data:
        #     if count1 % 2 == 0:
        #         ShoppingList.insert(parent='', index='end', iid=count1, text=count1+1, values=(record[0], record[1]), tags=('evenrow',))
        #     else:
        #         ShoppingList.insert(parent='', index='end', iid=count1, text=count1+1, values=(record[0], record[1]), tags=('oddrow',))
        #     count1 += 1

        # Delete Selected Items button
        delete_selected_button = Button(self, text= "Delete", command = controller.ShoppingList_delete_selected, font=("", 15))
        delete_selected_button.place(x=1038, y=130, width = 150, height=48)

        # Delete all Items button
        delete_all_button = Button(self, text = "Delete All Items", command=controller.ShoppingList_delete_all, font=("", 15))
        delete_all_button.place(x=1038, y=190, width = 150, height=48)



        # The Add button
        shopping_add =Button(self, text= "Add",font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=controller.ShoppingList_add_popup)
        shopping_add.place(x=475, y=644)

        tk.Button(self, text="Go Back", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command=lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")


class Settings(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg = bg_color)
        self.controller = controller

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        # Slicing the page
        design_frame1 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame1.place(x=75, y=120)
        design_frame2 = Listbox(self, bg=bg_color, width=100, height=33, highlightthickness=0, borderwidth=0)
        design_frame2.place(x=676, y=106)

        Label(design_frame2, text='Settings', fg="white", font=("TkMenuFont", 40), bg=bg_color).place(x=165, y=15)
        # Picture on left side
        Welcome_img = ImageTk.PhotoImage(file="assets/WVU_Welcome.png")
        Welcome_widget = tk.Label(design_frame1, image=Welcome_img, bg=bg_color)
        Welcome_widget.image = Welcome_img
        Welcome_widget.place(x=50, y=10)


        tk.Button(design_frame2, text="Adjust Interface", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=lambda:controller.show_frame("AdjustInterface")
                        ).place(x=100, y = 155)

        tk.Button(design_frame2, text="Reset", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=controller.Reset_prompt).place(x=100, y = 230)

        tk.Button(design_frame2, text="Shutdown", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=controller.Shutdown_prompt).place(x=100, y = 305)

        tk.Button(design_frame2, text="Reboot", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=controller.Restart_prompt).place(x=100, y = 380)

        tk.Button(design_frame2, text="Exit Interface", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", width = 20, command=controller.destroy).place(x=100, y = 460)

        tk.Button(self, text="Go Back", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command=lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")


class AdjustInterface(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg = bg_color)
        self.controller = controller

        global logo_widget
        global title

        logo_img = ImageTk.PhotoImage(file="assets/WVU_Logo.png")
        logo_widget = tk.Label(self, image=logo_img, bg=bg_color)
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        tk.Label(self, text="Adjust Interface Theme", bg=bg_color, fg="white", font=("TkMenuFont", 40)).place(x=365, y = 40)

        tk.Button(self, fg='#f8f8f8', text='Darkmode', bg='#ebac00', font=("TkHeadingFont", 20),
                           cursor='hand2', activebackground='#bb9008', width = 20, command=controller.Dark_Theme).place(x=475, y = 230)

        tk.Button(self, fg='#f8f8f8', text='Lightmode', bg='#ebac00', font=("TkHeadingFont", 20),
                           cursor='hand2', activebackground='#bb9008', width = 20, command=controller.Light_Theme).place(x=475, y = 305)

        tk.Button(self, fg='#f8f8f8', text='Default', bg='#ebac00', font=("TkHeadingFont", 20),
                           cursor='hand2', activebackground='#bb9008', width = 20, command=controller.Default_Theme).place(x=475, y = 380)

        tk.Button(self, text="Go Back", font=("TkHeadingFont", 20), bg="#ebac00", fg="white", cursor="hand2",
            activebackground="#bb9008", activeforeground="black", command=lambda:controller.show_frame("Settings")
            ).place(x=1260, y=700, anchor="se")


#class PageName(tk.Frame):
    #def __init__(self, master, controller):
        #tk.Frame.__init__(self, master, bg = bg_color)
        #self.controller = controller

############ Initiallize app ############
if __name__ == "__main__":
    root = SmartFridgeApp()
    root.title("Smart Fridge 1.7")
    root.geometry("1280x720")
    root.resizable(0, 0)
    root.attributes('-topmost', 0)
    #root.attributes('-fullscreen', 1)
    root.mainloop()
