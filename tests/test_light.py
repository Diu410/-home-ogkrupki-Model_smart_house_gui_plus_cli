# tests/test_light.py
import unittest
from Smarthome.light import Light

class TestLight(unittest.TestCase):
    def setUp(self):
        """Создаём источник света для тестов."""
        self.light = Light("Тестовый свет")

    def test_initial_brightness(self):
        """Проверяем начальную яркость."""
        self.assertEqual(self.light.brightness, 50)

    def test_set_brightness(self):
        """Проверяем установку яркости."""
        self.light.set_brightness(75)
        self.assertEqual(self.light.brightness, 75)

    def test_set_invalid_brightness(self):
        """Проверяем обработку недопустимой яркости."""
        with self.assertRaises(ValueError):
            self.light.set_brightness(150)  # Недопустимое значение

    def test_set_color_temperature(self):
        """Проверяем установку температуры света."""
        self.light.set_color_temperature("warm")
        self.assertEqual(self.light.color_temperature, "warm")

    def test_set_invalid_color_temperature(self):
        """Проверяем обработку недопустимой температуры света."""
        with self.assertRaises(ValueError):
            self.light.set_color_temperature("hot")  # Недопустимое значение

if __name__ == "__main__":
    unittest.main()