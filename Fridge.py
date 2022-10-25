from Pages.Login_Page import *
from Pages.Register_Page import *
from Pages.MainMenu_Page import *
from Pages.ItemsList_Page import *
from Pages.ShoppingList_Page import *
from Pages.Recipe_Page import *
from Pages.Settings_Page import *

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("assets/themes/wvu-dark.json")
#customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue", "sweetkind"


# Main Class
class SmartFridgeApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)
        window = customtkinter.CTkFrame(self)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        # this data is shared among all the classes
        self.app_login_cred = {'email': StringVar(), 'idToken': StringVar()}

        self.frames = {}
        for F in (Login, Register, MainMenu, ItemsList, AddItems, RecipeSuggestions, SuggestedShopping, Settings):
            page_name = F.__name__
            global frame
            frame = F(master=window, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

        # Styling the treeviews
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("", 15), background="#2a2d2e", foreground="white", rowheight=35, fieldbackground="#343638",
                        bordercolor="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", font=('Arial', 15, 'bold'), background="#565b5e", foreground="white", relief="flat",
                        rowheight=35, fieldbackground="#343638", bordercolor="#343638", borderwidth=0)
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        self.change_mode()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def entry_callback(self, event): # Call Matchbox keyboard automatically
        os.popen('matchbox-keyboard','r',4096)

    # Functions for Settings Page
    def Reset_prompt(self): # Popup confirming reset
        choice = messagebox.askquestion("Reset", "Are you sure you want to reset? \n Proceeding will sign you out")
        if choice == 'yes':
            self.show_frame("Login")

    def Shutdown_prompt(self): # Popup confirming shutdown
        choice = messagebox.askquestion("Shutdown", "Are you sure you want to shutdown the system?")
        if choice == 'yes':
            subprocess.call(['sudo', 'shutdown', '-h', '-t 5', 'now'])

    def Restart_prompt(self): # Popup confirming restart
        choice = messagebox.askquestion("Reboot", "Are you sure you want to reboot the system?")
        if choice == 'yes':
            subprocess.call(['sudo', 'shutdown', '-r', '-t 5', 'now'])


    def change_appearance_mode(self):
        if switch.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def change_mode(self):
        global switch
        switch = customtkinter.CTkSwitch(self, text="Dark Mode", bg_color= ("#001532", "gray20"), command = self.change_appearance_mode)
        switch.place(x=20, y=680)

######################################### Initiallize app ######################################
if __name__ == "__main__":
    root = SmartFridgeApp()
    root.title("Smart Fridge 1.8")
    root.geometry("1280x720")
    root.resizable(0, 0)
    root.attributes('-topmost', 0)
    ########################## positioning window in the center ###############################
    # Gets the requested values of the height and widht.
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth()/3.5 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/3.5 - windowHeight/2)
    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionRight, positionDown))
    ###########################################################################################
    #root.attributes('-fullscreen', 1)
    root.mainloop()
