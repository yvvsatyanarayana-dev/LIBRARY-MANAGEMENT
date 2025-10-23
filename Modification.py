import customtkinter as ctk
from tkinter import messagebox
from Database import Database
from CTkMessagebox import CTkMessagebox
import re
from datetime import date, timedelta
from CTkTable import CTkTable

class Modification:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.clear_frame()
        self.create_modification_ui()
        self.load_all_data()

    def clear_frame(self):
        # Clear existing widgets
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

    def create_modification_ui(self):
        # Title
        title = ctk.CTkLabel(self.parent_frame, text="MODIFICATION PANEL", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=10)

        # Notebook (Tabs)
        self.notebook = ctk.CTkTabview(self.parent_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Add tabs
        self.notebook.add("STUDENTS")
        self.notebook.add("BOOKS") 
        self.notebook.add("ISSUES")

        # Create UI for each tab
        self.create_students_tab()
        self.create_books_tab()
        self.create_issues_tab()

    # ========== STUDENTS TAB ==========
    def create_students_tab(self):
        frame = self.notebook.tab("STUDENTS")
        
        # Control frame
        control_frame = ctk.CTkFrame(frame)
        control_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Search
        ctk.CTkLabel(control_frame, text="Search:").pack(side="left", padx=(10, 5))
        self.student_search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(control_frame, textvariable=self.student_search_var, width=200)
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.bind("<KeyRelease>", lambda e: self.search_students())
        
        # Buttons
        ctk.CTkButton(control_frame, text="ADD", command=self.add_student_dialog, width=80).pack(side="right", padx=5)
        ctk.CTkButton(control_frame, text="EDIT", command=self.edit_student_dialog, width=80).pack(side="right", padx=5)
        ctk.CTkButton(control_frame, text="DELETE", command=self.delete_student, width=80).pack(side="right", padx=5)
        ctk.CTkButton(control_frame, text="REFRESH", command=self.load_all_students, width=80).pack(side="right", padx=5)
        
        # Table frame
        table_frame = ctk.CTkFrame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.students_table = CTkTable(table_frame, 
                                         columns=8,
                                         column_widths=[60, 80, 120, 150, 100, 150, 80, 60],
                                         header_color="blue",
                                         fg_color="white")
        self.students_table.pack(fill="both", expand=True, padx=10, pady=5)

    def load_all_students(self):
        data = Database.std_details()
        if data:
            # Headers
            headers = data[0]
            self.students_table.configure(columns=8)
            
            # Data rows
            rows = []
            for row in data[1:]:
                rows.append(row)
            
            self.students_table.update_data(rows)
            self.students_table.add_row(headers, 0)  # Header row

    def search_students(self):
        search_term = self.student_search_var.get().lower()
        data = Database.std_details()
        if data:
            filtered_rows = []
            for row in data[1:]:
                if (search_term in str(row[1]).lower() or  # ROLL NO
                    search_term in str(row[2]).lower()):   # NAME
                    filtered_rows.append(row)
            
            self.students_table.update_data(filtered_rows)
            self.students_table.add_row(data[0], 0)

    def add_student_dialog(self):
        dialog = StudentDialog(self)
        self.parent_frame.wait_window(dialog)
        if dialog.result:
            self.load_all_students()

    def edit_student_dialog(self):
        selected_row = self.students_table.get_selected_rows()
        if not selected_row:
            CTkMessagebox(title="Error", message="Please select a student to edit!")
            return
        
        # Get data from selected row (skip header)
        row_data = self.students_table.get_row_data(selected_row[0])
        if selected_row[0] == 0:  # Header row
            CTkMessagebox(title="Error", message="Cannot edit header!")
            return
        
        dialog = StudentDialog(self, "EDIT STUDENT", row_data)
        self.parent_frame.wait_window(dialog)
        if dialog.result:
            self.load_all_students()

    def delete_student(self):
        selected_row = self.students_table.get_selected_rows()
        if not selected_row:
            CTkMessagebox(title="Error", message="Please select a student to delete!")
            return
        
        if selected_row[0] == 0:  # Header row
            CTkMessagebox(title="Error", message="Cannot delete header!")
            return
        
        student_id = self.students_table.get_row_data(selected_row[0])[0]
        
        if CTkMessagebox(title="Confirm", message="Delete this student?", icon="question").get() == 'Yes':
            if Database.delete_student(student_id):
                self.load_all_students()

    # ========== BOOKS TAB ==========
    def create_books_tab(self):
        frame = self.notebook.tab("BOOKS")
        
        # Control frame
        control_frame = ctk.CTkFrame(frame)
        control_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Search
        ctk.CTkLabel(control_frame, text="Search ISBN:").pack(side="left", padx=(10, 5))
        self.book_search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(control_frame, textvariable=self.book_search_var, width=200)
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.bind("<KeyRelease>", lambda e: self.search_books())
        
        # Buttons
        ctk.CTkButton(control_frame, text="ADD", command=self.add_book_dialog, width=80).pack(side="right", padx=5)
        ctk.CTkButton(control_frame, text="EDIT", command=self.edit_book_dialog, width=80).pack(side="right", padx=5)
        ctk.CTkButton(control_frame, text="DELETE", command=self.delete_book, width=80).pack(side="right", padx=5)
        ctk.CTkButton(control_frame, text="REFRESH", command=self.load_all_books, width=80).pack(side="right", padx=5)
        
        # Table
        table_frame = ctk.CTkFrame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.books_table = CTkTable(table_frame, 
                                      columns=7,
                                      column_widths=[60, 120, 100, 100, 100, 80, 80],
                                      header_color="green",
                                      fg_color="white")
        self.books_table.pack(fill="both", expand=True, padx=10, pady=5)

    def load_all_books(self):
        data = Database.books_data()
        if data:
            headers = data[0]
            self.books_table.configure(columns=7)
            
            rows = [row for row in data[1:]]
            self.books_table.update_data(rows)
            self.books_table.add_row(headers, 0)

    def search_books(self):
        search_term = self.book_search_var.get()
        data = Database.books_data(isbn=search_term if search_term else None)
        if data:
            rows = [row for row in data[1:]]
            self.books_table.update_data(rows)
            self.books_table.add_row(data[0], 0)

    def add_book_dialog(self):
        dialog = BookDialog(self)
        self.parent_frame.wait_window(dialog)
        if dialog.result:
            self.load_all_books()

    def edit_book_dialog(self):
        selected_row = self.books_table.get_selected_rows()
        if not selected_row or selected_row[0] == 0:
            CTkMessagebox(title="Error", message="Please select a book to edit!")
            return
        
        row_data = self.books_table.get_row_data(selected_row[0])
        dialog = BookDialog(self, "EDIT BOOK", row_data)
        self.parent_frame.wait_window(dialog)
        if dialog.result:
            self.load_all_books()

    def delete_book(self):
        selected_row = self.books_table.get_selected_rows()
        if not selected_row or selected_row[0] == 0:
            CTkMessagebox(title="Error", message="Please select a book to delete!")
            return
        
        book_id = self.books_table.get_row_data(selected_row[0])[0]
        
        if CTkMessagebox(title="Confirm", message="Delete this book?", icon="question").get() == 'Yes':
            if Database.delete_book(book_id):
                self.load_all_books()

    # ========== ISSUES TAB ==========
    def create_issues_tab(self):
        frame = self.notebook.tab("ISSUES")
        
        # Control frame
        control_frame = ctk.CTkFrame(frame)
        control_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Search
        ctk.CTkLabel(control_frame, text="Search Roll No:").pack(side="left", padx=(10, 5))
        self.issue_search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(control_frame, textvariable=self.issue_search_var, width=200)
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.bind("<KeyRelease>", lambda e: self.search_issues())
        
        # Buttons
        ctk.CTkButton(control_frame, text="ISSUE", command=self.issue_book_dialog, width=80).pack(side="right", padx=5)
        ctk.CTkButton(control_frame, text="RETURN", command=self.return_book_dialog, width=80).pack(side="right", padx=5)
        ctk.CTkButton(control_frame, text="DELETE", command=self.delete_issue, width=80).pack(side="right", padx=5)
        ctk.CTkButton(control_frame, text="REFRESH", command=self.load_all_issues, width=80).pack(side="right", padx=5)
        
        # Table
        table_frame = ctk.CTkFrame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.issues_table = CTkTable(table_frame, 
                                       columns=8,
                                       column_widths=[60, 80, 120, 120, 100, 100, 100, 80],
                                       header_color="orange",
                                       fg_color="white")
        self.issues_table.pack(fill="both", expand=True, padx=10, pady=5)

    def load_all_issues(self):
        data = Database.get_all_transactions()
        if data:
            headers = ["ID", "ROLL NO", "STUDENT", "TITLE", "ISBN", "ISSUE DATE", "DUE DATE", "STATUS"]
            self.issues_table.configure(columns=8)
            
            rows = []
            for row in data:
                status = "ISSUED" if row[9] == 'Issued' else "RETURNED"
                rows.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], status))
            
            self.issues_table.update_data(rows)
            self.issues_table.add_row(headers, 0)

    def search_issues(self):
        search_term = self.issue_search_var.get()
        data = Database.get_all_transactions(search_term if search_term else None)
        if data:
            headers = ["ID", "ROLL NO", "STUDENT", "TITLE", "ISBN", "ISSUE DATE", "DUE DATE", "STATUS"]
            rows = []
            for row in data:
                status = "ISSUED" if row[9] == 'Issued' else "RETURNED"
                rows.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], status))
            
            self.issues_table.update_data(rows)
            self.issues_table.add_row(headers, 0)

    def issue_book_dialog(self):
        dialog = IssueDialog(self)
        self.parent_frame.wait_window(dialog)
        if dialog.result:
            self.load_all_issues()

    def return_book_dialog(self):
        selected_row = self.issues_table.get_selected_rows()
        if not selected_row or selected_row[0] == 0:
            CTkMessagebox(title="Error", message="Please select an issue to return!")
            return
        
        row_data = self.issues_table.get_row_data(selected_row[0])
        if row_data[7] == "RETURNED":
            CTkMessagebox(title="Error", message="Book already returned!")
            return
        
        issue_id = row_data[0]
        dialog = ReturnDialog(self, issue_id)
        self.parent_frame.wait_window(dialog)
        if dialog.result:
            self.load_all_issues()

    def delete_issue(self):
        selected_row = self.issues_table.get_selected_rows()
        if not selected_row or selected_row[0] == 0:
            CTkMessagebox(title="Error", message="Please select an issue to delete!")
            return
        
        issue_id = self.issues_table.get_row_data(selected_row[0])[0]
        
        if CTkMessagebox(title="Confirm", message="Delete this issue record?", icon="question").get() == 'Yes':
            if Database.delete_issue(issue_id):
                self.load_all_issues()

    def load_all_data(self):
        self.load_all_students()
        self.load_all_books()
        self.load_all_issues()


# ========== DIALOGS ==========
class StudentDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="ADD STUDENT", data=None):
        super().__init__()
        self.title(title)
        self.geometry("400x500")
        self.resizable(False, False)
        self.result = None
        self.transient(parent.parent_frame)
        self.grab_set()
        self.create_widgets(data)

    def create_widgets(self, data):
        self.roll_var = ctk.StringVar(value=data[1] if data else "")
        self.name_var = ctk.StringVar(value=data[2] if data else "")
        self.email_var = ctk.StringVar(value=data[3] if data else "")
        self.phone_var = ctk.StringVar(value=data[4] if data else "")
        self.address_var = ctk.StringVar(value=data[5] if data else "")
        self.group_var = ctk.StringVar(value=data[6] if data else "")
        self.year_var = ctk.StringVar(value=data[7] if data else "")
        
        fields = [
            ("Roll No:", self.roll_var),
            ("Name:", self.name_var),
            ("Email:", self.email_var),
            ("Phone:", self.phone_var),
            ("Address:", self.address_var),
            ("Group:", self.group_var),
            ("Year:", self.year_var)
        ]
        
        for label, var in fields:
            ctk.CTkLabel(self, text=label).pack(pady=5)
            ctk.CTkEntry(self, textvariable=var).pack(pady=5)
        
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="SAVE", command=self.save).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="CANCEL", command=self.destroy).pack(side="left", padx=10)

    def save(self):
        rollno, name, email, phone, address, group, year = [v.get() for v in [self.roll_var, self.name_var, self.email_var, self.phone_var, self.address_var, self.group_var, self.year_var]]
        
        if not all([rollno, name, email, phone, address, group, year]):
            CTkMessagebox(title="Error", message="Please fill all fields!")
            return
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            CTkMessagebox(title="Error", message="Invalid email format!")
            return
        
        if not re.match(r"^\d{10}$", phone):
            CTkMessagebox(title="Error", message="Phone must be 10 digits!")
            return
        
        success = Database.std_dtls_insert(rollno, name, email, phone, address, group, year)
        if success:
            self.result = True
            self.destroy()

class BookDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="ADD BOOK", data=None):
        super().__init__()
        self.title(title)
        self.geometry("400x350")
        self.resizable(False, False)
        self.result = None
        self.transient(parent.parent_frame)
        self.grab_set()
        self.create_widgets(data)

    def create_widgets(self, data):
        self.isbn_var = ctk.StringVar(value=data[3] if data else "")
        self.title_var = ctk.StringVar(value=data[1] if data else "")
        self.author_var = ctk.StringVar(value=data[2] if data else "")
        self.category_var = ctk.StringVar(value=data[4] if data else "")
        self.total_copies_var = ctk.StringVar(value=data[5] if data else "")
        
        fields = [
            ("ISBN:", self.isbn_var),
            ("Title:", self.title_var),
            ("Author:", self.author_var),
            ("Category:", self.category_var),
            ("Total Copies:", self.total_copies_var)
        ]
        
        for label, var in fields:
            ctk.CTkLabel(self, text=label).pack(pady=5)
            ctk.CTkEntry(self, textvariable=var).pack(pady=5)
        
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="SAVE", command=self.save).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="CANCEL", command=self.destroy).pack(side="left", padx=10)

    def save(self):
        isbn, title, author, category, total_copies = [v.get() for v in [self.isbn_var, self.title_var, self.author_var, self.category_var, self.total_copies_var]]
        
        if not all([isbn, title, author, category, total_copies]):
            CTkMessagebox(title="Error", message="Please fill all fields!")
            return
        
        if not total_copies.isdigit() or int(total_copies) <= 0:
            CTkMessagebox(title="Error", message="Total copies must be positive number!")
            return
        
        success = Database.add_book(isbn, title, author, category, int(total_copies))
        if success:
            self.result = True
            self.destroy()

class IssueDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__()
        self.title("ISSUE BOOK")
        self.geometry("300x200")
        self.result = None
        self.transient(parent.parent_frame)
        self.grab_set()
        
        self.roll_var = ctk.StringVar()
        self.isbn_var = ctk.StringVar()
        
        ctk.CTkLabel(self, text="Student Roll No:").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.roll_var).pack(pady=5)
        
        ctk.CTkLabel(self, text="Book ISBN:").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.isbn_var).pack(pady=5)
        
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="ISSUE", command=self.issue).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="CANCEL", command=self.destroy).pack(side="left", padx=10)

    def issue(self):
        roll_no = self.roll_var.get()
        isbn = self.isbn_var.get()
        
        if not roll_no or not isbn:
            CTkMessagebox(title="Error", message="Please fill all fields!")
            return
        
        issue_date = date.today().strftime('%Y-%m-%d')
        due_date = (date.today() + timedelta(days=14)).strftime('%Y-%m-%d')
        
        success = Database.issue_book_by_roll_isbn(roll_no, isbn, issue_date, due_date)
        if success:
            self.result = True
            self.destroy()

class ReturnDialog(ctk.CTkToplevel):
    def __init__(self, parent, issue_id):
        super().__init__()
        self.title("RETURN BOOK")
        self.geometry("300x150")
        self.result = None
        self.issue_id = issue_id
        self.transient(parent.parent_frame)
        self.grab_set()
        
        self.fine_var = ctk.StringVar(value="0")
        
        ctk.CTkLabel(self, text="Fine Amount:").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.fine_var).pack(pady=5)
        
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="RETURN", command=self.return_book).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="CANCEL", command=self.destroy).pack(side="left", padx=10)

    def return_book(self):
        fine_amount = float(self.fine_var.get() or 0)
        return_date = date.today().strftime('%Y-%m-%d')
        
        success = Database.return_book(self.issue_id, return_date, fine_amount)
        if success:
            self.result = True
            self.destroy()