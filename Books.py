import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from Database import Database
from CTkTable import CTkTable


class Books(ctk.CTkFrame):
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
        self.books_label = ctk.CTkLabel(
            self.master,
            text="BOOKS",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        )
        self.books_label.grid(row=0, column=0, sticky="wn", padx=25, pady=18)

        # Search Entry
        self.search_entry = ctk.CTkEntry(
            self.master,
            placeholder_text="Search by ISBN",
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
            command=self.search_books,
            cursor="hand2",
        )
        self.search_btn.grid(row=0, column=2, padx=15, pady=15)

        # Add Book Button
        self.add_btn = ctk.CTkButton(
            self.master,
            text="Add Book",
            text_color="white",
            fg_color="#001a23",
            font=("Segoe UI", 13, "bold"),
            hover_color="#1b3430",
            corner_radius=5,
            width=180,
            height=30,
            cursor="hand2",
            command=self.add_book_form,
        )
        self.add_btn.grid(row=0, column=3, padx=15, pady=15)

        # Data Frame
        self.data_frame = ctk.CTkScrollableFrame(
            self.master,
            fg_color="#1b3430",
            corner_radius=20,
        )
        self.data_frame.grid(row=1, columnspan=4, pady=15,
                             padx=15, sticky="nsew")

        # Load and display all books
        self.load_books()

    def load_books(self, isbn=None):
        """Load books from database and display in table"""
        try:
            # Get books data from database
            books_data = Database.books_data(isbn)

            # Create CTkTable
            if hasattr(self, "books_table"):
                self.books_table.destroy()

            self.books_table = CTkTable(
                self.data_frame,
                values=books_data,
                wraplength=300,
            )
            self.books_table.pack(expand=True, fill="both", padx=10, pady=10)

        except Exception as e:
            CTkMessagebox(
                title="Error", message=f"Error loading books: {str(e)}", icon="cancel"
            )

    def search_books(self):
        """Search books by ISBN"""
        isbn = self.search_entry.get().strip()
        if isbn:
            self.load_books(isbn)
            if len(Database.books_data(isbn)) > 1:  # More than just headers
                CTkMessagebox(
                    title="Info",
                    message=f"Showing results for ISBN: {isbn}",
                    icon="info",
                )
            else:
                CTkMessagebox(
                    title="Info",
                    message="No books found with that ISBN",
                    icon="warning",
                )
        else:
            self.load_books()  # Load all books if search is empty
            CTkMessagebox(
                title="Info", message="Showing all books", icon="info")

    def add_book_form(self):
        """Open form to add a new book"""
        form = ctk.CTkToplevel(self.master)
        form.title("ADD BOOK FORM")
        form.geometry("500x600")
        form.resizable(False, False)
        form.configure(fg_color="#1b3430")
        form.transient(self.master)
        form.focus_force()

        # Center the form
        screen_width = form.winfo_screenwidth()
        screen_height = form.winfo_screenheight()
        window_width = 500
        window_height = 600
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        form.geometry(f"{window_width}x{
                      window_height}+{x_position}+{y_position}")

        # Form frame
        form_frame = ctk.CTkFrame(
            form, fg_color="#001a23", corner_radius=10, width=450, height=550
        )
        form_frame.pack(padx=20, pady=25, fill="both", expand=True)

        # Title
        ctk.CTkLabel(
            form_frame,
            text="ADD NEW BOOK",
            font=("Segoe UI", 18, "bold"),
            text_color="white",
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # ISBN
        ctk.CTkLabel(
            form_frame,
            text="ISBN:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.isbn_entry = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=250,
        )
        self.isbn_entry.grid(row=1, column=1, padx=20, pady=10)

        # Title
        ctk.CTkLabel(
            form_frame,
            text="BOOK TITLE:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=2, column=0, sticky="w", padx=20, pady=10)
        self.title_entry = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=250,
        )
        self.title_entry.grid(row=2, column=1, padx=20, pady=10)

        # Author
        ctk.CTkLabel(
            form_frame,
            text="AUTHOR:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=3, column=0, sticky="w", padx=20, pady=10)
        self.author_entry = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=250,
        )
        self.author_entry.grid(row=3, column=1, padx=20, pady=10)

        # Category
        ctk.CTkLabel(
            form_frame,
            text="CATEGORY:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=4, column=0, sticky="w", padx=20, pady=10)
        self.category_entry = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=250,
        )
        self.category_entry.grid(row=4, column=1, padx=20, pady=10)

        # Total Copies
        ctk.CTkLabel(
            form_frame,
            text="TOTAL COPIES:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=5, column=0, sticky="w", padx=20, pady=10)
        self.copies_entry = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=250,
        )
        self.copies_entry.grid(row=5, column=1, padx=20, pady=10)

        # Validation message
        self.validation_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=("Segoe UI", 10),
            text_color="#90EE90",
        )
        self.validation_label.grid(row=6, column=0, columnspan=2, pady=5)

        # Buttons frame
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=7, column=0, columnspan=2, pady=30)

        # Submit button
        ctk.CTkButton(
            button_frame,
            text="Add Book",
            text_color="white",
            fg_color="#001a23",
            hover_color="#1b3430",
            font=("Segoe UI", 13, "bold"),
            corner_radius=5,
            width=140,
            height=35,
            cursor="hand2",
            border_color="#1b3430",
            border_width=1,
            command=lambda: self.process_add_book(form),
        ).grid(row=0, column=0, padx=10)

        # Clear button
        ctk.CTkButton(
            button_frame,
            text="Clear",
            text_color="white",
            fg_color="#001a23",
            border_color="#1b3430",
            border_width=1,
            hover_color="#1b3430",
            font=("Segoe UI", 13, "bold"),
            corner_radius=5,
            width=140,
            height=35,
            command=self.clear_form,
            cursor="hand2",
        ).grid(row=0, column=1, padx=10)

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
            height=35,
            command=form.destroy,
            cursor="hand2",
        ).grid(row=0, column=2, padx=10)

    def clear_form(self):
        """Clear all form fields"""
        self.isbn_entry.delete(0, ctk.END)
        self.title_entry.delete(0, ctk.END)
        self.author_entry.delete(0, ctk.END)
        self.category_entry.delete(0, ctk.END)
        self.copies_entry.delete(0, ctk.END)
        self.validation_label.configure(text="")

    def validate_form(self):
        """Validate form inputs"""
        isbn = self.isbn_entry.get().strip()
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        category = self.category_entry.get().strip()
        copies = self.copies_entry.get().strip()

        # Check if all fields are filled
        if not all([isbn, title, author, category, copies]):
            self.validation_label.configure(
                text="❌ Please fill all fields", text_color="#FF6B6B"
            )
            return False

        # Check if copies is a valid number
        try:
            copies_int = int(copies)
            if copies_int <= 0:
                self.validation_label.configure(
                    text="❌ Copies must be a positive number", text_color="#FF6B6B"
                )
                return False
        except ValueError:
            self.validation_label.configure(
                text="❌ Copies must be a valid number", text_color="#FF6B6B"
            )
            return False

        self.validation_label.configure(
            text="✅ Form is valid", text_color="#90EE90")
        return True

    def process_add_book(self, form):
        """Process adding the book to database"""
        try:
            if not self.validate_form():
                return

            isbn = self.isbn_entry.get().strip()
            title = self.title_entry.get().strip()
            author = self.author_entry.get().strip()
            category = self.category_entry.get().strip()
            copies = int(self.copies_entry.get().strip())

            # Check if book with same ISBN already exists
            existing_books = Database.books_data(isbn)
            if len(existing_books) > 1:  # More than just headers
                CTkMessagebox(
                    title="Error",
                    message="A book with this ISBN already exists!",
                    icon="warning",
                )
                return

            # Add book to database using your existing Database method
            if Database.add_book(isbn, title, author, category, copies):
                CTkMessagebox(
                    title="Success", message="Book added successfully!", icon="check"
                )
                form.destroy()
                self.load_books()  # Refresh the books table
            else:
                CTkMessagebox(
                    title="Error", message="Failed to add book!", icon="cancel"
                )

        except Exception as e:
            CTkMessagebox(
                title="Error", message=f"An error occurred: {str(e)}", icon="cancel"
            )

