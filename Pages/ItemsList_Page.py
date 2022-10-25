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
from Pages.Login_Page import FirebaseConfig

# Items List Page Class
class ItemsList(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller
        global List
        global count

        logo_img = ImageTk.PhotoImage(file="assets/images/WVU_Logo.png")
        logo_widget = customtkinter.CTkLabel(self, image=logo_img )
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=20)

        customtkinter.CTkLabel(self, text="List of Items" , text_font=("TkMenutext_font", 40)).place(x=493, y = 40)


        table_frame = customtkinter.CTkFrame(self,  highlightthickness=0, borderwidth=0, width=800, height=500)
        table_frame.place(relx=0.525, rely=0.53, anchor=tkinter.CENTER)

        # Define the headers/columns
        List_header = ["Name", "Brand", "Expiration Date", "Remaining"]
        # Creating Treeview List
        global List
        List = MyTreeview(table_frame, columns=List_header, show="headings")
        # positioning the Treeview List
        List.place(x=0, y=0, width = 735, height=420)
        # Tree View Scrollbar
        tree_Scroll = customtkinter.CTkScrollbar(table_frame, command=List.yview)
        tree_Scroll.place(x=737, y=0, height=420)
        List.configure(yscrollcommand=tree_Scroll.set)

        # Configure header/column
        List_ColWidth = [57, 53, 85, 69]
        List_ColAlignment = ["center", "center", "center", "center", "center"]
        # Define columns type for the "sort by" function
        List_SortType = ["name", "name", "date", "percentage"]
        # define the data data/rows
        List_data =[
            ["A", "C", "12-04-2022", "40%"],
            ["B", "A", "12-06-2022", "60%"],
            ["C", "D", "12-01-2022", "20%"],
            ["D", "B", "12-02-2022", "30%"],
            ["E", "F", "12-05-2022", "50%"],
            ["F", "E", "12-03-2022", "100%"]
            ]

        # Adding the headers with the "sort by" function
        for record in range(len(List_header)):
            strHdr = List_header[record]
            List.heading(strHdr, text=strHdr.title(), sort_by=List_SortType[record])
            List.column(List_header[record], width=List_ColWidth[record], stretch=True, anchor=List_ColAlignment[record])
        # Inserting the data
        for record in range(len(List_data)):
            List.insert("", "end", values=List_data[record])
            # FirebaseConfig().pushdb(record)

        # Delete Selected Items Button
        delete_selected_button = customtkinter.CTkButton(self, text= "Delete", command = List_delete_selected, text_font=("TkHeadingtext_font", 20))
        delete_selected_button.place(x=1260, y=150, anchor="e")

        # Delete all Items Button
        delete_all_button = customtkinter.CTkButton(self, text = "Delete All", command=List_delete_all, text_font=("TkHeadingtext_font", 20))
        delete_all_button.place(x=1260, y=210, anchor="e")

        # AddItems Page Button
        AddItems_page_button = customtkinter.CTkButton(self, text= "Add Items",text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                width =310, command=lambda:controller.show_frame("AddItems"))
        AddItems_page_button.place(x=475, y=655)

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")


# Add Items Page Class
class AddItems(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        global name_entry
        global brand_entry
        global exdate_entry
        global remain_entry

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

        # remain_entry = customtkinter.CTkEntry(Design_frame1, text_font=("yu gothic ui", 15))
        # remain_entry.grid(row=1, column=3)
        # remain_entry.bind('<FocusIn>', controller.entry_callback)

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
        add_record_button = customtkinter.CTkButton(self, text= "Add",text_font=("TkHeadingtext_font", 25) ,  cursor="hand2",
                width =310, command = add_record)
        add_record_button.place(x=475, y=655)
        # The Back Button
        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20)  , cursor="hand2",
                command=lambda:controller.show_frame("ItemsList")
            ).place(x=1260, y=700, anchor="se")


def List_delete_all(): # Delets all items
    for values in List.get_children():
        List.delete(values)

def List_delete_selected(): # Delete multiple selected ITEMS
    List_selected = List.selection()
    for values in List_selected:
        List.delete(values)

def add_record(): # adds the data to the table (List)
    List.insert("", "end", values=(name_entry.get(), brand_entry.get(), exdate_entry.get()))
    name_entry.delete(0, END)
    brand_entry.delete(0, END)
    exdate_entry.delete(0, END)


# Sort By Class
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
