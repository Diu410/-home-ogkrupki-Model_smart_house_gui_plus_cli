import curses
import os
import sys
from colorama import init, Fore, Style
from src.model.oxygen_monitor import OxygenMonitor
from src.model.door import Door
from src.model.light import Light
from src.model.socket import Socket
from src.model.thermostat import Thermostat

class SmartHomeCLI:
    def __init__(self):
        self.controller = None
        init()  # Инициализация colorama

    def set_controller(self, controller):
        self.controller = controller

    def run(self):
        try:
            curses.wrapper(self._main_menu)
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}Программа завершена пользователем.{Style.RESET_ALL}")
            sys.exit(0)

    def _main_menu(self, stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Голубой текст для заголовка
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)  # Зелёный фон, чёрный текст для выделения
        curses.curs_set(0)  # Скрыть курсор
        stdscr.timeout(-1)  # Блокировать до ввода
        menu_items = [
            "Управление источниками света",
            "Управление термостатами",
            "Управление розетками",
            "Управление кислородными мониторами",
            "Управление дверьми",
            "Показать все компоненты дома",
            "Выйти"
        ]
        selected_index = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "=== Умный дом ===", curses.A_BOLD | curses.color_pair(1))
            for i, item in enumerate(menu_items):
                if i == selected_index:
                    stdscr.addstr(i + 2, 0, f"> {item}", curses.color_pair(2))
                else:
                    stdscr.addstr(i + 2, 0, f"  {item}")
            stdscr.addstr(len(menu_items) + 3, 0, "Используйте 'w' (вверх), 's' (вниз), Enter (выбор)")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('w'):
                selected_index = (selected_index - 1) % len(menu_items)
            elif key == ord('s'):
                selected_index = (selected_index + 1) % len(menu_items)
            elif key == 10:  # Enter
                if selected_index == 0:
                    self._manage_lights(stdscr)
                elif selected_index == 1:
                    self._manage_thermostats(stdscr)
                elif selected_index == 2:
                    self._manage_sockets(stdscr)
                elif selected_index == 3:
                    self._manage_oxygen_monitors(stdscr)
                elif selected_index == 4:
                    self._manage_doors(stdscr)
                elif selected_index == 5:
                    self._show_all_components(stdscr)
                elif selected_index == 6:
                    self._reset_terminal(stdscr)
                    os.system("clear")
                    print(f"{Fore.GREEN}Выход из программы.{Style.RESET_ALL}")
                    break

    def _reset_terminal(self, stdscr):
        curses.reset_shell_mode()
        curses.endwin()
        os.system("clear")
        sys.stdout.flush()

    def _restore_terminal(self, stdscr):
        curses.reset_prog_mode()
        curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        stdscr.clear()
        stdscr.refresh()
        curses.doupdate()

    def _safe_input(self, prompt, type_cast, valid_range=None, allow_empty=False):
        while True:
            self._reset_terminal(None)
            sys.stdout.write(prompt)
            sys.stdout.flush()
            value = input().strip()
            if allow_empty and not value:
                return None
            try:
                value = type_cast(value)
                if valid_range is None or valid_range[0] <= value <= valid_range[1]:
                    return value
                print(f"{Fore.RED}Значение должно быть от {valid_range[0]} до {valid_range[1]}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Введите корректное число.{Style.RESET_ALL}")

    def _show_all_components(self, stdscr):
        self._reset_terminal(stdscr)
        print(f"{Fore.CYAN}=== Состояние умного дома ==={Style.RESET_ALL}")

        # Источники света
        lights = [device for device in self.controller.model.devices if isinstance(device, Light)]
        if lights:
            print(f"\n{Fore.CYAN}Источники света:{Style.RESET_ALL}")
            for light in lights:
                print(f"  - {light.name}: {light.get_status()}")
        else:
            print(f"\n{Fore.YELLOW}Источники света: нет устройств.{Style.RESET_ALL}")

        # Термостаты
        thermostats = [device for device in self.controller.model.devices if isinstance(device, Thermostat)]
        if thermostats:
            print(f"\n{Fore.CYAN}Термостаты:{Style.RESET_ALL}")
            for thermostat in thermostats:
                print(f"  - {thermostat.name}: {thermostat.get_status()}")
        else:
            print(f"\n{Fore.YELLOW}Термостаты: нет устройств.{Style.RESET_ALL}")

        # Розетки
        sockets = [device for device in self.controller.model.devices if isinstance(device, Socket)]
        if sockets:
            print(f"\n{Fore.CYAN}Розетки:{Style.RESET_ALL}")
            for socket in sockets:
                print(f"  - {socket.name}: {socket.get_status()}")
        else:
            print(f"\n{Fore.YELLOW}Розетки: нет устройств.{Style.RESET_ALL}")

        # Кислородные мониторы
        monitors = [device for device in self.controller.model.devices if isinstance(device, OxygenMonitor)]
        if monitors:
            print(f"\n{Fore.CYAN}Кислородные мониторы:{Style.RESET_ALL}")
            for monitor in monitors:
                print(f"  - {monitor.name}: {monitor.get_status()}")
        else:
            print(f"\n{Fore.YELLOW}Кислородные мониторы: нет устройств.{Style.RESET_ALL}")

        # Двери
        doors = [device for device in self.controller.model.devices if isinstance(device, Door)]
        if doors:
            print(f"\n{Fore.CYAN}Двери:{Style.RESET_ALL}")
            for door in doors:
                print(f"  - {door.name}: {door.get_status()}")
        else:
            print(f"\n{Fore.YELLOW}Двери: нет устройств.{Style.RESET_ALL}")

        print(f"{Fore.CYAN}============================{Style.RESET_ALL}")
        input("Нажмите Enter для возврата в меню...")
        self._restore_terminal(stdscr)

    def _select_device(self, stdscr, devices, device_type):
        if not devices:
            self._reset_terminal(stdscr)
            print(f"{Fore.YELLOW}Нет {device_type}.{Style.RESET_ALL}")
            input("Нажмите Enter для возврата в меню...")
            self._restore_terminal(stdscr)
            return None
        curses.curs_set(0)
        selected_index = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, f"=== Выбор {device_type} ===", curses.A_BOLD | curses.color_pair(1))
            for i, device in enumerate(devices):
                status = device.get_status()
                if i == selected_index:
                    stdscr.addstr(i + 2, 0, f"> {device.name} ({status})", curses.color_pair(2))
                else:
                    stdscr.addstr(i + 2, 0, f"  {device.name} ({status})")
            stdscr.addstr(len(devices) + 3, 0, "Используйте 'w' (вверх), 's' (вниз), Enter (выбор)")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('w'):
                selected_index = (selected_index - 1) % len(devices)
            elif key == ord('s'):
                selected_index = (selected_index + 1) % len(devices)
            elif key == 10:
                self._reset_terminal(stdscr)
                return devices[selected_index]

    def _manage_lights(self, stdscr):
        menu_items = [
            "Добавить источник света",
            "Удалить источник света",
            "Включить источник света",
            "Выключить источник света",
            "Изменить яркость",
            "Изменить температуру света",
            "Показать статус всех источников света",
            "Назад"
        ]
        selected_index = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "=== Управление источниками света ===", curses.A_BOLD | curses.color_pair(1))
            for i, item in enumerate(menu_items):
                if i == selected_index:
                    stdscr.addstr(i + 2, 0, f"> {item}", curses.color_pair(2))
                else:
                    stdscr.addstr(i + 2, 0, f"  {item}")
            stdscr.addstr(len(menu_items) + 3, 0, "Используйте 'w' (вверх), 's' (вниз), Enter (выбор)")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('w'):
                selected_index = (selected_index - 1) % len(menu_items)
            elif key == ord('s'):
                selected_index = (selected_index + 1) % len(menu_items)
            elif key == 10:  # Enter
                self._reset_terminal(stdscr)
                if selected_index == 0:  # Добавить
                    print("Добавление источника света...")
                    name = input("Введите имя источника света: ").strip()
                    if name:
                        self.controller.add_device("Свет", name)
                        print(f"{Fore.GREEN}Источник света '{name}' добавлен.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Имя не может быть пустым.{Style.RESET_ALL}")
                    input("Нажмите Enter для возврата в меню...")
                elif selected_index == 1:  # Удалить
                    lights = [device for device in self.controller.model.devices if isinstance(device, Light)]
                    selected_light = self._select_device(stdscr, lights, "источника света")
                    if selected_light:
                        self.controller.remove_device(selected_light.name)
                        print(f"{Fore.GREEN}Источник света '{selected_light.name}' удалён.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 2:  # Включить
                    lights = [device for device in self.controller.model.devices if isinstance(device, Light)]
                    selected_light = self._select_device(stdscr, lights, "источника света")
                    if selected_light:
                        self.controller.toggle_device(selected_light.name)
                        print(f"{Fore.GREEN}Источник света '{selected_light.name}' включён.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 3:  # Выключить
                    lights = [device for device in self.controller.model.devices if isinstance(device, Light)]
                    selected_light = self._select_device(stdscr, lights, "источника света")
                    if selected_light:
                        self.controller.toggle_device(selected_light.name)
                        print(f"{Fore.GREEN}Источник света '{selected_light.name}' выключен.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 4:  # Изменить яркость
                    lights = [device for device in self.controller.model.devices if isinstance(device, Light)]
                    selected_light = self._select_device(stdscr, lights, "источника света")
                    if selected_light:
                        brightness = self._safe_input("Введите яркость (0-100): ", int, (0, 100))
                        if brightness is not None:
                            self.controller.set_brightness(selected_light.name, {"brightness": brightness})
                            print(f"{Fore.GREEN}Яркость для '{selected_light.name}' установлена: {brightness}%.{Style.RESET_ALL}")
                            input("Нажмите Enter для возврата в меню...")
                elif selected_index == 5:  # Изменить температуру света
                    lights = [device for device in self.controller.model.devices if isinstance(device, Light)]
                    self._restore_terminal(stdscr)
                    self._select_light_temperature(stdscr, lights)
                elif selected_index == 6:  # Показать статус
                    lights = [device for device in self.controller.model.devices if isinstance(device, Light)]
                    if not lights:
                        print(f"{Fore.YELLOW}Нет источников света.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.CYAN}Источники света:{Style.RESET_ALL}")
                        for light in lights:
                            print(f"  - {light.name}: {light.get_status()}")
                    input("Нажмите Enter для возврата в меню...")
                elif selected_index == 7:  # Назад
                    self._restore_terminal(stdscr)
                    break
                self._restore_terminal(stdscr)

    def _select_light_temperature(self, stdscr, lights):
        if not lights:
            self._reset_terminal(stdscr)
            print(f"{Fore.YELLOW}Нет источников света.{Style.RESET_ALL}")
            input("Нажмите Enter для возврата в меню...")
            self._restore_terminal(stdscr)
            return
        curses.curs_set(0)
        selected_index = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "=== Выбор источника света ===", curses.A_BOLD | curses.color_pair(1))
            for i, light in enumerate(lights):
                status = light.get_status()
                if i == selected_index:
                    stdscr.addstr(i + 2, 0, f"> {light.name} ({status})", curses.color_pair(2))
                else:
                    stdscr.addstr(i + 2, 0, f"  {light.name} ({status})")
            stdscr.addstr(len(lights) + 3, 0, "Используйте 'w' (вверх), 's' (вниз), Enter (выбор)")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('w'):
                selected_index = (selected_index - 1) % len(lights)
            elif key == ord('s'):
                selected_index = (selected_index + 1) % len(lights)
            elif key == 10:
                selected_light = lights[selected_index]
                break
        temp_options = ["Тёплый", "Нейтральный", "Холодный"]
        selected_temp = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, f"=== Температура света для '{selected_light.name}' ===", curses.A_BOLD | curses.color_pair(1))
            for i, temp in enumerate(temp_options):
                if i == selected_temp:
                    stdscr.addstr(i + 2, 0, f"> {temp}", curses.color_pair(2))
                else:
                    stdscr.addstr(i + 2, 0, f"  {temp}")
            stdscr.addstr(len(temp_options) + 3, 0, "Используйте 'w' (вверх), 's' (вниз), Enter (выбор)")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('w'):
                selected_temp = (selected_temp - 1) % len(temp_options)
            elif key == ord('s'):
                selected_temp = (selected_temp + 1) % len(temp_options)
            elif key == 10:
                temp_map = {"Тёплый": "warm", "Нейтральный": "neutral", "Холодный": "cold"}
                self._reset_terminal(stdscr)
                self.controller.set_temperature(selected_light.name, {"temperature": temp_map[temp_options[selected_temp]]})
                print(f"{Fore.GREEN}Температура света для '{selected_light.name}' установлена: {temp_map[temp_options[selected_temp]]}.{Style.RESET_ALL}")
                input("Нажмите Enter для возврата в меню...")
                self._restore_terminal(stdscr)
                break

    def _manage_thermostats(self, stdscr):
        menu_items = [
            "Добавить термостат",
            "Удалить термостат",
            "Включить термостат",
            "Выключить термостат",
            "Изменить целевую температуру",
            "Показать статус всех термостатов",
            "Назад"
        ]
        selected_index = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "=== Управление термостатами ===", curses.A_BOLD | curses.color_pair(1))
            for i, item in enumerate(menu_items):
                if i == selected_index:
                    stdscr.addstr(i + 2, 0, f"> {item}", curses.color_pair(2))
                else:
                    stdscr.addstr(i + 2, 0, f"  {item}")
            stdscr.addstr(len(menu_items) + 3, 0, "Используйте 'w' (вверх), 's' (вниз), Enter (выбор)")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('w'):
                selected_index = (selected_index - 1) % len(menu_items)
            elif key == ord('s'):
                selected_index = (selected_index + 1) % len(menu_items)
            elif key == 10:  # Enter
                self._reset_terminal(stdscr)
                if selected_index == 0:  # Добавить
                    print("Добавление термостата...")
                    name = input("Введите имя термостата: ").strip()
                    if name:
                        self.controller.add_device("Термостат", name)
                        print(f"{Fore.GREEN}Термостат '{name}' добавлен.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Имя не может быть пустым.{Style.RESET_ALL}")
                    input("Нажмите Enter для возврата в меню...")
                elif selected_index == 1:  # Удалить
                    thermostats = [device for device in self.controller.model.devices if isinstance(device, Thermostat)]
                    selected_thermostat = self._select_device(stdscr, thermostats, "термостата")
                    if selected_thermostat:
                        self.controller.remove_device(selected_thermostat.name)
                        print(f"{Fore.GREEN}Термостат '{selected_thermostat.name}' удалён.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 2:  # Включить
                    thermostats = [device for device in self.controller.model.devices if isinstance(device, Thermostat)]
                    selected_thermostat = self._select_device(stdscr, thermostats, "термостата")
                    if selected_thermostat:
                        self.controller.toggle_device(selected_thermostat.name)
                        print(f"{Fore.GREEN}Термостат '{selected_thermostat.name}' включён.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 3:  # Выключить
                    thermostats = [device for device in self.controller.model.devices if isinstance(device, Thermostat)]
                    selected_thermostat = self._select_device(stdscr, thermostats, "термостата")
                    if selected_thermostat:
                        self.controller.toggle_device(selected_thermostat.name)
                        print(f"{Fore.GREEN}Термостат '{selected_thermostat.name}' выключен.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 4:  # Изменить температуру
                    thermostats = [device for device in self.controller.model.devices if isinstance(device, Thermostat)]
                    selected_thermostat = self._select_device(stdscr, thermostats, "термостата")
                    if selected_thermostat:
                        temp = self._safe_input("Введите целевую температуру (10-30°C): ", float, (10, 30))
                        if temp is not None:
                            self.controller.set_thermostat_temp(selected_thermostat.name, {"temp": temp})
                            print(f"{Fore.GREEN}Температура для '{selected_thermostat.name}' установлена: {temp}°C.{Style.RESET_ALL}")
                            input("Нажмите Enter для возврата в меню...")
                elif selected_index == 5:  # Показать статус
                    thermostats = [device for device in self.controller.model.devices if isinstance(device, Thermostat)]
                    if not thermostats:
                        print(f"{Fore.YELLOW}Нет термостатов.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.CYAN}Термостаты:{Style.RESET_ALL}")
                        for thermostat in thermostats:
                            print(f"  - {thermostat.name}: {thermostat.get_status()}")
                    input("Нажмите Enter для возврата в меню...")
                elif selected_index == 6:  # Назад
                    self._restore_terminal(stdscr)
                    break
                self._restore_terminal(stdscr)

    def _manage_sockets(self, stdscr):
        menu_items = [
            "Добавить розетку",
            "Удалить розетку",
            "Включить розетку",
            "Выключить розетку",
            "Показать статус всех розеток",
            "Назад"
        ]
        selected_index = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "=== Управление розетками ===", curses.A_BOLD | curses.color_pair(1))
            for i, item in enumerate(menu_items):
                if i == selected_index:
                    stdscr.addstr(i + 2, 0, f"> {item}", curses.color_pair(2))
                else:
                    stdscr.addstr(i + 2, 0, f"  {item}")
            stdscr.addstr(len(menu_items) + 3, 0, "Используйте 'w' (вверх), 's' (вниз), Enter (выбор)")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('w'):
                selected_index = (selected_index - 1) % len(menu_items)
            elif key == ord('s'):
                selected_index = (selected_index + 1) % len(menu_items)
            elif key == 10:  # Enter
                self._reset_terminal(stdscr)
                if selected_index == 0:  # Добавить
                    print("Добавление розетки...")
                    name = input("Введите имя розетки: ").strip()
                    if name:
                        self.controller.add_device("Розетка", name)
                        print(f"{Fore.GREEN}Розетка '{name}' добавлена.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Имя не может быть пустым.{Style.RESET_ALL}")
                    input("Нажмите Enter для возврата в меню...")
                elif selected_index == 1:  # Удалить
                    sockets = [device for device in self.controller.model.devices if isinstance(device, Socket)]
                    selected_socket = self._select_device(stdscr, sockets, "розетки")
                    if selected_socket:
                        self.controller.remove_device(selected_socket.name)
                        print(f"{Fore.GREEN}Розетка '{selected_socket.name}' удалена.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 2:  # Включить
                    sockets = [device for device in self.controller.model.devices if isinstance(device, Socket)]
                    selected_socket = self._select_device(stdscr, sockets, "розетки")
                    if selected_socket:
                        self.controller.toggle_device(selected_socket.name)
                        print(f"{Fore.GREEN}Розетка '{selected_socket.name}' включена.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 3:  # Выключить
                    sockets = [device for device in self.controller.model.devices if isinstance(device, Socket)]
                    selected_socket = self._select_device(stdscr, sockets, "розетки")
                    if selected_socket:
                        self.controller.toggle_device(selected_socket.name)
                        print(f"{Fore.GREEN}Розетка '{selected_socket.name}' выключена.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 4:  # Показать статус
                    sockets = [device for device in self.controller.model.devices if isinstance(device, Socket)]
                    if not sockets:
                        print(f"{Fore.YELLOW}Нет розеток.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.CYAN}Розетки:{Style.RESET_ALL}")
                        for socket in sockets:
                            print(f"  - {socket.name}: {socket.get_status()}")
                    input("Нажмите Enter для возврата в меню...")
                elif selected_index == 5:  # Назад
                    self._restore_terminal(stdscr)
                    break
                self._restore_terminal(stdscr)

    def _manage_oxygen_monitors(self, stdscr):
        menu_items = [
            "Добавить монитор",
            "Удалить монитор",
            "Включить монитор",
            "Выключить монитор",
            "Установить целевой уровень кислорода",
            "Показать статус всех мониторов",
            "Назад"
        ]
        selected_index = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "=== Управление кислородными мониторами ===", curses.A_BOLD | curses.color_pair(1))
            for i, item in enumerate(menu_items):
                if i == selected_index:
                    stdscr.addstr(i + 2, 0, f"> {item}", curses.color_pair(2))
                else:
                    stdscr.addstr(i + 2, 0, f"  {item}")
            stdscr.addstr(len(menu_items) + 3, 0, "Используйте 'w' (вверх), 's' (вниз), Enter (выбор)")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('w'):
                selected_index = (selected_index - 1) % len(menu_items)
            elif key == ord('s'):
                selected_index = (selected_index + 1) % len(menu_items)
            elif key == 10:  # Enter
                self._reset_terminal(stdscr)
                if selected_index == 0:  # Добавить
                    print("Добавление монитора...")
                    name = input("Введите имя монитора: ").strip()
                    if name:
                        self.controller.add_device("Кислородный монитор", name)
                        print(f"{Fore.GREEN}Монитор '{name}' добавлен.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Имя не может быть пустым.{Style.RESET_ALL}")
                    input("Нажмите Enter для возврата в меню...")
                elif selected_index == 1:  # Удалить
                    monitors = [device for device in self.controller.model.devices if isinstance(device, OxygenMonitor)]
                    selected_monitor = self._select_device(stdscr, monitors, "кислородного монитора")
                    if selected_monitor:
                        self.controller.remove_device(selected_monitor.name)
                        print(f"{Fore.GREEN}Монитор '{selected_monitor.name}' удалён.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 2:  # Включить
                    monitors = [device for device in self.controller.model.devices if isinstance(device, OxygenMonitor)]
                    selected_monitor = self._select_device(stdscr, monitors, "кислородного монитора")
                    if selected_monitor:
                        self.controller.toggle_device(selected_monitor.name)
                        print(f"{Fore.GREEN}Монитор '{selected_monitor.name}' включён.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 3:  # Выключить
                    monitors = [device for device in self.controller.model.devices if isinstance(device, OxygenMonitor)]
                    selected_monitor = self._select_device(stdscr, monitors, "кислородного монитора")
                    if selected_monitor:
                        self.controller.toggle_device(selected_monitor.name)
                        print(f"{Fore.GREEN}Монитор '{selected_monitor.name}' выключен.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 4:  # Установить уровень кислорода
                    monitors = [device for device in self.controller.model.devices if isinstance(device, OxygenMonitor)]
                    selected_monitor = self._select_device(stdscr, monitors, "кислородного монитора")
                    if selected_monitor:
                        level = self._safe_input("Введите целевой уровень кислорода (19-23%): ", float, (19, 23))
                        if level is not None:
                            self.controller.set_oxygen(selected_monitor.name, {"target": level})
                            print(f"{Fore.GREEN}Уровень кислорода для '{selected_monitor.name}' установлен: {level}%.{Style.RESET_ALL}")
                            input("Нажмите Enter для возврата в меню...")
                elif selected_index == 5:  # Показать статус
                    monitors = [device for device in self.controller.model.devices if isinstance(device, OxygenMonitor)]
                    if not monitors:
                        print(f"{Fore.YELLOW}Нет мониторов.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.CYAN}Кислородные мониторы:{Style.RESET_ALL}")
                        for monitor in monitors:
                            print(f"  - {monitor.name}: {monitor.get_status()}")
                    input("Нажмите Enter для возврата в меню...")
                elif selected_index == 6:  # Назад
                    self._restore_terminal(stdscr)
                    break
                self._restore_terminal(stdscr)

    def _manage_doors(self, stdscr):
        menu_items = [
            "Добавить дверь",
            "Удалить дверь",
            "Заблокировать дверь",
            "Разблокировать дверь",
            "Включить автоматическую блокировку",
            "Выключить автоматическую блокировку",
            "Показать статус всех дверей",
            "Назад"
        ]
        selected_index = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "=== Управление дверьми ===", curses.A_BOLD | curses.color_pair(1))
            for i, item in enumerate(menu_items):
                if i == selected_index:
                    stdscr.addstr(i + 2, 0, f"> {item}", curses.color_pair(2))
                else:
                    stdscr.addstr(i + 2, 0, f"  {item}")
            stdscr.addstr(len(menu_items) + 3, 0, "Используйте 'w' (вверх), 's' (вниз), Enter (выбор)")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('w'):
                selected_index = (selected_index - 1) % len(menu_items)
            elif key == ord('s'):
                selected_index = (selected_index + 1) % len(menu_items)
            elif key == 10:  # Enter
                self._reset_terminal(stdscr)
                if selected_index == 0:  # Добавить
                    print("Добавление двери...")
                    name = input("Введите имя двери: ").strip()
                    if name:
                        self.controller.add_device("Дверь", name)
                        print(f"{Fore.GREEN}Дверь '{name}' добавлена.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Имя не может быть пустым.{Style.RESET_ALL}")
                    input("Нажмите Enter для возврата в меню...")
                elif selected_index == 1:  # Удалить
                    doors = [device for device in self.controller.model.devices if isinstance(device, Door)]
                    selected_door = self._select_device(stdscr, doors, "двери")
                    if selected_door:
                        self.controller.remove_device(selected_door.name)
                        print(f"{Fore.GREEN}Дверь '{selected_door.name}' удалена.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 2:  # Заблокировать
                    doors = [device for device in self.controller.model.devices if isinstance(device, Door)]
                    selected_door = self._select_device(stdscr, doors, "двери")
                    if selected_door:
                        self.controller.toggle_lock(selected_door.name, {"action": "Заблокировать"})
                        print(f"{Fore.GREEN}Дверь '{selected_door.name}' заблокирована.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 3:  # Разблокировать
                    doors = [device for device in self.controller.model.devices if isinstance(device, Door)]
                    selected_door = self._select_device(stdscr, doors, "двери")
                    if selected_door:
                        self.controller.toggle_lock(selected_door.name, {"action": "Разблокировать"})
                        print(f"{Fore.GREEN}Дверь '{selected_door.name}' разблокирована.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 4:  # Включить автоблокировку
                    doors = [device for device in self.controller.model.devices if isinstance(device, Door)]
                    selected_door = self._select_device(stdscr, doors, "двери")
                    if selected_door:
                        self.controller.toggle_auto_lock(selected_door.name, {"action": "Включить автоблокировку"})
                        print(f"{Fore.GREEN}Автоблокировка для '{selected_door.name}' включена.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 5:  # Выключить автоблокировку
                    doors = [device for device in self.controller.model.devices if isinstance(device, Door)]
                    selected_door = self._select_device(stdscr, doors, "двери")
                    if selected_door:
                        self.controller.toggle_auto_lock(selected_door.name, {"action": "Выключить автоблокировку"})
                        print(f"{Fore.GREEN}Автоблокировка для '{selected_door.name}' выключена.{Style.RESET_ALL}")
                        input("Нажмите Enter для возврата в меню...")
                elif selected_index == 6:  # Показать статус
                    doors = [device for device in self.controller.model.devices if isinstance(device, Door)]
                    if not doors:
                        print(f"{Fore.YELLOW}Нет дверей.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.CYAN}Двери:{Style.RESET_ALL}")
                        for door in doors:
                            print(f"  - {door.name}: {door.get_status()}")
                    input("Нажмите Enter для возврата в меню...")
                elif selected_index == 7:  # Назад
                    self._restore_terminal(stdscr)
                    break
                self._restore_terminal(stdscr)