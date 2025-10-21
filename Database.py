import mysql.connector
from CTkMessagebox import CTkMessagebox


class Database:
    @staticmethod
    def connect():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="srimahavishnu",
            database="lib",
            auth_plugin="mysql_native_password",
        )

    @staticmethod
    def authenticate(username, password):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE Username=%s AND Password=%s",
            (username, password),
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def total_std():
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Students")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return str(result[0])
        else:
            return "0"

    @staticmethod
    def Books():
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Books")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return str(result[0])
        else:
            return "0"

    @staticmethod
    def total_inwords():
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM Issue_Return WHERE status = 'Returned'"
        )  # FIXED: Changed to 'Returned'
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return str(result[0])
        else:
            return "0"

    @staticmethod
    def total_outwords():
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM Issue_Return WHERE status = 'Issued'"
        )  # FIXED: Changed to 'Issued'
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return str(result[0])
        else:
            return "0"

    @staticmethod
    def students_per_group():
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT student_group, COUNT(*) as student_count FROM Students GROUP BY student_group"
        )
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result if result else []

    @staticmethod
    def total_books():
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(total_copies) as total_books FROM Books")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result and result[0]:
            return result[0]
        else:
            return 0

    @staticmethod
    def std_details(std_roll=None):
        conn = Database.connect()
        cursor = conn.cursor()
        query = "SELECT student_id, student_roll_no, name, email, phone, address, student_group, year FROM Students WHERE 1=1"
        params = []
        try:
            if std_roll:
                query += " AND student_roll_no = %s"
                params.append(std_roll)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            heading = [
                "ID",
                "ROLL NO",
                "NAME",
                "EMAIL",
                "PHONE",
                "ADDRESS",
                "GROUP",
                "YEAR",
            ]
            formatted_data = [heading] + list(results)
            return formatted_data
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Database error: {e}")
            return []

    @staticmethod
    def books_data(isbn=None):
        conn = Database.connect()
        cursor = conn.cursor()
        query = "SELECT book_id, title, author, isbn, category, total_copies, available_copies FROM Books WHERE 1=1"
        params = []
        try:
            if isbn:
                query += " AND isbn = %s"
                params.append(isbn)
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            heading = [
                "ID",
                "TITLE",
                "AUTHOR",
                "ISBN",
                "CATEGORY",
                "TOTAL COPIES",
                "AVAILABLE COPIES",
            ]
            formatted_data = [heading] + list(result)
            return formatted_data
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Database error: {e}")
            return []

    @staticmethod
    def std_dtls_insert(rollno, name, email, phone, address, group, year):
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            if (
                not rollno
                or not name
                or not email
                or not phone
                or not address
                or not group
                or not year
            ):
                CTkMessagebox(
                    title="info", message="Please Fill All Fields In Form")
                return False
            query = "INSERT INTO Students (student_roll_no, name, email, phone, address, student_group, year) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            params = (rollno, name, email, phone, address, group, year)
            cursor.execute(query, params)
            conn.commit()
            CTkMessagebox(title="info", message="Data Inserted Successfully")
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            CTkMessagebox(title="Error", message=f"{e}")
            return False

    @staticmethod
    def add_book(isbn, title, author, category, total_copies):
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            if not isbn or not title or not author or not category or not total_copies:
                CTkMessagebox(
                    title="info", message="Please Fill All Fields In Form")
                return False
            query = "INSERT INTO Books (isbn, title, author, category, total_copies, available_copies) VALUES (%s,%s,%s,%s,%s,%s)"
            params = (isbn, title, author, category,
                      total_copies, total_copies)
            cursor.execute(query, params)
            conn.commit()
            CTkMessagebox(title="info", message="Book Added Successfully")
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            CTkMessagebox(title="Error", message=f"{e}")
            return False

    @staticmethod
    def issue_book(student_id, book_id, issue_date, due_date, issued_by="admin"):
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            # Check if book is available
            cursor.execute(
                "SELECT available_copies FROM Books WHERE book_id = %s", (
                    book_id,)
            )
            book = cursor.fetchone()

            if book and book[0] > 0:
                # Issue the book
                cursor.execute(
                    "INSERT INTO Issue_Return (student_id, book_id, issue_date, due_date, issued_by) VALUES (%s,%s,%s,%s,%s)",
                    (student_id, book_id, issue_date, due_date, issued_by),
                )
                # Update available copies
                cursor.execute(
                    "UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = %s",
                    (book_id,),
                )
                conn.commit()
                CTkMessagebox(title="info", message="Book Issued Successfully")
                cursor.close()
                conn.close()
                return True
            else:
                CTkMessagebox(title="info", message="Book not available")
                return False
        except Exception as e:
            CTkMessagebox(title="Error", message=f"{e}")
            return False

    @staticmethod
    def return_book(issue_id, return_date, fine_amount=0):
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            # Get book_id from the issue
            cursor.execute(
                "SELECT book_id FROM Issue_Return WHERE issue_id = %s", (
                    issue_id,)
            )
            issue = cursor.fetchone()

            if issue:
                book_id = issue[0]
                # Update issue record
                cursor.execute(
                    "UPDATE Issue_Return SET return_date = %s, fine_amount = %s, status = 'Returned' WHERE issue_id = %s",
                    (return_date, fine_amount, issue_id),
                )
                # Update available copies
                cursor.execute(
                    "UPDATE Books SET available_copies = available_copies + 1 WHERE book_id = %s",
                    (book_id,),
                )
                conn.commit()
                CTkMessagebox(
                    title="info", message="Book Returned Successfully")
                cursor.close()
                conn.close()
                return True
            else:
                CTkMessagebox(title="Error", message="Issue record not found")
                return False
        except Exception as e:
            CTkMessagebox(title="Error", message=f"{e}")
            return False

    @staticmethod
    def get_student_by_roll(roll_no):
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT student_id, name FROM Students WHERE student_roll_no = %s",
                (roll_no,),
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_book_by_isbn(isbn):
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT book_id, title, available_copies FROM Books WHERE isbn = %s",
                (isbn,),
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_active_issues():
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT ir.issue_id, s.student_roll_no, s.name, b.title, b.isbn, ir.issue_date, ir.due_date 
                FROM Issue_Return ir
                JOIN Students s ON ir.student_id = s.student_id
                JOIN Books b ON ir.book_id = b.book_id
                WHERE ir.status = 'Issued'
            """)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def get_all_transactions(student_roll=None):
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            query = """
                SELECT 
                    ir.issue_id,
                    s.student_roll_no,
                    s.name as student_name,
                    b.title as book_title,
                    b.isbn,
                    ir.issue_date,
                    ir.due_date,
                    ir.return_date,
                    ir.fine_amount,
                    ir.status,
                    ir.issued_by
                FROM Issue_Return ir
                JOIN Students s ON ir.student_id = s.student_id
                JOIN Books b ON ir.book_id = b.book_id
                """

            params = []
            if student_roll:
                query += " WHERE s.student_roll_no = %s"
                params.append(student_roll)

            query += " ORDER BY ir.issue_date DESC"

            cursor.execute(query, params)
            result = cursor.fetchall()
            return result

        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_student_report():
        """Get student statistics for reports"""
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            # Total students per group
            cursor.execute("""
                SELECT student_group, COUNT(*) as count 
                FROM Students 
                GROUP BY student_group
            """)
            students_per_group = cursor.fetchall()

            # Total students
            cursor.execute("SELECT COUNT(*) FROM Students")
            total_students = cursor.fetchone()[0]

            return {
                "students_per_group": students_per_group,
                "total_students": total_students,
            }

        except Exception as e:
            # Remove the print statement below
            # print(f"Error generating student report: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_books_report():
        """Get books statistics for reports"""
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            # Books per category
            cursor.execute("""
                SELECT category, COUNT(*) as count, SUM(total_copies) as total_copies
                FROM Books 
                GROUP BY category
            """)
            books_per_category = cursor.fetchall()

            # Total books and available books
            cursor.execute("""
                SELECT SUM(total_copies) as total_books, 
                    SUM(available_copies) as available_books 
                FROM Books
            """)
            total_books_result = cursor.fetchone()
            total_books = total_books_result[0] or 0
            available_books = total_books_result[1] or 0

            return {
                "books_per_category": books_per_category,
                "total_books": total_books,
                "available_books": available_books,
            }

        except Exception as e:
            # Remove the print statement below
            # print(f"Error generating books report: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_issue_return_report():
        """Get issue/return statistics for reports"""
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            # Currently issued books
            cursor.execute(
                "SELECT COUNT(*) FROM Issue_Return WHERE status = 'Issued'")
            currently_issued = cursor.fetchone()[0]

            # Total returns
            cursor.execute(
                "SELECT COUNT(*) FROM Issue_Return WHERE status = 'Returned'"
            )
            total_returns = cursor.fetchone()[0]

            # Books with pending returns (overdue)
            cursor.execute("""
                SELECT COUNT(*) 
                FROM Issue_Return 
                WHERE status = 'Issued' AND due_date < CURDATE()
            """)
            overdue_books = cursor.fetchone()[0]

            # Total fines collected
            cursor.execute(
                "SELECT SUM(fine_amount) FROM Issue_Return WHERE status = 'Returned'"
            )
            total_fines = cursor.fetchone()[0] or 0

            return {
                "currently_issued": currently_issued,
                "total_returns": total_returns,
                "overdue_books": overdue_books,
                "total_fines": total_fines,
            }

        except Exception as e:
            # Remove the print statement below
            # print(f"Error generating issue/return report: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()
