import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from Database import Database
import datetime
from CTkTable import CTkTable


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

        # Title
        self.issue_return_label = ctk.CTkLabel(
            self.master,
            text="ISSUE & RETURN",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        )
        self.issue_return_label.grid(
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

        # Issue Book Button
        self.issue_btn = ctk.CTkButton(
            self.master,
            text="Issue Book",
            text_color="white",
            fg_color="#001a23",
            hover_color="#1b3430",
            font=("Segoe UI", 13, "bold"),
            corner_radius=5,
            width=180,
            height=30,
            command=self.issue_book_form,
            cursor="hand2",
        )
        self.issue_btn.grid(row=0, column=2, padx=15, pady=15)

        # Return Book Button
        self.return_btn = ctk.CTkButton(
            self.master,
            text="Return Book",
            text_color="white",
            fg_color="#001a23",
            font=("Segoe UI", 13, "bold"),
            hover_color="#1b3430",
            corner_radius=5,
            width=180,
            height=30,
            cursor="hand2",
            command=self.return_book_form,
        )
        self.return_btn.grid(row=0, column=3, padx=15, pady=15)

        # Data Frame for Active Issues
        self.data_frame = ctk.CTkScrollableFrame(
            self.master,
            fg_color="#1b3430",
            corner_radius=20,
        )
        self.data_frame.grid(row=1, columnspan=4, pady=15,
                             padx=15, sticky="nsew")

        # Load and display active issues
        self.load_active_issues()

    def load_active_issues(self):
        # Get active issues from database
        active_issues = Database.get_active_issues()

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
            ]
        ]

        # Add active issues to table data
        for issue in active_issues:
            table_data.append(list(issue))

        # Create CTkTable with same style as Books class
        self.issues_table = CTkTable(
            self.data_frame,
            values=table_data,
            wraplength=300,  # Same as Books class
        )
        self.issues_table.pack(expand=True)

    def issue_book_form(self):
        form = ctk.CTkToplevel(self.master)
        form.title("ISSUE BOOK FORM")
        form.geometry("450x500")
        form.resizable(False, False)
        form.configure(fg_color="#1b3430")
        form.transient(self.master)
        form.focus_force()

        # Center the form
        screen_width = form.winfo_screenwidth()
        screen_height = form.winfo_screenheight()
        window_width = 450
        window_height = 500
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        form.geometry(f"{window_width}x{
                      window_height}+{x_position}+{y_position}")

        # Form frame
        form_frame = ctk.CTkFrame(
            form, fg_color="#001a23", corner_radius=10, width=400, height=450
        )
        form_frame.pack(padx=20, pady=25, fill="both")

        # Title
        ctk.CTkLabel(
            form_frame,
            text="ISSUE BOOK FORM",
            font=("Segoe UI", 16, "bold"),
            text_color="white",
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Student Roll No
        ctk.CTkLabel(
            form_frame,
            text="STUDENT ROLL NO:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=1, column=0, sticky="w", padx=15, pady=10)
        self.student_roll = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.student_roll.grid(row=1, column=1, padx=15, pady=10)

        # Book ISBN
        ctk.CTkLabel(
            form_frame,
            text="BOOK ISBN:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=2, column=0, sticky="w", padx=15, pady=10)
        self.book_isbn = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.book_isbn.grid(row=2, column=1, padx=15, pady=10)

        # Issue Date
        ctk.CTkLabel(
            form_frame,
            text="ISSUE DATE:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=3, column=0, sticky="w", padx=15, pady=10)
        self.issue_date = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.issue_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.issue_date.grid(row=3, column=1, padx=15, pady=10)

        # Due Date
        ctk.CTkLabel(
            form_frame,
            text="DUE DATE:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=4, column=0, sticky="w", padx=15, pady=10)
        self.due_date = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        default_due_date = (
            datetime.datetime.now() + datetime.timedelta(days=15)
        ).strftime("%Y-%m-%d")
        self.due_date.insert(0, default_due_date)
        self.due_date.grid(row=4, column=1, padx=15, pady=10)

        # Validation labels
        self.student_info = ctk.CTkLabel(
            form_frame, text="", font=("Segoe UI", 10), text_color="#90EE90"
        )
        self.student_info.grid(row=5, column=0, columnspan=2, pady=5)

        self.book_info = ctk.CTkLabel(
            form_frame, text="", font=("Segoe UI", 10), text_color="#90EE90"
        )
        self.book_info.grid(row=6, column=0, columnspan=2, pady=5)

        # Buttons frame
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        # Submit button
        ctk.CTkButton(
            button_frame,
            text="Issue Book",
            text_color="white",
            fg_color="#001a23",
            hover_color="#1b3430",
            font=("Segoe UI", 13, "bold"),
            corner_radius=5,
            width=140,
            height=30,
            cursor="hand2",
            border_color="#1b3430",
            border_width=1,
            command=lambda: self.process_issue_book(form),
        ).grid(row=0, column=0, padx=10)

        # Exit button
        ctk.CTkButton(
            button_frame,
            text="Exit",
            text_color="white",
            fg_color="#001a23",
            border_color="#1b3430",
            border_width=1,
            hover_color="#1b3430",
            font=("Segoe UI", 13, "bold"),
            corner_radius=5,
            width=140,
            height=30,
            command=form.destroy,
            cursor="hand2",
        ).grid(row=0, column=1, padx=10)

        # Bind validation events
        self.student_roll.bind(
            "<KeyRelease>", lambda e: self.validate_student())
        self.book_isbn.bind("<KeyRelease>", lambda e: self.validate_book())

    def return_book_form(self):
        form = ctk.CTkToplevel(self.master)
        form.title("RETURN BOOK FORM")
        form.geometry("450x400")
        form.resizable(False, False)
        form.configure(fg_color="#1b3430")
        form.transient(self.master)
        form.focus_force()

        # Center the form
        screen_width = form.winfo_screenwidth()
        screen_height = form.winfo_screenheight()
        window_width = 450
        window_height = 400
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        form.geometry(f"{window_width}x{
                      window_height}+{x_position}+{y_position}")

        # Form frame
        form_frame = ctk.CTkFrame(
            form, fg_color="#001a23", corner_radius=10, width=400, height=350
        )
        form_frame.pack(padx=20, pady=25, fill="both")

        # Title
        ctk.CTkLabel(
            form_frame,
            text="RETURN BOOK FORM",
            font=("Segoe UI", 16, "bold"),
            text_color="white",
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Issue ID
        ctk.CTkLabel(
            form_frame,
            text="ISSUE ID:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=1, column=0, sticky="w", padx=15, pady=10)
        self.return_issue_id = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.return_issue_id.grid(row=1, column=1, padx=15, pady=10)

        # Return Date
        ctk.CTkLabel(
            form_frame,
            text="RETURN DATE:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=2, column=0, sticky="w", padx=15, pady=10)
        self.return_date = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.return_date.insert(
            0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.return_date.grid(row=2, column=1, padx=15, pady=10)

        # Fine Amount
        ctk.CTkLabel(
            form_frame,
            text="FINE AMOUNT:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=3, column=0, sticky="w", padx=15, pady=10)
        self.fine_amount = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.fine_amount.insert(0, "0.00")
        self.fine_amount.grid(row=3, column=1, padx=15, pady=10)

        # Buttons frame
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        # Submit button
        ctk.CTkButton(
            button_frame,
            text="Return Book",
            text_color="white",
            fg_color="#001a23",
            hover_color="#1b3430",
            font=("Segoe UI", 13, "bold"),
            corner_radius=5,
            width=140,
            height=30,
            cursor="hand2",
            border_color="#1b3430",
            border_width=1,
            command=lambda: self.process_return_book(form),
        ).grid(row=0, column=0, padx=10)

        # Exit button
        ctk.CTkButton(
            button_frame,
            text="Exit",
            text_color="white",
            fg_color="#001a23",
            border_color="#1b3430",
            border_width=1,
            hover_color="#1b3430",
            font=("Segoe UI", 13, "bold"),
            corner_radius=5,
            width=140,
            height=30,
            command=form.destroy,
            cursor="hand2",
        ).grid(row=0, column=1, padx=10)

    def validate_student(self):
        roll_no = self.student_roll.get().strip()
        if roll_no:
            student = Database.get_student_by_roll(roll_no)
            if student:
                self.student_info.configure(
                    text=f"✓ Student Found: {student[1]}", text_color="#90EE90"
                )
                return True
            else:
                self.student_info.configure(
                    text="✗ Student not found", text_color="#FF6B6B"
                )
                return False
        else:
            self.student_info.configure(text="")
            return False

    def validate_book(self):
        isbn = self.book_isbn.get().strip()
        if isbn:
            book = Database.get_book_by_isbn(isbn)
            if book:
                available_text = "Available" if book[2] > 0 else "Not Available"
                color = "#90EE90" if book[2] > 0 else "#FF6B6B"
                self.book_info.configure(
                    text=f"✓ Book Found: {book[1]} ({available_text})", text_color=color
                )
                return book[2] > 0
            else:
                self.book_info.configure(
                    text="✗ Book not found", text_color="#FF6B6B")
                return False
        else:
            self.book_info.configure(text="")
            return False

    def process_issue_book(self, form):
        try:
            roll_no = self.student_roll.get().strip()
            isbn = self.book_isbn.get().strip()
            issue_date = self.issue_date.get().strip()
            due_date = self.due_date.get().strip()

            if not all([roll_no, isbn, issue_date, due_date]):
                CTkMessagebox(title="Error", message="Please fill all fields!")
                return

            # Validate student and book
            if not self.validate_student() or not self.validate_book():
                CTkMessagebox(
                    title="Error", message="Please check student and book details!"
                )
                return

            student = Database.get_student_by_roll(roll_no)
            book = Database.get_book_by_isbn(isbn)

            # Issue the book
            if Database.issue_book(student[0], book[0], issue_date, due_date):
                CTkMessagebox(title="Success",
                              message="Book issued successfully!")
                form.destroy()
                self.load_active_issues()  # Refresh the table
            else:
                CTkMessagebox(title="Error", message="Failed to issue book!")

        except Exception as e:
            CTkMessagebox(
                title="Error", message=f"An error occurred: {str(e)}")

    def process_return_book(self, form):
        try:
            issue_id = self.return_issue_id.get().strip()
            return_date = self.return_date.get().strip()
            fine_amount = self.fine_amount.get().strip()

            if not all([issue_id, return_date, fine_amount]):
                CTkMessagebox(title="Error", message="Please fill all fields!")
                return

            if not issue_id.isdigit():
                CTkMessagebox(
                    title="Error", message="Issue ID must be a number!")
                return

            try:
                fine_amount = float(fine_amount)
            except ValueError:
                CTkMessagebox(
                    title="Error", message="Fine amount must be a number!")
                return

            # Return the book
            if Database.return_book(int(issue_id), return_date, fine_amount):
                CTkMessagebox(title="Success",
                              message="Book returned successfully!")
                form.destroy()
                self.load_active_issues()  # Refresh the table
            else:
                CTkMessagebox(title="Error", message="Failed to return book!")

        except Exception as e:
            CTkMessagebox(
                title="Error", message=f"An error occurred: {str(e)}")
