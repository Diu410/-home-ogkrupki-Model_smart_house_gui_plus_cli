# tests/test_socket.py
import unittest
from Smarthome.socket import Socket

class TestSocket(unittest.TestCase):
    def setUp(self):
        """Создаём розетку для тестов."""
        self.socket = Socket("Тестовая розетка")

    def test_initial_status(self):
        """Проверяем начальное состояние розетки."""
        self.assertEqual(self.socket.get_status(), "Тестовая розетка: off")

    def test_turn_on(self):
        """Проверяем включение розетки."""
        self.socket.turn_on()
        self.assertEqual(self.socket.get_status(), "Тестовая розетка: on")

    def test_turn_off(self):
        """Проверяем выключение розетки."""
        self.socket.turn_on()  # Включаем розетку
        self.socket.turn_off()  # Выключаем розетку
        self.assertEqual(self.socket.get_status(), "Тестовая розетка: off")

if __name__ == "__main__":
    unittest.main()