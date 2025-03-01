from Smarthome.device import Device

class OxygenMonitor(Device):
    def __init__(self, name: str):
        super().__init__(name)
        self.current_oxygen = 21.0  # Текущий уровень кислорода (в процентах)
        self.target_oxygen = 21.0   # Целевой уровень кислорода
        self.critical_level = 19.0  # Критический уровень кислорода

    def set_target_oxygen(self, target: float):
        if 19.0 <= target <= 23.0:
            self.target_oxygen = target
            print(f"Целевой уровень кислорода {self.name} установлен на {target}%.")
        else:
            raise ValueError("Ошибка: целевой уровень кислорода должен быть от 19% до 23%.")

    def update_oxygen_level(self, new_level: float):
        """Обновляет текущий уровень кислорода и автоматически управляет устройством."""
        self.current_oxygen = new_level
        if self.current_oxygen < self.critical_level and self.status == "off":
            self.turn_on()
            print(f"Кислородный монитор {self.name} включен из-за низкого уровня кислорода.")
        elif self.current_oxygen >= self.target_oxygen and self.status == "on":
            self.turn_off()
            print(f"Кислородный монитор {self.name} выключен, уровень кислорода в норме.")

    def get_status(self) -> str:
        status = super().get_status()
        return f"{status}, текущий уровень кислорода: {self.current_oxygen}%, целевой уровень: {self.target_oxygen}%"