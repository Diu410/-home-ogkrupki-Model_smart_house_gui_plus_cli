from .device import Device
from datetime import datetime, time

class Door(Device):
    def __init__(self, name: str):
        super().__init__(name)
        self.locked = False  # Состояние блокировки
        self.auto_lock = False  # Автоматическая блокировка на ночь

    def lock(self):
        """Блокирует дверь."""
        self.locked = True
        print(f"Дверь {self.name} заблокирована.")

    def unlock(self):
        """Разблокирует дверь."""
        self.locked = False
        print(f"Дверь {self.name} разблокирована.")

    def enable_auto_lock(self):
        """Включает автоматическую блокировку на ночь."""
        self.auto_lock = True
        print(f"Дверь {self.name} добавлена в список автоматической блокировки.")

    def disable_auto_lock(self):
        """Выключает автоматическую блокировку на ночь."""
        self.auto_lock = False
        print(f"Дверь {self.name} удалена из списка автоматической блокировки.")

    def check_night_lock(self):
        """Автоматически блокирует дверь, если наступило ночное время."""
        if self.auto_lock:
            now = datetime.now().time()
            night_start = time(22, 0)  # Начало ночного времени (22:00)
            night_end = time(6, 0)     # Конец ночного времени (06:00)

            if night_start <= now or now <= night_end:
                if not self.locked:
                    self.lock()
                    print(f"Дверь {self.name} автоматически заблокирована на ночь.")

    def get_status(self) -> str:
        """Возвращает статус двери."""
        status = super().get_status()
        return f"{status}, заблокирована: {self.locked}, автоматическая блокировка: {'включена' if self.auto_lock else 'выключена'}"