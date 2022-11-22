from Pages import *
from Tools.Firebase import FirebaseConfig


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



# Functions for Shooping Items
def query_database_shopping(accountid):
    empty_shopping()
    global UserID
    UserID = accountid
    # pull data
    db = FirebaseConfig().firebase.database()
    Items = db.child("shopping-list").child(accountid).get()
    try:
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
    except:
        pass
    try:
        generate_shopping()
    except:
        pass

def generate_shopping():
    db = FirebaseConfig().firebase.database()

    # Checking Low/Expired Items from Pantry List
    Items = db.child("pantry-items").child(UserID).get()
    try:
        for itemsData in Items.each():
            data = itemsData.val()
            datalist = list(data.values())

            Amount_Percentage  = int((int(datalist[5])/datalist[6])*100)
            ExpirationDay = datetime.datetime.strptime(datalist[2],"%m/%d/%Y").date()
            Today = date.today()

            my_tag = 'low' if Amount_Percentage<=20 or ExpirationDay<Today else 'normal'

            if my_tag == 'low':
                ShoppingList.insert("", "end", values=(
                                                datalist[0],
                                                datalist[1],
                                                datalist[8]
                                                )
                            )
                aShoppingList.insert("", "end", values=(
                                    datalist[0],
                                    datalist[1],
                                    datalist[8]
                                    )
                )
    except:
        pass
    try:
        # Checking Expired Items from Non Pantry List
        Items = db.child("non-pantry-items").child(UserID).get()
        for itemsData in Items.each():
            data = itemsData.val()
            datalist = list(data.values())

            ExpirationDay = datetime.datetime.strptime(datalist[2],"%m/%d/%Y").date()
            Today = date.today()

            my_tag = 'low' if ExpirationDay<Today else 'normal'

            if my_tag == 'low':
                ShoppingList.insert("", "end", values=(
                                                datalist[0],
                                                datalist[1],
                                                datalist[3]
                                                )
                            )
                aShoppingList.insert("", "end", values=(
                                    datalist[0],
                                    datalist[1],
                                    datalist[3]
                                    )
                )
    except:
        pass

def add_record_Shopping(): # adds data to the table (List)
    if name_entry_Shopping.get()=="":
        messagebox.showerror("", "Item's data needed")
    else:
        data =  {'A_Name': name_entry_Shopping.get(),
                'B_Brand': brand_entry_Shopping.get(),
                }
        db = FirebaseConfig().firebase.database()
        db.child("shopping-list").child(UserID).push(data)

        Items = db.child("shopping-list").child(UserID).get()
        for itemsData in Items.each():

            if itemsData.val() == data:
                data =  {'A_Name': name_entry_Shopping.get(),
                        'B_Brand': brand_entry_Shopping.get(),
                        'C_ID': itemsData.key(),
                        }
                db.child("shopping-list").child(UserID).child(itemsData.key()).update(data)

        # Clear the Treeview, clear entries, and pull database
        ShoppingList.delete(*ShoppingList.get_children())
        aShoppingList.delete(*aShoppingList.get_children())

        query_database_shopping(UserID)
        cleanup()

def select_record_Shopping(e):
    try:
        # clear entry boxes
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
    except:
        pass

def update_record_Shopping():
    db = FirebaseConfig().firebase.database()
    data =  {'A_Name': name_entry_Shopping.get(),
            'B_Brand': brand_entry_Shopping.get(),
            'C_ID': oid_entry_Shopping.get(),
            }
    db.child("shopping-list").child(UserID).child(oid_entry_Shopping.get()).update(data)
    # Clear the Treeview, clear entries, and pull database
    ShoppingList.delete(*ShoppingList.get_children())
    aShoppingList.delete(*aShoppingList.get_children())
    clear_entries()
    query_database_shopping(UserID)
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
            Items = db.child("shopping-list").child(UserID).child(oid_entry_Shopping.get()).remove()

            #########################################################

            # Clear the Treeview, clear entries, and pull database
            ShoppingList.delete(*ShoppingList.get_children())
            aShoppingList.delete(*aShoppingList.get_children())

            query_database_shopping(UserID)
            cleanup()

def delete_all_Shopping(): # Delets all ITEMS

    choice = messagebox.askquestion("Delete All Items", "Are you sure you want to delete ALL items?")

    if choice == 'yes':
        ############## Delete item from  Database ##############

        db = FirebaseConfig().firebase.database()
        Items = db.child("shopping-list").child(UserID).get()
        for itemsData in Items.each():
            db.child("shopping-list").child(UserID).child(itemsData.key()).remove()

        #########################################################

        # Clear the Treeview, clear entries, and pull database
        ShoppingList.delete(*ShoppingList.get_children())
        aShoppingList.delete(*aShoppingList.get_children())
        cleanup()
        messagebox.showinfo ("", "Items Deleted!")


# Clean Up Functions
def deselect():
    # clear entry boxes
    # clear_entries()
    def deselect_all():
        # Iterate over all root-level items.
        
        for item in ShoppingList.get_children():
            deselect_children(item)

    def deselect_children(item):
        # Deselect the current item.
        try:
            ShoppingList.selection_remove(item)
        except:
            pass
    deselect_all()

def cleanup():
    clear_entries()
    deselect()

def clear_entries():

    name_entry_Shopping.delete(0, END)
    brand_entry_Shopping.delete(0, END)
    oid_entry_Shopping.delete(0, END)
    update_button_Shopping.place_forget()
    delete_button_Shopping.place_forget()

    deselect()

def empty_shopping():
    ShoppingList.delete(*ShoppingList.get_children())
    aShoppingList.delete(*aShoppingList.get_children())