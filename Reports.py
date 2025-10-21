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
            height=50,  # Reduced height
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=5)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_propagate(False)

        # Compact Title
        self.reports_label = ctk.CTkLabel(
            self.header_frame,
            text="📊 Library Reports",
            font=("Segoe UI", 20, "bold"),  # Smaller font
            text_color="#90EE90",
        )
        self.reports_label.grid(row=0, column=0, sticky="w", padx=15)

        # Compact Controls Section
        self.controls_frame = ctk.CTkFrame(
            self.master,
            fg_color="#001a23",
            corner_radius=12,
            border_width=1,  # Thinner border
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
                font=("Segoe UI", 11, "bold"),  # Smaller font
                corner_radius=8,
                height=35,  # Smaller height
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
        header_frame.pack(fill="x", pady=(10, 5))  # Reduced padding

        label = ctk.CTkLabel(
            header_frame,
            text=f"{icon} {title}",
            font=("Segoe UI", 16, "bold"),  # Smaller font
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
            border_width=1,  # Thinner border
            border_color=color,
            height=60,  # Smaller height
        )
        card.pack(fill="x", pady=3, padx=8)  # Reduced padding
        card.pack_propagate(False)

        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True,
                           padx=12, pady=8)  # Reduced padding

        # Title
        ctk.CTkLabel(
            content_frame,
            text=f"{icon} {title}",
            font=("Segoe UI", 11),  # Smaller font
            text_color="#CCCCCC",
        ).pack(anchor="w")

        # Value
        ctk.CTkLabel(
            content_frame,
            text=str(value),
            font=("Segoe UI", 16, "bold"),  # Smaller font
            text_color=color,
        ).pack(anchor="w", pady=(2, 0))  # Reduced padding

        return card

    def create_data_table(self, parent, headers, data):
        """Create a compact data table"""
        table_container = ctk.CTkFrame(parent, fg_color="transparent")
        table_container.pack(
            fill="both", expand=True, pady=5, padx=8
        )  # Reduced padding

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
        date_frame.pack(fill="x", pady=(0, 10))  # Reduced padding
        ctk.CTkLabel(
            date_frame,
            text=f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=("Segoe UI", 10),  # Smaller font
            text_color="#CCCCCC",
        ).pack(anchor="w")
        return date_frame

    # Download methods (keep the same as before)
    def download_pdf(self):
        if not self.current_report_data:
            CTkMessagebox(
                title="No Data",
                message="Please generate a report first before downloading.",
                icon="warning",
            )
            return

        try:
            reports_dir = "Reports"
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{
                reports_dir}/{self.current_report_type}_{timestamp}.pdf"

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

    def download_excel(self):
        if not self.current_report_data:
            CTkMessagebox(
                title="No Data",
                message="Please generate a report first before downloading.",
                icon="warning",
            )
            return

        try:
            reports_dir = "Reports"
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{
                reports_dir}/{self.current_report_type}_{timestamp}.xlsx"

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

    # Report generation methods
    def generate_student_report(self):
        self.clear_report_content()
        try:
            student_data = Database.get_student_report()

            if not student_data or not student_data.get("students_per_group"):
                self.show_no_data_message("student")
                return

            self.set_current_report_data("student_statistics", student_data)
            self._display_student_report(student_data)

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Unable to generate student report:\n{str(e)}",
                icon="cancel",
            )

    def generate_books_report(self):
        self.clear_report_content()
        try:
            books_data = Database.get_books_report()

            if not books_data or not books_data.get("books_per_category"):
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
            issue_data = Database.get_issue_return_report()

            if not issue_data:
                self.show_no_data_message("transaction")
                return

            self.set_current_report_data("issue_return_statistics", issue_data)
            self._display_issue_return_report(issue_data)

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Unable to generate transaction report:\n{str(e)}",
                icon="cancel",
            )

    def generate_comprehensive_report(self):
        self.clear_report_content()
        try:
            student_data = Database.get_student_report()
            books_data = Database.get_books_report()
            issue_data = Database.get_issue_return_report()

            comprehensive_data = {
                "student_data": student_data,
                "books_data": books_data,
                "issue_data": issue_data,
            }
            self.set_current_report_data("comprehensive", comprehensive_data)
            self._display_comprehensive_report(
                student_data, books_data, issue_data)

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
        message_frame.pack(expand=True, fill="both",
                           pady=30)  # Reduced padding

        ctk.CTkLabel(
            message_frame,
            text="📊",
            font=("Segoe UI", 48),  # Smaller icon
            text_color="#90EE90",
        ).pack(pady=5)

        ctk.CTkLabel(
            message_frame,
            text="No Data Available",
            font=("Segoe UI", 16, "bold"),  # Smaller font
            text_color="#90EE90",
        ).pack(pady=2)

        ctk.CTkLabel(
            message_frame,
            text=f"No {report_type} data found.",
            font=("Segoe UI", 12),  # Smaller font
            text_color="#CCCCCC",
            justify="center",
        ).pack(pady=5)

    # Compact display methods
    def _display_student_report(self, student_data):
        self.create_section_header(
            self.report_content, "Student Statistics", "👥")
        self.create_compact_date(self.report_content)

        # Total Students Card
        self.create_stat_card(
            self.report_content,
            "Total Students",
            student_data.get("total_students", 0),
            "#4CAF50",
            "👥",
        )

        # Students by Group Table
        self.create_section_header(
            self.report_content, "Students by Group", "📊")

        table_data = []
        for group, count in student_data.get("students_per_group", []):
            table_data.append([group, str(count)])

        self.create_data_table(self.report_content, [
                               "Group", "Count"], table_data)

    def _display_books_report(self, books_data):
        self.create_section_header(self.report_content, "Books Inventory", "📚")
        self.create_compact_date(self.report_content)

        # Stats in a compact row
        stats_container = ctk.CTkFrame(
            self.report_content, fg_color="transparent")
        stats_container.pack(fill="x", pady=5)
        stats_container.grid_columnconfigure((0, 1, 2), weight=1)

        total_books = books_data.get("total_books", 0)
        available_books = books_data.get("available_books", 0)
        issued_books = total_books - available_books

        cards_data = [
            ("Total", total_books, "#2196F3", "📚"),
            ("Available", available_books, "#4CAF50", "✅"),
            ("Issued", issued_books, "#FF9800", "📤"),
        ]

        for i, (title, value, color, icon) in enumerate(cards_data):
            card_frame = ctk.CTkFrame(stats_container, fg_color="transparent")
            card_frame.grid(row=0, column=i, padx=3, sticky="ew")
            self.create_stat_card(card_frame, title, value, color, icon)

        # Books by Category Table
        self.create_section_header(
            self.report_content, "Books by Category", "📂")

        table_data = []
        for category, count, total_copies in books_data.get("books_per_category", []):
            table_data.append([category, str(count), str(total_copies)])

        self.create_data_table(
            self.report_content, ["Category", "Titles", "Copies"], table_data
        )

    def _display_issue_return_report(self, issue_data):
        self.create_section_header(
            self.report_content, "Transaction Analytics", "🔄")
        self.create_compact_date(self.report_content)

        # Compact stats grid
        stats_container = ctk.CTkFrame(
            self.report_content, fg_color="transparent")
        stats_container.pack(fill="x", pady=5)
        stats_container.grid_columnconfigure((0, 1), weight=1)

        stats_data = [
            ("Issued", issue_data.get("currently_issued", 0), "#FF9800", "📤"),
            ("Returns", issue_data.get("total_returns", 0), "#4CAF50", "✅"),
            ("Overdue", issue_data.get("overdue_books", 0), "#f44336", "⏰"),
            ("Fines", f"₹{issue_data.get(
                'total_fines', 0):.2f}", "#9C27B0", "💰"),
        ]

        for i, (title, value, color, icon) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            card_frame = ctk.CTkFrame(stats_container, fg_color="transparent")
            card_frame.grid(row=row, column=col, padx=3, pady=2, sticky="ew")
            self.create_stat_card(card_frame, title, value, color, icon)

    def _display_comprehensive_report(self, student_data, books_data, issue_data):
        self.create_section_header(
            self.report_content, "Library Overview", "📈")
        self.create_compact_date(self.report_content)

        # Key Metrics - more compact
        self.create_section_header(self.report_content, "Key Metrics", "📊")

        metrics_data = [
            ("Students", student_data.get("total_students", 0), "#4CAF50", "👥"),
            ("Total Books", books_data.get("total_books", 0), "#2196F3", "📚"),
            ("Available", books_data.get("available_books", 0), "#00BCD4", "✅"),
            ("Issued", issue_data.get("currently_issued", 0), "#FF9800", "📤"),
            ("Overdue", issue_data.get("overdue_books", 0), "#f44336", "⏰"),
            ("Fines", f"₹{issue_data.get(
                'total_fines', 0):.2f}", "#9C27B0", "💰"),
        ]

        for title, value, color, icon in metrics_data:
            self.create_stat_card(self.report_content,
                                  title, value, color, icon)

    # Include all the PDF and Excel helper methods from previous version
    # _add_student_data_to_pdf, _add_books_data_to_pdf, etc.
    def _add_student_data_to_pdf(self, elements, normal_style):
        data = self.current_report_data
        elements.append(
            Paragraph(
                f"<b>Total Students:</b> {
                    data.get('total_students', 0)}", normal_style
            )
        )
        elements.append(Spacer(1, 12))

        table_data = [["Student Group", "Count"]]
        students_per_group = data.get("students_per_group", [])
        for group, count in students_per_group:
            table_data.append([group, str(count)])

        if len(table_data) > 1:
            table = Table(table_data)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0),
                         colors.HexColor("#2d5a3c")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1),
                         colors.HexColor("#1b3430")),
                        ("TEXTCOLOR", (0, 1), (-1, -1), colors.white),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            elements.append(table)

    def _add_books_data_to_pdf(self, elements, normal_style):
        data = self.current_report_data
        elements.append(
            Paragraph(
                f"<b>Total Books:</b> {data.get('total_books', 0)}", normal_style)
        )
        elements.append(
            Paragraph(
                f"<b>Available Books:</b> {data.get('available_books', 0)}",
                normal_style,
            )
        )
        elements.append(
            Paragraph(
                f"<b>Issued Books:</b> {data.get('total_books', 0) -
                                        data.get('available_books', 0)}",
                normal_style,
            )
        )
        elements.append(Spacer(1, 12))

        table_data = [["Category", "Title Count", "Total Copies"]]
        books_per_category = data.get("books_per_category", [])
        for category, count, total_copies in books_per_category:
            table_data.append([category, str(count), str(total_copies)])

        if len(table_data) > 1:
            table = Table(table_data)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0),
                         colors.HexColor("#2d5a3c")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1),
                         colors.HexColor("#1b3430")),
                        ("TEXTCOLOR", (0, 1), (-1, -1), colors.white),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            elements.append(table)

    def _add_issue_data_to_pdf(self, elements, normal_style):
        data = self.current_report_data
        stats_data = [
            ("Currently Issued Books", data.get("currently_issued", 0)),
            ("Total Books Returned", data.get("total_returns", 0)),
            ("Overdue Books", data.get("overdue_books", 0)),
            ("Total Fines Collected", f"₹{data.get('total_fines', 0):.2f}"),
        ]

        for stat_name, stat_value in stats_data:
            elements.append(
                Paragraph(f"<b>{stat_name}:</b> {stat_value}", normal_style)
            )
            elements.append(Spacer(1, 8))

    def _add_comprehensive_data_to_pdf(self, elements, normal_style):
        student_data = self.current_report_data["student_data"]
        books_data = self.current_report_data["books_data"]
        issue_data = self.current_report_data["issue_data"]

        summary_data = [
            ("Total Students", student_data.get("total_students", 0)),
            ("Total Books", books_data.get("total_books", 0)),
            ("Available Books", books_data.get("available_books", 0)),
            ("Currently Issued", issue_data.get("currently_issued", 0)),
            ("Overdue Books", issue_data.get("overdue_books", 0)),
            ("Total Fines", f"₹{issue_data.get('total_fines', 0):.2f}"),
        ]

        for stat_name, stat_value in summary_data:
            elements.append(
                Paragraph(f"<b>{stat_name}:</b> {stat_value}", normal_style)
            )
            elements.append(Spacer(1, 8))

    def _add_student_data_to_excel(self, writer):
        data = self.current_report_data

        summary_data = {
            "Metric": ["Total Students"],
            "Value": [data.get("total_students", 0)],
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name="Student Summary", index=False)

        students_per_group = data.get("students_per_group", [])
        details_data = {
            "Student Group": [group for group, count in students_per_group],
            "Count": [count for group, count in students_per_group],
        }
        df_details = pd.DataFrame(details_data)
        df_details.to_excel(
            writer, sheet_name="Students by Group", index=False)

    def _add_books_data_to_excel(self, writer):
        data = self.current_report_data

        summary_data = {
            "Metric": ["Total Books", "Available Books", "Issued Books"],
            "Value": [
                data.get("total_books", 0),
                data.get("available_books", 0),
                data.get("total_books", 0) - data.get("available_books", 0),
            ],
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name="Books Summary", index=False)

        books_per_category = data.get("books_per_category", [])
        categories_data = {
            "Category": [cat for cat, count, copies in books_per_category],
            "Title Count": [count for cat, count, copies in books_per_category],
            "Total Copies": [copies for cat, count, copies in books_per_category],
        }
        df_categories = pd.DataFrame(categories_data)
        df_categories.to_excel(
            writer, sheet_name="Books by Category", index=False)

    def _add_issue_data_to_excel(self, writer):
        data = self.current_report_data

        summary_data = {
            "Metric": [
                "Currently Issued Books",
                "Total Books Returned",
                "Overdue Books",
                "Total Fines Collected",
            ],
            "Value": [
                data.get("currently_issued", 0),
                data.get("total_returns", 0),
                data.get("overdue_books", 0),
                f"₹{data.get('total_fines', 0):.2f}",
            ],
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(
            writer, sheet_name="Issue Return Summary", index=False)

    def _add_comprehensive_data_to_excel(self, writer):
        student_data = self.current_report_data["student_data"]
        books_data = self.current_report_data["books_data"]
        issue_data = self.current_report_data["issue_data"]

        summary_data = {
            "Metric": [
                "Total Students",
                "Total Books",
                "Available Books",
                "Currently Issued Books",
                "Overdue Books",
                "Total Fines Collected",
            ],
            "Value": [
                student_data.get("total_students", 0),
                books_data.get("total_books", 0),
                books_data.get("available_books", 0),
                issue_data.get("currently_issued", 0),
                issue_data.get("overdue_books", 0),
                f"₹{issue_data.get('total_fines', 0):.2f}",
            ],
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(
            writer, sheet_name="Comprehensive Summary", index=False)
