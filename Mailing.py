import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from Database import Database
import re
import datetime
from typing import List, Tuple


class Mailing(ctk.CTkFrame):
    def __init__(self, main):
        super().__init__(main)
        self.master = main
        self.setup_email_config()
        self.create_widgets()

    def setup_email_config(self):
        self.smtp_config = {
            "server": "smtp.gmail.com",
            "port": 587,
            "username": "darkofmyside@gmail.com",  # Change this
            "password": "fbjc ayix bgaj agew",  # Change this
            "from_name": "Library Management System",
        }

    def create_widgets(self):
        # Configure grid
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        # Header - using your app's color scheme
        self.header_label = ctk.CTkLabel(
            self.master,
            text="✉️ STUDENT MAILING SYSTEM",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        )
        self.header_label.grid(row=0, column=0, sticky="w", padx=25, pady=20)

        # Main container with tabs - using your app's colors
        self.tabview = ctk.CTkTabview(
            self.master,
            fg_color="#1b3430",  # Your dark green color
            segmented_button_fg_color="#001a23",  # Your darker green
            segmented_button_selected_color="#31493c",  # Your medium green
            segmented_button_unselected_color="#001a23",  # Your darker green
        )
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # Create tabs
        self.manual_tab = self.tabview.add("Manual Email")
        self.reminder_tab = self.tabview.add("Overdue Reminders")

        self.setup_manual_email_tab()
        self.setup_reminder_tab()

    def setup_manual_email_tab(self):
        # Configure tab grid
        self.manual_tab.grid_columnconfigure(0, weight=1)

        # Recipient selection
        ctk.CTkLabel(
            self.manual_tab,
            text="Select Recipients:",
            font=("Segoe UI", 14, "bold"),
            text_color="white",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        self.recipient_var = ctk.StringVar(value="all")
        recipient_frame = ctk.CTkFrame(self.manual_tab, fg_color="transparent")
        recipient_frame.grid(row=1, column=0, sticky="w", padx=20, pady=5)

        ctk.CTkRadioButton(
            recipient_frame,
            text="All Students",
            variable=self.recipient_var,
            value="all",
            font=("Segoe UI", 12),
            text_color="white",
            fg_color="#31493c",  # Your green color
            hover_color="#1b3430",  # Your dark green
        ).pack(side="left", padx=10)

        ctk.CTkRadioButton(
            recipient_frame,
            text="By Group",
            variable=self.recipient_var,
            value="group",
            font=("Segoe UI", 12),
            text_color="white",
            fg_color="#31493c",
            hover_color="#1b3430",
        ).pack(side="left", padx=10)

        ctk.CTkRadioButton(
            recipient_frame,
            text="Individual Student",
            variable=self.recipient_var,
            value="individual",
            font=("Segoe UI", 12),
            text_color="white",
            fg_color="#31493c",
            hover_color="#1b3430",
        ).pack(side="left", padx=10)

        # Group selection
        self.group_frame = ctk.CTkFrame(
            self.manual_tab, fg_color="transparent")
        self.group_frame.grid(row=2, column=0, sticky="w", padx=20, pady=5)
        self.group_frame.grid_remove()

        ctk.CTkLabel(
            self.group_frame,
            text="Select Group:",
            font=("Segoe UI", 12),
            text_color="white",
        ).pack(side="left", padx=5)

        self.group_var = ctk.StringVar(value="")
        self.group_dropdown = ctk.CTkComboBox(
            self.group_frame,
            values=self.get_student_groups(),
            variable=self.group_var,
            font=("Segoe UI", 12),
            state="readonly",
            width=200,
            fg_color="#001a23",  # Your dark color
            button_color="#31493c",  # Your green
            button_hover_color="#1b3430",  # Your dark green
            text_color="white",
        )
        self.group_dropdown.pack(side="left", padx=10)

        # Individual student selection
        self.individual_frame = ctk.CTkFrame(
            self.manual_tab, fg_color="transparent")
        self.individual_frame.grid(
            row=3, column=0, sticky="w", padx=20, pady=5)
        self.individual_frame.grid_remove()

        ctk.CTkLabel(
            self.individual_frame,
            text="Student Roll No:",
            font=("Segoe UI", 12),
            text_color="white",
        ).pack(side="left", padx=5)

        self.student_roll_var = ctk.StringVar()
        self.student_entry = ctk.CTkEntry(
            self.individual_frame,
            textvariable=self.student_roll_var,
            font=("Segoe UI", 12),
            width=150,
            placeholder_text="Enter roll number",
            fg_color="#001a23",  # Your dark color
            border_color="#31493c",  # Your green
            text_color="white",
        )
        self.student_entry.pack(side="left", padx=10)

        self.check_student_btn = ctk.CTkButton(
            self.individual_frame,
            text="Check",
            font=("Segoe UI", 11),
            height=30,
            command=self.check_student,
            fg_color="#31493c",  # Your green
            hover_color="#1b3430",  # Your dark green
        )
        self.check_student_btn.pack(side="left", padx=10)

        self.student_info_label = ctk.CTkLabel(
            self.individual_frame,
            text="",
            font=("Segoe UI", 11),
            text_color="#90EE90",
        )
        self.student_info_label.pack(side="left", padx=10)

        # Email composition
        ctk.CTkLabel(
            self.manual_tab,
            text="Subject:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=4, column=0, sticky="w", padx=20, pady=(20, 5))

        self.subject_var = ctk.StringVar()
        self.subject_entry = ctk.CTkEntry(
            self.manual_tab,
            textvariable=self.subject_var,
            font=("Segoe UI", 12),
            placeholder_text="Enter email subject",
            height=35,
            fg_color="#001a23",  # Your dark color
            border_color="#31493c",  # Your green
            text_color="white",
        )
        self.subject_entry.grid(row=5, column=0, sticky="ew", padx=20, pady=5)

        ctk.CTkLabel(
            self.manual_tab,
            text="Message:",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
        ).grid(row=6, column=0, sticky="w", padx=20, pady=(20, 5))

        self.message_text = ctk.CTkTextbox(
            self.manual_tab,
            font=("Segoe UI", 12),
            height=150,
            fg_color="#001a23",  # Your dark color
            border_color="#31493c",  # Your green
            text_color="white",
        )
        self.message_text.grid(row=7, column=0, sticky="nsew", padx=20, pady=5)
        self.message_text.insert("1.0", "Dear student,\n\n")

        # Sender email
        ctk.CTkLabel(
            self.manual_tab,
            text="Sender Email:",
            font=("Segoe UI", 12),
            text_color="white",
        ).grid(row=8, column=0, sticky="w", padx=20, pady=(20, 5))

        self.sender_email_var = ctk.StringVar(
            value=self.smtp_config["username"])
        self.sender_entry = ctk.CTkEntry(
            self.manual_tab,
            textvariable=self.sender_email_var,
            font=("Segoe UI", 12),
            width=300,
            fg_color="#001a23",  # Your dark color
            border_color="#31493c",  # Your green
            text_color="white",
        )
        self.sender_entry.grid(row=9, column=0, sticky="w", padx=20, pady=5)

        # Buttons
        button_frame = ctk.CTkFrame(self.manual_tab, fg_color="transparent")
        button_frame.grid(row=10, column=0, pady=20)

        self.preview_btn = ctk.CTkButton(
            button_frame,
            text="Preview Email",
            font=("Segoe UI", 12, "bold"),
            height=40,
            width=150,
            command=self.preview_email,
            fg_color="#31493c",  # Your green
            hover_color="#1b3430",  # Your dark green
        )
        self.preview_btn.pack(side="left", padx=10)

        self.send_btn = ctk.CTkButton(
            button_frame,
            text="Send Email",
            font=("Segoe UI", 12, "bold"),
            height=40,
            width=150,
            command=self.send_email,
            fg_color="#31493c",  # Your green
            hover_color="#1b3430",  # Your dark green
        )
        self.send_btn.pack(side="left", padx=10)

        # Progress
        self.progress_frame = ctk.CTkFrame(
            self.manual_tab, fg_color="transparent")
        self.progress_frame.grid(row=11, column=0, pady=10)
        self.progress_frame.grid_remove()

        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="",
            font=("Segoe UI", 11),
            text_color="white",
        )
        self.progress_label.pack()

        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=400,
            progress_color="#31493c",  # Your green
        )
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)

        # Bind recipient type change
        self.recipient_var.trace("w", self.on_recipient_change)

    def setup_reminder_tab(self):
        # Configure tab grid
        self.reminder_tab.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            self.reminder_tab,
            text="Overdue Book Reminders",
            font=("Segoe UI", 16, "bold"),
            text_color="white",
        ).grid(row=0, column=0, pady=20)

        # Description
        ctk.CTkLabel(
            self.reminder_tab,
            text="Send automatic reminder emails to students with overdue books",
            font=("Segoe UI", 12),
            text_color="lightgray",
        ).grid(row=1, column=0, pady=10)

        # Overdue books list
        self.overdue_list_frame = ctk.CTkFrame(
            self.reminder_tab,
            fg_color="#001a23",  # Your dark color
        )
        self.overdue_list_frame.grid(
            row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.overdue_list_frame.grid_columnconfigure(0, weight=1)

        # Load overdue books
        self.load_overdue_books()

        # Buttons
        button_frame = ctk.CTkFrame(self.reminder_tab, fg_color="transparent")
        button_frame.grid(row=3, column=0, pady=20)

        self.preview_reminder_btn = ctk.CTkButton(
            button_frame,
            text="Preview Reminder",
            font=("Segoe UI", 12, "bold"),
            height=40,
            width=150,
            command=self.preview_reminder_email,
            fg_color="#31493c",  # Your green
            hover_color="#1b3430",  # Your dark green
        )
        self.preview_reminder_btn.pack(side="left", padx=10)

        self.send_reminders_btn = ctk.CTkButton(
            button_frame,
            text="Send Reminders",
            font=("Segoe UI", 12, "bold"),
            height=40,
            width=150,
            command=self.send_overdue_reminders,
            fg_color="#800f2f",  # Your red/maroon color from login
            hover_color="#590d22",  # Your dark red
        )
        self.send_reminders_btn.pack(side="left", padx=10)

        # Progress
        self.reminder_progress_frame = ctk.CTkFrame(
            self.reminder_tab, fg_color="transparent"
        )
        self.reminder_progress_frame.grid(row=4, column=0, pady=10)
        self.reminder_progress_frame.grid_remove()

        self.reminder_progress_label = ctk.CTkLabel(
            self.reminder_progress_frame,
            text="",
            font=("Segoe UI", 11),
            text_color="white",
        )
        self.reminder_progress_label.pack()

        self.reminder_progress_bar = ctk.CTkProgressBar(
            self.reminder_progress_frame,
            width=400,
            progress_color="#31493c",  # Your green
        )
        self.reminder_progress_bar.pack(pady=5)
        self.reminder_progress_bar.set(0)

    def load_overdue_books(self):
        try:
            # Clear existing widgets
            for widget in self.overdue_list_frame.winfo_children():
                widget.destroy()

            overdue_books = self.get_overdue_books()

            if not overdue_books:
                ctk.CTkLabel(
                    self.overdue_list_frame,
                    text="✅ No overdue books found!",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#90EE90",
                ).pack(expand=True, pady=40)
                return

            # Create scrollable frame
            scroll_frame = ctk.CTkScrollableFrame(
                self.overdue_list_frame,
                height=200,
                fg_color="#001a23",  # Your dark color
            )
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

            for i, (
                student_name,
                student_email,
                book_title,
                due_date,
                days_overdue,
            ) in enumerate(overdue_books):
                book_frame = ctk.CTkFrame(
                    scroll_frame,
                    fg_color="#1b3430",  # Your dark green
                )
                book_frame.pack(fill="x", padx=5, pady=2)

                info_text = f"📖 {book_title} | 👤 {student_name} | 📧 {
                    student_email
                } | 📅 Due: {due_date} | ⏰ {days_overdue} days overdue"

                ctk.CTkLabel(
                    book_frame,
                    text=info_text,
                    font=("Segoe UI", 10),
                    text_color="white",
                    anchor="w",
                ).pack(fill="x", padx=10, pady=5)

            # Update send button text
            self.send_reminders_btn.configure(
                text=f"Send Reminders ({len(overdue_books)} students)"
            )

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Failed to load overdue books: {str(e)}",
                icon="cancel",
            )

    def get_overdue_books(self) -> List[Tuple]:
        try:
            # Use your existing Database class methods
            conn = Database.connect()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    s.name as student_name,
                    s.email as student_email,
                    b.title as book_title,
                    ir.due_date,
                    DATEDIFF(CURDATE(), ir.due_date) as days_overdue,
                    ir.issue_id
                FROM Issue_Return ir
                JOIN Students s ON ir.student_id = s.student_id
                JOIN Books b ON ir.book_id = b.book_id
                WHERE ir.status = 'Issued' 
                AND ir.due_date < CURDATE()
                AND s.email IS NOT NULL 
                AND s.email != ''
                ORDER BY days_overdue DESC
            """)

            results = cursor.fetchall()
            cursor.close()
            conn.close()

            return results

        except Exception as e:
            print(f"Error getting overdue books: {e}")
            return []

    def get_student_groups(self):
        try:
            conn = Database.connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT student_group FROM Students ORDER BY student_group"
            )
            groups = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            return groups if groups else ["No groups found"]
        except Exception as e:
            return ["Error loading groups"]

    def on_recipient_change(self, *args):
        recipient_type = self.recipient_var.get()

        # Hide all frames first
        self.group_frame.grid_remove()
        self.individual_frame.grid_remove()

        # Show selected frame
        if recipient_type == "group":
            self.group_frame.grid()
        elif recipient_type == "individual":
            self.individual_frame.grid()

    def check_student(self):
        roll_no = self.student_roll_var.get().strip()
        if not roll_no:
            CTkMessagebox(
                title="Error", message="Please enter a roll number", icon="warning"
            )
            return

        try:
            # Use your existing Database.std_details method
            student_data = Database.std_details(roll_no)
            if student_data and len(student_data) > 1:
                student = student_data[1]  # First data row after header
                name = student[2]  # Name column
                email = student[3]  # Email column

                if email:
                    self.student_info_label.configure(
                        text=f"✅ {name} - {email}", text_color="#90EE90"
                    )
                else:
                    self.student_info_label.configure(
                        text=f"✅ {name} - No email", text_color="#FF9800"
                    )
            else:
                self.student_info_label.configure(
                    text="❌ Student not found", text_color="#f44336"
                )
        except Exception as e:
            CTkMessagebox(
                title="Error", message=f"Database error: {str(e)}", icon="cancel"
            )

    def get_recipient_emails(self):
        """Get email addresses based on recipient selection - using your Database class"""
        recipient_type = self.recipient_var.get()

        try:
            conn = Database.connect()
            cursor = conn.cursor()

            if recipient_type == "all":
                cursor.execute(
                    "SELECT email, name FROM Students WHERE email IS NOT NULL AND email != ''"
                )
            elif recipient_type == "group":
                group = self.group_var.get()
                if not group or group == "No groups found":
                    return []
                cursor.execute(
                    "SELECT email, name FROM Students WHERE student_group = %s AND email IS NOT NULL AND email != ''",
                    (group,),
                )
            elif recipient_type == "individual":
                roll_no = self.student_roll_var.get().strip()
                if not roll_no:
                    return []
                cursor.execute(
                    "SELECT email, name FROM Students WHERE student_roll_no = %s AND email IS NOT NULL AND email != ''",
                    (roll_no,),
                )

            results = cursor.fetchall()
            cursor.close()
            conn.close()

            return [
                (email, name) for email, name in results if self.is_valid_email(email)
            ]

        except Exception as e:
            return []

    def is_valid_email(self, email):
        if not email or not isinstance(email, str):
            return False
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email.strip()) is not None

    def preview_email(self):
        recipients = self.get_recipient_emails()
        subject = self.subject_var.get().strip()
        message = self.message_text.get("1.0", "end-1c").strip()

        if not subject:
            CTkMessagebox(
                title="Error", message="Please enter a subject", icon="warning"
            )
            return

        if not message:
            CTkMessagebox(
                title="Error", message="Please enter a message", icon="warning"
            )
            return

        if not recipients:
            CTkMessagebox(
                title="Error", message="No valid recipients found", icon="warning"
            )
            return

        preview_text = f"""
        📧 EMAIL PREVIEW
        {"=" * 50}
        To: {len(recipients)} recipient(s)
        Subject: {subject}
        {"=" * 50}
        Message:
        {message}
        {"=" * 50}

        Recipients:
        {", ".join([name for _, name in recipients])}
        """

        self.show_preview_window("Email Preview", preview_text)

    def preview_reminder_email(self):
        overdue_books = self.get_overdue_books()

        if not overdue_books:
            CTkMessagebox(
                title="Info",
                message="No overdue books found to send reminders for.",
                icon="info",
            )
            return

        sample_student = overdue_books[0]
        student_name = sample_student[0]
        book_title = sample_student[2]
        due_date = sample_student[3]
        days_overdue = sample_student[4]

        subject = "Library Book Overdue Notice"
        message = self.generate_overdue_message(
            student_name, book_title, due_date, days_overdue
        )

        preview_text = f"""
        📧 OVERDUE REMINDER PREVIEW
        {"=" * 50}
        To: {len(overdue_books)} student(s) with overdue books
        Subject: {subject}
        {"=" * 50}
        Sample Message:
        {message}
        {"=" * 50}

        This reminder will be sent to {len(overdue_books)} students.
        """

        self.show_preview_window("Overdue Reminder Preview", preview_text)

    def generate_overdue_message(
        self, student_name: str, book_title: str, due_date: str, days_overdue: int
    ) -> str:
        return f"""Dear {student_name},

This is a reminder from the Library Management System regarding your overdue book.

Book Details:
Title: {book_title}
Due Date: {due_date}
Days Overdue: {days_overdue}

Please return the book to the library as soon as possible to avoid additional fines.

If you have already returned the book, please ignore this message.

For any questions, please contact the library.

Best regards,
Library Management System
Ideal College of Arts & Sciences"""

    def show_preview_window(self, title: str, content: str):
        """Show preview window with given content"""
        preview_window = ctk.CTkToplevel(self.master)
        preview_window.title(title)
        preview_window.geometry("600x500")
        preview_window.transient(self.master)
        preview_window.grab_set()

        ctk.CTkLabel(
            preview_window,
            text=title,
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=15)

        preview_textbox = ctk.CTkTextbox(
            preview_window, font=("Segoe UI", 12), width=550, height=400
        )
        preview_textbox.pack(padx=20, pady=10, fill="both", expand=True)
        preview_textbox.insert("1.0", content)
        preview_textbox.configure(state="disabled")

    def send_email(self):
        """Send manual email to selected recipients"""
        recipients = self.get_recipient_emails()
        subject = self.subject_var.get().strip()
        message = self.message_text.get("1.0", "end-1c").strip()
        sender_email = self.sender_email_var.get().strip()

        # Validation
        if not subject:
            CTkMessagebox(
                title="Error", message="Please enter a subject", icon="warning"
            )
            return

        if not message:
            CTkMessagebox(
                title="Error", message="Please enter a message", icon="warning"
            )
            return

        if not recipients:
            CTkMessagebox(
                title="Error", message="No valid recipients found", icon="warning"
            )
            return

        if not sender_email or not self.is_valid_email(sender_email):
            CTkMessagebox(
                title="Error",
                message="Please enter a valid sender email",
                icon="warning",
            )
            return

        confirm = CTkMessagebox(
            title="Confirm Send",
            message=f"Send this email to {len(recipients)} recipient(s)?",
            icon="question",
            option_1="Cancel",
            option_2="Send",
        )

        if confirm.get() == "Cancel":
            return

        # Start sending in separate thread
        self.progress_frame.grid()
        self.progress_bar.set(0)
        self.progress_label.configure(text="Preparing to send emails...")

        threading.Thread(
            target=self._send_emails_thread,
            args=(recipients, subject, message, sender_email),
            daemon=True,
        ).start()

    def send_overdue_reminders(self):
        """Send overdue reminder emails"""
        overdue_books = self.get_overdue_books()

        if not overdue_books:
            CTkMessagebox(
                title="Info",
                message="No overdue books found to send reminders for.",
                icon="info",
            )
            return

        confirm = CTkMessagebox(
            title="Confirm Send",
            message=f"Send overdue reminders to {
                len(overdue_books)} student(s)?",
            icon="question",
            option_1="Cancel",
            option_2="Send",
        )

        if confirm.get() == "Cancel":
            return

        # Start sending in separate thread
        self.reminder_progress_frame.grid()
        self.reminder_progress_bar.set(0)
        self.reminder_progress_label.configure(
            text="Preparing to send reminders...")

        threading.Thread(
            target=self._send_overdue_reminders_thread,
            args=(overdue_books,),
            daemon=True,
        ).start()

    def _send_emails_thread(self, recipients, subject, message, sender_email):
        try:
            self.smtp_config["username"] = sender_email

            server = smtplib.SMTP(
                self.smtp_config["server"], self.smtp_config["port"])
            server.starttls()
            server.login(self.smtp_config["username"],
                         self.smtp_config["password"])

            total_recipients = len(recipients)
            successful_sends = 0
            failed_sends = []

            for i, (email, name) in enumerate(recipients):
                try:
                    progress = i / total_recipients
                    self.progress_bar.set(progress)
                    self.progress_label.configure(
                        text=f"Sending to {
                            name}... ({i + 1}/{total_recipients})"
                    )

                    msg = MIMEMultipart()
                    msg["From"] = f"{self.smtp_config['from_name']} <{
                        sender_email}>"
                    msg["To"] = email
                    msg["Subject"] = subject

                    personalized_message = message.replace("[Name]", name)
                    msg.attach(MIMEText(personalized_message, "plain"))

                    server.sendmail(sender_email, email, msg.as_string())
                    successful_sends += 1

                except Exception as e:
                    failed_sends.append((name, email, str(e)))

            server.quit()
            self.progress_bar.set(1.0)

            result_message = (
                f"✅ Successfully sent: {successful_sends}/{total_recipients}"
            )
            if failed_sends:
                result_message += f"\n\n❌ Failed sends:\n"
                for name, email, error in failed_sends:
                    result_message += f"• {name} ({email}): {error}\n"

            self.progress_label.configure(text=result_message)
            CTkMessagebox(title="Send Complete",
                          message=result_message, icon="info")

        except Exception as e:
            self.progress_label.configure(text=f"❌ Error: {str(e)}")
            CTkMessagebox(
                title="Send Failed",
                message=f"Failed to send emails: {str(e)}",
                icon="cancel",
            )

    def _send_overdue_reminders_thread(self, overdue_books):
        try:
            sender_email = self.smtp_config["username"]

            server = smtplib.SMTP(
                self.smtp_config["server"], self.smtp_config["port"])
            server.starttls()
            server.login(self.smtp_config["username"],
                         self.smtp_config["password"])

            total_recipients = len(overdue_books)
            successful_sends = 0
            failed_sends = []

            for i, (
                student_name,
                student_email,
                book_title,
                due_date,
                days_overdue,
                issue_id,
            ) in enumerate(overdue_books):
                try:
                    progress = i / total_recipients
                    self.reminder_progress_bar.set(progress)
                    self.reminder_progress_label.configure(
                        text=f"Sending reminder to {student_name}... ({i + 1}/{
                            total_recipients
                        })"
                    )

                    subject = "Library Book Overdue Notice"
                    message = self.generate_overdue_message(
                        student_name, book_title, due_date, days_overdue
                    )

                    msg = MIMEMultipart()
                    msg["From"] = f"{self.smtp_config['from_name']} <{
                        sender_email}>"
                    msg["To"] = student_email
                    msg["Subject"] = subject

                    msg.attach(MIMEText(message, "plain"))

                    server.sendmail(
                        sender_email, student_email, msg.as_string())
                    successful_sends += 1

                except Exception as e:
                    failed_sends.append((student_name, student_email, str(e)))

            server.quit()
            self.reminder_progress_bar.set(1.0)

            result_message = (
                f"✅ Successfully sent reminders: {
                    successful_sends}/{total_recipients}"
            )
            if failed_sends:
                result_message += f"\n\n❌ Failed sends:\n"
                for name, email, error in failed_sends:
                    result_message += f"• {name} ({email}): {error}\n"

            self.reminder_progress_label.configure(text=result_message)
            CTkMessagebox(title="Reminders Sent",
                          message=result_message, icon="info")

        except Exception as e:
            self.reminder_progress_label.configure(text=f"❌ Error: {str(e)}")
            CTkMessagebox(
                title="Send Failed",
                message=f"Failed to send reminders: {str(e)}",
                icon="cancel",
            )
