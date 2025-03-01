from Smarthome.device import Device

# light.py
class Light(Device):
    def __init__(self, name: str):
        super().__init__(name)
        self.brightness = 50
        self.color_temperature = "neutral"

    def set_brightness(self, brightness: int):
        if 0 <= brightness <= 100:
            self.brightness = brightness
            print(f"Яркость {self.name} установлена на {brightness}%.")
        else:
            raise ValueError("Ошибка: яркость должна быть от 0 до 100%.")

    def set_color_temperature(self, temperature: str):
        if temperature in ["warm", "neutral", "cold"]:
            self.color_temperature = temperature
            print(f"Температура света {self.name} установлена на {temperature}.")
        else:
            raise ValueError("Ошибка: допустимые значения — warm, neutral, cold.")

    def get_status(self) -> str:
        """Возвращает статус устройства с учетом яркости и температуры света."""
        status = super().get_status()
        return f"{status}, яркость: {self.brightness}%, температура: {self.color_temperature}"