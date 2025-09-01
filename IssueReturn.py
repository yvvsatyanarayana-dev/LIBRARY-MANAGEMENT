import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from Database import Database

class IssueReturn(ctk.CTkFrame):
    def __init__(self, main):
        super().__init__(main)
        self.master = main
        self.create_widgets()
    
    def create_widgets(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)
        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_rowconfigure(1, weight=1)
        self.issue_return_label = ctk.CTkLabel(
            self.master,
            text="ISSUE/RETURN BOOK",
            font=('Segeo UI', 20, 'bold'),
            text_color='white'
        )
        self.issue_return_label.grid(row=0, column=0, sticky='wn', padx=25, pady=18)