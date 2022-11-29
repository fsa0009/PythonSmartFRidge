from Pages import *
from Pages.Shopping import query_database_shopping
from Tools.Firebase import FirebaseConfig


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



# Functions for Non-Pantry Items
def query_database_non(accountid):
    global UserID
    UserID = accountid
    # pull data
    db = FirebaseConfig().firebase.database()
    Items = db.child("non-pantry-items").child(accountid).get()
    for itemsData in Items.each():
        data = itemsData.val()
        datalist = list(data.values())

        ExpirationDay = datetime.datetime.strptime(datalist[2],"%m/%d/%Y").date()
        Today = date.today()

        NonPantryList.tag_configure('expired', background = "red")
        NonPantryList.tag_configure('normal', background = "")

        aNonPantryList.tag_configure('expired', background = "red")
        aNonPantryList.tag_configure('normal', background = "")

        my_tag = 'normal'
        my_tag = 'expired' if ExpirationDay<Today else 'normal'

        NonPantryList.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2],
                                        datalist[3]
                                        ),
                                        tags=my_tag
                    )
        aNonPantryList.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2],
                                        datalist[3]
                                        ),
                                        tags=my_tag
                    )

        NonPantryList.tag_configure('low', background = "red")
        NonPantryList.tag_configure('normal', background = "")

        aNonPantryList.tag_configure('low', background = "red")
        aNonPantryList.tag_configure('normal', background = "")

        query_database_shopping(accountid)

def add_record_non(): # adds data to the table (List)
    if name_entry_non.get()=="":
        messagebox.showerror("", "Item's data needed")
    else:
        data =  {'A_Name': name_entry_non.get(),
                'B_Brand': brand_entry_non.get(),
                'C_ExpirationDate': exdate_entry_non.get(),
                }
        db = FirebaseConfig().firebase.database()
        db.child("non-pantry-items").child(UserID).push(data)

        Items = db.child("non-pantry-items").child(UserID).get()
        for itemsData in Items.each():

            if itemsData.val() == data:
                data =  {'A_Name': name_entry_non.get(),
                        'B_Brand': brand_entry_non.get(),
                        'C_ExpirationDate': exdate_entry_non.get(),
                        'D_ID': itemsData.key(),
                        }
                db.child("non-pantry-items").child(UserID).child(itemsData.key()).update(data)

        # Clear the Treeview, clear entries, and pull database
        NonPantryList.delete(*NonPantryList.get_children())
        aNonPantryList.delete(*aNonPantryList.get_children())
        query_database_non(UserID)
        cleanup()

def select_record_non(e):
    try:
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
    except:
        pass

def update_record_non():
    db = FirebaseConfig().firebase.database()
    data =  {'A_Name': name_entry_non.get(),
            'B_Brand': brand_entry_non.get(),
            'C_ExpirationDate': exdate_entry_non.get(),
            'D_ID': oid_entry_non.get(),
            }
    db.child("non-pantry-items").child(UserID).child(oid_entry_non.get()).update(data)
    # Clear the Treeview, clear entries, and pull database
    NonPantryList.delete(*NonPantryList.get_children())
    aNonPantryList.delete(*aNonPantryList.get_children())

    query_database_non(UserID)
    cleanup()
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
            Items = db.child("non-pantry-items").child(UserID).child(oid_entry_non.get()).remove()

            #########################################################

            # Clear the Treeview, clear entries, and pull database
            NonPantryList.delete(*NonPantryList.get_children())
            aNonPantryList.delete(*aNonPantryList.get_children())
            try:
                query_database_non(UserID)
            except:
                pass
            cleanup()

def delete_all_non(): # Delets all ITEMS

    choice = messagebox.askquestion("Delete All Items", "Are you sure you want to delete ALL items?")

    if choice == 'yes':
        ############## Delete item from  Database ##############

        db = FirebaseConfig().firebase.database()
        Items = db.child("non-pantry-items").child(UserID).get()
        for itemsData in Items.each():
            db.child("non-pantry-items").child(UserID).child(itemsData.key()).remove()

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


# Clean Up Functions
def deselect():
    def deselect_all():
        # Iterate over all root-level items.
        for item in NonPantryList.get_children():
            deselect_children(item)

    def deselect_children(item):
        # Deselect the current item.
        try:
            NonPantryList.selection_remove(item)
        except:
            pass
    deselect_all()

def cleanup():
    clear_entries()
    deselect()
    
def clear_entries():
    name_entry_non.delete(0, END)
    brand_entry_non.delete(0, END)
    exdate_entry_non.delete(0, END)
    oid_entry_non.delete(0, END)
    barcode_entry_non.delete(0, END)
    update_button_non.place_forget()
    delete_button_non.place_forget()
    deselect()

def empty_nonpantry():
    NonPantryList.delete(*NonPantryList.get_children())
    aNonPantryList.delete(*aNonPantryList.get_children())
