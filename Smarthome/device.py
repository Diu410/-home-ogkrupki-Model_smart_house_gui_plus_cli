# device.py
class Device:
    def __init__(self, name: str):
        self.name = name
        self.status = "off"

    def turn_on(self):
        self.status = "on"
        print(f"{self.name} включен.")

    def turn_off(self):
        self.status = "off"
        print(f"{self.name} выключен.")

    def get_status(self) -> str:
        return f"{self.name}: {self.status}"  # Добавляем имя устройства