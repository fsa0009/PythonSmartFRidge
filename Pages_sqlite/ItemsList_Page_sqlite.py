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

        ## uncomment this to inser fake Database
        # fake_database()
        query_database()

        # Delete one Items Button
        delete_one_button = customtkinter.CTkButton(self, text= "Delete", command = delete_one_item, text_font=("TkHeadingtext_font", 20))
        delete_one_button.place(x=1260, y=150, anchor="e")

        # Delete Selected Items Button
        delete_selected_button = customtkinter.CTkButton(self, text= "Del multi", command = delete_multi_items, text_font=("TkHeadingtext_font", 20))
        delete_selected_button.place(x=1260, y=210, anchor="e")

        # Delete all Items Button
        delete_all_button = customtkinter.CTkButton(self, text = "Delete All", command = delete_all_items, text_font=("TkHeadingtext_font", 20))
        delete_all_button.place(x=1260, y=270, anchor="e")

        # Clear all Entry Boxes Button
        clear_button = customtkinter.CTkButton(self, text = "Clear Entry", command = clear_entries, text_font=("TkHeadingtext_font", 20), width = 180)
        clear_button.place(x=1260, y=550, anchor="e")

        # Update Items Button
        update_button = customtkinter.CTkButton(self, text = "Update Item", command = update_record, text_font=("TkHeadingtext_font", 20), width = 180)
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
        AddItems_page_button = customtkinter.CTkButton(self, text = "Add Items", text_font = ("TkHeadingtext_font", 25) , cursor = "hand2",
                width = 310, command = add_record)
        AddItems_page_button.place(x=475, y=655)

        customtkinter.CTkButton(self, text="Go Back", text_font = ("TkHeadingtext_font", 20) , cursor = "hand2",
                command = lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")

        # Bind the treeview
        List.bind("<ButtonRelease-1>", select_record)


# Functions for ItemsList Page
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

def add_record(): # adds the data to the table (List)
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
        query_database()

        clear_entries()

def update_record():
    # Update the database
    conn = sqlite3.connect('items_list.db')
    c = conn.cursor()

    c.execute(""" UPDATE items SET
        item_name = :name,
        brand_name = :brand,
        expiration_date = :exdate,
        remaining_amount = :amount

        where oid = :oid""",
        {
            'name': name_entry.get(),
            'brand': brand_entry.get(),
            'exdate': exdate_entry.get(),
            'amount': amount_entry.get(),
            'oid': oid_entry.get()
        })

    # Commit changes
    conn.commit()
    # Close our connection
    conn.close()

    # Clear the Treeview
    List.delete(*List.get_children())
    # Requiry
    query_database()

    clear_entries()

def delete_one_item(): # Delete one selected ITEM
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
            clear_entries()
            # Commit changes
            conn.commit()
            # Close our connection
            conn.close()
            #########################################################
            # Clear the Treeview
            List.delete(*List.get_children())
            # Requiry
            query_database()
            messagebox.showinfo ("", "Item Deleted!")

def delete_multi_items(): # Delete multiple selected ITEMS
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
            clear_entries()
            # Commit changes
            conn.commit()
            # Close our connection
            conn.close()
            #############################################################################
            # Clear the Treeview
            List.delete(*List.get_children())
            # Requiry
            query_database()
            messagebox.showinfo ("", "Item/s Deleted!")

def delete_all_items(): # Delets all items

    choice = messagebox.askquestion("Delete All Items", "Are you sure you want to delete ALL items?")

    if choice == 'yes':
        ############## Delete everything from the Database ##############
        conn = sqlite3.connect('items_list.db')
        c = conn.cursor()
        # Delete everything from the table

        c.execute("DROP TABLE items ")

        # clear entries
        clear_entries()
        # Commit changes
        conn.commit()
        # Close our connection
        conn.close()

        ##################################################################
        # Clear the Treeview
        List.delete(*List.get_children())
        # Recreate the Table
        create_after_drop()
        messagebox.showinfo ("", "Items Deleted!")

def create_after_drop():
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

def query_database():
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

def fake_database():
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
