import datetime

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