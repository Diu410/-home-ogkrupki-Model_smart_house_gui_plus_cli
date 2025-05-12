from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTreeWidget,
    QTreeWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QInputDialog,
    QMessageBox,
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import Callable
from src.model.device import Device
from src.model.oxygen_monitor import OxygenMonitor
from src.model.door import Door
from src.model.light import Light
from src.model.socket import Socket
from src.model.thermostat import Thermostat

class SmartHomeView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Умный дом")
        self.setGeometry(100, 100, 1000, 600)

        # Устанавливаем тёмную тему для окна
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2A2A2E;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 16px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

        # Layout
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Заголовок
        title_label = QLabel("Умный дом")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Tree view for devices
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Имя", "Статус", "Действия"])
        self.tree.setColumnWidth(0, 250)
        self.tree.setColumnWidth(1, 400)
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: #35353A;
                color: #FFFFFF;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
                border: 1px solid #4A4A4F;
                border-radius: 5px;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:selected {
                background-color: #2E7D32;  /* Тёмно-зелёный для выделения */
                color: #FFFFFF;
            }
            QTreeWidget::item:hover {
                background-color: #4A4A4F;
            }
        """)
        layout.addWidget(self.tree)

        # Buttons
        self.add_device_btn = QPushButton("Добавить устройство")
        self.remove_device_btn = QPushButton("Удалить выбранное устройство")
        self.toggle_device_btn = QPushButton("Включить/выключить")
        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: #FFFFFF;
                font-size: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 8px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QPushButton:pressed {
                background-color: #3D8B40;
            }
        """
        self.add_device_btn.setStyleSheet(button_style)
        self.remove_device_btn.setStyleSheet(button_style)
        self.toggle_device_btn.setStyleSheet(button_style)
        layout.addWidget(self.add_device_btn)
        layout.addWidget(self.remove_device_btn)
        layout.addWidget(self.toggle_device_btn)

    def update_view(self, smarthome):
        self.tree.clear()
        # Группировка по типам без иконок
        type_groups = {
            "Кислородный монитор": [],
            "Дверь": [],
            "Свет": [],
            "Розетка": [],
            "Термостат": []
        }
        for device in smarthome.devices:
            if isinstance(device, OxygenMonitor):
                type_groups["Кислородный монитор"].append(device)
            elif isinstance(device, Door):
                type_groups["Дверь"].append(device)
            elif isinstance(device, Light):
                type_groups["Свет"].insert(0, device)
            elif isinstance(device, Socket):
                type_groups["Розетка"].insert(0, device)
            elif isinstance(device, Thermostat):
                type_groups["Термостат"].append(device)

        for type_name, devices in type_groups.items():
            if devices:  # Показываем только непустые категории
                type_item = QTreeWidgetItem(self.tree, [type_name, "", ""])
                for device in devices:
                    device_item = QTreeWidgetItem(type_item, [device.name, device.get_status(), ""])
                    # Добавляем кнопки для специфических функций
                    self._add_device_buttons(device, device_item)

    def _add_device_buttons(self, device: Device, item: QTreeWidgetItem):
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        container = QWidget()
        container.setLayout(button_layout)

        # Стили для кнопок в дереве (тёмно-фиолетовый)
        button_style = """
            QPushButton {
                background-color: #6A1B9A;  /* Тёмно-фиолетовый */
                color: #FFFFFF;
                font-size: 11px;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 4px 8px;
                border-radius: 4px;
                border: none;
                min-height: 20px;
                max-height: 20px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;  /* Чуть светлее для наведения */
            }
            QPushButton:pressed {
                background-color: #4A148C;  /* Темнее для нажатия */
            }
        """

        # Функция для сохранения выделения по имени устройства
        def preserve_selection(callback, device_name):
            callback(device_name)
            # Ищем элемент дерева по имени устройства
            for i in range(self.tree.topLevelItemCount()):
                type_item = self.tree.topLevelItem(i)
                for j in range(type_item.childCount()):
                    child_item = type_item.child(j)
                    if child_item.text(0) == device_name:
                        self.tree.setCurrentItem(child_item)  # Восстанавливаем выделение
                        return

        if isinstance(device, OxygenMonitor):
            set_oxygen_btn = QPushButton("Уровень O₂")
            set_oxygen_btn.setStyleSheet(button_style)
            set_oxygen_btn.clicked.connect(lambda: preserve_selection(self._oxygen_callback, device.name))
            button_layout.addWidget(set_oxygen_btn)
        elif isinstance(device, Door):
            auto_lock_btn = QPushButton("Автоблокировка")
            auto_lock_btn.setStyleSheet(button_style)
            auto_lock_btn.clicked.connect(lambda: preserve_selection(self._door_callback, device.name))
            lock_btn = QPushButton("Замок")
            lock_btn.setStyleSheet(button_style)
            lock_btn.clicked.connect(lambda: preserve_selection(self._lock_callback, device.name))
            button_layout.addWidget(auto_lock_btn)
            button_layout.addWidget(lock_btn)
        elif isinstance(device, Light):
            brightness_btn = QPushButton("Яркость")
            brightness_btn.setStyleSheet(button_style)
            brightness_btn.clicked.connect(lambda: preserve_selection(self._brightness_callback, device.name))
            temp_btn = QPushButton("Температура")
            temp_btn.setStyleSheet(button_style)
            temp_btn.clicked.connect(lambda: preserve_selection(self._temp_callback, device.name))
            button_layout.addWidget(brightness_btn)
            button_layout.addWidget(temp_btn)
        elif isinstance(device, Thermostat):
            set_temp_btn = QPushButton("Температура")
            set_temp_btn.setStyleSheet(button_style)
            set_temp_btn.clicked.connect(lambda: preserve_selection(self._thermostat_callback, device.name))
            button_layout.addWidget(set_temp_btn)

        self.tree.setItemWidget(item, 2, container)

    def set_add_device_callback(self, callback: Callable):
        self.add_device_btn.clicked.connect(callback)

    def set_remove_device_callback(self, callback: Callable):
        self.remove_device_btn.clicked.connect(lambda: self._handle_selection(callback))

    def set_toggle_device_callback(self, callback: Callable):
        self.toggle_device_btn.clicked.connect(lambda: self._handle_selection(callback, preserve=True))

    def set_oxygen_callback(self, callback: Callable):
        self._oxygen_callback = callback

    def set_door_callback(self, callback: Callable):
        self._door_callback = callback

    def set_lock_callback(self, callback: Callable):
        self._lock_callback = callback

    def set_brightness_callback(self, callback: Callable):
        self._brightness_callback = callback

    def set_temp_callback(self, callback: Callable):
        self._temp_callback = callback

    def set_thermostat_callback(self, callback: Callable):
        self._thermostat_callback = callback

    def _handle_selection(self, callback: Callable, preserve: bool = False):
        selected_items = self.tree.selectedItems()
        if not selected_items or selected_items[0].parent() is None:  # Игнорируем корневые узлы (типы)
            self.show_error("Пожалуйста, выберите устройство")
            return
        device_name = selected_items[0].text(0)
        callback(device_name)
        if preserve:
            # Восстанавливаем выделение по имени устройства
            for i in range(self.tree.topLevelItemCount()):
                type_item = self.tree.topLevelItem(i)
                for j in range(type_item.childCount()):
                    child_item = type_item.child(j)
                    if child_item.text(0) == device_name:
                        self.tree.setCurrentItem(child_item)
                        return

    def get_device_info(self):
        device_types = ["Кислородный монитор", "Дверь", "Свет", "Розетка", "Термостат"]
        device_type, ok1 = QInputDialog.getItem(self, "Ввод", "Выберите тип устройства:", device_types, 0, False)
        if not ok1:
            return None, None
        name, ok2 = QInputDialog.getText(self, "Ввод", "Введите имя устройства:")
        return device_type, name if ok2 else None

    def configure_oxygen(self):
        target, ok = QInputDialog.getDouble(self, "Настройка", "Введите целевой уровень кислорода (19–23%):", 21.0, 19, 23, 1)
        return {"target": target} if ok else None

    def configure_door(self):
        action, ok = QInputDialog.getItem(self, "Настройка", "Выберите действие:", ["Включить автоблокировку", "Выключить автоблокировку"], 0, False)
        return {"action": action} if ok else None

    def configure_lock(self):
        action, ok = QInputDialog.getItem(self, "Настройка", "Выберите действие:", ["Заблокировать", "Разблокировать"], 0, False)
        return {"action": action} if ok else None

    def configure_brightness(self):
        brightness, ok = QInputDialog.getInt(self, "Настройка", "Введите яркость (0–100%):", 50, 0, 100)
        return {"brightness": brightness} if ok else None

    def configure_temperature(self):
        temp, ok = QInputDialog.getItem(self, "Настройка", "Выберите температуру света:", ["Тёплый", "Нейтральный", "Холодный"], 0, False)
        if ok:
            # Переводим русские значения в английские
            temp_map = {"Тёплый": "warm", "Нейтральный": "neutral", "Холодный": "cold"}
            return {"temperature": temp_map.get(temp, "neutral")}  # Дефолт — neutral
        return None

    def configure_thermostat(self):
        temp, ok = QInputDialog.getDouble(self, "Настройка", "Введите целевую температуру (10–30°C):", 22.0, 10, 30, 1)
        return {"temp": temp} if ok else None

    def show_error(self, message: str):
        QMessageBox.critical(self, "Ошибка", message)