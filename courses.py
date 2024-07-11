#courses.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

def search_courses(courses_list, search_date, search_name):
    filtered_courses = []

    for course in courses_list:
        if (not search_date or course["date"] == search_date.strftime("%d/%m/%Y")) and \
           (not search_name or search_name.lower() in course["object"].lower()):
            filtered_courses.append(course)

    return filtered_courses

def visualize_courses(courses_list):
    def search():
        search_date = entry_date.get_date()
        search_name = entry_name.get().strip()

        filtered_courses = search_courses(courses_list, search_date, search_name)
        update_table(filtered_courses)

    def update_table(courses):
        tree.delete(*tree.get_children())
        for idx, course in enumerate(courses, start=1):
            tree.insert("", "end", text=idx, values=(course["object"], course["date"], course["points-pet-course"], course["price"]))

    courses_window = tk.Toplevel()
    courses_window.title("Курсове")
    
    screen_width = courses_window.winfo_screenwidth()
    screen_height = courses_window.winfo_screenheight()
    window_width = 800 
    window_height = 600  
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    courses_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    search_frame = tk.Frame(courses_window)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Търси по дата:").grid(row=0, column=0, padx=5)
    entry_date = DateEntry(search_frame, width=12, background="darkblue", foreground="white", borderwidth=2)
    entry_date.grid(row=0, column=1, padx=5)

    tk.Label(search_frame, text="Търси по име на курс:").grid(row=0, column=2, padx=5)
    entry_name = tk.Entry(search_frame)
    entry_name.grid(row=0, column=3, padx=5)

    search_button = tk.Button(search_frame, text="Търси", command=search)
    search_button.grid(row=0, column=4, padx=5)

    tree = ttk.Treeview(courses_window, columns=("Object", "Date", "Points per Course", "Price"))
    tree.heading("#0", text="Номерация")
    tree.heading("Object", text="Дисциплина")
    tree.heading("Date", text="Дата")
    tree.heading("Points per Course", text="Точки за съответен курс")
    tree.heading("Price", text="Цена")

    update_table(courses_list)
    tree.pack(expand=True, fill="both")

def load_and_visualize_courses(filename):
    courses_list = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            next(file)  
            for line in file:
                data = line.strip().split(",")
                if len(data) == 4: 
                    course = {
                        "object": data[0].strip(),
                        "date": data[1].strip(),
                        "points-pet-course": int(data[2].strip()),
                        "price": float(data[3].strip())
                    }
                    courses_list.append(course)
    except FileNotFoundError:
        messagebox.showerror("Грешка", "Файлът с курсовете не е намерен.")

    visualize_courses(courses_list)

def show_courses():
    load_and_visualize_courses("courses.csv")
