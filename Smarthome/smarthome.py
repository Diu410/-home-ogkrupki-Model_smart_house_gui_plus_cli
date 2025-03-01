from typing import List
from Smarthome.device import Device

class SmartHome:
    def __init__(self):
        self.devices: List[Device] = []

    def add_device(self, device: Device):
        self.devices.append(device)
        print(f"Устройство {device.name} добавлено.")

    def remove_device(self, name: str):
        for device in self.devices:
            if device.name == name:
                self.devices.remove(device)
                print(f"Устройство {name} удалено.")
                return
        print(f"Устройство {name} не найдено.")

    def show_status(self):
        for device in self.devices:
            print(f"{device.name}: {device.get_status()}")