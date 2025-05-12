from src.model.smarthome import SmartHome
from src.model.device import Device
from src.model.oxygen_monitor import OxygenMonitor
from src.model.door import Door
from src.model.light import Light
from src.model.socket import Socket
from src.model.thermostat import Thermostat
from src.view.gui import SmartHomeView
from typing import Optional, Callable

class SmartHomeController:
    def __init__(self, model: SmartHome, view=None):
        self.model = model
        self.view = view
        if isinstance(self.view, SmartHomeView):
            self.model.add_observer(self.view.update_view)
            self.setup_connections()

    def setup_connections(self):
        self.view.set_add_device_callback(self.add_device)
        self.view.set_remove_device_callback(self.remove_device)
        self.view.set_toggle_device_callback(self.toggle_device)
        self.view.set_oxygen_callback(self.set_oxygen)
        self.view.set_door_callback(self.toggle_auto_lock)
        self.view.set_lock_callback(self.toggle_lock)
        self.view.set_brightness_callback(self.set_brightness)
        self.view.set_temp_callback(self.set_temperature)
        self.view.set_thermostat_callback(self.set_thermostat_temp)

    def add_device(self, device_type: str = None, name: str = None):
        if not device_type or not name:
            if not isinstance(self.view, SmartHomeView):
                raise ValueError("CLI requires device_type and name arguments")
            device_type, name = self.view.get_device_info()
        if device_type and name:
            try:
                if device_type == "Кислородный монитор":
                    device = OxygenMonitor(name)
                elif device_type == "Дверь":
                    device = Door(name)
                elif device_type == "Свет":
                    device = Light(name)
                elif device_type == "Розетка":
                    device = Socket(name)
                elif device_type == "Термостат":
                    device = Thermostat(name)
                else:
                    raise ValueError("Неизвестный тип устройства")
                self.model.add_device(device)
            except Exception as e:
                if isinstance(self.view, SmartHomeView):
                    self.view.show_error(str(e))
                else:
                    print(f"Ошибка: {str(e)}")

    def remove_device(self, name: str):
        try:
            self.model.remove_device(name)
        except Exception as e:
            if isinstance(self.view, SmartHomeView):
                self.view.show_error(str(e))
            else:
                print(f"Ошибка: {str(e)}")

    def toggle_device(self, name: str):
        try:
            for device in self.model.devices:
                if device.name == name:
                    print(f"Переключение устройства {name}: текущий статус {device.status}")  # Отладочный вывод
                    if device.status == "on":
                        device.turn_off()
                    else:
                        device.turn_on()
                    self.model.notify_observers()
                    print(f"Новый статус устройства {name}: {device.status}")  # Отладочный вывод
                    return
            error = f"Устройство {name} не найдено"
            if isinstance(self.view, SmartHomeView):
                self.view.show_error(error)
            else:
                print(f"Ошибка: {error}")
        except Exception as e:
            if isinstance(self.view, SmartHomeView):
                self.view.show_error(f"Ошибка: {str(e)}")
            else:
                print(f"Ошибка: {str(e)}")

    def set_oxygen(self, name: str, config: Optional[dict] = None):
        try:
            for device in self.model.devices:
                if device.name == name and isinstance(device, OxygenMonitor):
                    if not config and isinstance(self.view, SmartHomeView):
                        config = self.view.configure_oxygen()
                    if config:
                        device.set_target_oxygen(config["target"])
                    self.model.notify_observers()
                    break
            else:
                error = f"Устройство {name} не найдено"
                if isinstance(self.view, SmartHomeView):
                    self.view.show_error(error)
                else:
                    print(f"Ошибка: {error}")
        except Exception as e:
            if isinstance(self.view, SmartHomeView):
                self.view.show_error(str(e))
            else:
                print(f"Ошибка: {str(e)}")

    def toggle_auto_lock(self, name: str, config: Optional[dict] = None):
        try:
            for device in self.model.devices:
                if device.name == name and isinstance(device, Door):
                    if not config and isinstance(self.view, SmartHomeView):
                        config = self.view.configure_door()
                    if config:
                        if config["action"] == "Включить автоблокировку":
                            device.enable_auto_lock()
                        elif config["action"] == "Выключить автоблокировку":
                            device.disable_auto_lock()
                    self.model.notify_observers()
                    break
            else:
                error = f"Устройство {name} не найдено"
                if isinstance(self.view, SmartHomeView):
                    self.view.show_error(error)
                else:
                    print(f"Ошибка: {error}")
        except Exception as e:
            if isinstance(self.view, SmartHomeView):
                self.view.show_error(str(e))
            else:
                print(f"Ошибка: {str(e)}")

    def toggle_lock(self, name: str, config: Optional[dict] = None):
        try:
            for device in self.model.devices:
                if device.name == name and isinstance(device, Door):
                    if not config and isinstance(self.view, SmartHomeView):
                        config = self.view.configure_lock()
                    if config:
                        if config["action"] == "Заблокировать":
                            device.lock()
                        elif config["action"] == "Разблокировать":
                            device.unlock()
                    self.model.notify_observers()
                    break
            else:
                error = f"Устройство {name} не найдено"
                if isinstance(self.view, SmartHomeView):
                    self.view.show_error(error)
                else:
                    print(f"Ошибка: {error}")
        except Exception as e:
            if isinstance(self.view, SmartHomeView):
                self.view.show_error(str(e))
            else:
                print(f"Ошибка: {str(e)}")

    def set_brightness(self, name: str, config: Optional[dict] = None):
        try:
            for device in self.model.devices:
                if device.name == name and isinstance(device, Light):
                    if not config and isinstance(self.view, SmartHomeView):
                        config = self.view.configure_brightness()
                    if config:
                        device.set_brightness(config["brightness"])
                    self.model.notify_observers()
                    break
            else:
                error = f"Устройство {name} не найдено"
                if isinstance(self.view, SmartHomeView):
                    self.view.show_error(error)
                else:
                    print(f"Ошибка: {error}")
        except Exception as e:
            if isinstance(self.view, SmartHomeView):
                self.view.show_error(str(e))
            else:
                print(f"Ошибка: {str(e)}")

    def set_temperature(self, name: str, config: Optional[dict] = None):
        try:
            for device in self.model.devices:
                if device.name == name and isinstance(device, Light):
                    if not config and isinstance(self.view, SmartHomeView):
                        config = self.view.configure_temperature()
                    if config:
                        device.set_color_temperature(config["temperature"])
                    self.model.notify_observers()
                    break
            else:
                error = f"Устройство {name} не найдено"
                if isinstance(self.view, SmartHomeView):
                    self.view.show_error(error)
                else:
                    print(f"Ошибка: {error}")
        except Exception as e:
            if isinstance(self.view, SmartHomeView):
                self.view.show_error(str(e))
            else:
                print(f"Ошибка: {str(e)}")

    def set_thermostat_temp(self, name: str, config: Optional[dict] = None):
        try:
            for device in self.model.devices:
                if device.name == name and isinstance(device, Thermostat):
                    if not config and isinstance(self.view, SmartHomeView):
                        config = self.view.configure_thermostat()
                    if config:
                        device.set_target_temp(config["temp"])
                    self.model.notify_observers()
                    break
            else:
                error = f"Устройство {name} не найдено"
                if isinstance(self.view, SmartHomeView):
                    self.view.show_error(error)
                else:
                    print(f"Ошибка: {error}")
        except Exception as e:
            if isinstance(self.view, SmartHomeView):
                self.view.show_error(str(e))
            else:
                print(f"Ошибка: {str(e)}")