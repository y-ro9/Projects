#!/usr/bin/env python3
"""
Student Management System
A Python application to manage student records with persistent CSV storage.
"""

import csv
import os
from typing import List, Dict, Optional

# ---------- Data File ----------
DATA_FILE = "students.csv"

# ---------- Student Class ----------
class Student:
    """Represents a student record."""
    def __init__(self, roll_no: str, name: str, age: int, grade: str, email: str):
        self.roll_no = roll_no
        self.name = name.title().strip()
        self.age = age
        self.grade = grade.upper().strip()
        self.email = email.strip().lower()

    def to_dict(self) -> Dict:
        """Convert student object to dictionary for CSV."""
        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "email": self.email
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Student':
        """Create a Student object from dictionary."""
        return Student(
            roll_no=data["roll_no"],
            name=data["name"],
            age=int(data["age"]),
            grade=data["grade"],
            email=data["email"]
        )

    def __str__(self):
        return f"{self.roll_no} | {self.name} | {self.age} | {self.grade} | {self.email}"


# ---------- File Handling ----------
def load_students() -> List[Student]:
    """Load student records from CSV file."""
    students = []
    if not os.path.exists(DATA_FILE):
        return students
    try:
        with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(Student.from_dict(row))
    except Exception as e:
        print(f"⚠️ Error loading data: {e}")
    return students

def save_students(students: List[Student]) -> None:
    """Save student records to CSV file."""
    try:
        with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["roll_no", "name", "age", "grade", "email"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for student in students:
                writer.writerow(student.to_dict())
        print("✅ Data saved successfully.")
    except Exception as e:
        print(f"❌ Error saving data: {e}")

# ---------- Validation ----------
def validate_roll_no(roll_no: str, students: List[Student], ignore: Optional[str] = None) -> bool:
    """Check if roll number already exists (except when updating)."""
    for s in students:
        if s.roll_no == roll_no and (ignore is None or s.roll_no != ignore):
            return False
    return True

def validate_age(age_str: str) -> bool:
    """Check if age is a valid integer between 5 and 100."""
    try:
        age = int(age_str)
        return 5 <= age <= 100
    except ValueError:
        return False

def validate_email(email: str) -> bool:
    """Simple email validation (presence of @ and .)."""
    return "@" in email and "." in email

def get_student_by_roll(roll_no: str, students: List[Student]) -> Optional[Student]:
    """Return student object if found else None."""
    for student in students:
        if student.roll_no == roll_no:
            return student
    return None

# ---------- CRUD Operations ----------
def add_student(students: List[Student]) -> None:
    """Add a new student record."""
    print("\n--- Add New Student ---")
    while True:
        roll_no = input("Roll Number: ").strip()
        if not roll_no:
            print("❌ Roll number cannot be empty.")
            continue
        if not validate_roll_no(roll_no, students):
            print("❌ Roll number already exists. Please use a unique roll number.")
            continue
        break

    name = input("Full Name: ").strip()
    while not name:
        print("❌ Name cannot be empty.")
        name = input("Full Name: ").strip()

    age_str = input("Age: ").strip()
    while not validate_age(age_str):
        print("❌ Age must be a number between 5 and 100.")
        age_str = input("Age: ").strip()
    age = int(age_str)

    grade = input("Grade (e.g., A, B+, C): ").strip()
    while not grade:
        print("❌ Grade cannot be empty.")
        grade = input("Grade: ").strip()

    email = input("Email: ").strip()
    while not validate_email(email):
        print("❌ Invalid email format (must contain @ and .).")
        email = input("Email: ").strip()

    student = Student(roll_no, name, age, grade, email)
    students.append(student)
    save_students(students)
    print("✅ Student added successfully!")

def view_students(students: List[Student]) -> None:
    """Display all student records."""
    if not students:
        print("\n📭 No student records found.")
        return
    print("\n📋 All Students:")
    print("-" * 70)
    print(f"{'Roll No':<10} {'Name':<20} {'Age':<5} {'Grade':<8} {'Email'}")
    print("-" * 70)
    for student in students:
        print(f"{student.roll_no:<10} {student.name:<20} {student.age:<5} {student.grade:<8} {student.email}")
    print("-" * 70)
    print(f"Total: {len(students)} student(s)")

def search_student(students: List[Student]) -> None:
    """Search for a student by roll number."""
    roll_no = input("\nEnter Roll Number to search: ").strip()
    if not roll_no:
        print("❌ Roll number cannot be empty.")
        return
    student = get_student_by_roll(roll_no, students)
    if student:
        print("\n🔍 Student Found:")
        print("-" * 50)
        print(f"Roll No : {student.roll_no}")
        print(f"Name    : {student.name}")
        print(f"Age     : {student.age}")
        print(f"Grade   : {student.grade}")
        print(f"Email   : {student.email}")
        print("-" * 50)
    else:
        print(f"❌ No student found with Roll Number '{roll_no}'.")

def update_student(students: List[Student]) -> None:
    """Update an existing student record."""
    roll_no = input("\nEnter Roll Number to update: ").strip()
    if not roll_no:
        print("❌ Roll number cannot be empty.")
        return
    student = get_student_by_roll(roll_no, students)
    if not student:
        print(f"❌ No student found with Roll Number '{roll_no}'.")
        return

    print("\n✏️  Update Student (press Enter to keep current value):")
    print(f"1. Name    : {student.name}")
    print(f"2. Age     : {student.age}")
    print(f"3. Grade   : {student.grade}")
    print(f"4. Email   : {student.email}")

    # Update name
    new_name = input(f"New Name ({student.name}): ").strip()
    if new_name:
        student.name = new_name.title()

    # Update age
    new_age = input(f"New Age ({student.age}): ").strip()
    if new_age:
        while not validate_age(new_age):
            print("❌ Invalid age. Must be between 5 and 100.")
            new_age = input(f"New Age ({student.age}): ").strip()
        student.age = int(new_age)

    # Update grade
    new_grade = input(f"New Grade ({student.grade}): ").strip()
    if new_grade:
        student.grade = new_grade.upper()

    # Update email
    new_email = input(f"New Email ({student.email}): ").strip()
    if new_email:
        while not validate_email(new_email):
            print("❌ Invalid email format.")
            new_email = input(f"New Email ({student.email}): ").strip()
        student.email = new_email.lower()

    save_students(students)
    print("✅ Student record updated successfully!")

def delete_student(students: List[Student]) -> None:
    """Delete a student record."""
    roll_no = input("\nEnter Roll Number to delete: ").strip()
    if not roll_no:
        print("❌ Roll number cannot be empty.")
        return
    student = get_student_by_roll(roll_no, students)
    if not student:
        print(f"❌ No student found with Roll Number '{roll_no}'.")
        return

    confirm = input(f"Are you sure you want to delete {student.name} (y/n)? ").strip().lower()
    if confirm == 'y':
        students.remove(student)
        save_students(students)
        print(f"✅ Student '{student.name}' deleted successfully.")
    else:
        print("❌ Deletion cancelled.")

# ---------- Main Menu ----------
def display_menu():
    print("\n" + "="*50)
    print("🎓 STUDENT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")
    print("="*50)

def main():
    students = load_students()
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            print("\n👋 Exiting Student Management System. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()