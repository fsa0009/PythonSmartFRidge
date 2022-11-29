from Pages import *


class Recipes(customtkinter.CTkFrame):
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

        settings_image = ImageTk.PhotoImage(file="assets/images/Buttons/settings.png")  #122e54

        label_1 = customtkinter.CTkLabel(right_frame, text='Recipes', text_font=("TkMenutext_font", 50), text_color = ("#1e3d6d", "#ebe7e4"))
        label_1.pack(pady = (110, 80))

        button_1 = customtkinter.CTkButton(right_frame, text="Recipes Suggestions", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=lambda:controller.show_frame("RecipeSuggestions"))
        button_1.pack(pady = (0,30))

        button_2 = customtkinter.CTkButton(right_frame, text="All Recipes", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=lambda:controller.show_frame("AllRecipes"))
        button_2.pack()

        button_3 = customtkinter.CTkButton(right_frame, text="Add Recipe", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=lambda:controller.show_frame("AddRecipes"))
        button_3.pack(pady = 30)

        button_5 = customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                    command=lambda:controller.show_frame("MainMenu"))
        button_5.place(relx=0.985, rely=0.97, anchor= "se")

class AllRecipes(customtkinter.CTkFrame):
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

        customtkinter.CTkLabel(top_frame, text="All Recipes" , text_font=("TkMenutext_font", 40), text_color = ("#1e3d6d", "#ebe7e4")).place(x=505, y = 40)
        ###################################################################################################################


        ############################### Frame for the bottom bar containing go back button #################################
        bottom_frame = customtkinter.CTkFrame(self, width=1260, height=100)
        bottom_frame.place(x=0, y = 650)

        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("Recipes")
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
            Recipe_items = list(Recipe_data_values[1].values())
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

            def View_Recipe(x):
                pop = customtkinter.CTkToplevel()
                pop.attributes('-topmost', 1)
                width = 1150
                height = 600
                # Centering the app in the middle of the screen
                screen_width = pop.winfo_screenwidth()
                screen_height = pop.winfo_screenheight()
                x_cordinate = int((screen_width/2) - (width/2))
                y_cordinate = int((screen_height/2) - (height/2))
                pop.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))

                Recipes_data_pop = Recipes.val()
                Recipes_values_pop = list(Recipes_data_pop.values())
                Recipe_pop = list(Recipes_values_pop[x].values())

                # Assigning variables for each value
                Recipe_Name_pop = Recipe_pop[0]
                Recipe_items_pop = list(Recipe_pop[1].values())
                Items_count = len(Recipe_items_pop)
                Recipe_instructions = Recipe_pop[5]

                Recipe_Name_pop_label = customtkinter.CTkLabel(pop, text = Recipe_Name_pop, text_font=("TkMenutext_font", 40), text_color = ("#1e3d6d", "#ebe7e4"))
                Recipe_Name_pop_label.pack(pady=20)

                # Recipe_items_Box = customtkinter.CTkTextbox(pop, height=Items_count*27, text_font = ("TkHeadingtext_font", 15), fg_color=("pink", "green"), text_color = ("#1e3d6d", "#ebe7e4"))
                # Recipe_items_Box.pack()
                customtkinter.CTkLabel(pop, text = "Items:", text_font = ("TkHeadingtext_font", 15, "bold"), text_color = ("#1e3d6d", "#ebe7e4"), justify=LEFT).pack(pady = (0, 5))
                Recipe_items_Box = customtkinter.CTkLabel(pop, text = "", text_font = ("TkHeadingtext_font", 15), fg_color = "#343638", text_color = "white", justify=LEFT, corner_radius=10)
                Recipe_items_Box.pack()

                text = []

                for count in range(0, Items_count):
                    text.append(f'{count+1}. {Recipe_items_pop[count]}')

                text = '[' + ' +'.join(text) + ']'
                text = f'\n'.join(str(text)[1:-1].split('+'))
                Recipe_items_Box.configure(text = text)

                customtkinter.CTkLabel(pop, text = "Instructions:", text_font = ("TkHeadingtext_font", 15, "bold"), text_color = ("#1e3d6d", "#ebe7e4"), justify=LEFT).pack(pady = (10, 5))

                Recipe_instructions_box = customtkinter.CTkLabel(pop, text = "", text_font = ("TkHeadingtext_font", 15), fg_color = "#343638", text_color = "white", justify=LEFT, corner_radius=10)
                Recipe_instructions_box.pack()
                Recipe_instructions_box.configure(text = Recipe_instructions)

                pop.title(f'View Recipe: {Recipe_Name_pop}')

            View_Recipe_btn = customtkinter.CTkButton(frame, text="View Recipe", text_font=("TkHeadingtext_font", 15), cursor="hand2", width = 250, command = lambda x=x: View_Recipe(x))
            View_Recipe_btn.pack(pady = 20)


class RecipeSuggestions(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master)
        self.controller = controller
        global db
        global Recipes
        global Recipe_number
        global my_canvas1
        global recipe
        global scrollheight
        global content_frame
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
                command=lambda:controller.show_frame("Recipes")
            ).place(relx=0.98, rely=0.97, anchor= "se")
        ###################################################################################################################

        db = FirebaseConfig().firebase.database()
        Recipes = db.child("recipes").child("global").get()
        Recipe_number = len(Recipes.val())
        # this is just to sit a width for the canvas
        scrollheight = customtkinter.CTkLabel(content_frame, text="", text_font=("", Recipe_number*325), width = 5000) #text_font=("", Recipe_number*325)
        scrollheight.grid(row=0, column=0, pady=150, padx=10) #, text_font=("",3250) #2550

        recipe = customtkinter.CTkFrame(content_frame, corner_radius=0,  fg_color = "white")
        recipe.place(relx= 0.09, rely = 0)

        # scrollheight = customtkinter.CTkLabel(content_frame, text="" , text_font=("", Recipe_number*325), width = 5000)
        # scrollheight.grid(row=0, column=0, pady=150, padx=10) #, text_font=("",3250) #2550

        # Frame to use pack
        my_canvas1 = customtkinter.CTkFrame(recipe, corner_radius=0)
        my_canvas1.pack(pady=(125,0))

def generate_recipe(accoountid):
    global UserID
    global suggested_count
    UserID = accoountid
    User_Items = []
    # try:
    Items = db.child("non-pantry-items").child(UserID).get()
    for itemsData in Items.each():
        data = itemsData.val()["A_Name"]
        User_Items.append(data)
    # except:
    #     pass
    # try:
    Items = db.child("pantry-items").child(UserID).get()
    for itemsData in Items.each():
        data = itemsData.val()["A_Name"]
        User_Items.append(data)
    # except:
    #     pass

    # Grab all the user's items and make them lowercase
    User_Items  = [element.lower() for element in User_Items]
    y = []
    for x in range(0, Recipe_number):

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
        # Recipe_instructions = Recipe_data_values[5]
        Recipe_items = list(Recipe_data_values[1].values())
        #Items_count = len(Recipe_items)

        # Grab all the recipies' items and make them lowercase
        Recipe_items  = [element.lower() for element in Recipe_items]

        # ---------------------------------------------------------------- #

        # Compare the two lists
        if all(item in User_Items for item in Recipe_items):
            y.append(+1)
            left_frame = customtkinter.CTkFrame(my_canvas1, corner_radius=0,  fg_color = "white", width = 500)
            left_frame.grid(row = x, column = 0, pady=(0,10), padx=(40,0))
            # Recipe Image Image
            Recipe_Image = Image.open(Recipe_Image_Path)
            Recipe_Image = Recipe_Image.resize((300, 300), Image.ANTIALIAS)
            Recipe_Image = ImageTk.PhotoImage(Recipe_Image)
            Recipe_Image_widget = customtkinter.CTkLabel(left_frame, image = Recipe_Image)
            Recipe_Image_widget.image = Recipe_Image
            Recipe_Image_widget.pack()

            # Recipe Name Label
            Recipe_Name_Label = customtkinter.CTkLabel(left_frame, text = Recipe_Name, text_font = ("TkHeadingtext_font", 15, "bold"), text_color = "black")
            Recipe_Name_Label.pack()

            # Recipe Calories Label
            Recipe_Calories_Label = customtkinter.CTkLabel(left_frame, text = f'Calories: {Recipe_Calories} Cal', text_font = ("TkHeadingtext_font", 15), text_color = "black")
            Recipe_Calories_Label.pack()

            # Recipe Cooking Time Label
            Recipe_Cooking_Time_Label = customtkinter.CTkLabel(left_frame, text = f'Cooking Time: {Recipe_Cooking_Time} mins', text_font = ("TkHeadingtext_font", 15), text_color = "black")
            Recipe_Cooking_Time_Label.pack()

            # Recipe Servings Label
            Recipe_Servings_Label = customtkinter.CTkLabel(left_frame, text = f'Servings: {Recipe_Servings} Servings', text_font = ("TkHeadingtext_font", 15), text_color = "black")
            Recipe_Servings_Label.pack()

            def View_Recipe(x):
                pop = customtkinter.CTkToplevel()
                pop.attributes('-topmost', 1)
                width = 1150
                height = 600
                # Centering the app in the middle of the screen
                screen_width = pop.winfo_screenwidth()
                screen_height = pop.winfo_screenheight()
                x_cordinate = int((screen_width/2) - (width/2))
                y_cordinate = int((screen_height/2) - (height/2))
                pop.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))

                Recipes_data_pop = Recipes.val()
                Recipes_values_pop = list(Recipes_data_pop.values())
                Recipe_pop = list(Recipes_values_pop[x].values())

                # Assigning variables for each value
                Recipe_Name_pop = Recipe_pop[0]
                Recipe_items_pop = list(Recipe_pop[1].values())
                Items_count = len(Recipe_items_pop)
                Recipe_instructions = Recipe_pop[5]

                Recipe_Name_pop_label = customtkinter.CTkLabel(pop, text = Recipe_Name_pop, text_font=("TkMenutext_font", 40), text_color = ("#1e3d6d", "#ebe7e4"))
                Recipe_Name_pop_label.pack(pady=20)

                # Recipe_items_Box = customtkinter.CTkTextbox(pop, height=Items_count*27, text_font = ("TkHeadingtext_font", 15), fg_color=("pink", "green"), text_color = ("#1e3d6d", "#ebe7e4"))
                # Recipe_items_Box.pack()
                customtkinter.CTkLabel(pop, text = "Items:", text_font = ("TkHeadingtext_font", 15, "bold"), text_color = ("#1e3d6d", "#ebe7e4"), justify=LEFT).pack(pady = (0, 5))
                Recipe_items_Box = customtkinter.CTkLabel(pop, text = "", text_font = ("TkHeadingtext_font", 15), fg_color = "#343638", text_color = "white", justify=LEFT, corner_radius=10)
                Recipe_items_Box.pack()

                text = []

                for count in range(0, Items_count):
                    text.append(f'{count+1}. {Recipe_items_pop[count]}')

                text = '[' + ' +'.join(text) + ']'
                text = f'\n'.join(str(text)[1:-1].split('+'))
                Recipe_items_Box.configure(text = text)

                # for item in text:

                #     Recipe_items_Box = customtkinter.CTkLabel(pop, text = item, text_font = ("TkHeadingtext_font", 15), fg_color=("pink", "green"), text_color = ("#1e3d6d", "#ebe7e4"), justify=LEFT)
                #     Recipe_items_Box.pack()
                #     count += 1

                # Recipe_instructions_box = customtkinter.CTkTextbox(pop, width = 1000, text_font = ("TkHeadingtext_font", 15), fg_color=("green", "pink"), text_color = ("#1e3d6d", "#ebe7e4"))
                # Recipe_instructions_box.pack(pady = 20)
                # Recipe_instructions_box.insert("0.0", Recipe_instructions)

                customtkinter.CTkLabel(pop, text = "Instructions:", text_font = ("TkHeadingtext_font", 15, "bold"), text_color = ("#1e3d6d", "#ebe7e4"), justify=LEFT).pack(pady = (10, 5))

                Recipe_instructions_box = customtkinter.CTkLabel(pop, text = "", text_font = ("TkHeadingtext_font", 15), fg_color = "#343638", text_color = "white", justify=LEFT, corner_radius=10)
                Recipe_instructions_box.pack()
                Recipe_instructions_box.configure(text = Recipe_instructions)

                pop.title(f'View Recipe: {Recipe_Name_pop}')

            View_Recipe_btn = customtkinter.CTkButton(left_frame, text="View Recipe", text_font=("TkHeadingtext_font", 15), cursor="hand2", width = 250, command = lambda x=x: View_Recipe(x))
            View_Recipe_btn.pack(pady = 20)
    #suggested_count= len(y)



class AddRecipes(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master)
        self.controller = controller

        back_btn = customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                    command=lambda:controller.show_frame("Recipes"))
        back_btn.place(relx=0.985, rely=0.97, anchor= "se")
