from Smarthome.device import Device

class Thermostat(Device):
    def __init__(self, name: str):
        super().__init__(name)
        self.current_temp = 20  # Текущая температура
        self.target_temp = 22   # Целевая температура

    def set_target_temp(self, temp: float):
        if 10 <= temp <= 30:
            self.target_temp = temp
            print(f"Целевая температура {self.name} установлена на {temp}°C.")
        else:
            raise ValueError("Ошибка: температура должна быть в диапазоне от 10 до 30°C.")

    def get_status(self) -> str:
        """Возвращает статус термостата."""
        status = super().get_status()
        return f"{status}, текущая температура: {self.current_temp}°C, целевая температура: {self.target_temp}°C"