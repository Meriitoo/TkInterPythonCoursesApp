#main.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk 
import profiles
import courses
import operations
import total
import choose
import output  

def open_profiles():
    profiles.show_profiles()

def open_courses():
    courses.show_courses()

def perform_operations_courses():
    operations.perform_operations_courses()

def perform_operations_students():
    total.perform_operations_students()

def open_operation_selection():
    operations_types_dict = choose.load_operations_types()
    operations_list = choose.load_operations("operations.csv")
    choose.show_students_by_operation(operations_types_dict, operations_list)

def generate_report_handler():
    student_name = student_combobox.get()
    if student_name:
        student_id = [id for id, name in profiles_dict.items() if name == student_name][0]
        output.generate_report(profiles_dict, operations_list, courses_dict, bonuses_list, student_id)
    else:
        messagebox.showerror("Грешка", "Моля изберете студент.")

def exit_application():
    if messagebox.askokcancel("Изход", "Сигурни ли сте, че искате да излезете?"):
        root.destroy()

profiles_dict = output.load_profiles("profiles.csv")
operations_list = output.load_operations("operations.csv")
courses_dict = output.load_courses("courses.csv")
bonuses_list = output.load_bonuses("bonuses.csv")

root = tk.Tk()
root.title("Меню")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 800
window_height = 600

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.grid(row=0, column=0, columnspan=2, rowspan=10)

background_image = Image.open("background_image.png")
background_image = background_image.resize((window_width, window_height), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)

style = ttk.Style()
style.configure("TButton", font=("Times New Roman", 12), foreground="blue")
style.configure("TLabel", font=("Times New Roman", 12), foreground="blue")

btn_profiles = ttk.Button(root, text="Профили", command=open_profiles, style="TButton")
btn_profiles.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

btn_courses = ttk.Button(root, text="Курсове", command=open_courses, style="TButton")
btn_courses.grid(row=2, column=0, padx=10, pady=5, sticky='ew')

btn_operations = ttk.Button(root, text="Курсове на студенти", command=perform_operations_courses, style="TButton")
btn_operations.grid(row=3, column=0, padx=10, pady=5, sticky='ew')

btn_operations_2 = ttk.Button(root, text="Търси информация за студент", command=perform_operations_students, style="TButton")
btn_operations_2.grid(row=4, column=0, padx=10, pady=5, sticky='ew')

btn_operation_selection = ttk.Button(root, text="Видове операции", command=open_operation_selection, style="TButton")
btn_operation_selection.grid(row=5, column=0, padx=10, pady=5, sticky='ew')

label_select_student = ttk.Label(root, text="Изберете студент за доклада:", style="TLabel")
label_select_student.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

student_combobox = ttk.Combobox(root, state="readonly", values=list(profiles_dict.values()))
student_combobox.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

btn_generate_report = ttk.Button(root, text="Доклад", command=generate_report_handler, style="TButton")
btn_generate_report.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

btn_exit = ttk.Button(root, text="Изход", command=exit_application, style="TButton")
btn_exit.grid(row=4, column=1, padx=10, pady=5, sticky='ew')

root.mainloop()
