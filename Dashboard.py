import threading
import customtkinter as ctk
import os
import sys
from PIL import Image, ImageTk
import datetime
from Database import Database
from StudentsRecords import StudentRecord
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from CTkMessagebox import CTkMessagebox
import random as rand
from Books import Books

class Dashboard(ctk.CTkToplevel):
    ctk.set_appearance_mode("light")
    def __init__(self, parent):
        super().__init__(parent)
        self.title("DASHBOARD")
        self.geometry("500x500")
        self.iconbitmap(os.path.abspath("Assets/Ideal-College.ico"))
        self.state("zoomed")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.request = self.quotes_req()
        self.create_widgets()
    #     self.after(0,self.dashboard_content)
    #     threading.Thread(target=self.load_data, daemon=True).start()

    # def load_data(self):  # Added method
    #     # Fetch quote
    #     self.quote = self.quotes_req()
    #     # Fetch database data
    #     self.student_data = Database.students_per_group()
    #     self.total_books = Database.total_books()
    #     # Update the dashboard content on the main thread
    #     self.after(0, self.dashboard_content)

    def create_widgets(self):
        self.images()

        # Header Frame
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="#001a23",#8b2635
            height=60,
            corner_radius=10
        )
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=0)
        self.header_frame.grid_columnconfigure(1, weight=1)

        # Logo
        # self.logo_labe = ctk.CTkLabel(
        #     self.header_frame,
        #     image=self.logo_img,
        #     text="",
        # )
        # self.logo_labe.grid(row=0, column=0, padx=80, pady=5, sticky="nw")

        # College Name
        self.clg_name = ctk.CTkLabel(
            self.header_frame,
            text="IDEAL COLLEGE OF ARTS & SCIENCES",
            font=("Segoe UI", 17, "bold"),
            text_color="white"
        )
        self.clg_name.grid(row=0, column=0, pady=15, sticky="nw",padx=50)

        # Date Time
        self.date_time = ctk.CTkLabel(
            self.header_frame,
            text=f"{datetime.datetime.now().strftime('%d/%m/%Y')}/{datetime.datetime.now().strftime('%H:%M:%S')}",
            font=("Segoe UI", 12, "bold"),
            text_color="white"
        )
        self.date_time.grid(row=0, column=2, padx=20, pady=15, sticky="ne")

        # Main Content Area
        self.back_frame = ctk.CTkFrame(
            self,
            fg_color="#31493c",#2e3532
            corner_radius=10
        )
        self.back_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(10, 10))
        self.back_frame.grid_rowconfigure(0, weight=1)
        self.back_frame.grid_columnconfigure(1, weight=1)

        # Menu Frame
        self.menu_frame = ctk.CTkFrame(
            self.back_frame,
            fg_color="#001a23",#8b2635
            corner_radius=10,
            width=200
        )
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=10)
        self.menu_frame.grid_propagate(False)

        self.logo = ctk.CTkLabel(
            self.menu_frame,
            image=f"{self.logo_img}",
            text="",
        )
        self.logo.grid(row=0,column=0,pady=10)

        # Dashboard Button
        self.dashboard_btn = ctk.CTkButton(
            self.menu_frame,
            text="Dashboard         ",
            compound="left",
            image=self.dashicon,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",#2e3532
            cursor="hand2",
            width=180,
            command=self.dashboard_content
        )
        self.dashboard_btn.grid(row=1, column=0, padx=10, pady=(30, 0), sticky="w")

        # Student Record Button
        self.student_rec = ctk.CTkButton(
            self.menu_frame,
            text="STUDENT RECORD",
            compound="left",
            image=self.student_record,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",#2e3532
            cursor="hand2",
            width=180,
            command=self.students_records
        )
        self.student_rec.grid(row=2, column=0, padx=10, pady=(20, 0), sticky="w")

        # Books Button
        self.book_btn = ctk.CTkButton(
            self.menu_frame,
            text="BOOKS             ",
            compound="left",
            image=self.book,
            width=180,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",#2e3532
            cursor="hand2",
            command=self.student_book
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
            fg_color="#31493c",#2e3532
            cursor="hand2",
            command=self.issue_return
        )
        self.issue_re_btn.grid(row=4, column=0, padx=10, pady=(20, 0), sticky="w")

        # Transaction Button
        self.transaction_btn = ctk.CTkButton(
            self.menu_frame,
            text="TRANSACTION",
            compound="left",
            image=self.transaction_list,
            width=180,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",#2e3532
            cursor="hand2",
        )
        self.transaction_btn.grid(row=5, column=0, padx=10, pady=(20, 0), sticky="w")

        # Reports Button
        self.reports_btn = ctk.CTkButton(
            self.menu_frame,
            text="REPORTS                 ",
            image=self.reports,
            width=180,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",#2e3532
            cursor="hand2",
        )
        self.reports_btn.grid(row=6, column=0, padx=10, pady=(20, 0), sticky="w")

        # Mailing Button
        self.mailing_btn = ctk.CTkButton(
            self.menu_frame,
            text="MAILING            ",
            image=self.mail,
            width=180,
            corner_radius=10,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",#2e3532
            cursor="hand2",
        )
        self.mailing_btn.grid(row=7, column=0, padx=10, pady=(20, 0), sticky="w")

        #Modification button
        self.modification_btn = ctk.CTkButton(
            self.menu_frame,
            text='MODIFICATION',
            image=self.modification_img,
            corner_radius=10,
            width=180,
            font=("Segoe UI", 10, "bold"),
            hover_color="#2e3532",
            fg_color="#31493c",#2e3532
            cursor="hand2",
        )
        self.modification_btn.grid(row=8,column=0,padx=10, pady=(20, 0), sticky="w")

        # #Modification button
        # self.modification_btn = ctk.CTkButton(
        #     self.menu_frame,
        #     text='MODIFICATION',
        #     image=self.modification_img,
        #     corner_radius=20,
        #     width=180,
        #     font=("Segoe UI", 10, "bold"),
        #     hover_color="#2e3532",
        #     fg_color="#31493c",#2e3532
        #     cursor="hand2",
        # )
        # self.modification_btn.grid(row=7,column=0,padx=10, pady=(20, 0), sticky="w")


        # Logout Button
        self.logout_btn = ctk.CTkButton(
            self.menu_frame,
            image=self.logout,
            text="LOGOUT",
            height=30,
            width=150,
            fg_color="#001a23",#8b2635
            hover_color="#2e3532",
            font=("Segoe UI", 10, "bold"),
            corner_radius=10,
            command=self.close
        )
        self.logout_btn.grid(row=9, column=0, padx=20, pady=(40, 0), sticky="w")

        # Main Content Frame
        self.main_frame = ctk.CTkFrame(
            self.back_frame,
            fg_color="#001a23",
            corner_radius=10
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.dashboard_content()

    def dashboard_content(self):
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
            text_color="black"
        )
        self.total_std.grid(column=0, row=1, padx=5, pady=(5, 5))
        self.std_label = ctk.CTkLabel(
            self.frame1,
            text="TOTAL STUDENTS",
            font=("Segoe UI", 15, "bold"),
            text_color="black"
        )
        self.std_label.grid(column=0, row=2, padx=5, pady=(1, 5))
        ################## FRAME 2 ########################
        self.total_book_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=30,
        )
        self.total_book_frame.grid(column=1, row=0, padx=20, pady=20, sticky="nsew")
        self.total_book_frame.grid_columnconfigure(0,weight=1)
        self.total_book_frame.grid_rowconfigure(0,weight=1)
        self.total_book_frame.grid_rowconfigure(1,weight=1)
        self.total_book_frame.grid_rowconfigure(2,weight=1)
        self.total_book_img = ctk.CTkLabel(
            self.total_book_frame,
            text="",
            image=self.total_books_img
        )
        self.total_book_img.grid(row=0,column=0,padx=10,pady=(10,0))
        self.lable2 = Database.Books()
        self.total_book_db = ctk.CTkLabel(
            self.total_book_frame,
            text=f'{self.lable2}',
            font=("Segoe UI", 35, "bold"),
            text_color="black"
        )
        self.total_book_db.grid(row=1,column=0,padx=5, pady=(5, 5))
        self.total_book_label = ctk.CTkLabel(
            self.total_book_frame,
            text='TOTAL BOOKS',
            font=("Segoe UI", 15, "bold"),
            text_color='black'
        )
        self.total_book_label.grid(row=2,column=0,padx=5, pady=(1, 5))
        ############## FRAME 3 #####################
        self.issued_bookd_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=30
        )
        self.issued_bookd_frame.grid(column=2, row=0, padx=20, pady=20, sticky="nsew")
        self.issued_bookd_frame.grid_columnconfigure(0,weight=1)
        self.issued_bookd_frame.grid_rowconfigure(0,weight=1)
        self.issued_bookd_frame.grid_rowconfigure(1,weight=1)
        self.issued_bookd_frame.grid_rowconfigure(2,weight=1)
        self.issued_book_img = ctk.CTkLabel(
            self.issued_bookd_frame,
            image=self.inword_books,
            text=""
        )
        self.issued_book_img.grid(row=0,column=0,pady=10,padx=(10,0))
        self.label3 = Database.total_inwords()
        self.issued_book_db = ctk.CTkLabel(
            self.issued_bookd_frame,
            text=f'{self.label3}',
             font=("Segoe UI", 35, "bold"),
            text_color="black"
        )
        self.issued_book_db.grid(row=1,column=0,padx=5,pady=(5,5))
        self.issued_book_label = ctk.CTkLabel(
            self.issued_bookd_frame,
            text="TOTAL INWORDS",
            font=("Segoe UI", 15, "bold"),
            text_color='black'
        )
        self.issued_book_label.grid(row=2,column=0,padx=1, pady=(1, 5))
        ############## FRAME 4 #######################
        self.return_book_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=30
        )
        self.return_book_frame.grid(column=3, row=0, padx=20, pady=20, sticky="nsew")
        self.return_book_frame.grid_columnconfigure(0,weight=1)
        self.return_book_frame.grid_rowconfigure(0,weight=1)
        self.return_book_frame.grid_rowconfigure(1,weight=1)
        self.return_book_frame.grid_rowconfigure(2,weight=1)
        self.return_img = ctk.CTkLabel(
            self.return_book_frame,
            image=self.outword_img,
            text=""
        )
        self.return_img.grid(column=0,row=0,padx=10,pady=(10,0))
        self.label4 = Database.total_outwords()
        self.return_book_db = ctk.CTkLabel(
            self.return_book_frame,
            text=f'{self.label4}',
            font=("Segoe UI", 35, "bold"),
            text_color="black"
        )
        self.return_book_db.grid(row=1,column=0,padx=5,pady=(5,5))
        self.return_book_label = ctk.CTkLabel(
            self.return_book_frame,
            text='TOTAL OUTWORDS',
            font=("Segoe UI", 15, "bold"),
            text_color='black'
        )
        self.return_book_label.grid(row=2,column=0,padx=5,pady=(2,5))
        ############### FRAME 5 ####################
        self.graph_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=30,
            height=220,
        )
        self.graph_frame.grid(row=1, column=0, columnspan=3,padx=20, pady=(0, 20), sticky="nsew")
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graph_frame.grid_rowconfigure(0, weight=1)

        # Fetch data from database
        student_data = Database.students_per_group()
        total_books = Database.total_books()

        # Prepare data for plotting
        groups = [row[0] for row in student_data]
        counts = [row[1] for row in student_data]
        all_groups = ['Science', 'Arts', 'BCA', 'AI_CS', 'BBA', 'Total Books']
        group_counts = {group: 0 for group in all_groups[:-1]}
        for group, count in student_data:
            if group in group_counts:
                group_counts[group] = count
        groups = all_groups
        counts = [group_counts.get(group, 0) for group in all_groups[:-1]] + [total_books]

        # Create Matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 3))  # Adjusted for graph_frame size
        bars = ax.bar(groups, counts, color=['#4CAF50', '#2196F3', '#FF9800', '#F44336', '#9C27B0', '#795548'], edgecolor='white', linewidth=0.5)

        # Styling the graph
        ax.set_title("STUDENTS PER GROUP AND TOTAL BOOKS", fontsize=14, color="black", pad=10,fontweight="bold",)
        ax.set_facecolor("#31493c")  # Match frame background
        fig.patch.set_facecolor("#31493c")  # Match frame background

        # Remove y-axis label and tick labels
        ax.set_ylabel("")  # Already removed "Count" label
        ax.set_yticklabels([])  # Remove y-axis numerical tick labels
        ax.set_ylim(0, max(counts) + 2)  # Add padding to y-axis for better visibility

        # Adjust x-axis (labels already straight)
        ax.set_xlabel("")  # No x-axis label for cleaner look
        ax.tick_params(axis='x', rotation=0, colors="white", labelsize=10)

        # Add gridlines (horizontal)
        ax.grid(True, axis='y', linestyle='-', color='white', alpha=0.2)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}', 
                    ha='center', va='bottom', color="white", fontsize=10)

        # Remove spines for a cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')

        # Embed in graph_frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
        ################# FRAME 6 ###################
        self.info_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            corner_radius=10,
            height=150
        )
        self.info_frame.grid(row=1,column=3,padx=20, pady=(0, 20), sticky="nsew")
        self.info_frame.grid_columnconfigure(0,weight=1)
        self.info_frame.grid_rowconfigure(0,weight=1)
        self.info_frame.grid_rowconfigure(1,weight=1)
        self.info_frame.grid_rowconfigure(2,weight=1)

        self.quote_label = ctk.CTkLabel(
            self.info_frame,
            text="QUOTE OF THE DAY",
            font=("Segoe UI", 15, "bold"),
            text_color="black"
        )
        self.quote_label.grid(row=0,column=0,)

        self.request = self.quotes_req()
        self.request_quote = ctk.CTkLabel(
            self.info_frame,
            text=self.request,
            font=('Segoe UI',15,'bold'),
            text_color='white',
            wraplength=180,
            justify='center'
        )
        self.request_quote.grid(row=1,column=0)

    def students_records(self):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        self.layer_frame1 = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            # height=650,
            # width=500,
            corner_radius=10
        )
        self.layer_frame1.grid(row=0,column=0,sticky='nsew',padx=15,pady=15,columnspan=5,rowspan=2)
        StudentRecord(self.layer_frame1)
    
    def student_book(self):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        self.layer_frame2 = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            # height=650,
            # width=500,
            corner_radius=10
        )
        self.layer_frame2.grid(row=0,column=0,sticky='nsew',padx=15,pady=15,columnspan=5,rowspan=2)
        Books(self.layer_frame2)

    def issue_return(self):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        self.layer_frame3 = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            # height=650,
            # width=500,
            corner_radius=10
        )
        self.layer_frame3.grid(row=0,column=0,sticky='nsew',padx=15,pady=15,columnspan=5,rowspan=2)
        Books(self.layer_frame3)

    def issue_return(self):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        self.layer_frame3 = ctk.CTkFrame(
            self.main_frame,
            fg_color="#31493c",
            # height=650,
            # width=500,
            corner_radius=10
        )
        self.layer_frame3.grid(row=0,column=0,sticky='nsew',padx=15,pady=15,columnspan=5,rowspan=2)
        Books(self.layer_frame3)

    def close(self):
        self.quit()

    def images(self):
        logo = Image.open("Assets/Ideal-College.png").resize((185, 140))
        self.logo_img = ImageTk.PhotoImage(logo)

        logout = Image.open("Assets/logout.png").resize((30, 30))
        self.logout = ImageTk.PhotoImage(logout)

        dashicon = Image.open("Assets/icons8-home-24.png")
        self.dashicon = ImageTk.PhotoImage(dashicon)

        stduent_rec = Image.open("Assets/student_records.png").resize((30, 30))
        self.student_record = ImageTk.PhotoImage(stduent_rec)

        book = Image.open("Assets/open-book.png").resize((30, 30))
        self.book = ImageTk.PhotoImage(book)

        issue = Image.open("Assets/return-box.png").resize((30, 30))
        self.issue_return = ImageTk.PhotoImage(issue)

        transaction = Image.open("Assets/transaction-history.png").resize((30, 30))
        self.transaction_list = ImageTk.PhotoImage(transaction)

        reports = Image.open("Assets/report.png").resize((30,30))
        self.reports = ImageTk.PhotoImage(reports)

        mail = Image.open("Assets/mail.png").resize((30,30))
        self.mail = ImageTk.PhotoImage(mail)

        modification = Image.open('Assets\modification.png').resize((30,30))
        self.modification_img = ImageTk.PhotoImage(modification)

        students = Image.open("Assets/students.png").resize((100,100))
        self.students = ImageTk.PhotoImage(students)

        return_book = Image.open("Assets/return-book.png").resize((100,100))
        self.return_book = ImageTk.PhotoImage(return_book)
        
        inword_books = Image.open('Assets\inword.png').resize((80,80))
        self.inword_books = ImageTk.PhotoImage(inword_books)

        outword = Image.open('Assets\outword.png').resize((80,80))
        self.outword_img = ImageTk.PhotoImage(outword)

        totoal_books = Image.open('Assets\open-book.png').resize((100,100))
        self.total_books_img = ImageTk.PhotoImage(totoal_books)

    def quotes_req(self):
        education_quotes = [
            '"Education is the key to unlocking the world." - Oprah Winfrey',
            '"Learn as if you’ll live forever." - Mahatma Gandhi',
            '"Knowledge is power." - Francis Bacon',
            '"Education shapes the future." - Malala Yousafzai',
            '"Study hard, grow wise." - Benjamin Franklin',
            '"The mind is a fire to be kindled." - Plutarch',
            '"Education opens doors." - W.E.B. Du Bois',
            '"Grow through what you learn." - Socrates',
            '"Reality doesn’t bend to your wishes." - Jordan Peterson',
            '"Life is suffering; find meaning in it." - Viktor Frankl',
            '"Truth hurts, but lies destroy." - Warren Buffett',
            '"The world owes you nothing." - Mark Twain',
            '"Failure is the default; success is earned." - Elon Musk',
            '"Time waits for no one." - Geoffrey Chaucer'
        ]
        q = rand.choice(education_quotes)
        return q

    # def quotes_req(self):
    #     URL = "https://zenquotes.io/api/random"
    #     try:
    #         response = requests.get(URL)
    #         if response.status_code == 200:
    #             data = response.json()
    #             quote_data = random.choice(data)
    #             quote = quote_data['q']
    #             author = quote_data.get('a')  # Handle missing author
    #             return f'"{quote}" - {author}'
    #         else:
    #             education_quotes = [
    #                 '"Education is the key to unlocking the world." - Oprah Winfrey',
    #                 '"Learn as if you’ll live forever." - Mahatma Gandhi',
    #                 '"Knowledge is power." - Francis Bacon',
    #                 '"Education shapes the future." - Malala Yousafzai',
    #                 '"Study hard, grow wise." - Benjamin Franklin',
    #                 '"The mind is a fire to be kindled." - Plutarch',
    #                 '"Education opens doors." - W.E.B. Du Bois',
    #                 '"Grow through what you learn." - Socrates'
    #                 ]
    #             q = rand.choice(education_quotes)
    #             return q
    #             # return "Failed to fetch quote."
    #     except requests.exceptions.RequestException as e:
    #         CTkMessagebox(
    #             master=self,
    #             title="Info",
    #             message=f"Could not connect to the API. Details: {e}"
    #         )
    #         return "Error: Could not connect to the API."

if __name__ == "__main__":
    app = ctk.CTk()
    dashboard = Dashboard(app)
    app.mainloop()