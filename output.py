#output.py
from tkinter import messagebox

def load_profiles(filename):
    profiles = {}
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            lines = csvfile.readlines()[1:] 
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) >= 2:  
                    profiles[int(parts[0])] = parts[1]
    except FileNotFoundError:
        messagebox.showerror("Грешка", f"{filename} не е намерен.")
    return profiles

def load_operations(filename):
    operations = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            lines = csvfile.readlines()[1:]  
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) >= 4:  
                    operations.append({
                        "СТУДЕНТСКИ НОМЕР": int(parts[0]),
                        "ОПЕРАЦИЯ": int(parts[1]),
                        "КУРС": parts[2],
                        "ОБЩ БРОЙ ТОЧКИ ДО МОМЕНТА": int(parts[3])
                    })
    except FileNotFoundError:
        messagebox.showerror("Грешка", f"{filename} не е намерен.")
    return operations

def load_courses(filename):
    courses = {}
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            lines = csvfile.readlines()[1:] 
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) >= 4:  
                    courses[parts[0]] = {
                        "СТАРТОВА ДАТА": parts[1],
                        "ТОЧКИ": int(parts[2]),
                        "СУМА": int(parts[3])
                    }
    except FileNotFoundError:
        messagebox.showerror("Грешка", f"{filename} не е намерен.")
    return courses

def load_bonuses(filename):
    bonuses = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            lines = csvfile.readlines()[1:]  
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) >= 2:  
                    bonuses.append({
                        "ТОЧКИ": int(parts[0]),
                        "ОТСТЪПКИ ОТ СУМАТА": int(parts[1])
                    })
    except FileNotFoundError:
        messagebox.showerror("Грешка", f"{filename} не е намерен.")
    return bonuses

def calculate_discount(total_points, bonuses):
    discount = 0
    for bonus in sorted(bonuses, key=lambda x: x['ТОЧКИ']):
        if total_points >= bonus['ТОЧКИ']:
            discount = bonus['ОТСТЪПКИ ОТ СУМАТА']
        else:
            break
    return discount

def generate_report(profiles, operations, courses, bonuses, student_id):
    student_name = profiles.get(student_id)
    student_operations = [op for op in operations if op['СТУДЕНТСКИ НОМЕР'] == student_id]

    if not student_operations:
        messagebox.showinfo("Информация", "Няма курсове за селектирания студент.")
        return

    total_points = 0
    total_price = 0
    report_lines = [
        "*" * 80,
        f"| Име на студент: {student_name}",
    "*" * 80
    ]

    for op in student_operations:
        course_name = op['КУРС']
        point_per_person = op['ОБЩ БРОЙ ТОЧКИ ДО МОМЕНТА']
        course_points = courses[course_name]['ТОЧКИ']
        course_price = courses[course_name]['СУМА']
        total_points += course_points
        total_price += course_price
        report_lines.extend([
            f"| Курс: {course_name}",
            f"| Точки, които курса дава: {course_points}",
            f"| Общо точки натрупани за момента: {point_per_person}",
            f"| Цена: {course_price}лв.",
            "*" * 80
        ])

    total_points += sum(op['ОБЩ БРОЙ ТОЧКИ ДО МОМЕНТА'] for op in student_operations)
    discount = calculate_discount(total_points, bonuses)
    total_price_after_discount = total_price - (total_price * discount / 100)

    report_lines.extend([
        f"| Общ брой точки: {total_points}",
        f"| Обща цена без отстъпка: {total_price}лв.",
        f"| Отстъпка: {discount}%",
        f"| Обща цена с отстъпка: {total_price_after_discount}лв.",
        "*" * 80
    ])

    with open("result.txt", "w", encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    messagebox.showinfo("Доклад", "Докладът е готов и съхранен в result.txt.")
