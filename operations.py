#operations.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def load_profiles(profiles_filename):
    profiles_dict = {}

    try:
        with open(profiles_filename, "r", encoding="utf-8") as file:
            lines = file.readlines()[1:]
            for line in lines:
                data = line.strip().split(",")
                if len(data) == 2:
                    student_number, name = data
                    profiles_dict[student_number] = name
    except FileNotFoundError:
        messagebox.showerror("Грешка", "Файла с профилите не е намерен.")
    
    return profiles_dict

def load_operations(filename):
    operations_dict = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()[1:]
            for line in lines:
                data = line.strip().split(",")
                if len(data) == 4:
                    student_number, operation, course, total_points = data
                    if student_number not in operations_dict:
                        operations_dict[student_number] = []
                    operations_dict[student_number].append(course)
    except FileNotFoundError:
        messagebox.showerror("Грешка", "Файла за операциите не е намерен.")
    
    return operations_dict

def show_student_courses(operations_dict, profiles_dict):
    def update_courses():
        student_name = student_var.get()
        student_number = [key for key, value in profiles_dict.items() if value == student_name][0]
        courses = operations_dict.get(student_number, [])
        num_courses = len(courses)
        courses_list_var.set(f"Общ брой курсове записани: {num_courses}\nИмена на курсовете: {', '.join(courses)}")

    operations_window = tk.Toplevel()
    operations_window.title("Курсове на студенти")
    
    screen_width = operations_window.winfo_screenwidth()
    screen_height = operations_window.winfo_screenheight()
    window_width = 800  
    window_height = 600 
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    operations_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    center_frame = tk.Frame(operations_window)
    center_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
    
    operations_window.grid_rowconfigure(0, weight=1)
    operations_window.grid_columnconfigure(0, weight=1)
    center_frame.grid_rowconfigure(0, weight=1)
    center_frame.grid_columnconfigure(0, weight=1)

    student_var = tk.StringVar()
    student_dropdown = ttk.Combobox(center_frame, textvariable=student_var)
    student_dropdown['values'] = list(profiles_dict.values())
    student_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
    student_dropdown.bind("<<ComboboxSelected>>", lambda event: update_courses())

    courses_list_var = tk.StringVar()
    courses_list_label = tk.Label(center_frame, textvariable=courses_list_var)
    courses_list_label.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

def perform_operations_courses():
    profiles_dict = load_profiles("profiles.csv")
    operations_dict = load_operations("operations.csv")
    show_student_courses(operations_dict, profiles_dict)

