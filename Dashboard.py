import customtkinter as ctk
import os
from PIL import Image
import datetime
from Database import Database
import IssueReturn
from StudentsRecords import StudentRecord
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random as rand
from Books import Books
from IssueReturn import IssueReturn
from Transaction import Transaction  # ADD THIS IMPORT
from Reports import Reports
from Mailing import Mailing


class Dashboard(ctk.CTkToplevel):
    ctk.set_appearance_mode("light")

    def __init__(self, parent):
        super().__init__(parent)
        self.title("DASHBOARD")
        self.geometry("1200x700")  # Set a reasonable default size
        self._set_window_icon()  # Fixed icon loading

        # Maximize the window properly for CTkToplevel
        self._maximize_window()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.request = self.quotes_req()
        self.create_widgets()

    def _maximize_window(self):
        """Maximize the window in a way that works with CTkToplevel"""
        try:
            # Method 1: Try to maximize using tkinter method
            self.attributes("-zoomed", True)
        except:
            try:
                # Method 2: Try to set fullscreen
                self.attributes("-fullscreen", True)
            except:
                # Method 3: Fallback - get screen dimensions and set window size
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                self.geometry(f"{screen_width}x{screen_height}+0+0")

    def _set_window_icon(self):
        """Set window icon with proper error handling"""
        icon_path = os.path.abspath("Assets/Ideal-College.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception as e:
                print(f"Could not load icon: {e}")
                # Try alternative method
                try:
                    img = Image.open(icon_path)
                    from PIL import ImageTk

                    photo = ImageTk.PhotoImage(img)
                    self.wm_iconphoto(True, photo)
                except Exception as e2:
                    print(f"Alternative icon method also failed: {e2}")
        else:
            print(f"Icon file not found: {icon_path}")

    def create_widgets(self):
        self.images()

        # Header Frame
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="#001a23",
            height=60,
            corner_radius=10,
        )
        self.header_frame.grid(
            row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.header_frame.grid_columnconfigure(1, weight=1)

        # College Name
        self.clg_name = ctk.CTkLabel(
            self.header_frame,
            text="IDEAL COLLEGE OF ARTS & SCIENCES",
            font=("Segoe UI", 17, "bold"),
            text_color="white",
        )
        self.clg_name.grid(row=0, column=0, pady=15, sticky="nw", padx=50)

        # Date Time
        self.date_time = ctk.CTkLabel(
            self.header_frame,
            text=f"{datetime.datetime.now().strftime('%d/%m/%Y')} {
                datetime.datetime.now().strftime('%H:%M:%S')
            }",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        )
        self.date_time.grid(row=0, column=2, padx=20, pady=15, sticky="ne")

        # Main Content Area
        self.back_frame = ctk.CTkFrame(
            self,
            fg_color="#31493c",
            corner_radius=10,
        )
        self.back_frame.grid(row=1, column=0, sticky="nsew",
                             padx=10, pady=(10, 10))
        self.back_frame.grid_rowconfigure(0, weight=1)
        self.back_frame.grid_columnconfigure(1, weight=1)

        # Menu Frame
        self.menu_frame = ctk.CTkFrame(
            self.back_frame,
            fg_color="#001a23",
            corner_radius=10,
            width=200,
        )
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=10)
        self.menu_frame.grid_propagate(False)

        # Logo
        self.logo = ctk.CTkLabel(
            self.menu_frame,
            image=self.logo_img,
            text="",
        )
        self.logo.grid(row=0, column=0, pady=10)

        # Dashboard Button
        self.dashboard_btn = ctk.CTkButton(
            self.menu_frame,
            text="Dashboard         ",
            compound="left",
            image=self.dashicon,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",
            cursor="hand2",
            width=180,
            command=self.dashboard_content,
        )
        self.dashboard_btn.grid(row=1, column=0, padx=10,
                                pady=(30, 0), sticky="w")

        # Student Record Button
        self.student_rec = ctk.CTkButton(
            self.menu_frame,
            text="STUDENT RECORD",
            compound="left",
            image=self.student_record,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",
            cursor="hand2",
            width=180,
            command=self.students_records,
        )
        self.student_rec.grid(row=2, column=0, padx=10,
                              pady=(20, 0), sticky="w")

        # Books Button
        self.book_btn = ctk.CTkButton(
            self.menu_frame,
            text="BOOKS             ",
            compound="left",
            image=self.book,
            width=180,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",
            cursor="hand2",
            command=self.student_book,
        )
        self.book_btn.grid(row=3, column=0, padx=10, pady=(20, 0), sticky="w")

        # Issue & Return Button
        self.issue_re_btn = ctk.CTkButton(
            self.menu_frame,
            text="ISSUE & RETURN",
            compound="left",
            image=self.issue_return,
            width=180,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",
            cursor="hand2",
            command=self.issue_return_func,
        )
        self.issue_re_btn.grid(row=4, column=0, padx=10,
                               pady=(20, 0), sticky="w")

        # Transaction Button - UPDATED WITH COMMAND
        self.transaction_btn = ctk.CTkButton(
            self.menu_frame,
            text="TRANSACTION",
            compound="left",
            image=self.transaction_list,
            width=180,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",
            cursor="hand2",
            command=self.transaction_func,  # ADDED COMMAND
        )
        self.transaction_btn.grid(
            row=5, column=0, padx=10, pady=(20, 0), sticky="w")

        # Reports Button
        self.reports_btn = ctk.CTkButton(
            self.menu_frame,
            text="REPORTS                 ",
            image=self.reports,
            width=180,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",
            cursor="hand2",
            command=self.reports_func,
        )
        self.reports_btn.grid(row=6, column=0, padx=10,
                              pady=(20, 0), sticky="w")

        # Mailing Button
        self.mailing_btn = ctk.CTkButton(
            self.menu_frame,
            text="MAILING            ",
            image=self.mail,
            width=180,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",
            cursor="hand2",
            command=self.mailing_func,
        )
        self.mailing_btn.grid(row=7, column=0, padx=10,
                              pady=(20, 0), sticky="w")

        # Modification button
        self.modification_btn = ctk.CTkButton(
            self.menu_frame,
            text="MODIFICATION",
            image=self.modification_img,
            corner_radius=10,
            width=180,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",
            cursor="hand2",
        )
        self.modification_btn.grid(
            row=8, column=0, padx=10, pady=(20, 0), sticky="w")

        # Logout Button
        self.logout_btn = ctk.CTkButton(
            self.menu_frame,
            image=self.logout,
            text="LOGOUT",
            height=30,
            width=150,
            fg_color="#001a23",
            hover_color="#2e3532",
            font=("Segoe UI", 10, "bold"),
            corner_radius=10,
            command=self.close,
        )
        self.logout_btn.grid(row=9, column=0, padx=20,
                             pady=(40, 0), sticky="w")

        # Main Content Frame
        self.main_frame = ctk.CTkFrame(
            self.back_frame, fg_color="#001a23", corner_radius=10
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.dashboard_content()

    def dashboard_content(self):
        # ... (your existing dashboard content code remains the same)
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(4, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        ################## FRAME 1 ##########################
        self.frame1 = ctk.CTkFrame(
            self.main_frame,
            corner_radius=30,
            fg_color="#31493c",
        )
        self.frame1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame1.grid_rowconfigure(0, weight=1)
        self.frame1.grid_rowconfigure(1, weight=1)
        self.frame1.grid_rowconfigure(2, weight=1)

        self.image = ctk.CTkLabel(
            self.frame1,
            image=self.students,
            text="",
        )
        self.image.grid(column=0, row=0, padx=5, pady=(10, 0))

        self.label1 = Database.total_std()
        self.total_std = ctk.CTkLabel(
            self.frame1,
            text=f"{self.label1}",
            font=("Segoe UI", 35, "bold"),
            text_color="white",
        )
        self.total_std.grid(column=0, row=1, padx=5, pady=(5, 5))

        self.std_label = ctk.CTkLabel(
            self.frame1,
            text="TOTAL STUDENTS",
            font=("Segoe UI", 15, "bold"),
            text_color="white",
        )
        self.std_label.grid(column=0, row=2, padx=5, pady=(1, 5))

        ################## FRAME 2 ########################
        self.total_book_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=30,
        )
        self.total_book_frame.grid(
            column=1, row=0, padx=20, pady=20, sticky="nsew")
        self.total_book_frame.grid_columnconfigure(0, weight=1)
        self.total_book_frame.grid_rowconfigure(0, weight=1)
        self.total_book_frame.grid_rowconfigure(1, weight=1)
        self.total_book_frame.grid_rowconfigure(2, weight=1)

        self.total_book_img = ctk.CTkLabel(
            self.total_book_frame, text="", image=self.total_books_img
        )
        self.total_book_img.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.lable2 = Database.Books()
        self.total_book_db = ctk.CTkLabel(
            self.total_book_frame,
            text=f"{self.lable2}",
            font=("Segoe UI", 35, "bold"),
            text_color="white",
        )
        self.total_book_db.grid(row=1, column=0, padx=5, pady=(5, 5))

        self.total_book_label = ctk.CTkLabel(
            self.total_book_frame,
            text="TOTAL BOOKS",
            font=("Segoe UI", 15, "bold"),
            text_color="white",
        )
        self.total_book_label.grid(row=2, column=0, padx=5, pady=(1, 5))

        ############## FRAME 3 #####################
        self.issued_bookd_frame = ctk.CTkFrame(
            self.main_frame, fg_color="#31493c", corner_radius=30
        )
        self.issued_bookd_frame.grid(
            column=2, row=0, padx=20, pady=20, sticky="nsew")
        self.issued_bookd_frame.grid_columnconfigure(0, weight=1)
        self.issued_bookd_frame.grid_rowconfigure(0, weight=1)
        self.issued_bookd_frame.grid_rowconfigure(1, weight=1)
        self.issued_bookd_frame.grid_rowconfigure(2, weight=1)

        self.issued_book_img = ctk.CTkLabel(
            self.issued_bookd_frame, image=self.inword_books, text=""
        )
        self.issued_book_img.grid(row=0, column=0, pady=10, padx=(10, 0))

        self.label3 = Database.total_inwords()
        self.issued_book_db = ctk.CTkLabel(
            self.issued_bookd_frame,
            text=f"{self.label3}",
            font=("Segoe UI", 35, "bold"),
            text_color="white",
        )
        self.issued_book_db.grid(row=1, column=0, padx=5, pady=(5, 5))

        self.issued_book_label = ctk.CTkLabel(
            self.issued_bookd_frame,
            text="TOTAL INWORDS",
            font=("Segoe UI", 15, "bold"),
            text_color="white",
        )
        self.issued_book_label.grid(row=2, column=0, padx=1, pady=(1, 5))

        ############## FRAME 4 #######################
        self.return_book_frame = ctk.CTkFrame(
            self.main_frame, fg_color="#31493c", corner_radius=30
        )
        self.return_book_frame.grid(
            column=3, row=0, padx=20, pady=20, sticky="nsew")
        self.return_book_frame.grid_columnconfigure(0, weight=1)
        self.return_book_frame.grid_rowconfigure(0, weight=1)
        self.return_book_frame.grid_rowconfigure(1, weight=1)
        self.return_book_frame.grid_rowconfigure(2, weight=1)

        self.return_img = ctk.CTkLabel(
            self.return_book_frame, image=self.outword_img, text=""
        )
        self.return_img.grid(column=0, row=0, padx=10, pady=(10, 0))

        self.label4 = Database.total_outwords()
        self.return_book_db = ctk.CTkLabel(
            self.return_book_frame,
            text=f"{self.label4}",
            font=("Segoe UI", 35, "bold"),
            text_color="white",
        )
        self.return_book_db.grid(row=1, column=0, padx=5, pady=(5, 5))

        self.return_book_label = ctk.CTkLabel(
            self.return_book_frame,
            text="TOTAL OUTWORDS",
            font=("Segoe UI", 15, "bold"),
            text_color="white",
        )
        self.return_book_label.grid(row=2, column=0, padx=5, pady=(2, 5))

        ############### FRAME 5 ####################
        self.graph_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=30,
            height=220,
        )
        self.graph_frame.grid(
            row=1, column=0, columnspan=3, padx=20, pady=(0, 20), sticky="nsew"
        )
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graph_frame.grid_rowconfigure(0, weight=1)

        # Fetch data from database
        student_data = Database.students_per_group()
        total_books = Database.total_books()

        # Prepare data for plotting
        groups = [row[0] for row in student_data]
        counts = [row[1] for row in student_data]
        all_groups = ["Science", "Arts", "BCA", "AI_CS", "BBA", "Total Books"]
        group_counts = {group: 0 for group in all_groups[:-1]}
        for group, count in student_data:
            if group in group_counts:
                group_counts[group] = count
        groups = all_groups
        counts = [group_counts.get(group, 0) for group in all_groups[:-1]] + [
            total_books
        ]

        # Create Matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 3))
        bars = ax.bar(
            groups,
            counts,
            color=["#4CAF50", "#2196F3", "#FF9800",
                   "#F44336", "#9C27B0", "#795548"],
            edgecolor="white",
            linewidth=0.5,
        )

        # Styling the graph
        ax.set_title(
            "STUDENTS PER GROUP AND TOTAL BOOKS",
            fontsize=14,
            color="white",
            pad=10,
            fontweight="bold",
        )
        ax.set_facecolor("#31493c")
        fig.patch.set_facecolor("#31493c")

        # Remove y-axis label and tick labels
        ax.set_ylabel("")
        ax.set_yticklabels([])
        ax.set_ylim(0, max(counts) + 2)

        # Adjust x-axis
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=0, colors="white", labelsize=10)

        # Add gridlines
        ax.grid(True, axis="y", linestyle="-", color="white", alpha=0.2)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
                color="white",
                fontsize=10,
            )

        # Remove spines for a cleaner look
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("white")
        ax.spines["bottom"].set_color("white")

        # Embed in graph_frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)

        ################# FRAME 6 ###################
        self.info_frame = ctk.CTkFrame(
            self.main_frame, fg_color="#31493c", corner_radius=10, height=150
        )
        self.info_frame.grid(row=1, column=3, padx=20,
                             pady=(0, 20), sticky="nsew")
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_rowconfigure(0, weight=1)
        self.info_frame.grid_rowconfigure(1, weight=1)
        self.info_frame.grid_rowconfigure(2, weight=1)

        self.quote_label = ctk.CTkLabel(
            self.info_frame,
            text="QUOTE OF THE DAY",
            font=("Segoe UI", 15, "bold"),
            text_color="white",
        )
        self.quote_label.grid(row=0, column=0)

        self.request = self.quotes_req()
        self.request_quote = ctk.CTkLabel(
            self.info_frame,
            text=self.request,
            font=("Segoe UI", 12, "bold"),
            text_color="white",
            wraplength=200,
            justify="center",
        )
        self.request_quote.grid(row=1, column=0)

    def students_records(self):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        self.layer_frame1 = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=10,
        )
        self.layer_frame1.grid(
            row=0, column=0, sticky="nsew", padx=15, pady=15, columnspan=5, rowspan=2
        )
        StudentRecord(self.layer_frame1)

    def student_book(self):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        self.layer_frame2 = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=10,
        )
        self.layer_frame2.grid(
            row=0, column=0, sticky="nsew", padx=15, pady=15, columnspan=5, rowspan=2
        )
        Books(self.layer_frame2)

    def issue_return_func(self):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        self.layer_frame3 = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=10,
        )
        self.layer_frame3.grid(
            row=0, column=0, sticky="nsew", padx=15, pady=15, columnspan=5, rowspan=2
        )
        IssueReturn(self.layer_frame3)

    def transaction_func(self):  # ADD THIS METHOD
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        self.layer_frame4 = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=10,
        )
        self.layer_frame4.grid(
            row=0, column=0, sticky="nsew", padx=15, pady=15, columnspan=5, rowspan=2
        )
        Transaction(self.layer_frame4)

    def reports_func(self):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        self.layer_frame5 = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=10,
        )
        self.layer_frame5.grid(
            row=0, column=0, sticky="nsew", padx=15, pady=15, columnspan=5, rowspan=2
        )
        Reports(self.layer_frame5)

    def mailing_func(self):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        self.mailing_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=10,
        )
        self.mailing_frame.grid(
            row=0, column=0, sticky="nsew", padx=15, pady=15, columnspan=5, rowspan=2
        )
        Mailing(self.mailing_frame)

    def close(self):
        self.destroy()

    def images(self):
        # ... (your existing images method remains the same)
        # FIXED: Use CTkImage instead of ImageTk.PhotoImage
        try:
            logo = Image.open("Assets/Ideal-College.png")
            self.logo_img = ctk.CTkImage(
                light_image=logo, dark_image=logo, size=(185, 140)
            )

            logout = Image.open("Assets/logout.png")
            self.logout = ctk.CTkImage(
                light_image=logout, dark_image=logout, size=(30, 30)
            )

            dashicon = Image.open("Assets/icons8-home-24.png")
            self.dashicon = ctk.CTkImage(
                light_image=dashicon, dark_image=dashicon, size=(24, 24)
            )

            stduent_rec = Image.open("Assets/student_records.png")
            self.student_record = ctk.CTkImage(
                light_image=stduent_rec, dark_image=stduent_rec, size=(30, 30)
            )

            book = Image.open("Assets/open-book.png")
            self.book = ctk.CTkImage(
                light_image=book, dark_image=book, size=(30, 30))

            issue = Image.open("Assets/return-box.png")
            self.issue_return = ctk.CTkImage(
                light_image=issue, dark_image=issue, size=(30, 30)
            )

            transaction = Image.open("Assets/transaction-history.png")
            self.transaction_list = ctk.CTkImage(
                light_image=transaction, dark_image=transaction, size=(30, 30)
            )

            reports = Image.open("Assets/report.png")
            self.reports = ctk.CTkImage(
                light_image=reports, dark_image=reports, size=(30, 30)
            )

            mail = Image.open("Assets/mail.png")
            self.mail = ctk.CTkImage(
                light_image=mail, dark_image=mail, size=(30, 30))

            modification = Image.open("Assets/modification.png")
            self.modification_img = ctk.CTkImage(
                light_image=modification, dark_image=modification, size=(
                    30, 30)
            )

            students = Image.open("Assets/students.png")
            self.students = ctk.CTkImage(
                light_image=students, dark_image=students, size=(100, 100)
            )

            return_book = Image.open("Assets/return-book.png")
            self.return_book = ctk.CTkImage(
                light_image=return_book, dark_image=return_book, size=(
                    100, 100)
            )

            inword_books = Image.open("Assets/inword.png")
            self.inword_books = ctk.CTkImage(
                light_image=inword_books, dark_image=inword_books, size=(
                    80, 80)
            )

            outword = Image.open("Assets/outword.png")
            self.outword_img = ctk.CTkImage(
                light_image=outword, dark_image=outword, size=(80, 80)
            )

            totoal_books = Image.open("Assets/open-book.png")
            self.total_books_img = ctk.CTkImage(
                light_image=totoal_books, dark_image=totoal_books, size=(
                    100, 100)
            )
        except Exception as e:
            print(f"Error loading images: {e}")

    def quotes_req(self):
        education_quotes = [
            '"Education is the key to unlocking the world." - Oprah Winfrey',
            '"Learn as if you\'ll live forever." - Mahatma Gandhi',
            '"Knowledge is power." - Francis Bacon',
            '"Education shapes the future." - Malala Yousafzai',
            '"Study hard, grow wise." - Benjamin Franklin',
            '"The mind is a fire to be kindled." - Plutarch',
            '"Education opens doors." - W.E.B. Du Bois',
            '"Grow through what you learn." - Socrates',
            '"Reality doesn\'t bend to your wishes." - Jordan Peterson',
            '"Life is suffering; find meaning in it." - Viktor Frankl',
            '"Truth hurts, but lies destroy." - Warren Buffett',
            '"The world owes you nothing." - Mark Twain',
            '"Failure is the default; success is earned." - Elon Musk',
            '"Time waits for no one." - Geoffrey Chaucer',
        ]
        return rand.choice(education_quotes)
