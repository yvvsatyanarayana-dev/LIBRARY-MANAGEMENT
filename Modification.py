import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from Database import Database
import tkinter as tk


class Modification(ctk.CTkFrame):
    def __init__(self, main):
        super().__init__(main)
        self.master = main
        self.current_table = "students"
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Configure grid
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        # Header - Consistent with your theme
        self.header_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="DATA MODIFICATION",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        )
        self.header_label.grid(row=0, column=0, sticky="w")

        # Main Content Frame - Using your app's colors
        self.main_frame = ctk.CTkFrame(
            self.master,
            fg_color="#31493c",
            corner_radius=10,
        )
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Top Controls Frame
        self.top_controls_frame = ctk.CTkFrame(
            self.main_frame, fg_color="transparent")
        self.top_controls_frame.grid(
            row=0, column=0, sticky="ew", padx=10, pady=5)
        self.top_controls_frame.grid_columnconfigure(0, weight=1)

        # Table Selection - Single row
        table_selection_frame = ctk.CTkFrame(
            self.top_controls_frame, fg_color="transparent"
        )
        table_selection_frame.grid(row=0, column=0, sticky="w", pady=5)

        ctk.CTkLabel(
            table_selection_frame,
            text="Select Table:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).pack(side="left", padx=(0, 10))

        self.table_var = ctk.StringVar(value="students")
        tables = [
            ("Students", "students"),
            ("Books", "books"),
            ("Transactions", "transactions"),
        ]

        for text, value in tables:
            btn = ctk.CTkButton(
                table_selection_frame,
                text=text,
                text_color="white",
                fg_color="#001a23",
                hover_color="#1b3430",
                font=("Segoe UI", 11, "bold"),
                corner_radius=8,
                height=32,
                command=lambda v=value: self.switch_table(v),
                cursor="hand2",
                border_width=1,
                border_color="#31493c",
            )
            btn.pack(side="left", padx=5)

        # Search and Actions - Single row
        self.search_action_frame = ctk.CTkFrame(
            self.top_controls_frame, fg_color="transparent"
        )
        self.search_action_frame.grid(row=1, column=0, sticky="ew", pady=5)
        self.search_action_frame.grid_columnconfigure(0, weight=1)

        # Search Entry
        self.search_entry = ctk.CTkEntry(
            self.search_action_frame,
            placeholder_text="Search...",
            placeholder_text_color="white",
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#001a23",
            border_width=1,
            fg_color="#1b3430",
            text_color="white",
            height=32,
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.search_entry.bind("<KeyRelease>", self.search_data)

        # Action Buttons Frame
        action_buttons_frame = ctk.CTkFrame(
            self.search_action_frame, fg_color="transparent"
        )
        action_buttons_frame.grid(row=0, column=1, sticky="e")

        # Add Button
        self.add_btn = ctk.CTkButton(
            action_buttons_frame,
            text="Add",
            text_color="white",
            fg_color="#001a23",
            hover_color="#1b3430",
            font=("Segoe UI", 11, "bold"),
            corner_radius=5,
            height=32,
            width=80,
            command=self.add_record,
            cursor="hand2",
        )
        self.add_btn.pack(side="left", padx=2)

        # Refresh Button
        self.refresh_btn = ctk.CTkButton(
            action_buttons_frame,
            text="Refresh",
            text_color="white",
            fg_color="#001a23",
            hover_color="#1b3430",
            font=("Segoe UI", 11, "bold"),
            corner_radius=5,
            height=32,
            width=80,
            command=self.load_data,
            cursor="hand2",
        )
        self.refresh_btn.pack(side="left", padx=2)

        # Data Display Frame - Takes most space
        self.data_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="#1b3430",
            corner_radius=10,
        )
        self.data_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.data_frame.grid_columnconfigure(0, weight=1)

    def switch_table(self, table_name):
        """Switch between different tables"""
        self.current_table = table_name
        self.search_entry.delete(0, tk.END)
        self.load_data()

    def load_data(self, search_term=None):
        """Load data based on current table"""
        try:
            # Clear existing data
            for widget in self.data_frame.winfo_children():
                widget.destroy()

            if self.current_table == "students":
                data = Database.std_details(search_term)
                self.display_students_data(data)
            elif self.current_table == "books":
                data = Database.books_data(search_term)
                self.display_books_data(data)
            elif self.current_table == "transactions":
                data = Database.get_all_transactions(search_term)
                self.display_transactions_data(data)

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error loading data: {str(e)}",
                icon="cancel",
            )

    def display_students_data(self, data):
        """Display students data with custom table"""
        if not data or len(data) <= 1:
            self.show_no_data_message()
            return

        self.create_aligned_table(data, "students")

    def display_books_data(self, data):
        """Display books data with custom table"""
        if not data or len(data) <= 1:
            self.show_no_data_message()
            return

        self.create_aligned_table(data, "books")

    def display_transactions_data(self, data):
        """Display transactions data with custom table"""
        if not data:
            self.show_no_data_message()
            return

        self.create_aligned_table(data, "transactions")

    def create_aligned_table(self, data, table_type):
        """Create a properly aligned table with consistent spacing"""
        try:
            # Define headers and column widths based on table type
            if table_type == "students":
                headers = [
                    "ROLL NO",
                    "NAME",
                    "EMAIL",
                    "PHONE",
                    "ADDRESS",
                    "GROUP",
                    "YEAR",
                    "ACTIONS",
                ]
                column_widths = [
                    100,
                    120,
                    180,
                    110,
                    150,
                    80,
                    60,
                    120,
                ]  # Fixed widths for perfect alignment
            elif table_type == "books":
                headers = [
                    "TITLE",
                    "AUTHOR",
                    "ISBN",
                    "CATEGORY",
                    "TOTAL COPIES",
                    "AVAILABLE COPIES",
                    "ACTIONS",
                ]
                column_widths = [150, 120, 120, 100, 90, 110, 120]
            else:  # transactions
                headers = [
                    "ISSUE ID",
                    "ROLL NO",
                    "STUDENT NAME",
                    "BOOK TITLE",
                    "ISBN",
                    "ISSUE DATE",
                    "DUE DATE",
                    "RETURN DATE",
                    "FINE AMOUNT",
                    "STATUS",
                ]
                column_widths = [80, 100, 120, 150,
                                 120, 100, 100, 100, 100, 80]

            # Create header container with fixed height
            header_container = ctk.CTkFrame(
                self.data_frame, fg_color="transparent")
            header_container.pack(fill="x", pady=(0, 5))

            # Create header frame
            header_frame = ctk.CTkFrame(
                header_container, fg_color="#001a23", height=45)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)

            # Create header labels with fixed widths for perfect alignment
            for i, (header, width) in enumerate(zip(headers, column_widths)):
                label = ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=("Segoe UI", 12, "bold"),
                    text_color="white",
                    width=width,
                    anchor="center"
                    if i == len(headers) - 1
                    else "w",  # Center actions, left-align others
                )
                if i == 0:
                    label.pack(side="left", padx=(10, 5), pady=12)
                elif i == len(headers) - 1:
                    label.pack(side="right", padx=(5, 10), pady=12)
                else:
                    label.pack(side="left", padx=5, pady=12)

            # Get data rows (skip header for students and books)
            if table_type in ["students", "books"]:
                data_rows = data[1:]
            else:
                data_rows = data

            # Create data rows
            for row_idx, row_data in enumerate(data_rows):
                row_color = "#1b3430" if row_idx % 2 == 0 else "#223b34"

                # Data row container
                row_container = ctk.CTkFrame(
                    self.data_frame, fg_color="transparent")
                row_container.pack(fill="x", pady=1)

                # Data row frame
                row_frame = ctk.CTkFrame(
                    row_container, fg_color=row_color, height=40)
                row_frame.pack(fill="x")
                row_frame.pack_propagate(False)

                # Get the record ID and display data
                if table_type == "students":
                    record_id = self.safe_get_value(row_data, 0)
                    display_data = [
                        self.safe_get_value(row_data, 1),  # ROLL NO
                        self.safe_get_value(row_data, 2),  # NAME
                        self.safe_get_value(row_data, 3),  # EMAIL
                        self.safe_get_value(row_data, 4),  # PHONE
                        self.safe_get_value(row_data, 5),  # ADDRESS
                        self.safe_get_value(row_data, 6),  # GROUP
                        self.safe_get_value(row_data, 7),  # YEAR
                    ]
                elif table_type == "books":
                    record_id = self.safe_get_value(row_data, 0)
                    display_data = [
                        self.safe_get_value(row_data, 1),  # TITLE
                        self.safe_get_value(row_data, 2),  # AUTHOR
                        self.safe_get_value(row_data, 3),  # ISBN
                        self.safe_get_value(row_data, 4),  # CATEGORY
                        self.safe_get_value(row_data, 5),  # TOTAL COPIES
                        self.safe_get_value(row_data, 6),  # AVAILABLE COPIES
                    ]
                else:  # transactions
                    record_id = self.safe_get_value(row_data, 0)
                    fine_amount = self.safe_get_value(row_data, 8)
                    fine_display = self.safe_format_fine(fine_amount)

                    display_data = [
                        self.safe_get_value(row_data, 0),  # ISSUE ID
                        self.safe_get_value(row_data, 1),  # ROLL NO
                        self.safe_get_value(row_data, 2),  # STUDENT NAME
                        self.safe_get_value(row_data, 3),  # BOOK TITLE
                        self.safe_get_value(row_data, 4),  # ISBN
                        self.safe_get_value(row_data, 5),  # ISSUE DATE
                        self.safe_get_value(row_data, 6),  # DUE DATE
                        self.safe_get_value(row_data, 7)
                        if self.safe_get_value(row_data, 7)
                        else "Not Returned",
                        fine_display,  # FINE AMOUNT
                        self.safe_get_value(row_data, 9),  # STATUS
                    ]

                # Create data labels with same widths as headers for perfect alignment
                for i, (cell_data, width) in enumerate(
                    zip(display_data, column_widths)
                ):
                    display_text = str(
                        cell_data) if cell_data is not None else ""
                    if len(display_text) > 25:
                        display_text = display_text[:22] + "..."

                    label = ctk.CTkLabel(
                        row_frame,
                        text=display_text,
                        font=("Segoe UI", 11),
                        text_color="white",
                        width=width,
                        anchor="w",  # Left align all data
                    )
                    if i == 0:
                        label.pack(side="left", padx=(10, 5), pady=8)
                    else:
                        label.pack(side="left", padx=5, pady=8)

                # Add actions buttons for students and books with proper spacing
                if table_type in ["students", "books"]:
                    actions_frame = ctk.CTkFrame(
                        row_frame, fg_color="transparent")
                    actions_frame.pack(side="right", padx=(5, 10))

                    edit_btn = ctk.CTkButton(
                        actions_frame,
                        text="Edit",
                        text_color="white",
                        fg_color="#001a23",
                        hover_color="#1b3430",
                        font=("Segoe UI", 10),
                        corner_radius=6,
                        height=28,
                        width=60,
                        command=lambda rid=record_id: self.edit_record(
                            rid, table_type[:-1]
                        ),
                        cursor="hand2",
                    )
                    edit_btn.pack(side="left", padx=2)

                    delete_btn = ctk.CTkButton(
                        actions_frame,
                        text="Delete",
                        text_color="white",
                        fg_color="#800f2f",
                        hover_color="#590d22",
                        font=("Segoe UI", 10),
                        corner_radius=6,
                        height=28,
                        width=60,
                        command=lambda rid=record_id: self.delete_record(
                            rid, table_type[:-1]
                        ),
                        cursor="hand2",
                    )
                    delete_btn.pack(side="left", padx=2)

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error displaying table: {str(e)}",
                icon="cancel",
            )

    def safe_get_value(self, row, index):
        """Safely get value from row with index checking"""
        try:
            if row is None:
                return ""
            if isinstance(row, (list, tuple)) and index < len(row):
                value = row[index]
                if value is None:
                    return ""
                return str(value)
            return ""
        except Exception:
            return ""

    def safe_format_fine(self, fine_value):
        """Very safe fine amount formatting"""
        try:
            if fine_value is None or fine_value == "":
                return "₹0.00"

            fine_str = str(fine_value).strip()

            if "₹" in fine_str:
                return fine_str

            try:
                fine_float = float(fine_str)
                return f"₹{fine_float:.2f}"
            except ValueError:
                return "₹0.00"

        except Exception:
            return "₹0.00"

    def edit_record(self, record_id, record_type):
        """Edit record based on type"""
        if record_type == "student":
            self.edit_student(record_id)
        elif record_type == "book":
            self.edit_book(record_id)

    def delete_record(self, record_id, record_type):
        """Delete record based on type"""
        if record_type == "student":
            self.delete_student(record_id)
        elif record_type == "book":
            self.delete_book(record_id)

    def show_no_data_message(self):
        """Show message when no data is available"""
        message_frame = ctk.CTkFrame(self.data_frame, fg_color="transparent")
        message_frame.pack(expand=True, fill="both", pady=40)

        ctk.CTkLabel(
            message_frame,
            text="📊",
            font=("Segoe UI", 48),
            text_color="white",
        ).pack(pady=10)

        ctk.CTkLabel(
            message_frame,
            text="No Data Available",
            font=("Segoe UI", 16, "bold"),
            text_color="white",
        ).pack(pady=5)

        ctk.CTkLabel(
            message_frame,
            text="No records found for the current selection.",
            font=("Segoe UI", 12),
            text_color="#CCCCCC",
        ).pack(pady=5)

    def search_data(self, event=None):
        """Search data based on current table"""
        search_term = self.search_entry.get().strip()
        if search_term:
            self.load_data(search_term)
        else:
            self.load_data()

    def add_record(self):
        """Open add record form based on current table"""
        self.master.after(100, self._open_add_form)

    def _open_add_form(self):
        """Open add form after delay to ensure window is viewable"""
        if self.current_table == "students":
            self.open_student_form()
        elif self.current_table == "books":
            self.open_book_form()

    def open_student_form(self, student_data=None):
        """Open student form for adding/editing"""
        try:
            form = ctk.CTkToplevel(self.master)
            form.title("Student Form" if not student_data else "Edit Student")
            form.geometry("500x600")
            form.resizable(False, False)
            form.configure(fg_color="#1b3430")
            form.transient(self.master)
            form.after(100, form.grab_set)
            self.center_window(form, 500, 600)

            # Form frame
            form_frame = ctk.CTkFrame(
                form, fg_color="#001a23", corner_radius=10)
            form_frame.pack(padx=20, pady=20, fill="both", expand=True)

            # Title
            title = "ADD STUDENT" if not student_data else "EDIT STUDENT"
            ctk.CTkLabel(
                form_frame,
                text=title,
                font=("Segoe UI", 18, "bold"),
                text_color="white",
            ).pack(pady=20)

            # Scrollable form content
            form_content = ctk.CTkScrollableFrame(
                form_frame, fg_color="transparent")
            form_content.pack(fill="both", expand=True, padx=20, pady=10)

            # Form fields
            fields = [
                ("Student Roll No:", "roll_no"),
                ("Name:", "name"),
                ("Email:", "email"),
                ("Phone:", "phone"),
                ("Address:", "address"),
                ("Group:", "group"),
                ("Year:", "year"),
            ]

            self.form_entries = {}
            for label, field in fields:
                field_frame = ctk.CTkFrame(
                    form_content, fg_color="transparent")
                field_frame.pack(fill="x", pady=8)

                ctk.CTkLabel(
                    field_frame,
                    text=label,
                    font=("Segoe UI", 12, "bold"),
                    text_color="white",
                ).pack(anchor="w")

                entry = ctk.CTkEntry(
                    field_frame,
                    font=("Segoe UI", 12),
                    corner_radius=5,
                    border_color="#1b3430",
                    border_width=1,
                    fg_color="#001a23",
                    text_color="white",
                    height=35,
                )
                entry.pack(fill="x", pady=5)
                self.form_entries[field] = entry

                # Fill data if editing
                if student_data:
                    if field == "roll_no":
                        entry.insert(0, self.safe_get_value(student_data, 1))
                    elif field == "name":
                        entry.insert(0, self.safe_get_value(student_data, 2))
                    elif field == "email":
                        entry.insert(0, self.safe_get_value(student_data, 3))
                    elif field == "phone":
                        entry.insert(0, self.safe_get_value(student_data, 4))
                    elif field == "address":
                        entry.insert(0, self.safe_get_value(student_data, 5))
                    elif field == "group":
                        entry.insert(0, self.safe_get_value(student_data, 6))
                    elif field == "year":
                        entry.insert(0, self.safe_get_value(student_data, 7))

            # Buttons frame
            button_frame = ctk.CTkFrame(form_content, fg_color="transparent")
            button_frame.pack(fill="x", pady=20)

            submit_text = "Add Student" if not student_data else "Update Student"
            submit_command = (
                lambda: self.submit_student(form)
                if not student_data
                else lambda: self.update_student(
                    self.safe_get_value(student_data, 0), form
                )
            )

            ctk.CTkButton(
                button_frame,
                text=submit_text,
                text_color="white",
                fg_color="#001a23",
                hover_color="#1b3430",
                font=("Segoe UI", 12, "bold"),
                corner_radius=5,
                height=35,
                command=submit_command,
                cursor="hand2",
            ).pack(side="left", padx=5, fill="x", expand=True)

            ctk.CTkButton(
                button_frame,
                text="Cancel",
                text_color="white",
                fg_color="#800f2f",
                hover_color="#590d22",
                font=("Segoe UI", 12, "bold"),
                corner_radius=5,
                height=35,
                command=form.destroy,
                cursor="hand2",
            ).pack(side="left", padx=5, fill="x", expand=True)

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error opening form: {str(e)}",
                icon="cancel",
            )

    def submit_student(self, form):
        """Submit new student data"""
        try:
            data = {
                field: entry.get().strip() for field, entry in self.form_entries.items()
            }

            if Database.std_dtls_insert(
                data["roll_no"],
                data["name"],
                data["email"],
                data["phone"],
                data["address"],
                data["group"],
                data["year"],
            ):
                form.destroy()
                self.load_data()

        except Exception as e:
            CTkMessagebox(
                title="Error", message=f"Error adding student: {str(e)}", icon="cancel"
            )

    def update_student(self, student_id, form):
        """Update student data"""
        try:
            CTkMessagebox(
                title="Info",
                message="Update functionality would be implemented here",
                icon="info",
            )
            form.destroy()
            self.load_data()

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error updating student: {str(e)}",
                icon="cancel",
            )

    def edit_student(self, student_id):
        """Edit student record"""
        try:
            data = Database.std_details()
            student_data = None
            for row in data[1:]:
                if str(row[0]) == str(student_id):
                    student_data = row
                    break

            if student_data:
                self.open_student_form(student_data)

        except Exception as e:
            CTkMessagebox(
                title="Error", message=f"Error editing student: {str(e)}", icon="cancel"
            )

    def edit_book(self, book_id):
        """Edit book record"""
        try:
            data = Database.books_data()
            book_data = None
            for row in data[1:]:
                if str(row[0]) == str(book_id):
                    book_data = row
                    break

            if book_data:
                self.open_book_form(book_data)

        except Exception as e:
            CTkMessagebox(
                title="Error", message=f"Error editing book: {str(e)}", icon="cancel"
            )

    def delete_student(self, student_id):
        """Delete student record"""
        confirm = CTkMessagebox(
            title="Confirm Delete",
            message="Are you sure you want to delete this student?",
            icon="question",
            option_1="Cancel",
            option_2="Delete",
        )

        if confirm.get() == "Delete":
            try:
                CTkMessagebox(
                    title="Info",
                    message="Delete functionality would be implemented here",
                    icon="info",
                )
                self.load_data()

            except Exception as e:
                CTkMessagebox(
                    title="Error",
                    message=f"Error deleting student: {str(e)}",
                    icon="cancel",
                )

    def delete_book(self, book_id):
        """Delete book record"""
        confirm = CTkMessagebox(
            title="Confirm Delete",
            message="Are you sure you want to delete this book?",
            icon="question",
            option_1="Cancel",
            option_2="Delete",
        )

        if confirm.get() == "Delete":
            try:
                CTkMessagebox(
                    title="Info",
                    message="Delete functionality would be implemented here",
                    icon="info",
                )
                self.load_data()

            except Exception as e:
                CTkMessagebox(
                    title="Error",
                    message=f"Error deleting book: {str(e)}",
                    icon="cancel",
                )

    def center_window(self, window, width, height):
        """Center a window on the screen"""
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def open_book_form(self, book_data=None):
        """Open book form for adding/editing"""
        try:
            form = ctk.CTkToplevel(self.master)
            form.title("Book Form" if not book_data else "Edit Book")
            form.geometry("500x500")
            form.resizable(False, False)
            form.configure(fg_color="#1b3430")
            form.transient(self.master)
            form.after(100, form.grab_set)
            self.center_window(form, 500, 500)

            # Form frame
            form_frame = ctk.CTkFrame(
                form, fg_color="#001a23", corner_radius=10)
            form_frame.pack(padx=20, pady=20, fill="both", expand=True)

            # Title
            title = "ADD BOOK" if not book_data else "EDIT BOOK"
            ctk.CTkLabel(
                form_frame,
                text=title,
                font=("Segoe UI", 18, "bold"),
                text_color="white",
            ).pack(pady=20)

            # Scrollable form content
            form_content = ctk.CTkScrollableFrame(
                form_frame, fg_color="transparent")
            form_content.pack(fill="both", expand=True, padx=20, pady=10)

            # Form fields
            fields = [
                ("ISBN:", "isbn"),
                ("Title:", "title"),
                ("Author:", "author"),
                ("Category:", "category"),
                ("Total Copies:", "copies"),
            ]

            self.book_form_entries = {}
            for label, field in fields:
                field_frame = ctk.CTkFrame(
                    form_content, fg_color="transparent")
                field_frame.pack(fill="x", pady=8)

                ctk.CTkLabel(
                    field_frame,
                    text=label,
                    font=("Segoe UI", 12, "bold"),
                    text_color="white",
                ).pack(anchor="w")

                entry = ctk.CTkEntry(
                    field_frame,
                    font=("Segoe UI", 12),
                    corner_radius=5,
                    border_color="#1b3430",
                    border_width=1,
                    fg_color="#001a23",
                    text_color="white",
                    height=35,
                )
                entry.pack(fill="x", pady=5)
                self.book_form_entries[field] = entry

                # Fill data if editing
                if book_data:
                    if field == "isbn":
                        entry.insert(0, self.safe_get_value(book_data, 3))
                    elif field == "title":
                        entry.insert(0, self.safe_get_value(book_data, 1))
                    elif field == "author":
                        entry.insert(0, self.safe_get_value(book_data, 2))
                    elif field == "category":
                        entry.insert(0, self.safe_get_value(book_data, 4))
                    elif field == "copies":
                        entry.insert(0, self.safe_get_value(book_data, 5))

            # Buttons frame
            button_frame = ctk.CTkFrame(form_content, fg_color="transparent")
            button_frame.pack(fill="x", pady=20)

            submit_text = "Add Book" if not book_data else "Update Book"
            submit_command = (
                lambda: self.submit_book(form)
                if not book_data
                else lambda: self.update_book(book_data[0], form)
            )

            ctk.CTkButton(
                button_frame,
                text=submit_text,
                text_color="white",
                fg_color="#001a23",
                hover_color="#1b3430",
                font=("Segoe UI", 12, "bold"),
                corner_radius=5,
                height=35,
                command=submit_command,
                cursor="hand2",
            ).pack(side="left", padx=5, fill="x", expand=True)

            ctk.CTkButton(
                button_frame,
                text="Cancel",
                text_color="white",
                fg_color="#800f2f",
                hover_color="#590d22",
                font=("Segoe UI", 12, "bold"),
                corner_radius=5,
                height=35,
                command=form.destroy,
                cursor="hand2",
            ).pack(side="left", padx=5, fill="x", expand=True)

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error opening form: {str(e)}",
                icon="cancel",
            )

    def submit_book(self, form):
        """Submit new book data"""
        try:
            data = {
                field: entry.get().strip()
                for field, entry in self.book_form_entries.items()
            }

            if Database.add_book(
                data["isbn"],
                data["title"],
                data["author"],
                data["category"],
                int(data["copies"]),
            ):
                form.destroy()
                self.load_data()

        except Exception as e:
            CTkMessagebox(
                title="Error", message=f"Error adding book: {str(e)}", icon="cancel"
            )

    def update_book(self, book_id, form):
        """Update book data"""
        try:
            CTkMessagebox(
                title="Info",
                message="Update functionality would be implemented here",
                icon="info",
            )
            form.destroy()
            self.load_data()

        except Exception as e:
            CTkMessagebox(
                title="Error", message=f"Error updating book: {str(e)}", icon="cancel"
            )
