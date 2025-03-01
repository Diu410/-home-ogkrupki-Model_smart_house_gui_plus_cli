# tests/test_oxygen_monitor.py
import unittest
from Smarthome.oxygen_monitor import OxygenMonitor

class TestOxygenMonitor(unittest.TestCase):
    def setUp(self):
        """Создаём кислородный монитор для тестов."""
        self.monitor = OxygenMonitor("Тестовый монитор")

    def test_initial_oxygen_level(self):
        """Проверяем начальный уровень кислорода."""
        self.assertEqual(self.monitor.current_oxygen, 21.0)
        self.assertEqual(self.monitor.target_oxygen, 21.0)

    def test_set_target_oxygen(self):
        """Проверяем установку целевого уровня кислорода."""
        self.monitor.set_target_oxygen(22.0)
        self.assertEqual(self.monitor.target_oxygen, 22.0)

    def test_set_invalid_oxygen_level(self):
        """Проверяем обработку недопустимого уровня кислорода."""
        with self.assertRaises(ValueError):
            self.monitor.set_target_oxygen(18.0)  # Недопустимое значение

    def test_auto_turn_on(self):
        """Проверяем автоматическое включение при низком уровне кислорода."""
        self.monitor.update_oxygen_level(18.0)  # Критический уровень
        self.assertEqual(self.monitor.get_status(), "Тестовый монитор: on, текущий уровень кислорода: 18.0%, целевой уровень: 21.0%")

    def test_auto_turn_off(self):
        """Проверяем автоматическое выключение при нормальном уровне кислорода."""
        self.monitor.update_oxygen_level(18.0)  # Включаем монитор
        self.monitor.update_oxygen_level(22.0)  # Возвращаем уровень в норму
        self.assertEqual(self.monitor.get_status(), "Тестовый монитор: off, текущий уровень кислорода: 22.0%, целевой уровень: 21.0%")

if __name__ == "__main__":
    unittest.main()