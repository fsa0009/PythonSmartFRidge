from Pages import *


class RecipeSuggestions(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master)
        self.controller = controller

    # Steps to create a scrollable window/page:
        # 1 Create a main frame
        main_frame = customtkinter.CTkFrame(self)
        main_frame.pack(fill = BOTH, expand = 1)

        # 2 Create a Canvas inside the main frame
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side = LEFT, fill = BOTH, expand = 1)

        # 3 Add a scrollbar to the Canvas
        my_scrollbar = customtkinter.CTkScrollbar(main_frame, command = my_canvas.yview)
        my_scrollbar.pack(side = RIGHT, fill = Y)

        # 4 Configure the Canvas
        my_canvas.configure(yscrollcommand = my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        # 5 Create anotehr frame inside the Canvas (Content Frame)
        content_frame = customtkinter.CTkFrame(my_canvas)

        # 6 Add that new frame to a window in the Canvas
        my_canvas.create_window((0, 0), window = content_frame, anchor = "nw")


        ############################### Frame for the top bar containing title and logo ###################################
        top_frame = customtkinter.CTkFrame(self, width=1260, height=130)
        top_frame.place(x=0, y = 0)

        # Corner Picture (logo)
        logo_img = Image.open("assets/images/WVU.png")
        logo_img = logo_img.resize((100, 100), Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo_img)
        logo_widget = customtkinter.CTkLabel(self, image=logo_img)
        logo_widget.image = logo_img
        logo_widget.place(relx=0.05, rely=0.09, anchor= "center")

        customtkinter.CTkLabel(top_frame, text="Recipe Suggestions" , text_font=("TkMenutext_font", 40), text_color = ("#1e3d6d", "#ebe7e4")).place(x=415, y = 40)
        ###################################################################################################################


        ############################### Frame for the bottom bar containing go back button #################################
        bottom_frame = customtkinter.CTkFrame(self, width=1260, height=100)
        bottom_frame.place(x=0, y = 650)

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(relx=0.98, rely=0.97, anchor= "se")
        ###################################################################################################################

        db = FirebaseConfig().firebase.database()
        Recipes = db.child("recipes").child("global").get()
        Recipe_number = len(Recipes.val())
        # this is just to sit a width for the canvas
        customtkinter.CTkLabel(content_frame, text="" , text_font=("", Recipe_number*325), width = 5000).grid(row=0, column=0, pady=150, padx=10) #, text_font=("",3250) #2550

        recipe = customtkinter.CTkFrame(content_frame, corner_radius=0,  fg_color = "white")
        recipe.place(relx= 0.09, rely = 0)

        # Frame to use pack
        my_canvas1 = customtkinter.CTkFrame(recipe, corner_radius=0)
        my_canvas1.pack(pady=(125,0))

        for x in range(0, Recipe_number):
            frame = customtkinter.CTkFrame(my_canvas1, corner_radius=0,  fg_color = "white", width = 500)
            frame.grid(row = x, column = 0, pady=(0,10), padx=(40,0))

            # ------------------------ Database Stuff ------------------------ #
            # Pulling all the recipes and getting each recipe number
            Recipes_data = Recipes.val()
            Recipes_values = list(Recipes_data.values())
            Recipe_data = Recipes_values[x]
            Recipe_data_values = list(Recipe_data.values())
            # Assigning variables for each value
            Recipe_Image_Path = Recipe_data_values[6]
            Recipe_Name = Recipe_data_values[0]
            Recipe_Calories = Recipe_data_values[3]
            Recipe_Cooking_Time = Recipe_data_values[2]
            Recipe_Servings = Recipe_data_values[4]
            Recipe_instructions = Recipe_data_values[5]
            # ---------------------------------------------------------------- #

            # ------------------------ Widgets Stuff ------------------------- #
            # Recipe Image Image
            Recipe_Image = Image.open(Recipe_Image_Path)
            Recipe_Image = Recipe_Image.resize((300, 300), Image.ANTIALIAS)
            Recipe_Image = ImageTk.PhotoImage(Recipe_Image)
            Recipe_Image_widget = customtkinter.CTkLabel(frame, image = Recipe_Image)
            Recipe_Image_widget.image = Recipe_Image
            #Recipe_Image_widget.place(x= 0, y = 0)
            Recipe_Image_widget.pack()

            # Recipe Name Label
            Recipe_Name_Label = customtkinter.CTkLabel(frame, text = Recipe_Name, text_font = ("TkHeadingtext_font", 15, "bold"), text_color = "black")
            #Recipe_Name_Label.place(x= 0, y = 300)
            Recipe_Name_Label.pack()

            # Recipe Calories Label
            Recipe_Calories_Label = customtkinter.CTkLabel(frame, text = f'Calories: {Recipe_Calories} Cal', text_font = ("TkHeadingtext_font", 15), text_color = "black")
            #Recipe_Calories_Label.place(x= 0, y = 300)
            Recipe_Calories_Label.pack()

            # Recipe Cooking Time Label
            Recipe_Cooking_Time_Label = customtkinter.CTkLabel(frame, text = f'Cooking Time: {Recipe_Cooking_Time} mins', text_font = ("TkHeadingtext_font", 15), text_color = "black")
            #Recipe_Calories_Label.place(x= 0, y = 300)
            Recipe_Cooking_Time_Label.pack()

            # Recipe Servings Label
            Recipe_Servings_Label = customtkinter.CTkLabel(frame, text = f'Servings: {Recipe_Servings} Servings', text_font = ("TkHeadingtext_font", 15), text_color = "black")
            # Recipe_Servings_Label.place(x= 0, y = 300)
            Recipe_Servings_Label.pack()

            Recipe_instructions_box = customtkinter.CTkTextbox(frame)
            Recipe_instructions_box.place(x=300, y=100)
            Recipe_instructions_box.insert("0.0", Recipe_instructions)

            View_Recipe_btn = customtkinter.CTkButton(frame, text="View Recipe", text_font=("TkHeadingtext_font", 15), cursor="hand2", width = 250)
            View_Recipe_btn.pack(pady = 20)