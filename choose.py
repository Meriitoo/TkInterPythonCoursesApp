#choose.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import total

def load_operations_types(operations_types_filename):
    operations_types_dict = {}
    try:
        with open(operations_types_filename, "r", encoding="utf-8") as file:
            next(file)
            for line in file:
                code, operation_type = line.strip().split(",")
                operations_types_dict[int(code)] = operation_type
    except FileNotFoundError:
        messagebox.showerror("Грешка", "Видовете операции не са намерени.")
    return operations_types_dict

def load_operations(operations_filename):
    operations_list = []
    try:
        with open(operations_filename, "r", encoding="utf-8") as file:
            next(file)
            for line in file:
                student_number, operation, course, total_points = line.strip().split(",")
                operations_list.append({
                    "student number": int(student_number),
                    "operation": int(operation),
                    "course": course,
                })
    except FileNotFoundError:
        messagebox.showerror("Грешка", "Файла за операции не е намерен.")
    return operations_list

def show_students_by_operation(operations_types_dict, operations_list):
    def on_operation_select():
        selected_operation = int(operation_combobox.get())
        operation_type = operations_types_dict.get(selected_operation)
        filtered_students = [row for row in operations_list if row['operation'] == selected_operation]

        students_window = tk.Toplevel()
        students_window.title(f"Избрахте операция за {operation_type}")

        tree = ttk.Treeview(students_window, columns=("Student Number", "Course", "Price"), show="headings")
        tree.heading("Student Number", text="Номер на студент")
        tree.heading("Course", text="Курс")
        tree.heading("Price", text="Цена")

        courses_dict = total.load_courses("courses.csv")

        for row in filtered_students:
            course = row['course']
            price = courses_dict.get(course, "N/A")
            tree.insert("", "end", values=(row['student number'], course, price))

        tree.pack(expand=True, fill="both")

        if selected_operation == 3:
            amount_button = ttk.Button(students_window, text="Въведи сума за разсроченото плащане", command=lambda: open_amount_window(filtered_students))
            amount_button.pack(pady=10)

        center_window(students_window, 800, 600)

    def open_amount_window(students):
        amount_window = tk.Toplevel()
        amount_window.title("Добавяне на сума")
        center_window(amount_window, 400, 200)

        student_label = tk.Label(amount_window, text="Изберете студент:")
        student_label.pack(pady=10)

        student_numbers = [student['student number'] for student in students]
        student_combobox = ttk.Combobox(amount_window, values=student_numbers, state="readonly")
        student_combobox.pack(pady=10)

        amount_label = tk.Label(amount_window, text="Въведете първоначална вноска:")
        amount_label.pack(pady=10)

        amount_entry = tk.Entry(amount_window)
        amount_entry.pack(pady=10)

        def add_amount():
            selected_student_number = student_combobox.get()
            amount = amount_entry.get()
            if selected_student_number and amount:
                student = next((student for student in students if str(student['student number']) == selected_student_number), None)
                if student:
                    student_name = student['student number']
                    with open("total_amount.csv", 'a', encoding='utf-8') as file:
                        file.write(f"Номер на студент: {student_name}, Първоначална сума за плащане: {amount}\n")
                    messagebox.showinfo("Информация за плащане", f"Студент с номер {student_name} ще плати {amount} лв.")
                    amount_window.destroy()
                else:
                    messagebox.showerror("Грешка", "Не може да се намери студент с този номер.")
            else:
                messagebox.showerror("Грешка", "Моля, въведете валидна сума и изберете студент.")

        submit_button = ttk.Button(amount_window, text="Потвърди", command=add_amount)
        submit_button.pack(pady=10)


    choose_window = tk.Toplevel()
    choose_window.title("Избор на операции")

    operation_label = tk.Label(choose_window, text="Изберете операция:")
    operation_label.pack(pady=10)

    operation_combobox = ttk.Combobox(choose_window, values=list(operations_types_dict.keys()), state="readonly")
    operation_combobox.pack(pady=10)

    select_button = tk.Button(choose_window, text="Избери", command=on_operation_select)
    select_button.pack(pady=10)

    center_window(choose_window, 400, 200)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
