from Pages import *


class Settings(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        customtkinter.CTkFrame.__init__(self, master )
        self.controller = controller
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        
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


        label_1 = customtkinter.CTkLabel(right_frame, text='Settings', text_font=("TkMenutext_font", 50), text_color = ("#1e3d6d", "#ebe7e4"))
        label_1.pack(pady = (110, 80))


        button_1 = customtkinter.CTkButton(right_frame, text="Reset", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=self.Reset_prompt)
        button_1.pack(pady = (0,30))


        button_2 = customtkinter.CTkButton(right_frame, text="Shutdown", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=self.Shutdown_prompt)
        button_2.pack()


        button_3 = customtkinter.CTkButton(right_frame, text="Reboot", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350, command=self.Restart_prompt)
        button_3.pack(pady = 30)


        button_4 = customtkinter.CTkButton(right_frame, text="Exit Interface", text_font=("TkHeadingtext_font", 25) , cursor="hand2",
                                            width = 350,  command=controller.destroy)
        button_4.pack()
        
        

        radio_frame = customtkinter.CTkFrame(right_frame, corner_radius=0, width = 350, height = 40)#, fg_color = "green")
        radio_frame.pack(pady = 30)
        
        radio_var = tkinter.IntVar(value=1)

        label_radio_group = customtkinter.CTkLabel(radio_frame, text="Date and Time:", text_color = ("#1e3d6d", "#ebe7e4"))
        label_radio_group.place(relx=0.15, rely=0.5, anchor= "center")
        
        radio_button_1 = customtkinter.CTkRadioButton(radio_frame, text = "Show", text_color = ("#1e3d6d", "#ebe7e4"), 
                                                      variable=radio_var, value=0, command = controller.show_clock_date)
        radio_button_1.place(relx=0.4, rely=0.5, anchor= "center")

        radio_button_2 = customtkinter.CTkRadioButton(radio_frame, text = " Hide ", text_color = ("#1e3d6d", "#ebe7e4"),  
                                                      variable=radio_var, value=1, command = controller.hide_clock_date)
        radio_button_2.place(relx=0.6, rely=0.5, anchor= "center")
        
        
        customtkinter.CTkButton(self, text="Go Back", text_font=("TkHeadingtext_font", 20) , cursor="hand2",
                command=lambda:controller.show_frame("MainMenu")
            ).place(relx=0.98, rely=0.97, anchor= "se")
        

    # Functions for Settings Page
    def Reset_prompt(self): # Popup confirming reset
        choice = messagebox.askquestion("Reset", "Are you sure you want to reset? \n Proceeding will sign you out")
        if choice == 'yes':
            cleanup()
            empty_pantry()
            empty_nonpantry()
            empty_shopping()
            self.controller.show_frame("Login")

    def Shutdown_prompt(self): # Popup confirming shutdown
        choice = messagebox.askquestion("Shutdown", "Are you sure you want to shutdown the system?")
        if choice == 'yes':
            subprocess.call(['sudo', 'shutdown', '-h', '-t 5', 'now'])

    def Restart_prompt(self): # Popup confirming restart
        choice = messagebox.askquestion("Reboot", "Are you sure you want to reboot the system?")
        if choice == 'yes':
            subprocess.call(['sudo', 'shutdown', '-r', '-t 5', 'now'])