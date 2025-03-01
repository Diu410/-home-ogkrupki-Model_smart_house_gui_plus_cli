# tests/test_thermostat.py
import unittest
from Smarthome.thermostat import Thermostat

class TestThermostat(unittest.TestCase):
    def setUp(self):
        """Создаём термостат для тестов."""
        self.thermostat = Thermostat("Тестовый термостат")

    def test_initial_temperature(self):
        """Проверяем начальную температуру."""
        self.assertEqual(self.thermostat.current_temp, 20)
        self.assertEqual(self.thermostat.target_temp, 22)

    def test_set_target_temp(self):
        """Проверяем установку целевой температуры."""
        self.thermostat.set_target_temp(25)
        self.assertEqual(self.thermostat.target_temp, 25)

    def test_set_invalid_temp(self):
        """Проверяем обработку недопустимой температуры."""
        with self.assertRaises(ValueError):
            self.thermostat.set_target_temp(5)  # Недопустимое значение

if __name__ == "__main__":
    unittest.main()