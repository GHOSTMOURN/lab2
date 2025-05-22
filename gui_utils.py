import tkinter as tk
from tkinter import ttk
from measurements import TemperatureMeasurement
from data_utils import parse_line, save_measurements_to_file

def update_table(tree, measurements):
    """Обновляет таблицу с измерениями."""
    for item in tree.get_children():
        tree.delete(item)
    for measurement in measurements:
        tree.insert("", "end", values=(str(measurement),))
    print(f"Таблица обновлена: {len(measurements)} записей.")

def add_measurement(tree, measurements, filename, entry_type, entry_date,
                    entry_place, entry_value1, entry_value2):
    """Добавляет новое измерение."""
    measurement_type = entry_type.get()
    date = entry_date.get()
    place = entry_place.get()
    value1 = entry_value1.get()
    value2 = entry_value2.get()

    try:
        if measurement_type == "temperature":
            if not value2:
                raise ValueError("Введите влажность для температуры")
            line = f"temperature {date} \"{place}\" {value1} {value2}"
        else:  # pressure
            if value2:
                raise ValueError("Влажность не нужна для давления")
            line = f"pressure {date} \"{place}\" {value1}"
        measurement = parse_line(line)
        measurements.append(measurement)
        update_table(tree, measurements)
        save_measurements_to_file(filename, measurements)
        print(f"Добавлено: {line}")
    except ValueError as e:
        print(f"Ошибка: {e}. Проверьте формат даты (гггг.мм.дд) и чисел.")

def delete_selected(tree, measurements, filename):
    """Удаляет выделенное измерение."""
    selected = tree.selection()
    if selected:
        for item in selected:
            index = tree.index(item)
            removed = measurements.pop(index)
            tree.delete(item)
            print(f"Удалено: {str(removed)}")
        save_measurements_to_file(filename, measurements)
        update_table(tree, measurements)

def create_interface(measurements, filename):
    """Создает оконный интерфейс."""
    window = tk.Tk()
    window.title("Измерения")
    window.geometry("600x400")

    # Таблица
    tree = ttk.Treeview(window, columns=("Измерение",), show="headings")
    tree.heading("Измерение", text="Данные измерения")
    tree.pack(fill="both", expand=True)

    # Поля ввода
    frame = tk.Frame(window)
    frame.pack()

    tk.Label(frame, text="Тип:").grid(row=0, column=0)
    entry_type = ttk.Combobox(frame, values=["temperature", "pressure"])
    entry_type.grid(row=0, column=1)
    entry_type.current(0)  # По умолчанию "temperature"

    tk.Label(frame, text="Дата (гггг.мм.дд):").grid(row=0, column=2)
    entry_date = tk.Entry(frame)
    entry_date.grid(row=0, column=3)

    tk.Label(frame, text="Место:").grid(row=1, column=0)
    entry_place = tk.Entry(frame)
    entry_place.grid(row=1, column=1)

    tk.Label(frame, text="Значение 1:").grid(row=1, column=2)
    entry_value1 = tk.Entry(frame)
    entry_value1.grid(row=1, column=3)

    tk.Label(frame, text="Значение 2:").grid(row=2, column=2)
    entry_value2 = tk.Entry(frame)
    entry_value2.grid(row=2, column=3)

    # Кнопки
    tk.Button(frame, text="Добавить",
              command=lambda: add_measurement(tree, measurements, filename,
                                             entry_type, entry_date, entry_place,
                                             entry_value1, entry_value2)).grid(
        row=3, column=0, columnspan=2)
    tk.Button(frame, text="Удалить",
              command=lambda: delete_selected(tree, measurements, filename)).grid(
        row=3, column=2, columnspan=2)

    # Инициализация таблицы
    update_table(tree, measurements)

    window.mainloop()