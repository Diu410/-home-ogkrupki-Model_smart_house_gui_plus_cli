# tests/test_device.py
import unittest
from Smarthome.device import Device

class TestDevice(unittest.TestCase):
    def setUp(self):
        """Создаём устройство для тестов."""
        self.device = Device("Тестовое устройство")

    def test_initial_status(self):
        """Проверяем, что устройство изначально выключено."""
        self.assertEqual(self.device.get_status(), "Тестовое устройство: off")

    def test_turn_on(self):
        """Проверяем включение устройства."""
        self.device.turn_on()
        self.assertEqual(self.device.get_status(), "Тестовое устройство: on")

    def test_turn_off(self):
        """Проверяем выключение устройства."""
        self.device.turn_on()  # Включаем устройство
        self.device.turn_off()  # Выключаем устройство
        self.assertEqual(self.device.get_status(), "Тестовое устройство: off")

if __name__ == "__main__":
    unittest.main()