import os
from measurements import TemperatureMeasurement, PressureMeasurement
#комментарий
def parse_line(line):
    """Создает объект измерения из строки."""
    parts = line.strip().split()
    if not parts:
        raise ValueError("Пустая строка")
    measurement_type = parts[0]
    if measurement_type == "temperature" and len(parts) == 5:
        return TemperatureMeasurement(parts[1], parts[2], parts[3], parts[4])
    elif measurement_type == "pressure" and len(parts) == 4:
        return PressureMeasurement(parts[1], parts[2], parts[3])
    raise ValueError(f"Некорректный формат строки: {line.strip()}")

def read_measurements_from_file(filename):
    """Читает измерения из файла."""
    measurements = []
    # Формируем путь к файлу в той же папке, где находится скрипт
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abs_filename = os.path.join(script_dir, filename)
    
    if not os.path.exists(abs_filename):
        print(f"Файл {abs_filename} не найден!")
        return measurements
    
    try:
        with open(abs_filename, "r", encoding="utf-8-sig") as file:
            for line in file:
                if line.strip():
                    try:
                        measurement = parse_line(line)
                        measurements.append(measurement)
                    except ValueError as e:
                        print(f"Ошибка в строке: {e}")
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
    print(f"Прочитано {len(measurements)} измерений.")
    return measurements

def save_measurements_to_file(filename, measurements):
    """Сохраняет измерения в файл."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abs_filename = os.path.join(script_dir, filename)
    
    try:
        with open(abs_filename, "w", encoding="utf-8") as file:
            for measurement in measurements:
                if isinstance(measurement, TemperatureMeasurement):
                    file.write(f'temperature {measurement.date.strftime("%Y.%m.%d")} '
                              f'"{measurement.place}" {measurement.temperature} '
                              f'{measurement.humidity}\n')
                else:  # PressureMeasurement
                    file.write(f'pressure {measurement.date.strftime("%Y.%m.%d")} '
                              f'"{measurement.place}" {measurement.pressure}\n')
        print(f"Данные сохранены в {abs_filename}")
    except Exception as e:
        print(f"Ошибка сохранения файла: {e}")
        