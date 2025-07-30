import mysql.connector
from CTkMessagebox import CTkMessagebox


class Database:
    @staticmethod
    def connect():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="SRIMAHAVISHNU@V",
            database="lib",
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
        cursor.execute(
            "SELECT student_id FROM students ORDER BY student_id DESC LIMIT 1"
        )
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
        cursor.execute("SELECT book_id FROM Books ORDER BY book_id DESC LIMIT 1")
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
            "SELECT COUNT(*) AS last_s_no FROM Issue_Return WHERE status = 'Issued'"
        )
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
            "SELECT COUNT(*) AS last_s_no FROM Issue_Return WHERE status = 'Returned'"
        )
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
            "SELECT student_group, COUNT(*) as student_count FROM students GROUP BY student_group"
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
        result = cursor.fetchone()[0] or 0
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def std_details(std_roll=None):
        conn = Database.connect()
        cursor = conn.cursor()
        query = "SELECT student_id, student_roll_no, name, email, phone, address, student_group , year FROM Students WHERE 1=1"
        params = []
        try:
            if std_roll:
                query += " AND student_roll_no = %s"
                params.append(std_roll)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            heading = ["ID", "ROLL NO", "NAME", "EMAIL", "PHONE", "ADDRESS", "GROUP"]
            formatted_data = [heading] + list(results)
            return formatted_data
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Database error: {e}")

    @staticmethod
    def books_data(isbn=None):
        conn = Database.connect()
        cursor = conn.cursor()
        query = "SELECT book_id, title, author, isbn, category, total_copies FROM Books WHERE 1=1"
        params = []
        try:
            if isbn:
                query += " AND isbn = %s"
                params.append(isbn)
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            heading = ["ID", "TITLE", "AUTHOR", "ISBN", "CATEGORY", "TOTAL COPIES"]
            formatted_data = [heading] + list(result)
            return formatted_data
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Database error: {e}")

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
                CTkMessagebox(title="info", message=f"Please Fill All Fields In Form")
                return
            query = "INSERT INTO Students (student_roll_no, name, email, phone, address, student_group, year) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            params = (rollno, name, email, phone, address, group, year)
            cursor.execute(query, params)
            CTkMessagebox(title="info", message=f"Data Inserted Sucuessfully")
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"{e}")
