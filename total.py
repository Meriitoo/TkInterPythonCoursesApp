#total.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import operations

def load_operations(operations_filename):
    operations_dict = {}
    try:
        with open(operations_filename, "r", encoding="utf-8") as file:
            lines = file.readlines()[1:] 
            for line in lines:
                data = line.strip().split(",")
                if len(data) == 4:  
                    student_number, operation, course, total_points = data
                    total_points = int(total_points)
                    if student_number not in operations_dict:
                        operations_dict[student_number] = {'courses': [], 'total_points': 0}
                    operations_dict[student_number]['courses'].append(course)
                    operations_dict[student_number]['total_points'] += total_points
    except FileNotFoundError:
        messagebox.showerror("Грешка", "Файла за операциите не е намерен.")
    return operations_dict

def load_bonuses(bonuses_filename):
    bonuses_dict = {}
    try:
        with open(bonuses_filename, "r", encoding="utf-8") as file:
            lines = file.readlines()[1:]  
            for line in lines:
                data = line.strip().split(",")
                if len(data) == 2: 
                    total_points, discount = map(int, data)
                    bonuses_dict[total_points] = discount
    except FileNotFoundError:
        messagebox.showerror("Грешка", "Файла за бонусите не е намерен.")
    return bonuses_dict

def load_courses(courses_filename):
    courses_dict = {}
    try:
        with open(courses_filename, "r", encoding="utf-8") as file:
            lines = file.readlines()[1:]  
            for line in lines:
                data = line.strip().split(",")
                if len(data) == 4: 
                    course_name, date, points_per_course, price = data
                    courses_dict[course_name] = float(price)
    except FileNotFoundError:
        messagebox.showerror("Грешка", "Файла с курсовете не е намерен.")
    return courses_dict

def show_student_discounts(tab, profiles_dict, operations_dict, bonuses_dict, courses_dict):
    def update_discounts():
        tree.delete(*tree.get_children())
        for student_number, student_data in operations_dict.items():
            total_points = student_data['total_points']
            student_name = profiles_dict.get(student_number, "Unknown")
            discount = next((bonuses_dict[points] for points in sorted(bonuses_dict.keys(), reverse=True) if total_points >= points), 0)
            for course in student_data['courses']:
                course_price = courses_dict.get(course, 0.0)
                discounted_price = course_price * (1 - discount / 100)
                if discount == 0:
                    discount_message = "Няма бонуси"
                else:
                    discount_message = f"${discounted_price:.2f}"
                tree.insert("", "end", values=(student_name, course, total_points, f"${course_price:.2f}", discount_message))

    tree = ttk.Treeview(tab, columns=("Student Name", "Course", "Total Points", "Original Price", "Discounted Price"), show="headings")
    tree.heading("Student Name", text="Име на студент")
    tree.heading("Course", text="Курс")
    tree.heading("Total Points", text="Общ брой точки")
    tree.heading("Original Price", text="Цена без отстъпка")
    tree.heading("Discounted Price", text="Цена с отстъпка")

    tree.pack(expand=True, fill="both")

    update_discounts()


def show_search_results(tab, profiles_dict, operations_dict, courses_dict):
    def search_student():
        search_id = askstring("Търси студент", "Въведете номера на студента:")
        if search_id in operations_dict:
            student_data = operations_dict[search_id]
            student_name = profiles_dict.get(search_id, "Unknown")
            total_points = student_data['total_points']
            tree.delete(*tree.get_children())
            for course in student_data['courses']:
                course_price = courses_dict.get(course, 0.0)
                tree.insert("", "end", values=(student_name, course, total_points, f"${course_price:.2f}"))
        else:
            messagebox.showinfo("Грешка", "Студента не е намерен.")

    search_button = tk.Button(tab, text="Търси студент", command=search_student)
    search_button.pack(pady=10)

    tree = ttk.Treeview(tab, columns=("Student Name", "Course", "Total Points", "Course Price"), show="headings")
    tree.heading("Student Name", text="Име на студент")
    tree.heading("Course", text="Курс")
    tree.heading("Total Points", text="Общ брой точки")
    tree.heading("Course Price", text="Цена на курс")

    tree.pack(expand=True, fill="both")

def perform_operations_students():
    profiles_dict = operations.load_profiles(("profiles.csv"))
    operations_dict = load_operations("operations.csv")
    bonuses_dict = load_bonuses("bonuses.csv")
    courses_dict = load_courses("courses.csv")

    operations_window = tk.Toplevel()
    operations_window.title("Обобщаване на данните за студента")

    notebook = ttk.Notebook(operations_window)

    discounts_tab = ttk.Frame(notebook)
    search_tab = ttk.Frame(notebook)

    notebook.add(discounts_tab, text="Студенти бонуси")
    notebook.add(search_tab, text="Търси за студент")

    notebook.pack(expand=True, fill="both")

    show_student_discounts(discounts_tab, profiles_dict, operations_dict, bonuses_dict, courses_dict)
    show_search_results(search_tab, profiles_dict, operations_dict, courses_dict)

    center_window(operations_window, 1000, 600)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

