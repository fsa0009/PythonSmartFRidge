from Pages import *
from Pages.Shopping import query_database_shopping
from Tools.Firebase import FirebaseConfig
import threading
import serial
import time
import re

global runningCurrentThreadBool

runningCurrentThreadBool = False

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
        aList.configure(yscrollcommand=tree_Scroll.set, selectmode="none")

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

        # amount_label = customtkinter.CTkLabel(self, text = "Amount: ", text_font=("TkHeadingtext_font", 18, "bold"), text_color = ("#1e3d6d", "#ebe7e4"))
        # amount_label.place(x=825, y=600, anchor="e")
        amount_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 200, justify = CENTER)
        #amount_entry.place(x=1007, y=600, anchor="e")
        barcode_entry = customtkinter.CTkEntry(self, text_font=("TkHeadingtext_font", 20), width = 150, justify = CENTER)
        barcode_entry.place(x=1190, y=430, anchor="e")

        # AddItems Page customtkinter.CTkButton
        #AddItems_button = customtkinter.CTkButton(self, image=add_image,  text="", width=60, height=60, corner_radius=10,  command = lambda: threading.Thread(target=add_record).start())
        AddItems_button = customtkinter.CTkButton(self, image=add_image,  text="", width=60, height=60, corner_radius=10,  command = lambda : threading.Thread(target= add_record).start())
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



# Functions for Pantry Items
# def query_database(accountid):
#     global UserID
#     UserID = accountid
#
#     # pull data
#     for item in List.get_children():
#         List.delete(item)
#
#     for item in aList.get_children():
#         aList.delete(item)
#
#     #List.delete(List.get_children())
#     #aList.delete(aList.get_children())
#
#
#
#     db = FirebaseConfig().firebase.database()
#     Items = db.child("pantry-items").child(accountid).get()
#     for itemsData in Items.each():
#         data = itemsData.val()
#         datalist = list(data.values())
#
#         Amount_Percentage  = int((int(datalist[5])/datalist[6])*100)
#         ExpirationDay = datetime.datetime.strptime(datalist[2],"%m/%d/%Y").date()
#         Today = date.today()
#
#         List.tag_configure('low and expired', background = "red")
#         List.tag_configure('normal', background = "")
#         List.tag_configure('low', background = "yellow")
#         List.tag_configure('expired', background = "red")
#
#         aList.tag_configure('low and expired', background = "red")
#         aList.tag_configure('normal', background = "")
#         aList.tag_configure('low', background = "yellow")
#         aList.tag_configure('expired', background = "red")
#
#
#
#
#         my_tag = 'normal'
#
#         my_tag = 'low and expired'  if Amount_Percentage<=20 and ExpirationDay<Today else 'normal'
#
#         my_tag = 'expired'  if ExpirationDay<Today else 'normal'
#
#         my_tag = 'low'  if Amount_Percentage<=20 else 'normal'
#
#
#
#         List.insert("", "end", values=(
#                                         datalist[0],
#                                         datalist[1],
#                                         datalist[2],
#                                         f'{Amount_Percentage}%',
#                                         datalist[8]
#                                         ),
#                                         tags=my_tag
#                     )
#
#         aList.insert("", "end", values=(
#                                         datalist[0],
#                                         datalist[1],
#                                         datalist[2],
#                                         f'{Amount_Percentage}%',
#                                         datalist[8]
#                                         ),
#                                         tag=my_tag
#                     )
#         query_database_shopping(accountid)

def query_database(accountid):
    global UserID
    UserID = accountid

    # Clearing List
    for item in List.get_children():
        List.delete(item)
    for item in aList.get_children():
        aList.delete(item)
    # pull data
    db = FirebaseConfig().firebase.database()
    Items = db.child("pantry-items").child(accountid).get()
    for itemsData in Items.each():
        data = itemsData.val()
        datalist = list(data.values())

        Amount_Percentage  = int((int(datalist[5])/int(datalist[6]))*100)
        ExpirationDay = datetime.datetime.strptime(datalist[2],"%m/%d/%Y").date()
        Today = date.today()

        List.tag_configure('LowExpired', background = "red")
        List.tag_configure('normal', background = "")
        List.tag_configure('low', background = "Orange")
        List.tag_configure('expired', background = "red")

        aList.tag_configure('LowExpired', background = "red")
        aList.tag_configure('normal', background = "")
        aList.tag_configure('low', background = "Orange")
        aList.tag_configure('expired', background = "red")

        if Amount_Percentage<=20 and ExpirationDay<Today:
            my_tag = 'LowExpired'

        elif ExpirationDay<Today:
            my_tag = 'expired'

        elif Amount_Percentage<=20:
            my_tag = 'low'

        else:
            my_tag = 'normal'

        List.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2],
                                        f'{Amount_Percentage}%',
                                        datalist[8]
                                        ),
                                        tags=my_tag
                    )

        aList.insert("", "end", values=(
                                        datalist[0],
                                        datalist[1],
                                        datalist[2],
                                        f'{Amount_Percentage}%',
                                        datalist[8]
                                        ),
                                        tag=my_tag
                    )
        query_database_shopping(accountid)

def add_record(): # adds data to the table (List)
    if name_entry.get()=="":
        messagebox.showerror("", "Item's data needed")
    else:
        # Killing  Arduino_Current
        try:
            #Arduino_Current.close()
            print("commented out")
        except:
            print("killing Arduino_Current failed")

        #threading.Thread(target=Initial_Weight).start()
        Initial_Weight()
        data =  {
                    'A_Name': name_entry.get(),
                    'B_Brand': brand_entry.get(),
                    'C_ExpirationDate': exdate_entry.get(),
                    'D_WeightPercentage':f'{int((InitialWeight/InitialWeight)*100)}%',
                    'E_ExpirationDateUnix': unix_time,
                    'F_CurrentWeight':InitialWeight,
                    'G_InitialWeight': InitialWeight,
                    'H_GridLocation': sensorLocation,
                }
        db = FirebaseConfig().firebase.database()
        db.child("pantry-items").child(UserID).child("sensor_" + sensorLocation).set(data)

        Items = db.child("pantry-items").child(UserID).get()
        for itemsData in Items.each():
            if itemsData.val() == data:
                key = itemsData.key()
                data =  {
                            'I_ID': itemsData.key()
                        }
                db.child("pantry-items").child(UserID).child(itemsData.key()).update(data)

        if barcode_entry.get()!="":
            datacode =  {
                            'A_Name': name_entry.get(),
                            'B_Brand': brand_entry.get()
                        }
            db.child("scanned").child("global").child(barcode_entry.get()).set(datacode)

        else:
            pass
        # Clear the Treeview, clear entries, and pull database
        #List.delete(*List.get_children())
        #aList.delete(*aList.get_children())
        query_database(UserID)

        #start_current_thread()
        threading.Thread(target=Current_Weight()).start()
        #cleanup()

def select_record(e):
    try:
        # clear entry boxes
        name_entry.delete(0, END)
        brand_entry.delete(0, END)
        exdate_entry.delete(0, END)
        #amount_entry.delete(0, END)
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
    except:
        pass

def update_record():
    if name_entry.get()=="":
        messagebox.showerror("", "Item's data needed")
    else:
        db = FirebaseConfig().firebase.database()
        data =  {
                    'A_Name': name_entry.get(),
                    'B_Brand': brand_entry.get(),
                    'C_ExpirationDate': exdate_entry.get(),
                    'E_ExpirationDateUnix': unix_time,
                }
        db.child("pantry-items").child(UserID).child(oid_entry.get()).update(data)
        # Clear the Treeview, clear entries, and pull database
        List.delete(*List.get_children())
        aList.delete(*aList.get_children())

        query_database(UserID)
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
            Items = db.child("pantry-items").child(UserID).child(oid_entry.get()).remove()

            #########################################################

            # Clear the Treeview, clear entries, and pull database
            List.delete(*List.get_children())
            aList.delete(*aList.get_children())

            query_database(UserID)
            cleanup()

def delete_all_items(): # Delets all ITEMS

    choice = messagebox.askquestion("Delete All Items", "Are you sure you want to delete ALL items?")

    if choice == 'yes':
        ############## Delete item from  Database ##############

        db = FirebaseConfig().firebase.database()
        Items = db.child("pantry-items").child(UserID).get()
        for itemsData in Items.each():
            db.child("pantry-items").child(UserID).child(itemsData.key()).remove()

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
        #try:
        db = FirebaseConfig().firebase.database()
        Items = db.child("scanned").child("global").get()
        for barcode in Items.each():
            keys = barcode.key()
        if upc in keys:
                database = db.child("scanned").child("global").child(upc).get()
                data = database.val()
                datalist = list(data.values())
                Item_name = datalist[0]
                name_entry.insert(0, Item_name)
                item_brand = datalist[1]
                brand_entry.insert(0, item_brand)

        elif upc not in keys:
                    # Use the universal database
                    # itemsData.val()['C_barcode']!=upc:
                response = requests.get(url)
                response.raise_for_status()

                upcData = json.loads(response.text)
                item_data = upcData['items']

                item_data_list = list(item_data[0].values())

                Item_name = item_data_list[1]
                name_entry.insert(0, Item_name)
                item_brand = item_data_list[4]
                brand_entry.insert(0, item_brand)
        else:
            messagebox.showerror("Text", "Item is not on the database\n" "Please use manually input instead")
            barcode_entry.delete(0, END)


# Clean Up Functions
def clear_entries():

    name_entry.delete(0, END)
    brand_entry.delete(0, END)
    exdate_entry.delete(0, END)
    amount_entry.delete(0, END)
    oid_entry.delete(0, END)
    barcode_entry.delete(0, END)
    update_button.place_forget()
    delete_button.place_forget()

    deselect()

def deselect():
    def deselect_all():
        # Iterate over all root-level items.
        for item in List.get_children():
            deselect_children(item)

    def deselect_children(item):
        # Deselect the current item.
        try:
            List.selection_remove(item)
        except:
            pass

    deselect_all()

def cleanup():
    clear_entries()
    deselect()

def empty_pantry():
    List.delete(*List.get_children())
    aList.delete(*aList.get_children())

def Current_Weight():

    global Arduino_Weight
    #print(runningCurrentThreadBool , "its false now ")
    #Boolean = True
    print(Boolean, "its true  now ")
    if (Boolean) :
        Arduino_Weight = serial.Serial('COM4' , 57600)
        db = FirebaseConfig().firebase.database()
        count = 0

        Items = db.child("pantry-items").child(UserID).shallow().get()
        try :
            URLs = list(Items.val())
        except:
            URLs = ""

        while True:
            if Arduino_Weight.inWaiting()>0:
                count += 1
                Reading_Weight = Arduino_Weight.readline().decode('ISO-8859-1')
                Weight_List = Reading_Weight.split()

                if len(Weight_List) == 3 :

                    result1 = re.sub(r'[^0-9.]', '', Weight_List[0])
                    CurrentWeight1 = int(result1)

                    result2 = re.sub(r'[^0-9.]', '', Weight_List[1])
                    CurrentWeight2 = int(result2)

                    result3 = re.sub(r'[^0-9.]', '', Weight_List[2])
                    CurrentWeight3 = int(result3)

                    #CurrentWeight1 = int((Weight_List[0]))
                    #CurrentWeight2 = int((Weight_List[1]))
                if count == 5:
                    Arduino_Weight.flush()
                    break

        print(CurrentWeight1 ,  "weight 1 current weight func")
        print(CurrentWeight2 ,  "weight 2 current weight func")
        print(CurrentWeight3 ,  "weight 3 current weight func")
        print(URLs, "this is urls")

        if "sensor_1" in URLs:

            Items = db.child("pantry-items").child(UserID).child("sensor_1").get()
            try:
                G_InitialWeight1 = Items.val()["G_InitialWeight"]
                print(G_InitialWeight1)

                data =  {
                            'D_WeightPercentage':f'{int((CurrentWeight1/G_InitialWeight1)*100)}%',
                            'F_CurrentWeight':CurrentWeight1
                        }
                db.child("pantry-items").child(UserID).child("sensor_1").update(data)


                ItemsDict = Items.val()
                ItemsValues = ItemsDict.values()
                ItemsList = list(ItemsValues)
                PreWeight = ItemsList[5]
                print("we are insside sensor 1")

                if PreWeight < CurrentWeight1-10 or PreWeight > CurrentWeight1+10  :
                    #List.delete(List.get_children())
                    #aList.delete(aList.get_children())
                    query_database(UserID)
                else:
                    pass

            except:
                pass
        if "sensor_2" in URLs:


            Items = db.child("pantry-items").child(UserID).child("sensor_2").get()
            try:
                G_InitialWeight2 = Items.val()["G_InitialWeight"]
            except:
                pass
            #print(G_InitialWeight1)


            Items = db.child("pantry-items").child(UserID).child("sensor_2").get()
            data =  {
                        'D_WeightPercentage':f'{int((CurrentWeight2/G_InitialWeight2)*100)}%',
                        'F_CurrentWeight':CurrentWeight2
                    }
            db.child("pantry-items").child(UserID).child("sensor_2").update(data)

            ItemsDict = Items.val()
            ItemsValues = ItemsDict.values()
            ItemsList = list(ItemsValues)
            PreWeight = ItemsList[5]
            print("we are insside sensor 2")

            if PreWeight < CurrentWeight2-10 or PreWeight > CurrentWeight2+10:
                #List.delete(List.get_children())
                #aList.delete(aList.get_children())
                query_database(UserID)
            else:
                pass

        if "sensor_3" in URLs:


            Items = db.child("pantry-items").child(UserID).child("sensor_3").get()

            G_InitialWeight3 = Items.val()["G_InitialWeight"]
            #print(G_InitialWeight1)


            Items = db.child("pantry-items").child(UserID).child("sensor_3").get()
            data =  {
                        'D_WeightPercentage':f'{int((CurrentWeight3/G_InitialWeight3)*100)}%',
                        'F_CurrentWeight':CurrentWeight3
                    }
            db.child("pantry-items").child(UserID).child("sensor_3").update(data)

            ItemsDict = Items.val()
            ItemsValues = ItemsDict.values()
            ItemsList = list(ItemsValues)
            PreWeight = ItemsList[5]
            print("we are insside sensor 3")

            if PreWeight < CurrentWeight3-10 or PreWeight > CurrentWeight3+10:
                #List.delete(List.get_children())
                #aList.delete(aList.get_children())
                query_database(UserID)

        #time.sleep(2)
        #Arduino_Current.close()
        Arduino_Weight.close()

    #print("conflict with initial weight function")
    # time.sleep(2)
    Current_Weight()

# Sensors Functions:
def Initial_Weight():
    #global Arduino_Weight
    try :

        Arduino_Weight.close()
    except :
        pass


    global starter
    starter = 0
    global InitialWeight
    global sensorLocation
    global InitialWeight1
    global InitialWeight2
    global InitialWeight3

    global Boolean
    Boolean = False
    if Boolean == False :
        Arduino = serial.Serial('COM4' , 57600)

        InitialWeight = None
        count = 0

        db = FirebaseConfig().firebase.database()

        Items = db.child("pantry-items").child(UserID).shallow().get()

        try :
            URLs = list(Items.val())
        except:
            URLs = ""

        while True:
            if Arduino.inWaiting()>0:
                count += 1
                Reading_Weight = Arduino.readline().decode('ISO-8859-1')
                Weight_List = Reading_Weight.split()

                if len(Weight_List) == 3 :
                    InitialWeight1 = int((Weight_List[0])) +1
                    InitialWeight2 = int((Weight_List[1]))+ 1
                    InitialWeight3 = int((Weight_List[2]))+ 1

                    if InitialWeight1 > 0+30  and "sensor_1" not in URLs :
                        if count == 5:
                            # print("Cell 1 initial Weight:")
                            print(f'{InitialWeight1} grams in sensor 1 (Initial Weight Func)')
                            print(f'{InitialWeight2} grams in sensor 2 (Initial Weight Func)')
                            print(f'{InitialWeight3} grams in sensor 3 (Initial Weight Func)')
                            InitialWeight = InitialWeight1
                            sensorLocation = "1"
                            Arduino.flush()
                            break

                    if InitialWeight2 > 0+30 and  "sensor_2" not in URLs :
                        if count == 5:
                            # print("Cell 1 initial Weight:")
                            print(f'{InitialWeight1} grams in sensor 1 (Initial Weight Func)')
                            print(f'{InitialWeight2} grams in sensor 2 (Initial Weight Func)')
                            print(f'{InitialWeight3} grams in sensor 3 (Initial Weight Func)')
                            InitialWeight = InitialWeight2
                            sensorLocation = "2"
                            Arduino.flush()
                            break

                    if InitialWeight3 > 0+30 and  "sensor_3" not in URLs :
                        if count == 5:
                            # print("Cell 3 initial Weight:")
                            print(f'{InitialWeight1} grams in sensor 1 (Initial Weight Func)')
                            print(f'{InitialWeight2} grams in sensor 2 (Initial Weight Func)')
                            print(f'{InitialWeight3} grams in sensor 3 (Initial Weight Func)')
                            InitialWeight = InitialWeight3
                            sensorLocation = "3"
                            Arduino.flush()
                            break
    starter +=1
    Arduino.close()
    # time.sleep(2)
    Boolean = True
    #currentThread = threading.Thread(target= Current_Weight()).start()
    #Current_Weight()

def start_current_thread():
    #pass
    global currentThread
    currentThread = threading.Thread(target= Current_Weight())
    try:
        time.sleep(5)
        if starter > 0:
            currentThread.start()
            print("we aren  in try ")
    except:
        print("starting current threadfailed")
