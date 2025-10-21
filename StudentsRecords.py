from CTkTable import CTkTable
import customtkinter as ctk
from Database import Database
import tkinter as tk
from CTkMessagebox import CTkMessagebox


class StudentRecord(ctk.CTkFrame):
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
        self.std_rec_lbl = ctk.CTkLabel(
            self.master,
            text="STUDENT RECORDS",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        )
        self.std_rec_lbl.grid(row=0, column=0, sticky="wn", padx=25, pady=18)
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
        self.submit_btn = ctk.CTkButton(
            self.master,
            text="Search",
            text_color="white",
            fg_color="#001a23",
            hover_color="#1b3430",
            font=("Segoe UI", 13, "bold"),
            corner_radius=5,
            width=180,
            height=30,
            command=self.search_std_dtls,
            cursor="hand2",
        )
        self.submit_btn.grid(row=0, column=2, padx=15, pady=15)

        self.add_std_dtls = ctk.CTkButton(
            self.master,
            text="Add Students",
            text_color="white",
            fg_color="#001a23",
            font=("Segoe UI", 13, "bold"),
            hover_color="#1b3430",
            corner_radius=5,
            width=180,
            height=30,
            cursor="hand2",
            command=self.add_students_dtls,
        )
        self.add_std_dtls.grid(row=0, column=3, padx=15, pady=15)
        self.data_frame = ctk.CTkScrollableFrame(
            self.master,
            fg_color="#1b3430",
            corner_radius=20,
        )
        self.data_frame.grid(row=1, columnspan=4, pady=15,
                             padx=15, sticky="nsew")

        self.std_data = Database.std_details()
        self.std_details = CTkTable(
            self.data_frame, values=self.std_data, wraplength=140
        )
        self.std_details.pack(expand=True)

    def search_std_dtls(self):
        self.std_roll = self.search_entry.get() if self.search_entry.get() else None
        data1 = Database.std_details(std_roll=self.std_roll)
        if data1:
            self.std_details.configure(values=data1)
        else:
            CTkMessagebox(title="Error", message="Please select a semester.")
        self.clear_std_dtls()

    def clear_std_dtls(self):
        self.search_entry.delete(0, tk.END)

    def add_students_dtls(self):
        form = ctk.CTkToplevel(self.master)
        form.title("STUDENT DETAILS FORM")
        form.geometry("450x500")
        form.resizable(False, False)
        form.configure(fg_color="#1b3430")
        form.transient(self.master)
        form.focus_force()

        # FIXED: Proper center positioning
        screen_width = form.winfo_screenwidth()
        screen_height = form.winfo_screenheight()
        window_width = 450
        window_height = 500
        x_position = (
            screen_width - window_width
        ) // 2  # Fixed: changed from // 1 to // 2
        y_position = (
            screen_height - window_height
        ) // 2  # Fixed: changed from // 1 to // 2
        form.geometry(f"{window_width}x{
                      window_height}+{x_position}+{y_position}")

        # Form frame
        form_frame = ctk.CTkFrame(form, fg_color="#001a23", corner_radius=10)
        form_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Configure form_frame grid for better layout
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        # Title - centered
        title_label = ctk.CTkLabel(
            form_frame,
            text="STUDENT DETAILS FORM",
            font=("Segoe UI", 16, "bold"),
            text_color="white",
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 20))

        # Student Roll No
        ctk.CTkLabel(
            form_frame,
            text="STUDENT ROLL NO:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=1, column=0, sticky="w", padx=15, pady=8)
        self.roll_no = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.roll_no.grid(row=1, column=1, padx=15, pady=8, sticky="w")

        # Name
        ctk.CTkLabel(
            form_frame, text="NAME:", font=("Segoe UI", 12, "bold"), text_color="white"
        ).grid(row=2, column=0, sticky="w", padx=15, pady=8)
        self.name = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.name.grid(row=2, column=1, padx=15, pady=8, sticky="w")

        # Email
        ctk.CTkLabel(
            form_frame, text="EMAIL:", font=("Segoe UI", 12, "bold"), text_color="white"
        ).grid(row=3, column=0, sticky="w", padx=15, pady=8)
        self.email = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.email.grid(row=3, column=1, padx=15, pady=8, sticky="w")

        # Phone
        ctk.CTkLabel(
            form_frame,
            text="STUDENT PHONENO:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=4, column=0, sticky="w", padx=15, pady=8)
        self.phone = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.phone.grid(row=4, column=1, padx=15, pady=8, sticky="w")

        # Address
        ctk.CTkLabel(
            form_frame,
            text="ADDRESS:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=5, column=0, sticky="w", padx=15, pady=8)
        self.address = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.address.grid(row=5, column=1, padx=15, pady=8, sticky="w")

        # Student Group
        ctk.CTkLabel(
            form_frame,
            text="STUDENT GROUP:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=6, column=0, sticky="w", padx=15, pady=8)
        self.group = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.group.grid(row=6, column=1, padx=15, pady=8, sticky="w")

        # Year
        ctk.CTkLabel(
            form_frame, text="YEAR:", font=("Segoe UI", 12, "bold"), text_color="white"
        ).grid(row=7, column=0, sticky="w", padx=15, pady=8)
        self.year = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 12),
            corner_radius=5,
            border_color="#1b3430",
            border_width=1,
            fg_color="#001a23",
            text_color="white",
            width=200,
        )
        self.year.grid(row=7, column=1, padx=15, pady=8, sticky="w")

        # Buttons frame
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Submit button
        ctk.CTkButton(
            button_frame,
            text="Submit",
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
            command=self.std_dtls_sub,
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
            height=35,
            command=form.destroy,
            cursor="hand2",
        ).grid(row=0, column=1, padx=10)

    def std_dtls_sub(self):
        rollno = self.roll_no.get()
        name = self.name.get()
        email = self.email.get()
        phone = self.phone.get()
        address = self.address.get()
        group = self.group.get()
        year = self.year.get()

        if Database.std_dtls_insert(
            rollno=rollno,
            name=name,
            email=email,
            phone=phone,
            address=address,
            group=group,
            year=year,
        ):
            # Refresh the table after successful insertion
            self.std_data = Database.std_details()
            self.std_details.configure(values=self.std_data)

        self.clearing_dtls()

    def clearing_dtls(self):
        self.roll_no.delete(0, tk.END)
        self.name.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.address.delete(0, tk.END)
        self.group.delete(0, tk.END)
        self.year.delete(0, tk.END)
