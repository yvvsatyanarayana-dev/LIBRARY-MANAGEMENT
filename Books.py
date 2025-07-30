from CTkTable import CTkTable
import customtkinter as ctk
from Database import Database
import tkinter as tk
from CTkMessagebox import CTkMessagebox

class Books(ctk.CTkFrame):
    def __init__(self,main):
        super().__init__(main)
        self.master = main
        self.create_widgets()
    
    def create_widgets(self):
        self.master.grid_columnconfigure(0,weight=1)
        self.master.grid_columnconfigure(1,weight=1)
        self.master.grid_columnconfigure(2,weight=1)
        self.master.grid_columnconfigure(3,weight=1)
        self.master.grid_rowconfigure(0,weight=0)
        self.master.grid_rowconfigure(1,weight=1)
        self.std_book_label = ctk.CTkLabel(
            self.master,
            text="BOOKS",
            font=('Segeo UI',20,'bold'),
            text_color='white'
        )
        self.std_book_label.grid(row=0,column=0,sticky='wn',padx=25,pady=18)

        self.search_entry = ctk.CTkEntry(
            self.master,
            placeholder_text="ISBN",
            placeholder_text_color="white",
            font=('Segeo UI',12,'bold'),
            corner_radius=5,
            border_color='black',
            border_width=1,
            fg_color="#1b3430",
            width=180,
            height=30,
            text_color='white'
        )
        self.search_entry.grid(row=0,column=1,sticky='e',padx=15,pady=15)
        self.submit_btn = ctk.CTkButton(
            self.master,
            text='Search',
            text_color='white',
            fg_color="#001a23",
            font=('Segeo UI',13,'bold'),
            hover_color="#1b3430",
            corner_radius=5,
            width=180,
            height=30,
            command=self.search_std_dtls,
            cursor='hand2'
        )
        self.submit_btn.grid(row=0,column=2,padx=10,pady=15)
        self.book_add = ctk.CTkButton(
            self.master,
            text="Add Book",
            text_color='white',
            font=('Segeo UI',13,'bold'),
            fg_color="#001a23",
            hover_color="#1b3430",
            corner_radius=5,
            width=180,
            height=30,
            cursor='hand2'
        )
        self.book_add.grid(row=0,column=3,padx=10,pady=15)
        self.data_frame = ctk.CTkScrollableFrame(
            self.master,
            fg_color='#1b3430',
            corner_radius=20,
        )
        self.data_frame.grid(row=1,columnspan=4,pady=15,padx=15,sticky='nsew')

        self.books_data = Database.books_data()
        self.std_details = CTkTable(
            self.data_frame,
            values=self.books_data,
            wraplength=300
        )
        self.std_details.pack(expand=True,)

    def search_std_dtls(self):
        self.isbn = self.search_entry.get() if self.search_entry.get() else None
        data2 = Database.books_data(isbn=self.isbn)
        if data2:
            self.std_details.configure(values=data2)
        else:
            CTkMessagebox(f'Please Enter Again')
        self.clear_book_dtls()
    def clear_book_dtls(self):
        self.search_entry.delete(0,tk.END)