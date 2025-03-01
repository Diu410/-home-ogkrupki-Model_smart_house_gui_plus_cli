from Smarthome.device import Device

class Socket(Device):
    def __init__(self, name: str):
        super().__init__(name)

    def get_status(self) -> str:
        return super().get_status()  # Используем метод родительского класса