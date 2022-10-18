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


class SuggestedShopping(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller

        global ShoppingList

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
        delete_selected_button = customtkinter.CTkButton(self, text= "Delete", command = ShoppingList_delete_selected, text_font=("TkHeadingtext_font", 20))
        delete_selected_button.place(x=1260, y=150, anchor="e")

        # Delete all Items customtkinter.CTkButton
        delete_all_button = customtkinter.CTkButton(self, text = "Delete All", command=ShoppingList_delete_all, text_font=("TkHeadingtext_font", 20))
        delete_all_button.place(x=1260, y=210, anchor="e")

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(x=1260, y=700, anchor="se")

        def ShoppingList_add_popup(): # add item pop up
            pop = customtkinter.CTkToplevel()
            pop.title("Add items to your Shopping list")
            pop.geometry("830x130")
            global name_entry1
            global brand_entry1
            ########################## Ignore This ##############################
            # Gets the requested values of the height and widht.
            windowWidth = self.winfo_reqwidth()
            windowHeight = self.winfo_reqheight()
            # Gets both half the screen width/height and window width/height
            positionRight = int(self.winfo_screenwidth()/3.1 - windowWidth/2.5)
            positionDown = int(self.winfo_screenheight()/2 - windowHeight/2)
            # Positions the window in the center of the page.
            pop.geometry("+{}+{}".format(positionRight, positionDown))
            pop.attributes('-topmost', 1)
            ####################################################################

            customtkinter.CTkLabel(pop, text = "Name:", text_font=("yu gothic ui", 15, 'bold')).place(x=163, y=30, anchor=tkinter.E)
            customtkinter.CTkLabel(pop, text = "Brand:", text_font=("yu gothic ui", 15, 'bold')).place(x=463, y=30, anchor=tkinter.E)

            #Entry Boxes
            name_entry1 = customtkinter.CTkEntry(pop, text_font=("yu gothic ui", 15), width = 280)
            name_entry1.bind('<FocusIn>', controller.entry_callback)
            name_entry1.place(x=200, y=68, anchor=tkinter.CENTER)

            brand_entry1 = customtkinter.CTkEntry(pop, text_font=("yu gothic ui", 15), width = 280)
            brand_entry1.bind('<FocusIn>', controller.entry_callback)
            brand_entry1.place(x=500, y=68, anchor=tkinter.CENTER)

            customtkinter.CTkButton(pop, text="Confirm", text_font=("TkHeadingtext_font", 19) , cursor="hand2",
                    command = ShoppingList_add_record).place(x=720, y=68, anchor=tkinter.CENTER)

        # The Add customtkinter.CTkButton
        shopping_add = customtkinter.CTkButton(self, text= "Add",text_font=("TkHeadingtext_font", 25) ,  cursor="hand2",
                width =310, command=ShoppingList_add_popup)
        shopping_add.place(x=475, y=655)


def ShoppingList_delete_all(): # Delets all items
    for values in ShoppingList.get_children():
        ShoppingList.delete(values)

def ShoppingList_delete_selected(): # Delete multiple selected ITEMS
    ShoppingList_delete_selected = ShoppingList.selection()
    for values in ShoppingList_delete_selected:
        ShoppingList.delete(values)

def ShoppingList_add_record(): # adds the data to the table (ShoppingList)
    ShoppingList.insert("", "end", values=(name_entry1.get(), brand_entry1.get()))
    # clear the entry boxes
    name_entry1.delete(0, END)
    brand_entry1.delete(0, END)


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
