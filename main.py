# main.py
from Smarthome.smarthome import SmartHome
from Smarthome.light import Light
from Smarthome.thermostat import Thermostat
from Smarthome.socket import Socket
from Smarthome.oxygen_monitor import OxygenMonitor
from Smarthome.door import Door
import inquirer


def show_all_components(home: SmartHome):
    """Показывает все компоненты дома в иерархическом виде."""
    print("\n=== Состояние умного дома ===")

    # Источники света
    lights = [device for device in home.devices if isinstance(device, Light)]
    if lights:
        print("\nИсточники света:")
        for light in lights:
            print(f"  - {light.name}: {light.get_status()}")
    else:
        print("\nИсточники света: нет устройств.")

    # Термостаты
    thermostats = [device for device in home.devices if isinstance(device, Thermostat)]
    if thermostats:
        print("\nТермостаты:")
        for thermostat in thermostats:
            print(f"  - {thermostat.name}: {thermostat.get_status()}")
    else:
        print("\nТермостаты: нет устройств.")

    # Розетки
    sockets = [device for device in home.devices if isinstance(device, Socket)]
    if sockets:
        print("\nРозетки:")
        for socket in sockets:
            print(f"  - {socket.name}: {socket.get_status()}")
    else:
        print("\nРозетки: нет устройств.")

    # Кислородные мониторы
    monitors = [device for device in home.devices if isinstance(device, OxygenMonitor)]
    if monitors:
        print("\nКислородные мониторы:")
        for monitor in monitors:
            print(f"  - {monitor.name}: {monitor.get_status()}")
    else:
        print("\nКислородные мониторы: нет устройств.")

    # Двери
    doors = [device for device in home.devices if isinstance(device, Door)]
    if doors:
        print("\nДвери:")
        for door in doors:
            print(f"  - {door.name}: {door.get_status()}")
    else:
        print("\nДвери: нет устройств.")

    print("============================\n")

def auto_lock_doors(home: SmartHome):
    """Автоматически блокирует двери на ночь."""
    for device in home.devices:
        if isinstance(device, Door):
            device.check_night_lock()

def manage_lights(home: SmartHome):
    """Меню для управления источниками света."""
    while True:
        questions = [
            inquirer.List('action',
                          message="Управление источниками света",
                          choices=[
                              'Добавить источник света',
                              'Удалить источник света',
                              'Включить источник света',
                              'Выключить источник света',
                              'Изменить яркость',
                              'Изменить температуру света',
                              'Показать статус всех источников света',
                              'Назад'
                          ],
                      ),
        ]
        answers = inquirer.prompt(questions)

        if answers['action'] == 'Добавить источник света':
            device_name = inquirer.prompt([
                inquirer.Text('name', message="Введите имя источника света"),
            ])['name']
            home.add_device(Light(device_name))

        elif answers['action'] == 'Удалить источник света':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Light
            lights = [device for device in home.devices if isinstance(device, Light)]
            if not lights:
                print("Нет источников света.")
                continue

            light_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите источник света",
                              choices=[light.name for light in lights],
                          ),
            ])['name']

            home.remove_device(light_name)

        elif answers['action'] == 'Включить источник света':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Light
            lights = [device for device in home.devices if isinstance(device, Light)]
            if not lights:
                print("Нет источников света.")
                continue

            light_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите источник света",
                              choices=[light.name for light in lights],
                          ),
            ])['name']

            for light in lights:
                if light.name == light_name:
                    light.turn_on()
                    break

        elif answers['action'] == 'Выключить источник света':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Light
            lights = [device for device in home.devices if isinstance(device, Light)]
            if not lights:
                print("Нет источников света.")
                continue

            light_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите источник света",
                              choices=[light.name for light in lights],
                          ),
            ])['name']

            for light in lights:
                if light.name == light_name:
                    light.turn_off()
                    break

        elif answers['action'] == 'Изменить яркость':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Light
            lights = [device for device in home.devices if isinstance(device, Light)]
            if not lights:
                print("Нет источников света.")
                continue

            light_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите источник света",
                              choices=[light.name for light in lights],
                          ),
            ])['name']

            brightness = inquirer.prompt([
                inquirer.Text('brightness', message="Введите яркость (0-100)"),
            ])['brightness']
            try:
                brightness = int(brightness)
                if 0 <= brightness <= 100:
                    for light in lights:
                        if light.name == light_name:
                            light.set_brightness(brightness)
                            break
                else:
                    print("Ошибка: яркость должна быть от 0 до 100.")
            except ValueError:
                print("Ошибка: введите число.")

        elif answers['action'] == 'Изменить температуру света':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Light
            lights = [device for device in home.devices if isinstance(device, Light)]
            if not lights:
                print("Нет источников света.")
                continue

            light_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите источник света",
                              choices=[light.name for light in lights],
                          ),
            ])['name']

            temperature = inquirer.prompt([
                inquirer.List('temperature',
                              message="Выберите температуру света",
                              choices=['warm', 'neutral', 'cold'],
                          ),
            ])['temperature']

            for light in lights:
                if light.name == light_name:
                    light.set_color_temperature(temperature)
                    break

        elif answers['action'] == 'Показать статус всех источников света':
            lights = [device for device in home.devices if isinstance(device, Light)]
            if not lights:
                print("Нет источников света.")
            else:
                print("Источники света:")
                for light in lights:
                    print(f"  - {light.get_status()}")

        elif answers['action'] == 'Назад':
            break

def manage_thermostats(home: SmartHome):
    """Меню для управления термостатами."""
    while True:
        questions = [
            inquirer.List('action',
                          message="Управление термостатами",
                          choices=[
                              'Добавить термостат',
                              'Удалить термостат',
                              'Включить термостат',
                              'Выключить термостат',
                              'Изменить целевую температуру',
                              'Показать статус всех термостатов',
                              'Назад'
                          ],
                      ),
        ]
        answers = inquirer.prompt(questions)

        if answers['action'] == 'Добавить термостат':
            device_name = inquirer.prompt([
                inquirer.Text('name', message="Введите имя термостата"),
            ])['name']
            home.add_device(Thermostat(device_name))

        elif answers['action'] == 'Удалить термостат':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Thermostat
            thermostats = [device for device in home.devices if isinstance(device, Thermostat)]
            if not thermostats:
                print("Нет термостатов.")
                continue

            thermostat_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите термостат",
                              choices=[thermostat.name for thermostat in thermostats],
                          ),
            ])['name']

            home.remove_device(thermostat_name)

        elif answers['action'] == 'Включить термостат':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Thermostat
            thermostats = [device for device in home.devices if isinstance(device, Thermostat)]
            if not thermostats:
                print("Нет термостатов.")
                continue

            thermostat_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите термостат",
                              choices=[thermostat.name for thermostat in thermostats],
                          ),
            ])['name']

            for thermostat in thermostats:
                if thermostat.name == thermostat_name:
                    thermostat.turn_on()
                    break

        elif answers['action'] == 'Выключить термостат':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Thermostat
            thermostats = [device for device in home.devices if isinstance(device, Thermostat)]
            if not thermostats:
                print("Нет термостатов.")
                continue

            thermostat_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите термостат",
                              choices=[thermostat.name for thermostat in thermostats],
                          ),
            ])['name']

            for thermostat in thermostats:
                if thermostat.name == thermostat_name:
                    thermostat.turn_off()
                    break

        elif answers['action'] == 'Изменить целевую температуру':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Thermostat
            thermostats = [device for device in home.devices if isinstance(device, Thermostat)]
            if not thermostats:
                print("Нет термостатов.")
                continue

            thermostat_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите термостат",
                              choices=[thermostat.name for thermostat in thermostats],
                          ),
            ])['name']

            target_temp = inquirer.prompt([
                inquirer.Text('temp', message="Введите целевую температуру (10-30°C)"),
            ])['temp']
            try:
                target_temp = float(target_temp)
                for thermostat in thermostats:
                    if thermostat.name == thermostat_name:
                        thermostat.set_target_temp(target_temp)
                        break
            except ValueError:
                print("Ошибка: введите число.")

        elif answers['action'] == 'Показать статус всех термостатов':
            thermostats = [device for device in home.devices if isinstance(device, Thermostat)]
            if not thermostats:
                print("Нет термостатов.")
            else:
                print("Термостаты:")
                for thermostat in thermostats:
                    print(f"  - {thermostat.get_status()}")

        elif answers['action'] == 'Назад':
            break
def manage_sockets(home: SmartHome):
    """Меню для управления розетками."""
    while True:
        questions = [
            inquirer.List('action',
                          message="Управление розетками",
                          choices=[
                              'Добавить розетку',
                              'Удалить розетку',
                              'Включить розетку',
                              'Выключить розетку',
                              'Показать статус всех розеток',
                              'Назад'
                          ],
                      ),
        ]
        answers = inquirer.prompt(questions)

        if answers['action'] == 'Добавить розетку':
            device_name = inquirer.prompt([
                inquirer.Text('name', message="Введите имя розетки"),
            ])['name']
            home.add_device(Socket(device_name))

        elif answers['action'] == 'Удалить розетку':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Socket
            sockets = [device for device in home.devices if isinstance(device, Socket)]
            if not sockets:
                print("Нет розеток.")
                continue

            socket_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите розетку",
                              choices=[socket.name for socket in sockets],
                          ),
            ])['name']

            home.remove_device(socket_name)

        elif answers['action'] == 'Включить розетку':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Socket
            sockets = [device for device in home.devices if isinstance(device, Socket)]
            if not sockets:
                print("Нет розеток.")
                continue

            socket_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите розетку",
                              choices=[socket.name for socket in sockets],
                          ),
            ])['name']

            for socket in sockets:
                if socket.name == socket_name:
                    socket.turn_on()
                    break

        elif answers['action'] == 'Выключить розетку':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Socket
            sockets = [device for device in home.devices if isinstance(device, Socket)]
            if not sockets:
                print("Нет розеток.")
                continue

            socket_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите розетку",
                              choices=[socket.name for socket in sockets],
                          ),
            ])['name']

            for socket in sockets:
                if socket.name == socket_name:
                    socket.turn_off()
                    break

        elif answers['action'] == 'Показать статус всех розеток':
            sockets = [device for device in home.devices if isinstance(device, Socket)]
            if not sockets:
                print("Нет розеток.")
            else:
                print("Розетки:")
                for socket in sockets:
                    print(f"  - {socket.get_status()}")

        elif answers['action'] == 'Назад':
            break
def manage_oxygen_monitors(home: SmartHome):
    """Меню для управления кислородными мониторами."""
    while True:
        questions = [
            inquirer.List('action',
                          message="Управление кислородными мониторами",
                          choices=[
                              'Добавить монитор',
                              'Удалить монитор',
                              'Включить монитор',
                              'Выключить монитор',
                              'Установить целевой уровень кислорода',
                              'Показать статус всех мониторов',
                              'Назад'
                          ],
                      ),
        ]
        answers = inquirer.prompt(questions)

        if answers['action'] == 'Добавить монитор':
            device_name = inquirer.prompt([
                inquirer.Text('name', message="Введите имя монитора"),
            ])['name']
            home.add_device(OxygenMonitor(device_name))

        elif answers['action'] == 'Удалить монитор':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа OxygenMonitor
            monitors = [device for device in home.devices if isinstance(device, OxygenMonitor)]
            if not monitors:
                print("Нет мониторов.")
                continue

            monitor_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите монитор",
                              choices=[monitor.name for monitor in monitors],
                          ),
            ])['name']

            home.remove_device(monitor_name)

        elif answers['action'] == 'Включить монитор':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа OxygenMonitor
            monitors = [device for device in home.devices if isinstance(device, OxygenMonitor)]
            if not monitors:
                print("Нет мониторов.")
                continue

            monitor_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите монитор",
                              choices=[monitor.name for monitor in monitors],
                          ),
            ])['name']

            for monitor in monitors:
                if monitor.name == monitor_name:
                    monitor.turn_on()
                    break

        elif answers['action'] == 'Выключить монитор':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа OxygenMonitor
            monitors = [device for device in home.devices if isinstance(device, OxygenMonitor)]
            if not monitors:
                print("Нет мониторов.")
                continue

            monitor_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите монитор",
                              choices=[monitor.name for monitor in monitors],
                          ),
            ])['name']

            for monitor in monitors:
                if monitor.name == monitor_name:
                    monitor.turn_off()
                    break

        elif answers['action'] == 'Установить целевой уровень кислорода':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа OxygenMonitor
            monitors = [device for device in home.devices if isinstance(device, OxygenMonitor)]
            if not monitors:
                print("Нет мониторов.")
                continue

            monitor_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите монитор",
                              choices=[monitor.name for monitor in monitors],
                          ),
            ])['name']

            target_level = inquirer.prompt([
                inquirer.Text('level', message="Введите целевой уровень кислорода (19-23%)"),
            ])['level']
            try:
                target_level = float(target_level)
                for monitor in monitors:
                    if monitor.name == monitor_name:
                        monitor.set_target_oxygen(target_level)
                        break
            except ValueError:
                print("Ошибка: введите число.")

        elif answers['action'] == 'Показать статус всех мониторов':
            monitors = [device for device in home.devices if isinstance(device, OxygenMonitor)]
            if not monitors:
                print("Нет мониторов.")
            else:
                print("Кислородные мониторы:")
                for monitor in monitors:
                    print(f"  - {monitor.get_status()}")

        elif answers['action'] == 'Назад':
            break
def manage_doors(home: SmartHome):
    """Меню для управления дверьми."""
    while True:
        questions = [
            inquirer.List('action',
                          message="Управление дверьми",
                          choices=[
                              'Добавить дверь',
                              'Удалить дверь',
                              'Заблокировать дверь',
                              'Разблокировать дверь',
                              'Включить автоматическую блокировку',
                              'Выключить автоматическую блокировку',
                              'Показать статус всех дверей',
                              'Назад'
                          ],
                      ),
        ]
        answers = inquirer.prompt(questions)

        if answers['action'] == 'Добавить дверь':
            device_name = inquirer.prompt([
                inquirer.Text('name', message="Введите имя двери"),
            ])['name']
            home.add_device(Door(device_name))

        elif answers['action'] == 'Удалить дверь':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Door
            doors = [device for device in home.devices if isinstance(device, Door)]
            if not doors:
                print("Нет дверей.")
                continue

            door_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите дверь",
                              choices=[door.name for door in doors],
                          ),
            ])['name']

            home.remove_device(door_name)

        elif answers['action'] == 'Заблокировать дверь':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Door
            doors = [device for device in home.devices if isinstance(device, Door)]
            if not doors:
                print("Нет дверей.")
                continue

            door_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите дверь",
                              choices=[door.name for door in doors],
                          ),
            ])['name']

            for door in doors:
                if door.name == door_name:
                    door.lock()
                    break

        elif answers['action'] == 'Разблокировать дверь':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Door
            doors = [device for device in home.devices if isinstance(device, Door)]
            if not doors:
                print("Нет дверей.")
                continue

            door_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите дверь",
                              choices=[door.name for door in doors],
                          ),
            ])['name']

            for door in doors:
                if door.name == door_name:
                    door.unlock()
                    break

        elif answers['action'] == 'Включить автоматическую блокировку':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Door
            doors = [device for device in home.devices if isinstance(device, Door)]
            if not doors:
                print("Нет дверей.")
                continue

            door_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите дверь",
                              choices=[door.name for door in doors],
                          ),
            ])['name']

            for door in doors:
                if door.name == door_name:
                    door.enable_auto_lock()
                    break

        elif answers['action'] == 'Выключить автоматическую блокировку':
            if not home.devices:
                print("Нет устройств для управления.")
                continue

            # Выбираем только устройства типа Door
            doors = [device for device in home.devices if isinstance(device, Door)]
            if not doors:
                print("Нет дверей.")
                continue

            door_name = inquirer.prompt([
                inquirer.List('name',
                              message="Выберите дверь",
                              choices=[door.name for door in doors],
                          ),
            ])['name']

            for door in doors:
                if door.name == door_name:
                    door.disable_auto_lock()
                    break

        elif answers['action'] == 'Показать статус всех дверей':
            doors = [device for device in home.devices if isinstance(device, Door)]
            if not doors:
                print("Нет дверей.")
            else:
                print("Двери:")
                for door in doors:
                    print(f"  - {door.name}: {door.get_status()}")

        elif answers['action'] == 'Назад':
            break
def main():
    home = SmartHome()

    while True:
        # Автоматическая блокировка дверей на ночь
        auto_lock_doors(home)

        questions = [
            inquirer.List('action',
                          message="Главное меню",
                          choices=[
                              'Управление источниками света',
                              'Управление термостатами',
                              'Управление розетками',
                              'Управление кислородными мониторами',
                              'Управление дверьми',
                              'Показать все компоненты дома',
                              'Выйти'
                          ],
                      ),
        ]
        answers = inquirer.prompt(questions)

        if answers['action'] == 'Управление источниками света':
            manage_lights(home)
        elif answers['action'] == 'Управление термостатами':
            manage_thermostats(home)
        elif answers['action'] == 'Управление розетками':
            manage_sockets(home)
        elif answers['action'] == 'Управление кислородными мониторами':
            manage_oxygen_monitors(home)
        elif answers['action'] == 'Управление дверьми':
            manage_doors(home)
        elif answers['action'] == 'Показать все компоненты дома':
            show_all_components(home)
        elif answers['action'] == 'Выйти':
            print("Выход из программы.")
            break

if __name__ == "__main__":
    main()