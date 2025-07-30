# Library Management System

## Overview

This project is a comprehensive Library Management System built with Python and a graphical user interface (GUI) using [customtkinter](https://github.com/TomSchimansky/CustomTkinter). It manages books, students, transactions, reports, and more, providing an intuitive dashboard and modular navigation for library staff.

---

## Main Modules and Files

### `main.py`
- **Entry point** for the application.
- Typically initializes the main window and launches the dashboard or login screen.

### `Dashboard.py`
- Implements the main **Dashboard** window.
- Displays key statistics (students, books, issued/returned books), a bar graph, and a "Quote of the Day".
- Provides navigation to all other modules.

### `Database.py`
- Contains the **Database** class and related functions.
- Handles all database operations, such as fetching student and book statistics, and managing records.

### `Books.py`
- Manages **book records**: adding, editing, deleting, and viewing books in the library.

### `StudentsRecords.py`
- Manages **student records**: adding, editing, deleting, and viewing student information.

### `IssueReturn.py`
- Handles the **issuing and returning** of books.
- Manages book availability and student borrowing history.

### `Transaction.py`
- Manages and displays **transaction history** for book issues and returns.

### `Reports.py`
- Generates various **reports** (e.g., overdue books, borrowing statistics).

### `Mailing.py`
- Handles **mailing features** such as sending notifications or reminders to students.

### `Modification.py`
- Provides an interface for **modifying system settings** or records.

### `UI/theme.py`
- Contains **UI theming** and styling options for a consistent look and feel.

---

## Assets

### `Assets/`
- Contains all **image assets** (icons, logos, etc.) used throughout the application.

---

## Other Files

### `README.md`
- Project-level documentation and instructions.

### `useless.txt`
- Placeholder or unused file (can be ignored or deleted).

### `__pycache__/`
- Python's **bytecode cache** directory (auto-generated).

---

## How to Run

1. Ensure all dependencies are installed:
   - `customtkinter`
   - `Pillow`
   - `matplotlib`
   - `requests`
   - Any other required libraries

2. Place all assets in the `Assets/` folder as referenced in the code.

3. Run the application:
   ```powershell
   python main.py
   ```

---

## Features

- **Dashboard:** Visual overview of library statistics and quick navigation.
- **Student Management:** Add, edit, and view student records.
- **Book Management:** Add, edit, and view book records.
- **Issue/Return:** Manage book lending and returns.
- **Transactions:** View transaction history.
- **Reports:** Generate and view library reports.
- **Mailing:** Send notifications to students.
- **Settings/Modification:** Update system settings and records.
- **Modern UI:** Clean, themed interface with icons and images.

---

## Folder Structure

```
LIBRARY MANAGEMENT/
│
├── Assets/                # All image and icon assets
├── UI/
│   └── theme.py           # UI theming and styling
├── Books.py
├── Dashboard.py
├── Database.py
├── IssueReturn.py
├── Mailing.py
├── main.py
├── Modification.py
├── README.md
├── Reports.py
├── StudentsRecords.py
├── Transaction.py
├── useless.txt
└── __pycache__/           # Python bytecode cache
```

---

## Notes

- The system is modular; each major function is in its own file for maintainability.
- All database interactions are abstracted in `Database.py`.
- The UI is built with `customtkinter` for a modern look.
- Ensure all assets are present for the UI to display correctly.
- This project is under development stage

---

## License

This project is for educational and demonstration purposes.
