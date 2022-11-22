from Pages import *


class MainMenu(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        global Welcom_label

        # Slicing the page
        left_frame = customtkinter.CTkFrame(master=self, corner_radius=0)#, fg_color = "red")
        left_frame.grid(row = 0, column = 0, sticky = "nesw")

        right_frame = customtkinter.CTkFrame(master=self, corner_radius=0)#,  fg_color = "green")
        right_frame.grid(row = 0, column = 1, sticky = "nesw")

        # Picture on left side
        Welcome_img = Image.open("assets/images/WVU.png")
        Welcome_img = Welcome_img.resize((500, 500), Image.ANTIALIAS)
        Welcome_img = ImageTk.PhotoImage(Welcome_img)
        Welcome_widget = customtkinter.CTkLabel(left_frame, image=Welcome_img)
        Welcome_widget.image = Welcome_img
        Welcome_widget.pack(pady = (120, 0) ,anchor = "center")

        Welcom_label = customtkinter.CTkLabel(left_frame, text="", text_font=("TkMenutext_font", 40), text_color = ("#1e3d6d", "#ebe7e4"))
        Welcom_label.place(relx = 0.5, rely=0.1, anchor=CENTER)

        settings_image = ImageTk.PhotoImage(file="assets/images/Buttons/settings.png")  #122e54

        label_1 = customtkinter.CTkLabel(right_frame, text='Main Menu', text_font=("TkMenutext_font", 50), text_color = ("#1e3d6d", "#ebe7e4"))
        label_1.pack(pady = (110, 80))

        button_1 = customtkinter.CTkButton(right_frame, text="Pantry Items", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=lambda:controller.show_frame("PantryList"))
        button_1.pack(pady = (0,30))

        button_2 = customtkinter.CTkButton(right_frame, text="Non-Pantry Items", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=lambda:controller.show_frame("NonPantryList"))
        button_2.pack()

        button_3 = customtkinter.CTkButton(right_frame, text="Shopping List", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=lambda:controller.show_frame("SuggestedShopping"))
        button_3.pack(pady = 30)

        button_4 = customtkinter.CTkButton(right_frame, text="Recipes", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=lambda:controller.show_frame("RecipeSuggestions"))
        button_4.pack()
        
        button_5 = customtkinter.CTkButton(right_frame, image=settings_image,  text="", width=60, height=60, corner_radius=10,  fg_color= ("#122e54", "#122e54"),
                                                                        hover_color= ("#1e3d6d", "#122e54"), command=lambda:controller.show_frame("Settings"))
        button_5.place(relx=0.99, rely=0.99, anchor= "se")

def welcome_label(user_name):
    Welcom_label.configure(text = f'Welcome {user_name}!')
