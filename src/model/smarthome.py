from typing import List, Callable
from src.model.device import Device

class SmartHome:
    def __init__(self):
        self.devices: List[Device] = []
        self.observers: List[Callable] = []

    def add_observer(self, observer: Callable):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer(self)

    def add_device(self, device: Device):
        self.devices.append(device)
        print(f"Устройство {device.name} добавлено.")
        self.notify_observers()

    def remove_device(self, name: str):
        for device in self.devices:
            if device.name == name:
                self.devices.remove(device)
                print(f"Устройство {name} удалено.")
                self.notify_observers()
                return
        print(f"Устройство {name} не найдено.")

    def show_status(self):
        for device in self.devices:
            print(f"{device.get_status()}")