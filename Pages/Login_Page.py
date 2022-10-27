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

class FirebaseConfig:
    def __init__(self):
        global user
        self.firebaseConfig = {
              "apiKey": "AIzaSyDEB5qdpI_D371iICJlHKfU67Op1e5JVeA",
              "authDomain": "smartfridgeapp-wvu.firebaseapp.com",
              "databaseURL": "https://smartfridgeapp-wvu-default-rtdb.firebaseio.com/",
              "projectId": "smartfridgeapp-wvu",
              "storageBucket": "smartfridgeapp-wvu.appspot.com",
              "messagingSenderId": "21386787655",
              "appId": "1:21386787655:web:cb406f9a8c8ffbaf5faa62",
              "measurementId": "G-YFLKE7K46T" }
        self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.auth = self.firebase.auth()
        self.storage = self.firebase.storage()

        self.app_login_cred = {'email': StringVar(), 'idToken': StringVar()}


    def register(self, username, password):
        try:
            user = self.auth.create_user_with_email_and_password(username, password)
            self.auth.send_email_verification(user['idToken'])
            return True
        except:
            return False

    def login(self, username, password):
        try:
            global user
            user = self.auth.sign_in_with_email_and_password(username, password)
            return user
        except:
            return False

    def reset_password(self, username_reset):
        try:
            self.auth.send_password_reset_email(username_reset)
            return
        except:
             return False

class Login(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        global username
        global password
        global username_entry
        global password_entry
        global user
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

        def password_command(): # show/password for login
            if password_entry.cget('show') == '•':
                password_entry.config(show='')
            else:
                password_entry.config(show='•')

        checkButton = customtkinter.CTkCheckBox(right_frame, text='show password', command = password_command)
        checkButton.place(x=174, y=390)


        def login_user(): # Login Process
            # a = FirebaseConfig()
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
                        # a.auth.refresh(user['refreshToken'])
                        messagebox.showinfo ("", "Login Success")
                        username_entry.delete(0, END)
                        password_entry.delete(0, END)
                        command = controller.show_frame("MainMenu")
                        query_database()
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

class ItemsList(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

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


        for record in range(len(List_header)):
            strHdr = List_header[record]
            List.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            List.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])

        # Delete one Items Button
        delete_one_button = customtkinter.CTkButton(self, text= "Delete", command = delete_item, text_font=("TkHeadingtext_font", 20))
        delete_one_button.place(x=1260, y=150, anchor="e")

        # # Delete Selected Items Button
        # delete_selected_button = customtkinter.CTkButton(self, text= "Del multi", command = delete_multi_items, text_font=("TkHeadingtext_font", 20))
        # delete_selected_button.place(x=1260, y=210, anchor="e")

        # Delete all Items Button
        delete_all_button = customtkinter.CTkButton(self, text = "Delete All", command = delete_all_items, text_font=("TkHeadingtext_font", 20))
        delete_all_button.place(x=1260, y=210, anchor="e")
        # delete_all_button.place(x=1260, y=270, anchor="e")

        # Clear all Entry Boxes Button
        clear_button = customtkinter.CTkButton(self, text = "Clear Entry", command = clear_entries, text_font=("TkHeadingtext_font", 20), width = 180)
        clear_button.place(x=1260, y=550, anchor="e")

        # Update Items Button
        update_button = customtkinter.CTkButton(self, text = "Update Item", command = update_record, text_font=("TkHeadingtext_font", 20), width = 180)
        update_button.place(x=1260, y=600, anchor="e")

        # oid_label = customtkinter.CTkLabel(self, text = "ID:", text_font=("TkHeadingtext_font", 20))
        # oid_label.place(x=120, y=210, anchor="e")
        oid_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20))
        # oid_entry.place(x=220, y=210, anchor="e")

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
        AddItems_page_button = customtkinter.CTkButton(self, text = "Add Items", text_font = ("TkHeadingtext_font", 25) , cursor = "hand2",
                width = 310, command = add_record)
        AddItems_page_button.place(x=475, y=655)

        customtkinter.CTkButton(self, text="Go Back", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")

        # Bind the treeview
        List.bind("<ButtonRelease-1>", select_record)
        

# Functions for ItemsList Page
def query_database():
    # pull data
    db = FirebaseConfig().firebase.database()

    Items = db.child("pantry-items").child(user['localId']).get()
    for itemsData in Items.each():
        data = itemsData.val()
        datakey = itemsData.key()
        datalist = list(data.values())
        List.insert("", "end", values=(datalist))
        
def clear_entries():
    name_entry.delete(0, END)
    brand_entry.delete(0, END)
    exdate_entry.delete(0, END)
    amount_entry.delete(0, END)
    oid_entry.delete(0, END)

def select_record(e):
    # clear entry boxes
    clear_entries()
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
    
def add_record(): # adds data to the table (List)
    global count
    if name_entry.get()=="":
        messagebox.showerror("", "Item's data needed")
    else:
        a = FirebaseConfig()

        data =  {'1 name': name_entry.get(),
                '2 brand': brand_entry.get(),
                '3 date': exdate_entry.get(),
                '4 amount': amount_entry.get()
                }
        db = FirebaseConfig().firebase.database()
        db.child("pantry-items").child(user['localId']).push(data)
        
        Items = db.child("pantry-items").child(user['localId']).get()
        for itemsData in Items.each():
            data =  {'1 name': name_entry.get(),
                '2 brand': brand_entry.get(),
                '3 date': exdate_entry.get(),
                '4 amount': amount_entry.get(),
                '5 id': itemsData.key(),
                }
            if itemsData.val()['1 name'] == name_entry.get() and itemsData.val()['2 brand'] == brand_entry.get() and itemsData.val()['3 date'] == exdate_entry.get() and itemsData.val()['4 amount'] == amount_entry.get():
                db.child("pantry-items").child(user['localId']).child(itemsData.key()).update(data)

        List_data = List.insert("", "end",  values=(name_entry.get(), brand_entry.get(), exdate_entry.get(), amount_entry.get(), itemsData.key()))
        
def update_record():
    db = FirebaseConfig().firebase.database()
    #Items = db.child(user['localId']).get()
    data =  {'1 name': name_entry.get(),
            '2 brand': brand_entry.get(),
            '3 date': exdate_entry.get(),
            '4 amount': amount_entry.get(),
            '5 id': oid_entry.get()
            }
    db.child("pantry-items").child(user['localId']).child(oid_entry.get()).update(data)
    # Clear the Treeview, clear entries, and pull database 
    List.delete(*List.get_children())
    clear_entries()
    query_database()
    messagebox.showinfo ("", "Item Updated!")
    
def delete_item(): # Delete selected ITEM
    List_selected = List.selection()
    if List.selection()==():
        messagebox.showerror("", "Please Select an Item to Delete")
    else:
        choice = messagebox.askquestion("Delete Item", "Are you sure you want to delete the selected item?")
        if choice == 'yes':

            ############## Delete item from  Database ##############

            db = FirebaseConfig().firebase.database()
            Items = db.child("pantry-items").child(user['localId']).child(oid_entry.get()).remove()

            #########################################################
            
            # Clear the Treeview, clear entries, and pull database 
            List.delete(*List.get_children())
            clear_entries()
            query_database()
            messagebox.showinfo ("", "Item Deleted!")

def delete_all_items(): # Delets all ITEMS

    choice = messagebox.askquestion("Delete All Items", "Are you sure you want to delete ALL items?")

    if choice == 'yes':
        ############## Delete item from  Database ##############
        
        db = FirebaseConfig().firebase.database()
        Items = db.child("pantry-items").child(user['localId']).get()
        for itemsData in Items.each():
            db.child("pantry-items").child(user['localId']).child(itemsData.key()).remove()
            
        #########################################################
        
        # Clear the Treeview, clear entries, and pull database 
        List.delete(*List.get_children())
        clear_entries()
        messagebox.showinfo ("", "Items Deleted!")


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