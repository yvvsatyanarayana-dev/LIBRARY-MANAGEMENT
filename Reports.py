import customtkinter as ctk
from Database import Database
from CTkMessagebox import CTkMessagebox
import datetime
from CTkTable import CTkTable
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Reports(ctk.CTkFrame):
    def __init__(self, main):
        super().__init__(main)
        self.master = main
        self.create_widgets()

    def create_widgets(self):
        # Configure grid weights - more compact
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=0)  # Header
        self.master.grid_rowconfigure(1, weight=0)  # Controls
        self.master.grid_rowconfigure(2, weight=1)  # Content

        # Compact Header Section
        self.header_frame = ctk.CTkFrame(
            self.master,
            fg_color="transparent",
            height=50,
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=5)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_propagate(False)

        # Compact Title
        self.reports_label = ctk.CTkLabel(
            self.header_frame,
            text="📊 Library Reports",
            font=("Segoe UI", 20, "bold"),
            text_color="#90EE90",
        )
        self.reports_label.grid(row=0, column=0, sticky="w", padx=15)

        # Compact Controls Section
        self.controls_frame = ctk.CTkFrame(
            self.master,
            fg_color="#001a23",
            corner_radius=12,
            border_width=1,
            border_color="#2d5a3c",
        )
        self.controls_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        self.controls_frame.grid_columnconfigure(0, weight=1)

        # Report Type Selection - More compact
        self.report_type_frame = ctk.CTkFrame(
            self.controls_frame, fg_color="transparent"
        )
        self.report_type_frame.grid(
            row=0, column=0, sticky="ew", padx=10, pady=8)
        self.report_type_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Compact Report Type Buttons
        report_buttons = [
            ("👥 Students", self.generate_student_report),
            ("📚 Books", self.generate_books_report),
            ("🔄 Transactions", self.generate_issue_return_report),
            ("📈 Overview", self.generate_comprehensive_report),
        ]

        for i, (text, command) in enumerate(report_buttons):
            btn = ctk.CTkButton(
                self.report_type_frame,
                text=text,
                text_color="white",
                fg_color="#2d5a3c",
                hover_color="#1e3e29",
                font=("Segoe UI", 11, "bold"),
                corner_radius=8,
                height=35,
                command=command,
                cursor="hand2",
                border_width=1,
                border_color="#90EE90",
            )
            btn.grid(row=0, column=i, padx=4, pady=2, sticky="ew")

        # Compact Download Section
        self.download_frame = ctk.CTkFrame(
            self.controls_frame, fg_color="transparent")
        self.download_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.download_frame.grid_columnconfigure(0, weight=1)

        # Download buttons in one line
        download_buttons_frame = ctk.CTkFrame(
            self.download_frame, fg_color="transparent"
        )
        download_buttons_frame.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            download_buttons_frame,
            text="Export:",
            font=("Segoe UI", 12, "bold"),
            text_color="#90EE90",
        ).grid(row=0, column=0, padx=(0, 10))

        self.pdf_btn = ctk.CTkButton(
            download_buttons_frame,
            text="📄 PDF",
            text_color="white",
            fg_color="#d9534f",
            hover_color="#c9302c",
            font=("Segoe UI", 11, "bold"),
            corner_radius=6,
            height=32,
            command=self.download_pdf,
            cursor="hand2",
            width=100,
        )
        self.pdf_btn.grid(row=0, column=1, padx=5)

        self.excel_btn = ctk.CTkButton(
            download_buttons_frame,
            text="📊 Excel",
            text_color="white",
            fg_color="#5cb85c",
            hover_color="#449d44",
            font=("Segoe UI", 11, "bold"),
            corner_radius=6,
            height=32,
            command=self.download_excel,
            cursor="hand2",
            width=100,
        )
        self.excel_btn.grid(row=0, column=2, padx=5)

        # Compact Report Display Area
        self.report_display_frame = ctk.CTkFrame(
            self.master,
            fg_color="#1b3430",
            corner_radius=12,
            border_width=1,
            border_color="#2d5a3c",
        )
        self.report_display_frame.grid(
            row=2, column=0, sticky="nsew", padx=15, pady=5)
        self.report_display_frame.grid_rowconfigure(0, weight=1)
        self.report_display_frame.grid_columnconfigure(0, weight=1)

        # Scrollable report content area
        self.report_content = ctk.CTkScrollableFrame(
            self.report_display_frame, fg_color="#1b3430", corner_radius=10
        )
        self.report_content.grid(
            row=0, column=0, sticky="nsew", padx=8, pady=8)

        # Store current report data for downloading
        self.current_report_data = None
        self.current_report_type = None

        # Generate comprehensive report by default
        self.generate_comprehensive_report()

    def clear_report_content(self):
        """Clear the report content area"""
        for widget in self.report_content.winfo_children():
            widget.destroy()

    def set_current_report_data(self, report_type, data):
        """Store current report data for downloading"""
        self.current_report_type = report_type
        self.current_report_data = data

    def create_section_header(self, parent, title, icon=""):
        """Create a compact section header"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 5))

        label = ctk.CTkLabel(
            header_frame,
            text=f"{icon} {title}",
            font=("Segoe UI", 16, "bold"),
            text_color="#90EE90",
        )
        label.pack(anchor="w")

        return header_frame

    def create_stat_card(self, parent, title, value, color="#90EE90", icon="📊"):
        """Create a compact stat card"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#001a23",
            corner_radius=10,
            border_width=1,
            border_color=color,
            height=60,
        )
        card.pack(fill="x", pady=3, padx=8)
        card.pack_propagate(False)

        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=12, pady=8)

        # Title
        ctk.CTkLabel(
            content_frame,
            text=f"{icon} {title}",
            font=("Segoe UI", 11),
            text_color="#CCCCCC",
        ).pack(anchor="w")

        # Value
        ctk.CTkLabel(
            content_frame,
            text=str(value),
            font=("Segoe UI", 16, "bold"),
            text_color=color,
        ).pack(anchor="w", pady=(2, 0))

        return card

    def create_data_table(self, parent, headers, data):
        """Create a compact data table"""
        table_container = ctk.CTkFrame(parent, fg_color="transparent")
        table_container.pack(fill="both", expand=True, pady=5, padx=8)

        table_data = [headers]
        table_data.extend(data)

        table = CTkTable(
            table_container,
            values=table_data,
            header_color="#2d5a3c",
            colors=["#1b3430", "#001a23"],
            text_color="white",
            hover_color="#2d5a3c",
        )
        table.pack(fill="both", expand=True)

        return table

    def create_compact_date(self, parent):
        """Create compact date display"""
        date_frame = ctk.CTkFrame(parent, fg_color="transparent")
        date_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(
            date_frame,
            text=f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=("Segoe UI", 10),
            text_color="#CCCCCC",
        ).pack(anchor="w")
        return date_frame

    def normalize_student_data(self, student_data):
        """Normalize student data to ensure consistent formatting"""
        if len(student_data) > 1:
            headers = student_data[0]
            normalized_data = [headers]

            for row in student_data[1:]:
                normalized_row = list(row)
                # Ensure roll number is properly formatted
                roll_no = str(normalized_row[1]).strip()
                if len(roll_no) > 10 and not roll_no.startswith("ROLL"):
                    normalized_row[1] = f"ROLL{roll_no[-3:]}"
                normalized_data.append(normalized_row)

            return normalized_data
        return student_data

    def download_pdf(self):
        if not self.current_report_data:
            CTkMessagebox(
                title="No Data",
                message="Please generate a report first before downloading.",
                icon="warning",
            )
            return

        try:
            reports_dir = os.path.join(
                os.path.expanduser("~"), "Downloads", "LibraryReports"
            )
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(
                reports_dir, f"{self.current_report_type}_{timestamp}.pdf"
            )

            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            title = Paragraph(
                f"{self.current_report_type.replace('_', ' ').upper()} REPORT",
                styles["Heading1"],
            )
            elements.append(title)
            elements.append(Spacer(1, 12))

            date_text = (
                f"Generated on: {
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            date_para = Paragraph(date_text, styles["Normal"])
            elements.append(date_para)
            elements.append(Spacer(1, 20))

            if self.current_report_type == "student_statistics":
                self._add_student_data_to_pdf(elements, styles["Normal"])
            elif self.current_report_type == "books_statistics":
                self._add_books_data_to_pdf(elements, styles["Normal"])
            elif self.current_report_type == "issue_return_statistics":
                self._add_issue_data_to_pdf(elements, styles["Normal"])
            elif self.current_report_type == "comprehensive":
                self._add_comprehensive_data_to_pdf(elements, styles["Normal"])

            doc.build(elements)
            CTkMessagebox(
                title="Success",
                message=f"PDF report saved successfully!\n\nLocation: {
                    filename}",
                icon="check",
            )

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Failed to generate PDF:\n{str(e)}",
                icon="cancel",
            )

    def _add_student_data_to_pdf(self, elements, normal_style):
        data = self.current_report_data

        # Title and header
        title = Paragraph(
            "STUDENT STATISTICS REPORT", getSampleStyleSheet()["Heading1"]
        )
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Generation date
        date_text = (
            f"Generated on: {
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        date_para = Paragraph(date_text, normal_style)
        elements.append(date_para)
        elements.append(Spacer(1, 12))

        # Total students
        total_students = len(data) - 1 if len(data) > 1 else 0
        elements.append(
            Paragraph(f"<b>Total Students:</b> {total_students}", normal_style)
        )
        elements.append(Spacer(1, 20))

        if len(data) > 1:
            # Create table data with proper headers
            headers = data[0]  # Use actual headers from data
            table_data = [headers]
            table_data.extend(data[1:])  # Add the actual data

            # Create table with column widths
            col_widths = [30, 60, 120, 150, 80, 120,
                          60, 40]  # Adjusted column widths

            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        # Header style
                        ("BACKGROUND", (0, 0), (-1, 0),
                         colors.HexColor("#2d5a3c")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                        # Data style
                        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                        ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 1), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.lightgrey],
                        ),
                    ]
                )
            )
            elements.append(table)

    def _add_books_data_to_pdf(self, elements, normal_style):
        data = self.current_report_data

        # Title and header
        title = Paragraph("BOOKS INVENTORY REPORT",
                          getSampleStyleSheet()["Heading1"])
        elements.append(title)
        elements.append(Spacer(1, 12))

        date_text = (
            f"Generated on: {
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        date_para = Paragraph(date_text, normal_style)
        elements.append(date_para)
        elements.append(Spacer(1, 12))

        # Calculate stats
        if len(data) > 1:
            total_books = sum(int(row[5]) for row in data[1:])
            available_books = sum(int(row[6]) for row in data[1:])

            elements.append(
                Paragraph(f"<b>Total Books:</b> {total_books}", normal_style)
            )
            elements.append(
                Paragraph(
                    f"<b>Available Books:</b> {available_books}", normal_style)
            )
            elements.append(
                Paragraph(
                    f"<b>Issued Books:</b> {total_books - available_books}",
                    normal_style,
                )
            )
            elements.append(Spacer(1, 20))

            # Create table
            headers = data[0]
            table_data = [headers]
            table_data.extend(data[1:])

            # Adjust column widths for books data
            col_widths = [40, 80, 120, 100, 80, 50, 50, 60, 60, 80]

            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0),
                         colors.HexColor("#2d5a3c")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                        ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 1), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.lightgrey],
                        ),
                    ]
                )
            )
            elements.append(table)

    def _add_issue_data_to_pdf(self, elements, normal_style):
        data = self.current_report_data

        # Title and header
        title = Paragraph("TRANSACTION REPORT",
                          getSampleStyleSheet()["Heading1"])
        elements.append(title)
        elements.append(Spacer(1, 12))

        date_text = (
            f"Generated on: {
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        date_para = Paragraph(date_text, normal_style)
        elements.append(date_para)
        elements.append(Spacer(1, 12))

        # Calculate stats
        currently_issued = sum(1 for t in data if t[9] == "Issued")
        total_returns = sum(1 for t in data if t[9] == "Returned")

        from datetime import datetime

        today = datetime.now().date()
        overdue_books = sum(
            1 for t in data if t[9] == "Issued" and t[6] and t[6] < today
        )
        total_fines = sum(float(t[8] or 0) for t in data)

        # Add statistics
        stats = [
            ("Currently Issued", currently_issued),
            ("Total Returns", total_returns),
            ("Overdue Books", overdue_books),
            ("Total Fines", f"₹{total_fines:.2f}"),
        ]

        for stat_name, stat_value in stats:
            elements.append(
                Paragraph(f"<b>{stat_name}:</b> {stat_value}", normal_style)
            )
        elements.append(Spacer(1, 20))

        # Create transaction table
        if data:
            headers = [
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
            ]
            table_data = [headers]

            for transaction in data:
                table_data.append(
                    [
                        str(transaction[0]),  # issue_id
                        str(transaction[1]),  # roll_no - ensure string
                        transaction[2],  # student_name
                        transaction[3],  # book_title
                        str(transaction[4]),  # isbn - ensure string
                        str(transaction[5]),  # issue_date
                        str(transaction[6]),  # due_date
                        str(transaction[7]
                            ) if transaction[7] else "Not Returned",
                        f"₹{float(transaction[8] or 0):.2f}",
                        transaction[9],  # status
                    ]
                )

            # Adjust column widths for transactions
            col_widths = [40, 60, 100, 120, 80, 60, 60, 60, 50, 50]

            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0),
                         colors.HexColor("#2d5a3c")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 9),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                        ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 1), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.lightgrey],
                        ),
                    ]
                )
            )
            elements.append(table)

    def _add_comprehensive_data_to_pdf(self, elements, normal_style):
        student_data = self.current_report_data["student_data"]
        books_data = self.current_report_data["books_data"]
        transaction_data = self.current_report_data["transaction_data"]

        # Title and header
        title = Paragraph(
            "COMPREHENSIVE LIBRARY REPORT", getSampleStyleSheet()["Heading1"]
        )
        elements.append(title)
        elements.append(Spacer(1, 12))

        date_text = (
            f"Generated on: {
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        date_para = Paragraph(date_text, normal_style)
        elements.append(date_para)
        elements.append(Spacer(1, 12))

        # Calculate summary metrics
        total_students = len(student_data) - 1 if student_data else 0
        total_books = (
            sum(int(row[5]) for row in books_data[1:])
            if books_data and len(books_data) > 1
            else 0
        )
        available_books = (
            sum(int(row[6]) for row in books_data[1:])
            if books_data and len(books_data) > 1
            else 0
        )
        currently_issued = (
            sum(1 for t in transaction_data if t[9] == "Issued")
            if transaction_data
            else 0
        )

        from datetime import datetime

        today = datetime.now().date()
        overdue_books = (
            sum(
                1
                for t in transaction_data
                if t[9] == "Issued" and t[6] and t[6] < today
            )
            if transaction_data
            else 0
        )

        total_fines = (
            sum(float(t[8] or 0)
                for t in transaction_data) if transaction_data else 0
        )

        summary_data = [
            ("Total Students", total_students),
            ("Total Books", total_books),
            ("Available Books", available_books),
            ("Currently Issued", currently_issued),
            ("Overdue Books", overdue_books),
            ("Total Fines", f"₹{total_fines:.2f}"),
        ]

        elements.append(
            Paragraph("<b>Library Overview</b>",
                      getSampleStyleSheet()["Heading2"])
        )
        elements.append(Spacer(1, 12))

        for stat_name, stat_value in summary_data:
            elements.append(
                Paragraph(f"<b>{stat_name}:</b> {stat_value}", normal_style)
            )
            elements.append(Spacer(1, 6))

        elements.append(Spacer(1, 20))

        # Add sample data from each section
        if student_data and len(student_data) > 1:
            elements.append(
                Paragraph(
                    "<b>Student Data (Sample)</b>", getSampleStyleSheet()[
                        "Heading3"]
                )
            )
            elements.append(Spacer(1, 10))

            headers = student_data[0]
            sample_data = student_data[1:6]  # First 5 students

            table_data = [headers]
            table_data.extend(sample_data)

            col_widths = [30, 60, 100, 120, 70, 100, 50, 35]

            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0),
                         colors.HexColor("#2d5a3c")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 9),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                        ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 1), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ]
                )
            )
            elements.append(table)
            elements.append(Spacer(1, 15))

    def download_excel(self):
        if not self.current_report_data:
            CTkMessagebox(
                title="No Data",
                message="Please generate a report first before downloading.",
                icon="warning",
            )
            return

        try:
            reports_dir = os.path.join(
                os.path.expanduser("~"), "Downloads", "LibraryReports"
            )
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(
                reports_dir, f"{self.current_report_type}_{timestamp}.xlsx"
            )

            with pd.ExcelWriter(filename, engine="openpyxl") as writer:
                if self.current_report_type == "student_statistics":
                    self._add_student_data_to_excel(writer)
                elif self.current_report_type == "books_statistics":
                    self._add_books_data_to_excel(writer)
                elif self.current_report_type == "issue_return_statistics":
                    self._add_issue_data_to_excel(writer)
                elif self.current_report_type == "comprehensive":
                    self._add_comprehensive_data_to_excel(writer)

            CTkMessagebox(
                title="Success",
                message=f"Excel report saved successfully!\n\nLocation: {
                    filename}",
                icon="check",
            )

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Failed to generate Excel file:\n{str(e)}",
                icon="cancel",
            )

    def generate_student_report(self):
        self.clear_report_content()
        try:
            # Get complete student data from Database
            student_data = Database.std_details()

            if not student_data or len(student_data) <= 1:
                self.show_no_data_message("student")
                return

            # Normalize data before displaying
            normalized_data = self.normalize_student_data(student_data)
            self.set_current_report_data("student_statistics", normalized_data)
            self._display_student_report(normalized_data)

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Unable to generate student report:\n{str(e)}",
                icon="cancel",
            )

    def generate_books_report(self):
        self.clear_report_content()
        try:
            # Get complete books data from Database
            books_data = Database.books_data()

            if not books_data or len(books_data) <= 1:
                self.show_no_data_message("books")
                return

            self.set_current_report_data("books_statistics", books_data)
            self._display_books_report(books_data)

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Unable to generate books report:\n{str(e)}",
                icon="cancel",
            )

    def generate_issue_return_report(self):
        self.clear_report_content()
        try:
            # Get complete transaction data from Database
            transaction_data = Database.get_all_transactions()

            if not transaction_data:
                self.show_no_data_message("transaction")
                return

            self.set_current_report_data(
                "issue_return_statistics", transaction_data)
            self._display_issue_return_report(transaction_data)

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Unable to generate transaction report:\n{str(e)}",
                icon="cancel",
            )

    def generate_comprehensive_report(self):
        self.clear_report_content()
        try:
            # Get all data for comprehensive report
            student_data = Database.std_details()
            books_data = Database.books_data()
            transaction_data = Database.get_all_transactions()

            comprehensive_data = {
                "student_data": student_data,
                "books_data": books_data,
                "transaction_data": transaction_data,
            }
            self.set_current_report_data("comprehensive", comprehensive_data)
            self._display_comprehensive_report(
                student_data, books_data, transaction_data
            )

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Unable to generate comprehensive report:\n{str(e)}",
                icon="cancel",
            )

    def show_no_data_message(self, report_type):
        """Show a compact no data message"""
        self.clear_report_content()

        message_frame = ctk.CTkFrame(
            self.report_content, fg_color="transparent")
        message_frame.pack(expand=True, fill="both", pady=30)

        ctk.CTkLabel(
            message_frame,
            text="📊",
            font=("Segoe UI", 48),
            text_color="#90EE90",
        ).pack(pady=5)

        ctk.CTkLabel(
            message_frame,
            text="No Data Available",
            font=("Segoe UI", 16, "bold"),
            text_color="#90EE90",
        ).pack(pady=2)

        ctk.CTkLabel(
            message_frame,
            text=f"No {report_type} data found.",
            font=("Segoe UI", 12),
            text_color="#CCCCCC",
            justify="center",
        ).pack(pady=5)

    def _display_student_report(self, student_data):
        """Display complete student records"""
        self.create_section_header(
            self.report_content, "Complete Student Records", "👥"
        )
        self.create_compact_date(self.report_content)

        # Total Students Card
        total_students = len(student_data) - 1  # Subtract header row
        self.create_stat_card(
            self.report_content,
            "Total Students",
            total_students,
            "#4CAF50",
            "👥",
        )

        # Complete Students Table
        self.create_section_header(self.report_content, "Student Details", "📋")

        # Use the actual headers from the data
        headers = student_data[0] if student_data else []
        table_data = student_data[1:] if len(student_data) > 1 else []

        self.create_data_table(self.report_content, headers, table_data)

    def _display_books_report(self, books_data):
        """Display complete books inventory"""
        self.create_section_header(
            self.report_content, "Complete Books Inventory", "📚"
        )
        self.create_compact_date(self.report_content)

        # Stats in a compact row
        stats_container = ctk.CTkFrame(
            self.report_content, fg_color="transparent")
        stats_container.pack(fill="x", pady=5)
        stats_container.grid_columnconfigure((0, 1, 2), weight=1)

        # Calculate stats from actual data
        if len(books_data) > 1:
            total_books = sum(
                int(row[5]) for row in books_data[1:]
            )  # total_copies column
            available_books = sum(
                int(row[6]) for row in books_data[1:]
            )  # available_copies column
            issued_books = total_books - available_books
        else:
            total_books = available_books = issued_books = 0

        cards_data = [
            ("Total Books", total_books, "#2196F3", "📚"),
            ("Available", available_books, "#4CAF50", "✅"),
            ("Issued", issued_books, "#FF9800", "📤"),
        ]

        for i, (title, value, color, icon) in enumerate(cards_data):
            card_frame = ctk.CTkFrame(stats_container, fg_color="transparent")
            card_frame.grid(row=0, column=i, padx=3, sticky="ew")
            self.create_stat_card(card_frame, title, value, color, icon)

        # Complete Books Table
        self.create_section_header(self.report_content, "Books Details", "📖")

        # Use the actual headers from the data
        headers = books_data[0] if books_data else []
        table_data = books_data[1:] if len(books_data) > 1 else []

        self.create_data_table(self.report_content, headers, table_data)

    def _display_issue_return_report(self, transaction_data):
        """Display complete transaction history"""
        self.create_section_header(
            self.report_content, "Complete Transaction History", "🔄"
        )
        self.create_compact_date(self.report_content)

        # Compact stats grid
        stats_container = ctk.CTkFrame(
            self.report_content, fg_color="transparent")
        stats_container.pack(fill="x", pady=5)
        stats_container.grid_columnconfigure((0, 1), weight=1)

        # Calculate stats from actual data
        currently_issued = sum(
            1 for t in transaction_data if t[9] == "Issued"
        )  # status column
        total_returns = sum(1 for t in transaction_data if t[9] == "Returned")

        # Calculate overdue books (issued and past due date)
        from datetime import datetime

        today = datetime.now().date()
        overdue_books = sum(
            1 for t in transaction_data if t[9] == "Issued" and t[6] and t[6] < today
        )  # due_date column

        total_fines = sum(
            float(t[8] or 0) for t in transaction_data
        )  # fine_amount column

        stats_data = [
            ("Currently Issued", currently_issued, "#FF9800", "📤"),
            ("Total Returns", total_returns, "#4CAF50", "✅"),
            ("Overdue Books", overdue_books, "#f44336", "⏰"),
            ("Total Fines", f"₹{total_fines:.2f}", "#9C27B0", "💰"),
        ]

        for i, (title, value, color, icon) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            card_frame = ctk.CTkFrame(stats_container, fg_color="transparent")
            card_frame.grid(row=row, column=col, padx=3, pady=2, sticky="ew")
            self.create_stat_card(card_frame, title, value, color, icon)

        # Complete Transactions Table
        self.create_section_header(
            self.report_content, "Transaction Details", "📋")

        # Define headers for transactions
        headers = [
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

        # Convert transaction data to table format
        table_data = []
        for transaction in transaction_data:
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
                    f"₹{float(transaction[8] or 0):.2f}",  # fine_amount
                    transaction[9],  # status
                    transaction[10],  # issued_by
                ]
            )

        self.create_data_table(self.report_content, headers, table_data)

    def _display_comprehensive_report(self, student_data, books_data, transaction_data):
        """Display comprehensive library overview"""
        self.create_section_header(
            self.report_content, "Library Overview", "📈")
        self.create_compact_date(self.report_content)

        # Key Metrics
        self.create_section_header(self.report_content, "Key Metrics", "📊")

        # Calculate metrics
        total_students = len(student_data) - 1 if student_data else 0
        total_books = (
            sum(int(row[5]) for row in books_data[1:])
            if books_data and len(books_data) > 1
            else 0
        )
        available_books = (
            sum(int(row[6]) for row in books_data[1:])
            if books_data and len(books_data) > 1
            else 0
        )
        currently_issued = (
            sum(1 for t in transaction_data if t[9] == "Issued")
            if transaction_data
            else 0
        )

        from datetime import datetime

        today = datetime.now().date()
        overdue_books = (
            sum(
                1
                for t in transaction_data
                if t[9] == "Issued" and t[6] and t[6] < today
            )
            if transaction_data
            else 0
        )

        total_fines = (
            sum(float(t[8] or 0)
                for t in transaction_data) if transaction_data else 0
        )

        metrics_data = [
            ("Students", total_students, "#4CAF50", "👥"),
            ("Total Books", total_books, "#2196F3", "📚"),
            ("Available Books", available_books, "#00BCD4", "✅"),
            ("Currently Issued", currently_issued, "#FF9800", "📤"),
            ("Overdue Books", overdue_books, "#f44336", "⏰"),
            ("Total Fines", f"₹{total_fines:.2f}", "#9C27B0", "💰"),
        ]

        for title, value, color, icon in metrics_data:
            self.create_stat_card(self.report_content,
                                  title, value, color, icon)

        # Show sample data from each section
        self.create_section_header(
            self.report_content, "Recent Students (Sample)", "👥"
        )
        student_headers = student_data[0] if student_data else []
        student_sample = (
            student_data[1:6] if student_data and len(student_data) > 1 else []
        )  # First 5 students
        if student_sample:
            self.create_data_table(self.report_content,
                                   student_headers, student_sample)

        self.create_section_header(
            self.report_content, "Recent Books (Sample)", "📚")
        book_headers = books_data[0] if books_data else []
        book_sample = (
            books_data[1:6] if books_data and len(books_data) > 1 else []
        )  # First 5 books
        if book_sample:
            self.create_data_table(self.report_content,
                                   book_headers, book_sample)

        self.create_section_header(
            self.report_content, "Recent Transactions (Sample)", "🔄"
        )
        transaction_headers = [
            "Issue ID",
            "Roll No",
            "Student Name",
            "Book Title",
            "Status",
        ]
        transaction_sample = []
        for i, transaction in enumerate(
            transaction_data[:5] if transaction_data else []
        ):  # First 5 transactions
            transaction_sample.append(
                [
                    str(transaction[0]),  # issue_id
                    transaction[1],  # student_roll_no
                    transaction[2],  # student_name
                    transaction[3],  # book_title
                    transaction[9],  # status
                ]
            )
        if transaction_sample:
            self.create_data_table(
                self.report_content, transaction_headers, transaction_sample
            )

    def _add_student_data_to_excel(self, writer):
        data = self.current_report_data

        if len(data) > 1:
            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])
            df.to_excel(writer, sheet_name="Student Details", index=False)

    def _add_books_data_to_excel(self, writer):
        data = self.current_report_data

        if len(data) > 1:
            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])
            df.to_excel(writer, sheet_name="Books Details", index=False)

    def _add_issue_data_to_excel(self, writer):
        data = self.current_report_data

        if data:
            # Convert to DataFrame
            df = pd.DataFrame(
                data,
                columns=[
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
                ],
            )
            df.to_excel(writer, sheet_name="Transaction Details", index=False)

    def _add_comprehensive_data_to_excel(self, writer):
        student_data = self.current_report_data["student_data"]
        books_data = self.current_report_data["books_data"]
        transaction_data = self.current_report_data["transaction_data"]

        # Export each section to different sheets
        if student_data and len(student_data) > 1:
            df_students = pd.DataFrame(
                student_data[1:], columns=student_data[0])
            df_students.to_excel(writer, sheet_name="Students", index=False)

        if books_data and len(books_data) > 1:
            df_books = pd.DataFrame(books_data[1:], columns=books_data[0])
            df_books.to_excel(writer, sheet_name="Books", index=False)

        if transaction_data:
            df_transactions = pd.DataFrame(
                transaction_data,
                columns=[
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
                ],
            )
            df_transactions.to_excel(
                writer, sheet_name="Transactions", index=False)
