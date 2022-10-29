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
import datetime as dt
import time

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
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        
        global username
        global password
        global username_entry
        global password_entry
        global user
        username = StringVar()
        password = StringVar()
        
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

        label_1 = customtkinter.CTkLabel(right_frame, text='Smart Fridge GUI', text_font=("TkMenutext_font", 25, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        label_1.pack(pady = (150, 0))

        tab_frame = customtkinter.CTkFrame(right_frame, corner_radius=0, width=260, height=40)#, fg_color = "green")
        tab_frame.pack(pady = 20)

        # Tab Login button
        login_button = customtkinter.CTkButton(tab_frame, text='Login', text_font=("yu gothic ui bold", 12), borderwidth=0, text_color = ("#1e3d6d", "#ebe7e4"),
                                               fg_color= ("#ebe7e4", "#122e54"), hover_color= ("#c6baba", "#1e3d6d"),  cursor='hand2', width = 2)
        login_button.place(anchor = "nw")
        login_line = Canvas(tab_frame, width=60, height=5, bg='#ebac00')
        login_line.place(relx = 0, rely = 0.7)

        # Tab Signup button
        SignUp_button = customtkinter.CTkButton(tab_frame, text='Sign up', text_font=("yu gothic ui bold", 12), borderwidth=0, text_color = ("#1e3d6d", "#ebe7e4"),
                                  fg_color= ("#ebe7e4", "#122e54"), hover_color= ("#c6baba", "#1e3d6d"),  cursor='hand2', width = 2, command=lambda: controller.show_frame("Register"))
        SignUp_button.place(relx = 0.86, anchor= "n")
        
        # Username Entry
        username_label = customtkinter.CTkLabel(right_frame, text='• Email', text_font=("yu gothic ui", 11, 'bold'), text_color = ("#1e3d6d", "#ebe7e4"))
        username_label.pack(padx = (0, 212))
        username_entry = Entry(right_frame, textvariable=username, font=("yu gothic ui", 15), width=23)
        username_entry.pack(pady = (0, 20))
        username_entry.bind('<FocusIn>', controller.entry_callback)
        # Password Entry
        password_label = customtkinter.CTkLabel(right_frame, text='• Password'  , text_font=("yu gothic ui", 11, 'bold'), text_color = ("#1e3d6d", "#ebe7e4"))
        password_label.pack(padx = (0, 185))
        password_entry = Entry(right_frame, textvariable=password, font=("yu gothic ui", 15), show='•', width=23)
        password_entry.pack(pady = (0, 15))
        password_entry.bind('<FocusIn>', controller.entry_callback)
        # checkbutton for hiding and showing password
        def password_command(): # show/password for login
            if password_entry.cget('show') == '•':
                password_entry.configure(show='')
            else:
                password_entry.configure(show='•')

        option_frame = customtkinter.CTkFrame(right_frame, corner_radius=0, width=260, height=40)#, fg_color = "green")
        option_frame.pack()
        
        checkButton = customtkinter.CTkCheckBox(option_frame, text='show password', command = password_command, text_color = ("#1e3d6d", "#ebe7e4"), hover_color= ("#c6baba", "#1e3d6d"),)
        checkButton.place(relx = 0, rely = 0.06)

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
        reset_pwd_button = customtkinter.CTkButton(option_frame, text='Forgot Password?', text_color = ("#1e3d6d", "#ebe7e4"), 
                                    fg_color= ("#ebe7e4", "#122e54"), hover_color= ("#c6baba", "#1e3d6d"),  borderwidth=0, cursor='hand2', width = 2,  command=pwd_reset)
        reset_pwd_button.place(relx = 0.76, anchor= "n")

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
                        query_database_non()
                        query_database_shopping()
                    else:
                         messagebox.showerror("", "User not found")
                else:
                    messagebox.showerror("", "Verification Failed")

        # Proceed Login button
        loginBtn1 = customtkinter.CTkButton(right_frame, text='Login', text_font=("yu gothic ui bold", 15), cursor='hand2', command = login_user, width=256, height=50)
        loginBtn1.pack()
    
    
class PantryList(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        global aList

        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU_Welcome.png")
        logo_img = logo_img.resize((100, 100), Image.ANTIALIAS)   
        logo_img = ImageTk.PhotoImage(logo_img)
        logo_widget = customtkinter.CTkLabel(self, image=logo_img)
        logo_widget.image = logo_img
        logo_widget.place(relx=0.05, rely=0.09, anchor= "center")

        customtkinter.CTkLabel(self, text="Pantry Items" , text_font=("TkMenutext_font", 40), text_color = ("#1e3d6d", "#ebe7e4")).place(x=493, y = 40)

        date=dt.datetime.now()
        format_date=f"{date:%a, %b %d %Y}"
        label=customtkinter.CTkLabel(self, text=format_date, text_font=("Calibri", 25))
        label.place(x=1050, y = 20)

        def Clock():
            hour = time.strftime("%I")
            minute = time.strftime("%M")
            second = time.strftime("%S")
            period = time.strftime("%p")
            clock.configure(text = hour + ":" + minute + ":" + second + " " + period)
            clock.after(1000, Clock)

        clock = customtkinter.CTkLabel(self, text = "", text_font=("Calibri", 25))
        clock.place(x=1050, y=60)
        Clock()


        table_frame = customtkinter.CTkFrame(self,  highlightthickness=0, borderwidth=0, width=800, height=500)
        table_frame.place(relx=0.525, rely=0.53, anchor=tkinter.CENTER)

        List_header = ["Name", "Brand", "Expiration Date", "Remaining"]

        # Creating Treeview List
        aList = MyTreeview(table_frame, columns=List_header, show="headings")
        # positioning the Treeview List
        aList.place(x=0, y=0, width = 735, height=650)
        # Tree View Scrollbar
        tree_Scroll = customtkinter.CTkScrollbar(table_frame, command=aList.yview)
        tree_Scroll.place(x=737, y=0, height=680)
        aList.configure(yscrollcommand=tree_Scroll.set)

        List_ColWidth = [57, 53, 85, 69]
        List_ColAlignment = ["center", "center", "center", "center"]
        List_SortType = ["name", "name", "date", "percentage"]

        for record in range(len(List_header)):
            strHdr = List_header[record]
            aList.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            aList.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])

        customtkinter.CTkButton(self, text="Show More Options", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:controller.show_frame("OptionsPantryList")
            ).pack(pady=(660, 0))

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(relx=0.98, rely=0.97, anchor= "se")
        
class OptionsPantryList(customtkinter.CTkFrame):
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
        global intitial_weight


        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU_Welcome.png")
        logo_img = logo_img.resize((100, 100), Image.ANTIALIAS)   
        logo_img = ImageTk.PhotoImage(logo_img)
        logo_widget = customtkinter.CTkLabel(self, image=logo_img)
        logo_widget.image = logo_img
        logo_widget.place(relx=0.05, rely=0.09, anchor= "center")

        customtkinter.CTkLabel(self, text="Pantry Items" , text_font=("TkMenutext_font", 40), text_color = ("#1e3d6d", "#ebe7e4")).place(x=493, y = 40)


        table_frame = customtkinter.CTkFrame(self,  highlightthickness=0, borderwidth=0, width=800, height=500)
        table_frame.place(relx=0.525, rely=0.53, anchor=tkinter.CENTER)

        List_header = ["Name", "Brand", "Expiration Date", "Remaining"]

        # Creating Treeview List
        List = MyTreeview(table_frame, columns=List_header, show="headings")
        # positioning the Treeview List
        List.place(x=0, y=0, width = 735, height=390)
        # Tree View Scrollbar
        tree_Scroll = customtkinter.CTkScrollbar(table_frame, command=List.yview)
        tree_Scroll.place(x=737, y=0, height=395)
        List.configure(yscrollcommand=tree_Scroll.set)

        List_ColWidth = [57, 53, 85, 69]
        List_ColAlignment = ["center", "center", "center", "center"]
        List_SortType = ["name", "name", "date", "percentage"]

        trash_image = ImageTk.PhotoImage(file="assets/images/trash.png")
        delete_image = ImageTk.PhotoImage(file="assets/images/delete.png")
        add_image = ImageTk.PhotoImage(file="assets/images/add.png")
        edit_image = ImageTk.PhotoImage(file="assets/images/edit.png")

        for record in range(len(List_header)):
            strHdr = List_header[record]
            List.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            List.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])

        oid_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20))
        #oid_entry.place(x=220, y=210, anchor="e")

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
        AddItems_button = customtkinter.CTkButton(self, image=add_image,  text="", width=60, height=60, corner_radius=10, command = add_record)
        AddItems_button.place(x=1260, y=150, anchor="e")

        # Update Items Button
        update_button = customtkinter.CTkButton(self, image=edit_image,  text="", width=60, height=60, corner_radius=10, command = update_record)
        update_button.place(x=1260, y=220, anchor="e")

        # Delete one Items Button
        delete_button = customtkinter.CTkButton(self, image=delete_image,  text="", width=60, height=60, corner_radius=10, command = delete_item)
        delete_button.place(x=1260, y=290, anchor="e")

        # Delete all Items Button
        delete_all_button = customtkinter.CTkButton(self, image=trash_image,  text="", width=60, height=60, corner_radius=10, command = delete_all_items)
        delete_all_button.place(x=1260, y=360, anchor="e")

        # Clear all Entry Boxes Button
        clear_button = customtkinter.CTkButton(self, text = "Clear Entry", command = clear_entries, text_font=("TkHeadingtext_font", 20), width = 180)
        clear_button.place(x=1260, y=580, anchor="e")

        customtkinter.CTkButton(self, text="Hide Options", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:controller.show_frame("PantryList")
            ).pack(pady=(660, 0))
        
        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(relx=0.98, rely=0.97, anchor= "se")

        # Bind the treeview
        List.bind("<ButtonRelease-1>", select_record)

        intitial_weight = 1500


class NonPantryList(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller
        global aNonPantryList
        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU_Welcome.png")
        logo_img = logo_img.resize((100, 100), Image.ANTIALIAS)   
        logo_img = ImageTk.PhotoImage(logo_img)
        logo_widget = customtkinter.CTkLabel(self, image=logo_img)
        logo_widget.image = logo_img
        logo_widget.place(relx=0.05, rely=0.09, anchor= "center")

        customtkinter.CTkLabel(self, text="Non-Pantry Items" , text_font=("TkMenutext_font", 40), text_color = ("#1e3d6d", "#ebe7e4")).pack(pady = 40)

        table_frame = customtkinter.CTkFrame(self,  highlightthickness=0, borderwidth=0, width=800, height=500)
        table_frame.pack(padx = (40, 0))

        List_header = ["Name", "Brand", "Expiration Date"]

        # Creating Treeview List
        aNonPantryList = MyTreeview(table_frame, columns=List_header, show="headings")
        # positioning the Treeview List
        aNonPantryList.place(x=0, y=0, width = 735, height=450)
        # Tree View Scrollbar
        tree_Scroll = customtkinter.CTkScrollbar(table_frame, command=aNonPantryList.yview)
        tree_Scroll.place(x=737, y=0, height=450)
        aNonPantryList.configure(yscrollcommand=tree_Scroll.set)

        List_ColWidth = [57, 53, 85]
        List_ColAlignment = ["center", "center", "center"]
        List_SortType = ["name", "name", "date"]

        for record in range(len(List_header)):
            strHdr = List_header[record]
            aNonPantryList.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            aNonPantryList.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])

        customtkinter.CTkButton(self, text="More Options", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:controller.show_frame("OptionsNonPantryList")
            ).pack(pady=17)

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(relx=0.98, rely=0.97, anchor= "se")
        
class OptionsNonPantryList(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        global NonPantryList
        global List_header
        global List_SortType
        global List_ColWidth
        global List_ColAlignment
        global name_entry_non
        global brand_entry_non
        global exdate_entry_non
        global amount_entry_non
        global oid_entry_non

        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU_Welcome.png")
        logo_img = logo_img.resize((100, 100), Image.ANTIALIAS)   
        logo_img = ImageTk.PhotoImage(logo_img)
        logo_widget = customtkinter.CTkLabel(self, image=logo_img)
        logo_widget.image = logo_img
        logo_widget.place(relx=0.05, rely=0.09, anchor= "center")

        customtkinter.CTkLabel(self, text="Non-Pantry Items" , text_font=("TkMenutext_font", 40), text_color = ("#1e3d6d", "#ebe7e4")).pack(pady = 40)

        table_frame = customtkinter.CTkFrame(self,  highlightthickness=0, borderwidth=0, width=800, height=383)
        table_frame.pack(padx = (40, 0))

        List_header = ["Name", "Brand", "Expiration Date"]

        # Creating Treeview List
        NonPantryList = MyTreeview(table_frame, columns=List_header, show="headings")
        # positioning the Treeview List
        NonPantryList.place(x=0, y=0, width = 735, height=450)
        # Tree View Scrollbar
        tree_Scroll = customtkinter.CTkScrollbar(table_frame, command=NonPantryList.yview)
        tree_Scroll.place(x=737, y=0, height=450)
        NonPantryList.configure(yscrollcommand=tree_Scroll.set)

        List_ColWidth = [57, 53, 85]
        List_ColAlignment = ["center", "center", "center"]
        List_SortType = ["name", "name", "date"]

        for record in range(len(List_header)):
            strHdr = List_header[record]
            NonPantryList.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            NonPantryList.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])

        trash_image = ImageTk.PhotoImage(file="assets/images/trash.png")
        delete_image = ImageTk.PhotoImage(file="assets/images/delete.png")
        add_image = ImageTk.PhotoImage(file="assets/images/add.png")
        edit_image = ImageTk.PhotoImage(file="assets/images/edit.png")

        entries_frame = customtkinter.CTkFrame(self, corner_radius=0, width=735, height=50)#, fg_color = "green")
        entries_frame.pack(pady = 30)
        
        oid_entry_non = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20))
        #oid_entry_non.place(x=220, y=210, anchor="e")

        def on_click_name_non(e):
            name_entry_non.configure(state=NORMAL)
            name_entry_non.delete(0, END)
            
        name_entry_non = Entry(entries_frame,font=("TkHeadingtext_font", 20), width = 15, justify = CENTER)
        name_entry_non.place(relx = 0.02, rely = 0.1)
        name_entry_non.insert(0,  "Item Name")
        name_entry_non.configure(state=DISABLED)
        name_entry_non.bind("<Button-1>", on_click_name_non)

        def on_click_brand_non(e):
            brand_entry_non.configure(state=NORMAL)
            brand_entry_non.delete(0, END)
        brand_entry_non = Entry(entries_frame,font=("TkHeadingtext_font", 20), width = 15, justify = CENTER)
        brand_entry_non.place(relx = 0.34, rely = 0.1)
        brand_entry_non.insert(0,  "Brand Name")
        brand_entry_non.configure(state=DISABLED)
        brand_entry_non.bind("<Button-1>", on_click_brand_non)

        def on_click_exdate_non(e):
            exdate_entry_non.configure(state=NORMAL)
            exdate_entry_non.delete(0, END)
        exdate_entry_non = Entry(entries_frame,font=("TkHeadingtext_font", 20), width = 15, justify = CENTER)
        exdate_entry_non.place(relx = 0.66, rely = 0.1)
        exdate_entry_non.insert(0,  "MM-DD-YYYY")
        exdate_entry_non.configure(state=DISABLED)
        exdate_entry_non.bind("<Button-1>", on_click_exdate_non)
        
        # AddItems Page customtkinter.CTkButton
        AddItems_button = customtkinter.CTkButton(self, image=add_image,  text="", width=60, height=60, corner_radius=10, command = add_record_non)
        AddItems_button.place(x=1260, y=150, anchor="e")

        # Update Items Button
        update_button = customtkinter.CTkButton(self, image=edit_image,  text="", width=60, height=60, corner_radius=10, command = update_record_non)
        update_button.place(x=1260, y=220, anchor="e")

        # Delete one Items Button
        delete_button = customtkinter.CTkButton(self, image=delete_image,  text="", width=60, height=60, corner_radius=10, command = delete_item_non)
        delete_button.place(x=1260, y=290, anchor="e")

        # Delete all Items Button
        delete_all_button = customtkinter.CTkButton(self, image=trash_image,  text="", width=60, height=60, corner_radius=10, command = delete_all_non)
        delete_all_button.place(x=1260, y=360, anchor="e")

        # Clear all Entry Boxes Button
        clear_button = customtkinter.CTkButton(self, text = "Clear Entry", command = clear_entries, text_font=("TkHeadingtext_font", 20), width = 180)
        clear_button.place(x=1260, y=580, anchor="e")

        customtkinter.CTkButton(self, text="Hide Options", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:controller.show_frame("NonPantryList")
            ).pack(pady=(24, 0))

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(relx=0.98, rely=0.97, anchor= "se")

        # Bind the treeview
        NonPantryList.bind("<ButtonRelease-1>", select_record_non)


class SuggestedShopping(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        global aShoppingList

        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU_Welcome.png")
        logo_img = logo_img.resize((100, 100), Image.ANTIALIAS)   
        logo_img = ImageTk.PhotoImage(logo_img)
        logo_widget = customtkinter.CTkLabel(self, image=logo_img)
        logo_widget.image = logo_img
        logo_widget.place(relx=0.05, rely=0.09, anchor= "center")

        customtkinter.CTkLabel(self, text="Suggested Shopping List" , text_font=("TkMenutext_font", 40), text_color = ("#1e3d6d", "#ebe7e4")).pack(pady=40)

        table_frame = customtkinter.CTkFrame(self,  highlightthickness=0, borderwidth=0, width=750, height=500)#, fg_color = "red")
        table_frame.pack(padx = (40, 0))

        List_header = ["Name", "Brand"]

        # Creating Treeview List
        aShoppingList = MyTreeview(table_frame, columns=List_header, show="headings")
        # positioning the Treeview List
        aShoppingList.place(x=0, y=0, width = 735, height=500)
        # Tree View Scrollbar
        tree_Scroll = customtkinter.CTkScrollbar(table_frame, command=aShoppingList.yview)
        tree_Scroll.place(x=737, y=0, height=510)
        aShoppingList.configure(yscrollcommand=tree_Scroll.set)

        List_ColWidth = [57, 53]
        List_ColAlignment = ["center", "center"]
        List_SortType = ["name", "name"]

        for record in range(len(List_header)):
            strHdr = List_header[record]
            aShoppingList.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            aShoppingList.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])


        customtkinter.CTkButton(self, text="Show Options", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:controller.show_frame("OptionsSuggestedShopping")
            ).pack(pady=(20, 0))
        
        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(relx=0.98, rely=0.97, anchor= "se")

class OptionsSuggestedShopping(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        global ShoppingList
        global List_header
        global List_SortType
        global List_ColWidth
        global List_ColAlignment
        global name_entry_Shopping
        global brand_entry_Shopping
        global oid_entry_Shopping

        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU_Welcome.png")
        logo_img = logo_img.resize((100, 100), Image.ANTIALIAS)   
        logo_img = ImageTk.PhotoImage(logo_img)
        logo_widget = customtkinter.CTkLabel(self, image=logo_img)
        logo_widget.image = logo_img
        logo_widget.place(relx=0.05, rely=0.09, anchor= "center")

        customtkinter.CTkLabel(self, text="Suggested Shopping List" , text_font=("TkMenutext_font", 40), text_color = ("#1e3d6d", "#ebe7e4")).pack(pady=40)

        table_frame = customtkinter.CTkFrame(self,  highlightthickness=0, borderwidth=0, width=750, height=410)#, fg_color = "red")
        table_frame.pack(padx = (40, 0))

        List_header = ["Name", "Brand"]

        # Creating Treeview List
        ShoppingList = MyTreeview(table_frame, columns=List_header, show="headings")
        # positioning the Treeview List
        ShoppingList.place(x=0, y=0, width = 735, height=450)
        # Tree View Scrollbar
        tree_Scroll = customtkinter.CTkScrollbar(table_frame, command=ShoppingList.yview)
        tree_Scroll.place(x=737, y=0, height=450)
        ShoppingList.configure(yscrollcommand=tree_Scroll.set)

        List_ColWidth = [57, 53]
        List_ColAlignment = ["center", "center"]
        List_SortType = ["name", "name"]

        trash_image = ImageTk.PhotoImage(file="assets/images/trash.png")
        delete_image = ImageTk.PhotoImage(file="assets/images/delete.png")
        add_image = ImageTk.PhotoImage(file="assets/images/add.png")
        edit_image = ImageTk.PhotoImage(file="assets/images/edit.png")

        for record in range(len(List_header)):
            strHdr = List_header[record]
            ShoppingList.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            ShoppingList.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])

        entries_frame = customtkinter.CTkFrame(self, corner_radius=0, width=735, height=50)#, fg_color = "green")
        entries_frame.pack(pady = 10)
        
        oid_entry_Shopping = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20))
        #oid_entry_Shopping.place(x=220, y=210, anchor="e")

        name_label = customtkinter.CTkLabel(entries_frame, text = "Name:", text_font=("TkHeadingtext_font", 18))
        name_label.place(relx = 0.02, rely = 0.16)
            
        name_entry_Shopping = customtkinter.CTkEntry(entries_frame, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        name_entry_Shopping.place(relx = 0.18, rely = 0.1)
        
        brand_label = customtkinter.CTkLabel(entries_frame, text = "Brand:", text_font=("TkHeadingtext_font", 18))
        brand_label.place(relx = 0.5, rely = 0.16)
        brand_entry_Shopping = customtkinter.CTkEntry(entries_frame, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        brand_entry_Shopping.place(relx = 0.66, rely = 0.1)

        # AddItems Page customtkinter.CTkButton
        AddItems_button = customtkinter.CTkButton(self, image=add_image,  text="", width=60, height=60, corner_radius=10, command = add_record_Shopping)
        AddItems_button.place(x=1260, y=150, anchor="e")

        # Update Items Button
        update_button = customtkinter.CTkButton(self, image=edit_image,  text="", width=60, height=60, corner_radius=10, command = update_record_Shopping)
        update_button.place(x=1260, y=220, anchor="e")

        # Delete one Items Button
        delete_button = customtkinter.CTkButton(self, image=delete_image,  text="", width=60, height=60, corner_radius=10, command = delete_item_Shopping)
        delete_button.place(x=1260, y=290, anchor="e")

        # Delete all Items Button
        delete_all_button = customtkinter.CTkButton(self, image=trash_image,  text="", width=60, height=60, corner_radius=10, command = delete_all_Shopping)
        delete_all_button.place(x=1260, y=360, anchor="e")

        # Clear all Entry Boxes Button
        clear_button = customtkinter.CTkButton(self, text = "Clear Entries", command = clear_entries, text_font=("TkHeadingtext_font", 20), width = 180)
        clear_button.place(x=1260, y=585, anchor="e")

        customtkinter.CTkButton(self, text="Hide Options", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:controller.show_frame("SuggestedShopping")
            ).pack(pady=(40, 0))
        
        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(relx=0.98, rely=0.97, anchor= "se")

        # Bind the treeview
        ShoppingList.bind("<ButtonRelease-1>", select_record_Shopping)


def query_database():
    # pull data
    db = FirebaseConfig().firebase.database()
    Items = db.child("pantry-items").child(user['localId']).get()
    for itemsData in Items.each():
        data = itemsData.val()
        datalist = list(data.values())
        List.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2],
                                        f'{int((int(datalist[3])/datalist[4])*100)}%',
                                        datalist[6]
                                        )
                    )

        aList.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2],
                                        f'{int((int(datalist[3])/datalist[4])*100)}%',
                                        datalist[6]
                                        )
                    )
def query_database_non():
    # pull data
    db = FirebaseConfig().firebase.database()
    Items = db.child("non-pantry-items").child(user['localId']).get()
    for itemsData in Items.each():
        data = itemsData.val()
        datalist = list(data.values())
        NonPantryList.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2],
                                        datalist[3]
                                        )
                    )
        aNonPantryList.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2],
                                        datalist[3]
                                        )
                    )
def query_database_shopping():
    # pull data
    db = FirebaseConfig().firebase.database()
    Items = db.child("shopping-list").child(user['localId']).get()
    for itemsData in Items.each():
        data = itemsData.val()
        datalist = list(data.values())
        ShoppingList.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2]
                                        )
                    )
        aShoppingList.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2]
                                        )
                    )
        
def clear_entries():
    name_entry.delete(0, END)
    brand_entry.delete(0, END)
    exdate_entry.delete(0, END)
    amount_entry.delete(0, END)
    oid_entry.delete(0, END)
    
    name_entry_non.delete(0, END)
    brand_entry_non.delete(0, END)
    exdate_entry_non.delete(0, END)
    oid_entry_non.delete(0, END)
    
    name_entry_Shopping.delete(0, END)
    brand_entry_Shopping.delete(0, END)
    oid_entry_Shopping.delete(0, END)
    
# Functions for Pantry Items
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
    #amount_entry.insert(0, values[3])
    oid_entry.insert(0, values[4])

def add_record(): # adds data to the table (List)
    if name_entry.get()=="":
        messagebox.showerror("", "Item's data needed")
    else:
        data =  {'1 Name': name_entry.get(),
                '2 Brand': brand_entry.get(),
                '3 Expiration-Date': exdate_entry.get(),
                '4 Current-Weight': amount_entry.get(),
                '5 Initial-Weight': intitial_weight,
                '6 Grid-Location': "1"
                }
        db = FirebaseConfig().firebase.database()
        db.child("pantry-items").child(user['localId']).push(data)

        Items = db.child("pantry-items").child(user['localId']).get()
        for itemsData in Items.each():

            if itemsData.val() == data:
                data =  {'1 Name': name_entry.get(),
                        '2 Brand': brand_entry.get(),
                        '3 Expiration-Date': exdate_entry.get(),
                        '4 Current-Weight': amount_entry.get(),
                        '5 Initial-Weight': intitial_weight,
                        '6 Grid-Location': "1",
                        '7 id': itemsData.key(),
                        }
                db.child("pantry-items").child(user['localId']).child(itemsData.key()).update(data)

        List.insert("", "end",
                            values=(
                                    name_entry.get(),
                                    brand_entry.get(),
                                    exdate_entry.get(),
                                    f'{int((int(amount_entry.get())/intitial_weight)*100)}%',
                                    itemsData.key()
                                    )
                                )
        aList.insert("", "end",
                    values=(
                            name_entry.get(),
                            brand_entry.get(),
                            exdate_entry.get(),
                            f'{int((int(amount_entry.get())/intitial_weight)*100)}%',
                            itemsData.key()
                            )
                    )

def update_record():
    db = FirebaseConfig().firebase.database()
    data =  {'1 Name': name_entry.get(),
            '2 Brand': brand_entry.get(),
            '3 Expiration-Date': exdate_entry.get(),
            '4 Current-Weight': amount_entry.get(),
            '5 Initial-Weight': intitial_weight,
            '6 Grid-Location': "1",
            '7 id': oid_entry.get(),
            }
    db.child("pantry-items").child(user['localId']).child(oid_entry.get()).update(data)
    # Clear the Treeview, clear entries, and pull database
    List.delete(*List.get_children())
    aList.delete(*aList.get_children())
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
            aList.delete(*aList.get_children())
            
            NonPantryList.delete(*NonPantryList.get_children())
            aNonPantryList.delete(*aNonPantryList.get_children())
            
            ShoppingList.delete(*ShoppingList.get_children())
            aShoppingList.delete(*aShoppingList.get_children())
            
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
        aList.delete(*aList.get_children())
        clear_entries()
        messagebox.showinfo ("", "Items Deleted!")

# Functions for Non-Pantry Items
def select_record_non(e):
    # Grab record number
    selected = NonPantryList.focus()
    # Grab record VALUES
    values = NonPantryList.item(selected, "values")
    
    name_entry_non.configure(state=NORMAL)
    brand_entry_non.configure(state=NORMAL)
    exdate_entry_non.configure(state=NORMAL)
    # clear entry boxes
    clear_entries()
    # output to entry boxes
    name_entry_non.insert(0, values[0])
    brand_entry_non.insert(0, values[1])
    exdate_entry_non.insert(0, values[2])
    oid_entry_non.insert(0, values[3])

def add_record_non(): # adds data to the table (List)
    if name_entry_non.get()=="":
        messagebox.showerror("", "Item's data needed")
    else:
        data =  {'1 Name': name_entry_non.get(),
                '2 Brand': brand_entry_non.get(),
                '3 Expiration-Date': exdate_entry_non.get(),
                }
        db = FirebaseConfig().firebase.database()
        db.child("non-pantry-items").child(user['localId']).push(data)

        Items = db.child("non-pantry-items").child(user['localId']).get()
        for itemsData in Items.each():

            if itemsData.val() == data:
                data =  {'1 Name': name_entry_non.get(),
                        '2 Brand': brand_entry_non.get(),
                        '3 Expiration-Date': exdate_entry_non.get(),
                        '4 id': itemsData.key(),
                        }
                db.child("non-pantry-items").child(user['localId']).child(itemsData.key()).update(data)

        NonPantryList.insert("", "end",
                            values=(
                                    name_entry_non.get(),
                                    brand_entry_non.get(),
                                    exdate_entry_non.get(),
                                    itemsData.key()
                                    )
                                )
        aNonPantryList.insert("", "end",
                    values=(
                            name_entry_non.get(),
                            brand_entry_non.get(),
                            exdate_entry_non.get(),
                            itemsData.key()
                            )
                    )

def update_record_non():
    db = FirebaseConfig().firebase.database()
    data =  {'1 Name': name_entry_non.get(),
            '2 Brand': brand_entry_non.get(),
            '3 Expiration-Date': exdate_entry_non.get(),
            '4 id': oid_entry_non.get(),
            }
    db.child("non-pantry-items").child(user['localId']).child(oid_entry_non.get()).update(data)
    # Clear the Treeview, clear entries, and pull database
    NonPantryList.delete(*NonPantryList.get_children())
    aNonPantryList.delete(*aNonPantryList.get_children())
    clear_entries()
    query_database_non()
    messagebox.showinfo ("", "Item Updated!")

def delete_item_non(): # Delete selected ITEM
    List_selected = NonPantryList.selection()
    if NonPantryList.selection()==():
        messagebox.showerror("", "Please Select an Item to Delete")
    else:
        choice = messagebox.askquestion("Delete Item", "Are you sure you want to delete the selected item?")
        if choice == 'yes':

            ############## Delete item from  Database ##############

            db = FirebaseConfig().firebase.database()
            Items = db.child("non-pantry-items").child(user['localId']).child(oid_entry_non.get()).remove()

            #########################################################

            # Clear the Treeview, clear entries, and pull database
            NonPantryList.delete(*NonPantryList.get_children())
            aNonPantryList.delete(*aNonPantryList.get_children())
            clear_entries()
            query_database_non()
            messagebox.showinfo ("", "Item Deleted!")

def delete_all_non(): # Delets all ITEMS

    choice = messagebox.askquestion("Delete All Items", "Are you sure you want to delete ALL items?")

    if choice == 'yes':
        ############## Delete item from  Database ##############

        db = FirebaseConfig().firebase.database()
        Items = db.child("non-pantry-items").child(user['localId']).get()
        for itemsData in Items.each():
            db.child("non-pantry-items").child(user['localId']).child(itemsData.key()).remove()

        #########################################################

        # Clear the Treeview, clear entries, and pull database
        NonPantryList.delete(*NonPantryList.get_children())
        aNonPantryList.delete(*aNonPantryList.get_children())
        clear_entries()
        messagebox.showinfo ("", "Items Deleted!")

# Functions for Shooping Items
def select_record_Shopping(e):
    # Grab record number
    selected = ShoppingList.focus()
    # Grab record VALUES
    values = ShoppingList.item(selected, "values")
    # clear entry boxes
    clear_entries()
    # output to entry boxes
    name_entry_Shopping.insert(0, values[0])
    brand_entry_Shopping.insert(0, values[1])
    oid_entry_Shopping.insert(0, values[2])

def add_record_Shopping(): # adds data to the table (List)
    if name_entry_Shopping.get()=="":
        messagebox.showerror("", "Item's data needed")
    else:
        data =  {'1 Name': name_entry_Shopping.get(),
                '2 Brand': brand_entry_Shopping.get(),
                }
        db = FirebaseConfig().firebase.database()
        db.child("shopping-list").child(user['localId']).push(data)

        Items = db.child("shopping-list").child(user['localId']).get()
        for itemsData in Items.each():

            if itemsData.val() == data:
                data =  {'1 Name': name_entry_Shopping.get(),
                        '2 Brand': brand_entry_Shopping.get(),
                        '3 id': itemsData.key(),
                        }
                db.child("shopping-list").child(user['localId']).child(itemsData.key()).update(data)

        ShoppingList.insert("", "end",
                            values=(
                                    name_entry_Shopping.get(),
                                    brand_entry_Shopping.get(),
                                    itemsData.key()
                                    )
                                )
        aShoppingList.insert("", "end",
                    values=(
                            name_entry_Shopping.get(),
                            brand_entry_Shopping.get(),
                            itemsData.key()
                            )
                    )

def update_record_Shopping():
    db = FirebaseConfig().firebase.database()
    data =  {'1 Name': name_entry_Shopping.get(),
            '2 Brand': brand_entry_Shopping.get(),
            '3 id': oid_entry_Shopping.get(),
            }
    db.child("shopping-list").child(user['localId']).child(oid_entry_Shopping.get()).update(data)
    # Clear the Treeview, clear entries, and pull database
    ShoppingList.delete(*ShoppingList.get_children())
    aShoppingList.delete(*aShoppingList.get_children())
    clear_entries()
    query_database_shopping()
    messagebox.showinfo ("", "Item Updated!")

def delete_item_Shopping(): # Delete selected ITEM
    List_selected = ShoppingList.selection()
    if ShoppingList.selection()==():
        messagebox.showerror("", "Please Select an Item to Delete")
    else:
        choice = messagebox.askquestion("Delete Item", "Are you sure you want to delete the selected item?")
        if choice == 'yes':

            ############## Delete item from  Database ##############

            db = FirebaseConfig().firebase.database()
            Items = db.child("shopping-list").child(user['localId']).child(oid_entry_Shopping.get()).remove()

            #########################################################

            # Clear the Treeview, clear entries, and pull database
            ShoppingList.delete(*ShoppingList.get_children())
            aShoppingList.delete(*aShoppingList.get_children())
            clear_entries()
            query_database_shopping()
            messagebox.showinfo ("", "Item Deleted!")

def delete_all_Shopping(): # Delets all ITEMS

    choice = messagebox.askquestion("Delete All Items", "Are you sure you want to delete ALL items?")

    if choice == 'yes':
        ############## Delete item from  Database ##############

        db = FirebaseConfig().firebase.database()
        Items = db.child("shopping-list").child(user['localId']).get()
        for itemsData in Items.each():
            db.child("shopping-list").child(user['localId']).child(itemsData.key()).remove()

        #########################################################

        # Clear the Treeview, clear entries, and pull database
        ShoppingList.delete(*ShoppingList.get_children())
        aShoppingList.delete(*aShoppingList.get_children())
        clear_entries
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
