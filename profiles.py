#profiles.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def show_profiles():
    profiles_window = tk.Toplevel()
    profiles_window.title("Профили")

    screen_width = profiles_window.winfo_screenwidth()
    screen_height = profiles_window.winfo_screenheight()
    window_width = 800  
    window_height = 600  
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    
    profiles_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tree = ttk.Treeview(profiles_window)
    tree["columns"] = ("Student Number", "Names")
    tree.heading("#0", text="Номерация")
    tree.heading("Student Number", text="Студентски номер")
    tree.heading("Names", text="Име")

    try:
        with open("profiles.csv", "r", encoding="utf-8") as file:
            next(file)  
            for idx, line in enumerate(file, start=1):
                data = line.strip().split(",")
                if len(data) == 2:
                    tree.insert("", "end", text=idx, values=(data[0], data[1]))
    except FileNotFoundError:
        messagebox.showerror("Error", "Профилите не са намерени.")

    tree.pack(expand=True, fill="both")

