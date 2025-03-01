# tests/test_door.py
import unittest
from Smarthome.door import Door

class TestDoor(unittest.TestCase):
    def setUp(self):
        """Создаём дверь для тестов."""
        self.door = Door("Тестовая дверь")

    def test_initial_lock_status(self):
        """Проверяем начальное состояние блокировки."""
        self.assertFalse(self.door.locked)

    def test_lock_unlock(self):
        """Проверяем блокировку и разблокировку двери."""
        self.door.lock()
        self.assertTrue(self.door.locked)

        self.door.unlock()
        self.assertFalse(self.door.locked)

    def test_auto_lock(self):
        """Проверяем автоматическую блокировку."""
        self.door.enable_auto_lock()
        self.assertTrue(self.door.auto_lock)

        self.door.disable_auto_lock()
        self.assertFalse(self.door.auto_lock)

if __name__ == "__main__":
    unittest.main()