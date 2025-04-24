import datetime
import tkinter as tk
from tkinter import ttk
import os

# Классы для измерений
class Measurement:
    """Базовый класс для хранения данных об измерении."""
    def __init__(self, date, place):
        self.date = datetime.datetime.strptime(date, "%Y.%m.%d").date()
        self.place = place.strip('"')

    def __str__(self):
        return f"Дата: {self.date}, Место: {self.place}"

class TemperatureMeasurement(Measurement):
    """Класс для измерения температуры и влажности."""
    def __init__(self, date, place, temperature, humidity):
        super().__init__(date, place)
        self.temperature = float(temperature)
        self.humidity = float(humidity)

    def __str__(self):
        return (f"{super().__str__()}, "
                f"Температура: {self.temperature:.2f}°C, "
                f"Влажность: {self.humidity:.2f}%")

class PressureMeasurement(Measurement):
    """Класс для измерения давления."""
    def __init__(self, date, place, pressure):
        super().__init__(date, place)
        self.pressure = float(pressure)

    def __str__(self):
        return f"{super().__str__()}, Давление: {self.pressure:.2f} мм рт. ст."

# Функции для работы с данными
def parse_line(line):
    """Создает объект измерения из строки."""
    parts = line.strip().split()
    measurement_type = parts[0]
    if measurement_type == "temperature" and len(parts) == 5:
        return TemperatureMeasurement(parts[1], parts[2], parts[3], parts[4])
    elif measurement_type == "pressure" and len(parts) == 4:
        return PressureMeasurement(parts[1], parts[2], parts[3])
    raise ValueError("Некорректный формат строки")

def read_measurements_from_file(filename):
    """Читает измерения из файла."""
    measurements = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                if line.strip():
                    try:
                        measurement = parse_line(line)
                        measurements.append(measurement)
                    except ValueError:
                        print(f"Пропущена строка: {line.strip()}")
    return measurements

def save_measurements_to_file(filename, measurements):
    """Сохраняет измерения в файл."""
    with open(filename, "w") as file:
        for measurement in measurements:
            if isinstance(measurement, TemperatureMeasurement):
                file.write(f'temperature {measurement.date.strftime("%Y.%m.%d")} '
                          f'"{measurement.place}" {measurement.temperature} '
                          f'{measurement.humidity}\n')
            else:  # PressureMeasurement
                file.write(f'pressure {measurement.date.strftime("%Y.%m.%d")} '
                          f'"{measurement.place}" {measurement.pressure}\n')

# Функции для интерфейса
def update_table(tree, measurements):
    """Обновляет таблицу с измерениями."""
    for item in tree.get_children():
        tree.delete(item)
    for measurement in measurements:
        tree.insert("", "end", values=(str(measurement),))

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
    except ValueError as e:
        print(f"Ошибка: {e}. Проверьте формат даты (гггг.мм.дд) и чисел.")

def delete_selected(tree, measurements, filename):
    """Удаляет выделенное измерение."""
    selected = tree.selection()
    if selected:
        for item in selected:
            index = tree.index(item)
            measurements.pop(index)
            tree.delete(item)
        save_measurements_to_file(filename, measurements)

# Создание интерфейса
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

# Основная программа
def main():
    """Запускает программу."""
    filename = "measurements.txt"
    measurements = read_measurements_from_file(filename)
    create_interface(measurements, filename)

if __name__ == "__main__":
    main()