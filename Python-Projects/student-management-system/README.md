# 🎓 Student Management System

A Python-based command-line application to manage student records with persistent file storage.

---

## 📌 Problem Statement

Educational institutions need an efficient way to store, retrieve, and manage student information. Manual record‑keeping is error‑prone and hard to maintain.  
This system provides a digital solution with **CRUD** operations and persistent data storage.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Add Student** | Insert new student records with validation (roll number uniqueness, age range, email format). |
| **View All Students** | Display all stored records in a tabular format. |
| **Search Student** | Find a student by roll number and show detailed information. |
| **Update Student** | Modify any field (name, age, grade, email) with validation. |
| **Delete Student** | Remove a student record after confirmation. |
| **Persistent Storage** | Data is saved in a CSV file (`students.csv`) and reloaded automatically. |
| **Data Validation** | Ensures data integrity (roll number uniqueness, age 5‑100, email format). |
| **Error Handling** | Gracefully handles file I/O errors and invalid inputs. |

---

## 🏗️ How It Works

### Architecture
User Input (CLI)
↓
Main Menu
↓
CRUD Functions (add, view, search, update, delete)
↓
Student Objects (in-memory list)
↓
Save/Load via CSV file


### Data Flow

1. On startup, the program loads all records from `students.csv` into a list of `Student` objects.
2. All operations are performed on this in‑memory list.
3. After every add, update, or delete, the list is written back to the CSV file.
4. The CSV file uses a header row and stores data in plain text.

### Validation Logic

- **Roll Number** – Must be unique (checked against existing records).
- **Age** – Must be an integer between 5 and 100.
- **Email** – Must contain `@` and a dot `.` (basic format check).
- **Name / Grade** – Cannot be empty.

---

## 🚀 Installation & Setup

### Requirements
- Python 3.6 or higher (no external libraries required)

### Steps

1. **Clone or download** the project files.
2. **Navigate** to the project folder.
3. **Run** the script:

```bash
python student_management.py
```

The file students.csv will be created automatically in the same directory when you add the first student.

##📖 Usage Guide

#Main Menu

==================================================
🎓 STUDENT MANAGEMENT SYSTEM
==================================================
1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. Exit
==================================================

# Examples
1. Add a Student
--- Add New Student ---
Roll Number: S001
Full Name: Riya Sharma
Age: 20
Grade: A
Email: riya@example.com
✅ Student added successfully!

2. View All Students
📋 All Students:
----------------------------------------------------------------------
Roll No    Name                 Age  Grade    Email
----------------------------------------------------------------------
S001       Riya Sharma          20   A        riya@example.com
S002       Amit Kumar           19   B+       amit@example.com
----------------------------------------------------------------------
Total: 2 student(s)

3. Search Student
Enter Roll Number to search: S001

🔍 Student Found:
--------------------------------------------------
Roll No : S001
Name    : Riya Sharma
Age     : 20
Grade   : A
Email   : riya@example.com
--------------------------------------------------

4. Update Student
Enter Roll Number to update: S001

✏️  Update Student (press Enter to keep current value):
1. Name    : Riya Sharma
2. Age     : 20
3. Grade   : A
4. Email   : riya@example.com
New Name (Riya Sharma): Riya Kumari
New Age (20): 21
New Grade (A): A+
New Email (riya@example.com): riya.kumari@example.com
✅ Student record updated successfully!

5. Delete Student
Enter Roll Number to delete: S002
Are you sure you want to delete Amit Kumar (y/n)? y
✅ Student 'Amit Kumar' deleted successfully.

## 📂 Project Structure
student-management-system/
│
├── student_management.py    # Main application code
├── students.csv             # Data file (auto‑generated)
├── README.md                # This documentation
└── screenshots/             (optional – for report)

## 🧪 Sample Test Cases
Test Case	Input	Expected Output
Add student with duplicate roll number	| Roll = S001 (already exists)	| ❌ Roll number already exists.
Add student with invalid age            | Age = 150			| ❌ Age must be between 5 and 100.
Add student with invalid email   	| Email = "abc"			| ❌ Invalid email format.
Update non‑existent student		| Roll = S999			| ❌ No student found.
Delete with confirmation		| Confirm = y			| ✅ Student deleted.
Delete with cancellation		| Confirm = n			| ❌ Deletion cancelled.

## 📚 Technical Details

    Language: Python 3

    Data Storage: CSV (Comma‑Separated Values)

    Modules used: csv, os, typing

    OOP: Student class with methods for conversion and representation.

    Validation: Functions for roll number, age, and email.

    Error Handling: try-except blocks for file operations and type conversions.

## ⚠️ Limitations

    No graphical interface (CLI only).

    Basic email validation (does not check actual domain existence).

    No authentication / login system (all data accessible).

    CSV file is not encrypted.

    No support for bulk import/export.

## 🚀 Future Improvements

    ✅ Add a GUI (Tkinter / PyQt).

    ✅ Implement search by name, grade, or email.

    ✅ Add sorting and filtering options.

    ✅ Support for database (SQLite) instead of CSV.

    ✅ Export data to PDF or Excel.

    ✅ Add backup and restore functionality.

    ✅ Implement user authentication.
    

## 👨‍💻 Author

Your Name
Roll No: [Your Roll Number]
Course: [Course Name]
College: [College Name]
Date: [Date]

## 📜 License

This project is created for academic purposes. All rights reserved.

## 🙏 Acknowledgements

    Open‑source Python community.

# Thank you for using the Student Management System! 🎓