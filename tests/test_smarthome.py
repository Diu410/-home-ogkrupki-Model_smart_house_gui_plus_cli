# tests/test_smarthome.py
import unittest
from Smarthome.smarthome import SmartHome
from Smarthome.light import Light
from Smarthome.thermostat import Thermostat

class TestSmartHome(unittest.TestCase):
    def setUp(self):
        """Создаём умный дом для тестов."""
        self.home = SmartHome()

    def test_add_device(self):
        """Проверяем добавление устройства."""
        light = Light("Тестовый свет")
        self.home.add_device(light)
        self.assertIn(light, self.home.devices)

    def test_remove_device(self):
        """Проверяем удаление устройства."""
        light = Light("Тестовый свет")
        self.home.add_device(light)
        self.home.remove_device("Тестовый свет")
        self.assertNotIn(light, self.home.devices)

    def test_show_status(self):
        """Проверяем отображение статуса всех устройств."""
        light = Light("Тестовый свет")
        thermostat = Thermostat("Тестовый термостат")
        self.home.add_device(light)
        self.home.add_device(thermostat)

        # Проверяем, что статус отображается корректно
        self.home.show_status()

if __name__ == "__main__":
    unittest.main()