from CTkTable import CTkTable
import customtkinter as ctk
from Database import Database
import tkinter as tk
from CTkMessagebox import CTkMessagebox
import datetime


class Transaction(ctk.CTkFrame):
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

        # Title
        self.transaction_label = ctk.CTkLabel(
            self.master,
            text="TRANSACTION HISTORY",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        )
        self.transaction_label.grid(
            row=0, column=0, sticky="wn", padx=25, pady=18)

        # Search Entry
        self.search_entry = ctk.CTkEntry(
            self.master,
            placeholder_text="Student RollNo",
            placeholder_text_color="white",
            font=("Segoe UI", 12, "bold"),
            corner_radius=5,
            border_color="black",
            border_width=1,
            fg_color="#1b3430",
            width=180,
            height=30,
            text_color="white",
        )
        self.search_entry.grid(row=0, column=1, sticky="e", padx=15, pady=15)

        # Search Button
        self.search_btn = ctk.CTkButton(
            self.master,
            text="Search",
            text_color="white",
            fg_color="#001a23",
            hover_color="#1b3430",
            font=("Segoe UI", 13, "bold"),
            corner_radius=5,
            width=180,
            height=30,
            command=self.search_transactions,
            cursor="hand2",
        )
        self.search_btn.grid(row=0, column=2, padx=15, pady=15)

        # Refresh Button
        self.refresh_btn = ctk.CTkButton(
            self.master,
            text="Refresh",
            text_color="white",
            fg_color="#001a23",
            font=("Segoe UI", 13, "bold"),
            hover_color="#1b3430",
            corner_radius=5,
            width=180,
            height=30,
            cursor="hand2",
            command=self.load_transactions,
        )
        self.refresh_btn.grid(row=0, column=3, padx=15, pady=15)

        # Data Frame
        self.data_frame = ctk.CTkScrollableFrame(
            self.master,
            fg_color="#1b3430",
            corner_radius=20,
        )
        self.data_frame.grid(row=1, columnspan=4, pady=15,
                             padx=15, sticky="nsew")

        # Load all transactions (issued and returned books)
        self.load_transactions()

    def load_transactions(self, student_roll=None):
        try:
            # Get all book transactions from Database class
            transactions = Database.get_all_transactions(student_roll)

            # Prepare table data with headers
            table_data = [
                [
                    "Issue ID",
                    "Roll No",
                    "Student Name",
                    "Book Title",
                    "ISBN",
                    "Issue Date",
                    "Due Date",
                    "Return Date",
                    "Fine Amount",
                    "Status",
                    "Issued By",
                ]
            ]

            # Add transactions to table data
            for transaction in transactions:
                table_data.append(
                    [
                        str(transaction[0]),  # issue_id
                        transaction[1],  # student_roll_no
                        transaction[2],  # student_name
                        transaction[3],  # book_title
                        transaction[4],  # isbn
                        str(transaction[5]),  # issue_date
                        str(transaction[6]),  # due_date
                        str(transaction[7])
                        if transaction[7]
                        else "Not Returned",  # return_date
                        f"₹{transaction[8]:.2f}"
                        if transaction[8]
                        else "₹0.00",  # fine_amount
                        transaction[9],  # status
                        transaction[10],  # issued_by
                    ]
                )

            # Create or update CTkTable
            if hasattr(self, "transactions_table"):
                self.transactions_table.destroy()

            self.transactions_table = CTkTable(
                self.data_frame, values=table_data, wraplength=300
            )
            self.transactions_table.pack(expand=True, fill="both")

        except Exception as e:
            CTkMessagebox(
                title="Error", message=f"Error loading transactions: {str(e)}"
            )

    def search_transactions(self):
        student_roll = (
            self.search_entry.get().strip() if self.search_entry.get() else None
        )
        self.load_transactions(student_roll)
        if student_roll:
            CTkMessagebox(
                title="Info",
                message=f"Showing transactions for student: {student_roll}",
            )

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
