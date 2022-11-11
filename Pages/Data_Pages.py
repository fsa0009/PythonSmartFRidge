from Pages import *


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

        self.app_login_cred = {'email': StringVar(), 'idToken': StringVar(), 'localId': StringVar()}


    def register(self, username, password, name):
        try:
            user = self.auth.create_user_with_email_and_password(username, password)
            self.auth.send_email_verification(user['idToken'])
            user_info =  {
                        'Email':username,
                        'Name': name,
                        'TheID': user['localId'],
                        'Username':username.replace("@gmail.com", ""),
                    }
            db = FirebaseConfig().firebase.database()
            db.child("my-info").child(user['localId']).set(user_info)

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


class PantryList(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller
        global aList

        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU.png")
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

        customtkinter.CTkButton(self, text="Show Options", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:controller.show_frame("OptionsPantryList")
            ).pack(pady=(660, 0))

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(relx=0.985, rely=0.97, anchor= "se")

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
        global barcode_entry
        global oid_entry
        global intitial_weight
        global update_button
        global delete_button
        global unix_time
        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU.png")
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

        trash_image = ImageTk.PhotoImage(file="assets/images/Buttons/trash.png")
        delete_image = ImageTk.PhotoImage(file="assets/images/Buttons/delete.png")
        add_image = ImageTk.PhotoImage(file="assets/images/Buttons/add.png")
        edit_image = ImageTk.PhotoImage(file="assets/images/Buttons/edit.png")
        scanner_image = ImageTk.PhotoImage(file="assets/images/Buttons/scanner.png")
        refresh_image = ImageTk.PhotoImage(file="assets/images/Buttons/refresh.png")

        for record in range(len(List_header)):
            strHdr = List_header[record]
            List.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            List.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])

        oid_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20))
        #oid_entry.place(x=220, y=210, anchor="e")

        name_label = customtkinter.CTkLabel(self, text = "Name:", text_font=("TkHeadingtext_font", 18, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        name_label.place(x=380, y=550, anchor="e")

        name_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        name_entry.place(x=600, y=550, anchor="e")

        brand_label = customtkinter.CTkLabel(self, text = "Brand:", text_font=("TkHeadingtext_font", 18, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        brand_label.place(x=825, y=550, anchor="e")
        brand_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        brand_entry.place(x=1007, y=550, anchor="e")

        exdate_label = customtkinter.CTkLabel(self, text = "Exp. Date: ", text_font=("TkHeadingtext_font", 18, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        exdate_label.place(x=404, y=600, anchor="e")
        exdate_entry = DateEntry(self, selectmode="day", font = ("TkHeadingtext_font", 20), date_pattern = 'mm/dd/y')
        exdate_entry.place(x=600, y=600, anchor="e")

        date_format = datetime.datetime.strptime(exdate_entry.get(),
                                                 "%m/%d/%Y")
        unix_time = datetime.datetime.timestamp(date_format)
        # print(unix_time)
        #date_time.strftime('%Y-%m-%d'))

        amount_label = customtkinter.CTkLabel(self, text = "Amount: ", text_font=("TkHeadingtext_font", 18, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        amount_label.place(x=825, y=600, anchor="e")
        amount_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        amount_entry.place(x=1007, y=600, anchor="e")
        barcode_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 150, justify = CENTER)
        barcode_entry.place(x=1190, y=430, anchor="e")

        # AddItems Page customtkinter.CTkButton
        AddItems_button = customtkinter.CTkButton(self, image=add_image,  text="", width=60, height=60, corner_radius=10,  command = add_record)
        AddItems_button.place(x=1260, y=150, anchor="e")

        # Update Items Button
        update_button = customtkinter.CTkButton(self, image=edit_image,  text="", width=60, height=60, corner_radius=10, command = update_record)

        # Delete one Items Button
        delete_button = customtkinter.CTkButton(self, image=trash_image,  text="", width=60, height=60, corner_radius=10, command = delete_item)

        # refresh_button = customtkinter.CTkButton(self, image=refresh_image,  text="", width=60, height=60, corner_radius=10, command = refresh)
        # refresh_button.place(x=1260, y=360, anchor="e")

        barcode_button = customtkinter.CTkButton(self, image=scanner_image,  text="", width=60, height=60, corner_radius=10, command = barcode_scanner)
        barcode_button.place(x=1260, y=430, anchor="e")

        # Clear all Entry Boxes Button
        clear_button = customtkinter.CTkButton(self, text = "Clear", command = clear_entries, text_font=("TkHeadingtext_font", 20))
        clear_button.place(x=1260, y=550, anchor="e")

        # deletelist_button = customtkinter.CTkButton(self, text = "Reset List", command = delete_all_items, text_font=("TkHeadingtext_font", 20), width = 180)
        # deletelist_button.place(x=200, y=150, anchor="e")

        customtkinter.CTkButton(self, text="Hide Options", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:[controller.show_frame("PantryList"),  cleanup()]
            ).pack(pady=(660, 0))

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:[controller.show_frame("MainMenu"), cleanup()]
            ).place(relx=0.985, rely=0.97, anchor= "se")

        # Bind the treeview
        List.bind("<ButtonRelease-1>", select_record)

        intitial_weight = 1500
        exdate_entry.delete(0,END)


class NonPantryList(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master)
        self.controller = controller

        global aNonPantryList
        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU.png")
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
            ).place(relx=0.985, rely=0.97, anchor= "se")

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
        global oid_entry_non
        global barcode_entry_non
        global update_button_non
        global delete_button_non

        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU.png")
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

        trash_image = ImageTk.PhotoImage(file="assets/images/Buttons/trash.png")
        delete_image = ImageTk.PhotoImage(file="assets/images/Buttons/delete.png")
        add_image = ImageTk.PhotoImage(file="assets/images/Buttons/add.png")
        edit_image = ImageTk.PhotoImage(file="assets/images/Buttons/edit.png")
        scanner_image = ImageTk.PhotoImage(file="assets/images/Buttons/scanner.png")

        entries_frame = customtkinter.CTkFrame(self, corner_radius=0, width=735, height=50)#, fg_color = "green")
        entries_frame.pack(pady = 30)

        oid_entry_non = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20))
        #oid_entry_non.place(x=220, y=210, anchor="e")

        name_label = customtkinter.CTkLabel(self, text = "Name:", text_font=("TkHeadingtext_font", 18, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        name_label.place(x=380, y=550, anchor="e")

        name_entry_non = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        name_entry_non.place(x=600, y=550, anchor="e")

        brand_label = customtkinter.CTkLabel(self, text = "Brand:", text_font=("TkHeadingtext_font", 18, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        brand_label.place(x=825, y=550, anchor="e")
        brand_entry_non = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        brand_entry_non.place(x=1007, y=550, anchor="e")

        exdate_entry_non = DateEntry(self, selectmode="day", font = ("TkHeadingtext_font", 20), date_pattern = 'mm/dd/y')
        exdate_entry_non.place(x=600, y=600, anchor="e")


        exdate_label = customtkinter.CTkLabel(self, text = "Exp. Date: ", text_font=("TkHeadingtext_font", 18, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        exdate_label.place(x=404, y=600, anchor="e")

        barcode_entry_non = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 150, justify = CENTER)
        barcode_entry_non.place(x=1190, y=430, anchor="e")

        # AddItems Page customtkinter.CTkButton
        AddItems_button = customtkinter.CTkButton(self, image=add_image,  text="", width=60, height=60, corner_radius=10, command = add_record_non)
        AddItems_button.place(x=1260, y=150, anchor="e")

        # Update Items Button
        update_button_non = customtkinter.CTkButton(self, image=edit_image,  text="", width=60, height=60, corner_radius=10, command = update_record_non)

        # Delete one Items Button
        delete_button_non = customtkinter.CTkButton(self, image=delete_image,  text="", width=60, height=60, corner_radius=10, command = delete_item_non)

        # Delete all Items Button
        # delete_all_button = customtkinter.CTkButton(self, image=trash_image,  text="", width=60, height=60, corner_radius=10, command = delete_all_non)
        # delete_all_button.place(x=1260, y=360, anchor="e")

        barcode_button = customtkinter.CTkButton(self, image=scanner_image,  text="", width=60, height=60, corner_radius=10, command = barcode_scanner_non)
        barcode_button.place(x=1260, y=430, anchor="e")

        # Clear all Entry Boxes Button
        clear_button = customtkinter.CTkButton(self, text = "Clear", command = clear_entries, text_font=("TkHeadingtext_font", 20), width = 180)
        clear_button.place(x=1260, y=580, anchor="e")

        customtkinter.CTkButton(self, text="Hide Options", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:[controller.show_frame("NonPantryList"), cleanup()]
            ).pack(pady=(24, 0))

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:[controller.show_frame("MainMenu"), cleanup()]
            ).place(relx=0.985, rely=0.97, anchor= "se")

        # Bind the treeview
        NonPantryList.bind("<ButtonRelease-1>", select_record_non)
        exdate_entry_non.delete(0,END)


class SuggestedShopping(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        global aShoppingList

        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU.png")
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
            ).place(relx=0.985, rely=0.97, anchor= "se")

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

        global update_button_Shopping
        global delete_button_Shopping

        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU.png")
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

        trash_image = ImageTk.PhotoImage(file="assets/images/Buttons/trash.png")
        delete_image = ImageTk.PhotoImage(file="assets/images/Buttons/delete.png")
        add_image = ImageTk.PhotoImage(file="assets/images/Buttons/add.png")
        edit_image = ImageTk.PhotoImage(file="assets/images/Buttons/edit.png")

        for record in range(len(List_header)):
            strHdr = List_header[record]
            ShoppingList.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            ShoppingList.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])

        entries_frame = customtkinter.CTkFrame(self, corner_radius=0, width=735, height=50)#, fg_color = "green")
        entries_frame.pack(pady = 10)

        oid_entry_Shopping = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20))
        #oid_entry_Shopping.place(x=220, y=210, anchor="e")

        name_label = customtkinter.CTkLabel(entries_frame, text = "Name:", text_font=("TkHeadingtext_font", 18, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        name_label.place(relx = 0.02, rely = 0.16)

        name_entry_Shopping = customtkinter.CTkEntry(entries_frame, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        name_entry_Shopping.place(relx = 0.18, rely = 0.1)

        brand_label = customtkinter.CTkLabel(entries_frame, text = "Brand:", text_font=("TkHeadingtext_font", 18, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        brand_label.place(relx = 0.5, rely = 0.16)
        brand_entry_Shopping = customtkinter.CTkEntry(entries_frame, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        brand_entry_Shopping.place(relx = 0.66, rely = 0.1)

        # AddItems Page customtkinter.CTkButton
        AddItems_button = customtkinter.CTkButton(self, image=add_image,  text="", width=60, height=60, corner_radius=10, command = add_record_Shopping)
        AddItems_button.place(x=1260, y=150, anchor="e")

        # Update Items Button
        update_button_Shopping = customtkinter.CTkButton(self, image=edit_image,  text="", width=60, height=60, corner_radius=10, command = update_record_Shopping)

        # Delete one Items Button
        delete_button_Shopping = customtkinter.CTkButton(self, image=delete_image,  text="", width=60, height=60, corner_radius=10, command = delete_item_Shopping)

        # Delete all Items Button
        # delete_all_button = customtkinter.CTkButton(self, image=trash_image,  text="", width=60, height=60, corner_radius=10, command = delete_all_Shopping)
        # delete_all_button.place(x=1260, y=360, anchor="e")

        # Clear all Entry Boxes Button
        clear_button = customtkinter.CTkButton(self, text = "Clear", command = clear_entries, text_font=("TkHeadingtext_font", 20))
        clear_button.place(x=1260, y=585, anchor="e")

        customtkinter.CTkButton(self, text="Hide Options", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:[controller.show_frame("SuggestedShopping"), cleanup()]
            ).pack(pady=(40, 0))

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:[controller.show_frame("MainMenu"), cleanup()]
            ).place(relx=0.985, rely=0.97, anchor= "se")

        # Bind the treeview
        ShoppingList.bind("<ButtonRelease-1>", select_record_Shopping)


class RecipeSuggestions(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master)
        self.controller = controller
        n_rows = 8
        for i in range(n_rows):
            self.grid_rowconfigure(i,  weight = 1)

        self.grid_columnconfigure(0,  weight = 1)
        self.grid_columnconfigure(1,  weight = 4)
        # self.grid(padx=20)

        global Recipe_name_Entry
        global Recipe_items_Entry
        global Recipe_cookingtime_Entry
        global Recipe_calories_Entry
        global Recipe_servings_Entry
        global Recipe_inst_Entry
        global next_btn

        Recipe_name_Entry = customtkinter.CTkLabel(self, text="", text_font=("TkHeadingtext_font", 25),
                                                    text_color = ("#1e3d6d", "#ebe7e4"))
        Recipe_name_Entry.grid(row=0, column = 0, columnspan = 2)


        customtkinter.CTkLabel(self, text="Items:", text_font=("TkHeadingtext_font", 15),
                                text_color = ("#1e3d6d", "#ebe7e4")).grid(row=1, column = 0, sticky="E")
        Recipe_items_Entry = Text(self, font=("TkHeadingtext_font", 15),  width = 40, height = 7, fg = "white",
                                    bg = "#403c3c", relief = GROOVE, padx = 20, pady =20, bd =0)
        Recipe_items_Entry.grid(row=1, column = 1, sticky="W")


        customtkinter.CTkLabel(self, text="Cooking Time:", text_font=("TkHeadingtext_font", 15),
                                text_color = ("#1e3d6d", "#ebe7e4")).grid(row=2, column = 0, sticky="E")
        Recipe_cookingtime_Entry = customtkinter.CTkLabel(self, text="", text_font=("TkHeadingtext_font", 15), fg_color= "#403c3c")
        Recipe_cookingtime_Entry.grid(row=2, column = 1, sticky="W")


        customtkinter.CTkLabel(self, text="Calories:", text_font=("TkHeadingtext_font", 15),
                                text_color = ("#1e3d6d", "#ebe7e4")).grid(row=3, column = 0, sticky="E")
        Recipe_calories_Entry = customtkinter.CTkLabel(self, text="", text_font=("TkHeadingtext_font", 15), fg_color= "#403c3c")
        Recipe_calories_Entry.grid(row=3, column = 1, sticky="W")


        customtkinter.CTkLabel(self, text="Servings:", text_font=("TkHeadingtext_font", 15),
                                text_color = ("#1e3d6d", "#ebe7e4")).grid(row=4, column = 0, sticky="E")
        Recipe_servings_Entry = customtkinter.CTkLabel(self, text="", text_font=("TkHeadingtext_font", 15), fg_color= "#403c3c")
        Recipe_servings_Entry.grid(row=4, column = 1, sticky="W")


        customtkinter.CTkLabel(self, text="Instructions:", text_font=("TkHeadingtext_font", 15),
                                text_color = ("#1e3d6d", "#ebe7e4")).grid(row=5, column = 0, sticky="E")
        Recipe_inst_Entry = Text(self, font=("TkHeadingtext_font", 15),  width = 90, height = 5, fg = "white",
                                    bg = "#403c3c", relief = GROOVE, padx = 20, pady =20, bd =0)
        Recipe_inst_Entry.grid(row=5, column = 1, sticky="W")

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:[controller.show_frame("MainMenu"), cleanup()]
            ).place(relx=0.985, rely=0.97, anchor= "se")

        next_btn = customtkinter.CTkButton(self, text="Next Recipe", text_font=("TkHeadingtext_font", 20) , cursor="hand2")
        next_btn.place(relx=0.985, rely=0.2, anchor= "se")

        recipes1()


def recipes1():

    # pull data
    db = FirebaseConfig().firebase.database()

    Recipe01 = db.child("recipes").child("global").child("Recipe_01").get()
    Recipe01_data = Recipe01.val()
    Recipe01_values = list(Recipe01_data.values())

    Recipe01_name = Recipe01_values[0]
    Recipe_name_Entry.configure(text = Recipe01_name)
    # print(Recipe01_name)

    Recipe01_items = list(Recipe01_values[1].values())
    Recipe_items_Entry.config(state='normal')
    Recipe_items_Entry.delete(1.0, END)
    #print(Recipe01_items)
    try:
        Recipe_items_Entry.insert(1.0 , f'1. {Recipe01_items[0]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(2.0 , f'2. {Recipe01_items[1]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(3.0 , f'3. {Recipe01_items[2]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(4.0 , f'4. {Recipe01_items[3]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(5.0 , f'5. {Recipe01_items[4]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(6.0 , f'6. {Recipe01_items[5]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(7.0 , f'7. {Recipe01_items[6]}\n')
    except:
        pass
    Recipe_items_Entry.config(state='disabled')

    Recipe01_cookingtime = Recipe01_values[2]
    Recipe_cookingtime_Entry.configure(text = Recipe01_cookingtime)
    #print(Recipe01_cookingtime)

    Recipe01_calories = Recipe01_values[3]
    Recipe_calories_Entry.configure(text = Recipe01_calories)
    #print(Recipe01_calories)

    Recipe01_servings = Recipe01_values[4]
    Recipe_servings_Entry.configure(text = Recipe01_servings)
    #print(Recipe01_servings)

    Recipe01_instruction = Recipe01_values[5]
    Recipe_inst_Entry.config(state='normal')
    Recipe_inst_Entry.delete(1.0, END)
    Recipe_inst_Entry.insert(1.0, Recipe01_instruction)
    Recipe_inst_Entry.config(state='disabled')
    # print(Recipe01_instruction)

    next_btn.configure(command=recipes2)

def recipes2():

    # pull data
    db = FirebaseConfig().firebase.database()

    Recipe02 = db.child("recipes").child("global").child("Recipe_02").get()
    Recipe02_data = Recipe02.val()
    Recipe02_values = list(Recipe02_data.values())

    Recipe02_name = Recipe02_values[0]
    Recipe_name_Entry.configure(text = Recipe02_name)
    # print(Recipe02_name)

    Recipe02_items = list(Recipe02_values[1].values())
    Recipe_items_Entry.config(state='normal')
    Recipe_items_Entry.delete(1.0, END)
    #print(Recipe02_items)
    try:
        Recipe_items_Entry.insert(1.0 , f'1. {Recipe02_items[0]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(2.0 , f'2. {Recipe02_items[1]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(3.0 , f'3. {Recipe02_items[2]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(4.0 , f'4. {Recipe02_items[3]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(5.0 , f'5. {Recipe02_items[4]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(6.0 , f'6. {Recipe02_items[5]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(7.0 , f'7. {Recipe02_items[6]}\n')
    except:
        pass
    Recipe_items_Entry.config(state='disabled')

    Recipe02_cookingtime = Recipe02_values[2]
    Recipe_cookingtime_Entry.configure(text = Recipe02_cookingtime)
    #print(Recipe02_cookingtime)

    Recipe02_calories = Recipe02_values[3]
    Recipe_calories_Entry.configure(text = Recipe02_calories)
    #print(Recipe02_calories)

    Recipe02_servings = Recipe02_values[4]
    Recipe_servings_Entry.configure(text = Recipe02_servings)
    #print(Recipe02_servings)


    Recipe02_instruction = Recipe02_values[5]
    Recipe_inst_Entry.config(state='normal')
    Recipe_inst_Entry.delete(1.0, END)
    Recipe_inst_Entry.insert(1.0, Recipe02_instruction)
    Recipe_inst_Entry.config(state='disabled')
    # print(Recipe02_instruction)

    next_btn.configure(command=recipes3)

def recipes3():

    # pull data
    db = FirebaseConfig().firebase.database()

    Recipe03 = db.child("recipes").child("global").child("Recipe_03").get()
    Recipe03_data = Recipe03.val()
    Recipe03_values = list(Recipe03_data.values())

    Recipe03_name = Recipe03_values[0]
    Recipe_name_Entry.configure(text = Recipe03_name)
    # print(Recipe03_name)

    Recipe03_items = list(Recipe03_values[1].values())
    Recipe_items_Entry.config(state='normal')
    Recipe_items_Entry.delete(1.0, END)
    #print(Recipe03_items)
    try:
        Recipe_items_Entry.insert(1.0 , f'1. {Recipe03_items[0]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(2.0 , f'2. {Recipe03_items[1]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(3.0 , f'3. {Recipe03_items[2]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(4.0 , f'4. {Recipe03_items[3]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(5.0 , f'5. {Recipe03_items[4]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(6.0 , f'6. {Recipe03_items[5]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(7.0 , f'7. {Recipe03_items[6]}\n')
    except:
        pass
    Recipe_items_Entry.config(state='disabled')

    Recipe03_cookingtime = Recipe03_values[2]
    Recipe_cookingtime_Entry.configure(text = Recipe03_cookingtime)
    #print(Recipe03_cookingtime)

    Recipe03_calories = Recipe03_values[3]
    Recipe_calories_Entry.configure(text = Recipe03_calories)
    #print(Recipe03_calories)

    Recipe03_servings = Recipe03_values[4]
    Recipe_servings_Entry.configure(text = Recipe03_servings)
    #print(Recipe03_servings)


    Recipe03_instruction = Recipe03_values[5]
    Recipe_inst_Entry.config(state='normal')
    Recipe_inst_Entry.delete(1.0, END)
    Recipe_inst_Entry.insert(1.0, Recipe03_instruction)
    Recipe_inst_Entry.config(state='disabled')
    # print(Recipe03_instruction)

    next_btn.configure(command=recipes4)

def recipes4():

    # pull data
    db = FirebaseConfig().firebase.database()

    Recipe04 = db.child("recipes").child("global").child("Recipe_04").get()
    Recipe04_data = Recipe04.val()
    Recipe04_values = list(Recipe04_data.values())

    Recipe04_name = Recipe04_values[0]
    Recipe_name_Entry.configure(text = Recipe04_name)
    # print(Recipe04_name)

    Recipe04_items = list(Recipe04_values[1].values())
    Recipe_items_Entry.config(state='normal')
    Recipe_items_Entry.delete(1.0, END)
    #print(Recipe04_items)
    try:
        Recipe_items_Entry.insert(1.0 , f'1. {Recipe04_items[0]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(2.0 , f'2. {Recipe04_items[1]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(3.0 , f'3. {Recipe04_items[2]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(4.0 , f'4. {Recipe04_items[3]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(5.0 , f'5. {Recipe04_items[4]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(6.0 , f'6. {Recipe04_items[5]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(7.0 , f'7. {Recipe04_items[6]}\n')
    except:
        pass
    Recipe_items_Entry.config(state='disabled')

    Recipe04_cookingtime = Recipe04_values[2]
    Recipe_cookingtime_Entry.configure(text = Recipe04_cookingtime)
    #print(Recipe04_cookingtime)

    Recipe04_calories = Recipe04_values[3]
    Recipe_calories_Entry.configure(text = Recipe04_calories)
    #print(Recipe04_calories)

    Recipe04_servings = Recipe04_values[4]
    Recipe_servings_Entry.configure(text = Recipe04_servings)
    #print(Recipe04_servings)


    Recipe04_instruction = Recipe04_values[5]
    Recipe_inst_Entry.config(state='normal')
    Recipe_inst_Entry.delete(1.0, END)
    Recipe_inst_Entry.insert(1.0, Recipe04_instruction)
    Recipe_inst_Entry.config(state='disabled')
    # print(Recipe04_instruction)

    next_btn.configure(command=recipes5)

def recipes5():

    # pull data
    db = FirebaseConfig().firebase.database()

    Recipe05 = db.child("recipes").child("global").child("Recipe_05").get()
    Recipe05_data = Recipe05.val()
    Recipe05_values = list(Recipe05_data.values())

    Recipe05_name = Recipe05_values[0]
    Recipe_name_Entry.configure(text = Recipe05_name)
    # print(Recipe05_name)

    Recipe05_items = list(Recipe05_values[1].values())
    Recipe_items_Entry.config(state='normal')
    Recipe_items_Entry.delete(1.0, END)
    #print(Recipe05_items)
    try:
        Recipe_items_Entry.insert(1.0 , f'1. {Recipe05_items[0]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(2.0 , f'2. {Recipe05_items[1]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(3.0 , f'3. {Recipe05_items[2]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(4.0 , f'4. {Recipe05_items[3]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(5.0 , f'5. {Recipe05_items[4]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(6.0 , f'6. {Recipe05_items[5]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(7.0 , f'7. {Recipe05_items[6]}\n')
    except:
        pass
    Recipe_items_Entry.config(state='disabled')

    Recipe05_cookingtime = Recipe05_values[2]
    Recipe_cookingtime_Entry.configure(text = Recipe05_cookingtime)
    #print(Recipe05_cookingtime)

    Recipe05_calories = Recipe05_values[3]
    Recipe_calories_Entry.configure(text = Recipe05_calories)
    #print(Recipe05_calories)

    Recipe05_servings = Recipe05_values[4]
    Recipe_servings_Entry.configure(text = Recipe05_servings)
    #print(Recipe05_servings)


    Recipe05_instruction = Recipe05_values[5]
    Recipe_inst_Entry.config(state='normal')
    Recipe_inst_Entry.delete(1.0, END)
    Recipe_inst_Entry.insert(1.0, Recipe05_instruction)
    Recipe_inst_Entry.config(state='disabled')
    # print(Recipe05_instruction)

    next_btn.configure(command=recipes6)

def recipes6():

    # pull data
    db = FirebaseConfig().firebase.database()

    Recipe06 = db.child("recipes").child("global").child("Recipe_06").get()
    Recipe06_data = Recipe06.val()
    Recipe06_values = list(Recipe06_data.values())

    Recipe06_name = Recipe06_values[0]
    Recipe_name_Entry.configure(text = Recipe06_name)
    # print(Recipe06_name)

    Recipe06_items = list(Recipe06_values[1].values())
    Recipe_items_Entry.config(state='normal')
    Recipe_items_Entry.delete(1.0, END)
    #print(Recipe06_items)
    try:
        Recipe_items_Entry.insert(1.0 , f'1. {Recipe06_items[0]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(2.0 , f'2. {Recipe06_items[1]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(3.0 , f'3. {Recipe06_items[2]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(4.0 , f'4. {Recipe06_items[3]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(5.0 , f'5. {Recipe06_items[4]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(6.0 , f'6. {Recipe06_items[5]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(7.0 , f'7. {Recipe06_items[6]}\n')
    except:
        pass
    Recipe_items_Entry.config(state='disabled')

    Recipe06_cookingtime = Recipe06_values[2]
    Recipe_cookingtime_Entry.configure(text = Recipe06_cookingtime)
    #print(Recipe06_cookingtime)

    Recipe06_calories = Recipe06_values[3]
    Recipe_calories_Entry.configure(text = Recipe06_calories)
    #print(Recipe06_calories)

    Recipe06_servings = Recipe06_values[4]
    Recipe_servings_Entry.configure(text = Recipe06_servings)
    #print(Recipe06_servings)


    Recipe06_instruction = Recipe06_values[5]
    Recipe_inst_Entry.config(state='normal')
    Recipe_inst_Entry.delete(1.0, END)
    Recipe_inst_Entry.insert(1.0, Recipe06_instruction)
    Recipe_inst_Entry.config(state='disabled')
    # print(Recipe06_instruction)

    next_btn.configure(command=recipes7)

def recipes7():

    # pull data
    db = FirebaseConfig().firebase.database()

    Recipe07 = db.child("recipes").child("global").child("Recipe_07").get()
    Recipe07_data = Recipe07.val()
    Recipe07_values = list(Recipe07_data.values())

    Recipe07_name = Recipe07_values[0]
    Recipe_name_Entry.configure(text = Recipe07_name)
    # print(Recipe07_name)

    Recipe07_items = list(Recipe07_values[1].values())
    Recipe_items_Entry.config(state='normal')
    Recipe_items_Entry.delete(1.0, END)
    #print(Recipe07_items)
    try:
        Recipe_items_Entry.insert(1.0 , f'1. {Recipe07_items[0]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(2.0 , f'2. {Recipe07_items[1]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(3.0 , f'3. {Recipe07_items[2]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(4.0 , f'4. {Recipe07_items[3]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(5.0 , f'5. {Recipe07_items[4]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(6.0 , f'6. {Recipe07_items[5]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(7.0 , f'7. {Recipe07_items[6]}\n')
    except:
        pass
    Recipe_items_Entry.config(state='disabled')

    Recipe07_cookingtime = Recipe07_values[2]
    Recipe_cookingtime_Entry.configure(text = Recipe07_cookingtime)
    #print(Recipe07_cookingtime)

    Recipe07_calories = Recipe07_values[3]
    Recipe_calories_Entry.configure(text = Recipe07_calories)
    #print(Recipe07_calories)

    Recipe07_servings = Recipe07_values[4]
    Recipe_servings_Entry.configure(text = Recipe07_servings)
    #print(Recipe07_servings)


    Recipe07_instruction = Recipe07_values[5]
    Recipe_inst_Entry.config(state='normal')
    Recipe_inst_Entry.delete(1.0, END)
    Recipe_inst_Entry.insert(1.0, Recipe07_instruction)
    Recipe_inst_Entry.config(state='disabled')
    # print(Recipe07_instruction)

    next_btn.configure(command=recipes8)

def recipes8():

    # pull data
    db = FirebaseConfig().firebase.database()

    Recipe08 = db.child("recipes").child("global").child("Recipe_08").get()
    Recipe08_data = Recipe08.val()
    Recipe08_values = list(Recipe08_data.values())

    Recipe08_name = Recipe08_values[0]
    Recipe_name_Entry.configure(text = Recipe08_name)
    # print(Recipe08_name)

    Recipe08_items = list(Recipe08_values[1].values())
    Recipe_items_Entry.config(state='normal')
    Recipe_items_Entry.delete(1.0, END)
    #print(Recipe08_items)
    try:
        Recipe_items_Entry.insert(1.0 , f'1. {Recipe08_items[0]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(2.0 , f'2. {Recipe08_items[1]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(3.0 , f'3. {Recipe08_items[2]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(4.0 , f'4. {Recipe08_items[3]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(5.0 , f'5. {Recipe08_items[4]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(6.0 , f'6. {Recipe08_items[5]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(7.0 , f'7. {Recipe08_items[6]}\n')
    except:
        pass
    Recipe_items_Entry.config(state='disabled')

    Recipe08_cookingtime = Recipe08_values[2]
    Recipe_cookingtime_Entry.configure(text = Recipe08_cookingtime)
    #print(Recipe08_cookingtime)

    Recipe08_calories = Recipe08_values[3]
    Recipe_calories_Entry.configure(text = Recipe08_calories)
    #print(Recipe08_calories)

    Recipe08_servings = Recipe08_values[4]
    Recipe_servings_Entry.configure(text = Recipe08_servings)
    #print(Recipe08_servings)


    Recipe08_instruction = Recipe08_values[5]
    Recipe_inst_Entry.config(state='normal')
    Recipe_inst_Entry.delete(1.0, END)
    Recipe_inst_Entry.insert(1.0, Recipe08_instruction)
    Recipe_inst_Entry.config(state='disabled')
    # print(Recipe08_instruction)

    next_btn.configure(command=recipes9)

def recipes9():

    # pull data
    db = FirebaseConfig().firebase.database()

    Recipe09 = db.child("recipes").child("global").child("Recipe_09").get()
    Recipe09_data = Recipe09.val()
    Recipe09_values = list(Recipe09_data.values())

    Recipe09_name = Recipe09_values[0]
    Recipe_name_Entry.configure(text = Recipe09_name)
    # print(Recipe09_name)

    Recipe09_items = list(Recipe09_values[1].values())
    Recipe_items_Entry.config(state='normal')
    Recipe_items_Entry.delete(1.0, END)
    #print(Recipe09_items)
    try:
        Recipe_items_Entry.insert(1.0 , f'1. {Recipe09_items[0]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(2.0 , f'2. {Recipe09_items[1]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(3.0 , f'3. {Recipe09_items[2]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(4.0 , f'4. {Recipe09_items[3]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(5.0 , f'5. {Recipe09_items[4]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(6.0 , f'6. {Recipe09_items[5]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(7.0 , f'7. {Recipe09_items[6]}\n')
    except:
        pass
    Recipe_items_Entry.config(state='disabled')

    Recipe09_cookingtime = Recipe09_values[2]
    Recipe_cookingtime_Entry.configure(text = Recipe09_cookingtime)
    #print(Recipe09_cookingtime)

    Recipe09_calories = Recipe09_values[3]
    Recipe_calories_Entry.configure(text = Recipe09_calories)
    #print(Recipe09_calories)

    Recipe09_servings = Recipe09_values[4]
    Recipe_servings_Entry.configure(text = Recipe09_servings)
    #print(Recipe09_servings)


    Recipe09_instruction = Recipe09_values[5]
    Recipe_inst_Entry.config(state='normal')
    Recipe_inst_Entry.delete(1.0, END)
    Recipe_inst_Entry.insert(1.0, Recipe09_instruction)
    Recipe_inst_Entry.config(state='disabled')
    # print(Recipe09_instruction)

    next_btn.configure(command=recipes10)

def recipes10():

    # pull data
    db = FirebaseConfig().firebase.database()

    Recipe10 = db.child("recipes").child("global").child("Recipe_10").get()
    Recipe10_data = Recipe10.val()
    Recipe10_values = list(Recipe10_data.values())

    Recipe10_name = Recipe10_values[0]
    Recipe_name_Entry.configure(text = Recipe10_name)
    # print(Recipe10_name)

    Recipe10_items = list(Recipe10_values[1].values())
    Recipe_items_Entry.config(state='normal')
    Recipe_items_Entry.delete(1.0, END)
    #print(Recipe10_items)
    try:
        Recipe_items_Entry.insert(1.0 , f'1. {Recipe10_items[0]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(2.0 , f'2. {Recipe10_items[1]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(3.0 , f'3. {Recipe10_items[2]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(4.0 , f'4. {Recipe10_items[3]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(5.0 , f'5. {Recipe10_items[4]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(6.0 , f'6. {Recipe10_items[5]}\n')
    except:
        pass
    try:
        Recipe_items_Entry.insert(7.0 , f'7. {Recipe10_items[6]}\n')
    except:
        pass
    Recipe_items_Entry.config(state='disabled')

    Recipe10_cookingtime = Recipe10_values[2]
    Recipe_cookingtime_Entry.configure(text = Recipe10_cookingtime)
    #print(Recipe10_cookingtime)

    Recipe10_calories = Recipe10_values[3]
    Recipe_calories_Entry.configure(text = Recipe10_calories)
    #print(Recipe10_calories)

    Recipe10_servings = Recipe10_values[4]
    Recipe_servings_Entry.configure(text = Recipe10_servings)
    #print(Recipe10_servings)


    Recipe10_instruction = Recipe10_values[5]
    Recipe_inst_Entry.config(state='normal')
    Recipe_inst_Entry.delete(1.0, END)
    Recipe_inst_Entry.insert(1.0, Recipe10_instruction)
    Recipe_inst_Entry.config(state='disabled')
    # print(Recipe10_instruction)

    next_btn.configure(command=recipes1)
                    
def reset_settings():
    # this is for logging out/reset

    cleanup()
    List.delete(*List.get_children())
    aList.delete(*aList.get_children())

    NonPantryList.delete(*NonPantryList.get_children())
    aNonPantryList.delete(*aNonPantryList.get_children())

    ShoppingList.delete(*ShoppingList.get_children())
    aShoppingList.delete(*aShoppingList.get_children())

def deselect():
    # clear entry boxes
    # clear_entries()
    def deselect_all():
        # Iterate over all root-level items.
        for item in List.get_children():
            deselect_children(item)
        for item in NonPantryList.get_children():
            deselect_children(item)
        for item in ShoppingList.get_children():
            deselect_children(item)

    def deselect_children(item):
        # Deselect the current item.
        try:
            List.selection_remove(item)
        except:
            pass
        try:
            NonPantryList.selection_remove(item)
        except:
            pass
        try:
            ShoppingList.selection_remove(item)
        except:
            pass
    deselect_all()

def cleanup():
    clear_entries()
    deselect()

# Database Pulling Functions for all the lists
def refresh():

    try:
        clear_entries()
        List.delete(*List.get_children())
        aList.delete(*aList.get_children())
        query_database()
    except:
        pass
    try:
        NonPantryList.delete(*NonPantryList.get_children())
        aNonPantryList.delete(*aNonPantryList.get_children())
        query_database_non()
    except:
        pass
    try:
        ShoppingList.delete(*ShoppingList.get_children())
        aShoppingList.delete(*aShoppingList.get_children())
        query_database_shopping()
    except:
        pass

def query_database():
    # pull data
    db = FirebaseConfig().firebase.database()
    Items = db.child("pantry-items").child(user['localId']).get()
    for itemsData in Items.each():
        data = itemsData.val()
        datalist = list(data.values())
        # a = OptionsPantryList()
        List.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2],
                                        f'{int((int(datalist[5])/datalist[6])*100)}%',
                                        datalist[8]
                                        )
                    )

        aList.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2],
                                        f'{int((int(datalist[5])/datalist[6])*100)}%',
                                        datalist[8]
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
    barcode_entry.delete(0, END)
    update_button.place_forget()
    delete_button.place_forget()

    name_entry_non.delete(0, END)
    brand_entry_non.delete(0, END)
    exdate_entry_non.delete(0, END)
    oid_entry_non.delete(0, END)
    barcode_entry_non.delete(0, END)
    update_button_non.place_forget()
    delete_button_non.place_forget()

    name_entry_Shopping.delete(0, END)
    brand_entry_Shopping.delete(0, END)
    oid_entry_Shopping.delete(0, END)
    update_button_Shopping.place_forget()
    delete_button_Shopping.place_forget()

    deselect()

# Functions for Pantry Items
def select_record(e):
    # clear entry boxes
    name_entry.delete(0, END)
    brand_entry.delete(0, END)
    exdate_entry.delete(0, END)
    amount_entry.delete(0, END)
    oid_entry.delete(0, END)
    barcode_entry.delete(0, END)

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

    update_button.place(x=1260, y=220, anchor="e")

    delete_button.place(x=1260, y=290, anchor="e")

def add_record(): # adds data to the table (List)
    if name_entry.get()=="":
        messagebox.showerror("", "Item's data needed")
    elif amount_entry.get()=="":
        messagebox.showerror("", "You must add the current amount \nThis is for testing only")
    elif int(amount_entry.get())>1500:
        messagebox.showerror("", "The current amount cannot be greater than 1500 \nThis is for testing only")
    else:
        data =  {
                    'A_Name': name_entry.get(),
                    'B_Brand': brand_entry.get(),
                    'C_ExpirationDate': exdate_entry.get(),
                    'D_WeightPercentage':f'{int((int(amount_entry.get())/intitial_weight)*100)}%',
                    'E_ExpirationDateUnix': unix_time,
                    'F_CurrentWeight':amount_entry.get(),
                    'G_InitialWeight': intitial_weight,
                    'H_GridLocation': "1",
                }
        db = FirebaseConfig().firebase.database()
        db.child("pantry-items").child(user['localId']).push(data)

        Items = db.child("pantry-items").child(user['localId']).get()
        for itemsData in Items.each():
            if itemsData.val() == data:
                data =  {
                            'A_Name': name_entry.get(),
                            'B_Brand': brand_entry.get(),
                            'C_ExpirationDate': exdate_entry.get(),
                            'D_WeightPercentage':f'{int((int(amount_entry.get())/intitial_weight)*100)}%',
                            'E_ExpirationDateUnix': unix_time,
                            'F_CurrentWeight':amount_entry.get(),
                            'G_InitialWeight': intitial_weight,
                            'H_GridLocation': "1",
                            'I_ID': itemsData.key()
                        }
                db.child("pantry-items").child(user['localId']).child(itemsData.key()).update(data)

        # Clear the Treeview, clear entries, and pull database
        List.delete(*List.get_children())
        aList.delete(*aList.get_children())
        query_database()
        cleanup()

def update_record():
    if name_entry.get()=="":
        messagebox.showerror("", "Item's data needed")
    elif amount_entry.get()=="":
        messagebox.showerror("", "You must add the current amount \nThis is for testing only")
    elif int(amount_entry.get())>1500:
        messagebox.showerror("", "The current amount cannot be greater than 1500 \nThis is for testing only")
    else:
        db = FirebaseConfig().firebase.database()
        data =  {
                    'A_Name': name_entry.get(),
                    'B_Brand': brand_entry.get(),
                    'C_ExpirationDate': exdate_entry.get(),
                    'D_WeightPercentage':f'{int((int(amount_entry.get())/intitial_weight)*100)}%',
                    'E_ExpirationDateUnix': unix_time,
                    'F_CurrentWeight':amount_entry.get(),
                    'G_InitialWeight': intitial_weight,
                    'H_GridLocation': "1",
                    'I_ID': oid_entry.get()
                }
        db.child("pantry-items").child(user['localId']).child(oid_entry.get()).update(data)
        # Clear the Treeview, clear entries, and pull database
        List.delete(*List.get_children())
        aList.delete(*aList.get_children())

        query_database()
        cleanup()
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

            query_database()
            cleanup()

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
        cleanup()
        messagebox.showinfo ("", "Items Deleted!")

def barcode_scanner():
    if barcode_entry.get()=="":
        messagebox.showerror("", "Please scan an item first.")
    else:
        upc = barcode_entry.get()
        url ='https://api.upcitemdb.com/prod/trial/lookup?upc=%s' % (upc)
        try:
            response = requests.get(url)
            response.raise_for_status()

            upcData = json.loads(response.text)
            item_data = upcData['items']

            item_data_list = list(item_data[0].values())

            Item_name = item_data_list[1]
            name_entry.insert(0, Item_name)
            item_brand = item_data_list[4]
            brand_entry.insert(0, item_brand)
        except:
            messagebox.showerror("Text", "Item is not on the database\n" "Please use manually input instead")
            barcode_entry.delete(0, END)

        # print(f'#0 {item_data_list[0]}')
        # print(f'#1 {item_data_list[1]}')
        # print(f'#2 {item_data_list[2]}')
        # print(f'#3 {item_data_list[3]}')
        # print(f'#4 {item_data_list[4]}')
        # print(f'#5 {item_data_list[5]}')
        # print(f'#6 {item_data_list[6]}')
        # print(f'#7 {item_data_list[7]}')
        # print(f'#8 {item_data_list[8]}')

# Functions for Non-Pantry Items
def select_record_non(e):
    # clear entry boxes
    name_entry_non.delete(0, END)
    brand_entry_non.delete(0, END)
    exdate_entry_non.delete(0, END)

    # Grab record number
    selected = NonPantryList.focus()
    # Grab record VALUES
    values = NonPantryList.item(selected, "values")

    # output to entry boxes
    name_entry_non.insert(0, values[0])
    brand_entry_non.insert(0, values[1])
    exdate_entry_non.insert(0, values[2])
    oid_entry_non.insert(0, values[3])

    update_button_non.place(x=1260, y=220, anchor="e")
    delete_button_non.place(x=1260, y=290, anchor="e")

def add_record_non(): # adds data to the table (List)
    if name_entry_non.get()=="":
        messagebox.showerror("", "Item's data needed")
    else:
        data =  {'A_Name': name_entry_non.get(),
                'B_Brand': brand_entry_non.get(),
                'C_ExpirationDate': exdate_entry_non.get(),
                }
        db = FirebaseConfig().firebase.database()
        db.child("non-pantry-items").child(user['localId']).push(data)

        Items = db.child("non-pantry-items").child(user['localId']).get()
        for itemsData in Items.each():

            if itemsData.val() == data:
                data =  {'A_Name': name_entry_non.get(),
                        'B_Brand': brand_entry_non.get(),
                        'C_ExpirationDate': exdate_entry_non.get(),
                        'D_ID': itemsData.key(),
                        }
                db.child("non-pantry-items").child(user['localId']).child(itemsData.key()).update(data)

        # Clear the Treeview, clear entries, and pull database
        NonPantryList.delete(*NonPantryList.get_children())
        aNonPantryList.delete(*aNonPantryList.get_children())
        query_database_non()
        cleanup()

def update_record_non():
    db = FirebaseConfig().firebase.database()
    data =  {'A_Name': name_entry_non.get(),
            'B_Brand': brand_entry_non.get(),
            'C_ExpirationDate': exdate_entry_non.get(),
            'D_ID': oid_entry_non.get(),
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
            query_database_non()
            cleanup()

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
        cleanup()
        messagebox.showinfo ("", "Items Deleted!")

def barcode_scanner_non():
    if barcode_entry_non.get()=="":
        messagebox.showerror("", "Please scan an item first.")
    else:
        upc = barcode_entry_non.get()
        url ='https://api.upcitemdb.com/prod/trial/lookup?upc=%s' % (upc)
        try:
            response = requests.get(url)
            response.raise_for_status()

            upcData = json.loads(response.text)
            item_data = upcData['items']

            item_data_list = list(item_data[0].values())

            Item_name = item_data_list[1]
            name_entry_non.insert(0, Item_name)
            item_brand = item_data_list[4]
            brand_entry_non.insert(0, item_brand)
        except:
            messagebox.showerror("Text", "Item is not on the database\n" "Please use manually input instead")
            barcode_entry_non.delete(0, END)

# Functions for Shooping Items
def select_record_Shopping(e):
    # clear entry boxes
    oid_entry_non.delete(0, END)
    name_entry_Shopping.delete(0, END)
    brand_entry_Shopping.delete(0, END)
    oid_entry_Shopping.delete(0, END)

    # Grab record number
    selected = ShoppingList.focus()
    # Grab record VALUES
    values = ShoppingList.item(selected, "values")

    # output to entry boxes
    name_entry_Shopping.insert(0, values[0])
    brand_entry_Shopping.insert(0, values[1])
    oid_entry_Shopping.insert(0, values[2])

    update_button_Shopping.place(x=1260, y=220, anchor="e")

    delete_button_Shopping.place(x=1260, y=290, anchor="e")

def add_record_Shopping(): # adds data to the table (List)
    if name_entry_Shopping.get()=="":
        messagebox.showerror("", "Item's data needed")
    else:
        data =  {'A_Name': name_entry_Shopping.get(),
                'B_Brand': brand_entry_Shopping.get(),
                }
        db = FirebaseConfig().firebase.database()
        db.child("shopping-list").child(user['localId']).push(data)

        Items = db.child("shopping-list").child(user['localId']).get()
        for itemsData in Items.each():

            if itemsData.val() == data:
                data =  {'A_Name': name_entry_Shopping.get(),
                        'B_Brand': brand_entry_Shopping.get(),
                        'C_ID': itemsData.key(),
                        }
                db.child("shopping-list").child(user['localId']).child(itemsData.key()).update(data)

        # Clear the Treeview, clear entries, and pull database
        ShoppingList.delete(*ShoppingList.get_children())
        aShoppingList.delete(*aShoppingList.get_children())

        query_database_shopping()
        cleanup()

def update_record_Shopping():
    db = FirebaseConfig().firebase.database()
    data =  {'A_Name': name_entry_Shopping.get(),
            'B_Brand': brand_entry_Shopping.get(),
            'C_ID': oid_entry_Shopping.get(),
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

            query_database_shopping()
            cleanup()

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
        cleanup()
        messagebox.showinfo ("", "Items Deleted!")
