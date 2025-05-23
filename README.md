# Умный дом

Добро пожаловать в проект **Умный дом**! Это приложение для управления устройствами умного дома, включая источники света, термостаты, розетки, кислородные мониторы и двери. Проект поддерживает два интерфейса: командную строку (CLI) с удобной навигацией и графический интерфейс (GUI) с современным дизайном.

## Основной функционал

- **Управление устройствами**:
  - **Источники света**: вкл/выкл, изменение яркости (0–100%), температуры света (тёплый, нейтральный, холодный).
  - **Термостаты**: вкл/выкл, установка температуры (10–30°C).
  - **Розетки**: вкл/выкл.
  - **Кислородные мониторы**: вкл/выкл, установка уровня кислорода (19–23%).
  - **Двери**: блокировка/разблокировка, вкл/выкл автоблокировки.
- **Добавление и удаление устройств**.
- **Просмотр статуса**:
  - Индивидуальный статус устройств (например, "Лампа1: Включено, яркость: 75%, температура: warm").
  - Полный обзор всех устройств в доме.
- **Интерфейсы**:
  - **CLI**: меню с навигацией через `w` (вверх), `s` (вниз), `Enter` (выбор). Цвета: голубой (`#00ACC1`) для заголовков, зелёный (`#4CAF50`) для выделения, красный (`#F44336`) для ошибок, жёлтый (`#FFEB3B`) для предупреждений.
  - **GUI**: кнопки (`#6A1B9A`, `#4CAF50`), выделение (`#2E7D32`), тёмный фон (`#2A2A2E`).

## Требования

- **Python**: 3.8 или выше.
- **Операционная система**: Linux, macOS, Windows (CLI требует `curses` на Linux/macOS или `windows-curses` на Windows).
- **Зависимости**:
  - `colorama==0.4.6` (для цветного вывода в CLI).
  - GUI библиотека (например, `tkinter`, уточняется в зависимости от реализации).
- Доступ к терминалу для CLI или оконная система для GUI.

## Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/Diu410/-home-ogkrupki-Model_smart_house_gui_plus_cli
   cd Model_smart_house_gui_plus_cli
   ```

2. **Создайте виртуальную среду**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости**:
   ```bash
   pip install colorama==0.4.6
   ```
   Для Windows, если используете CLI:
   ```bash
   pip install windows-curses
   ```

4. **Проверьте Python**:
   ```bash
   python --version
   ```

## Запуск

1. **CLI режим**:
   ```bash
   cd src
   python main.py --cli
   ```

2. **GUI режим**:
   ```bash
   cd src
   python main.py
   ```

## Использование

### CLI
- **Навигация**: Используйте `w` (вверх), `s` (вниз), `Enter` (выбор) для перемещения по меню.
- **Цвета**:
  - Заголовки: голубой (`#00ACC1`).
  - Выделение: зелёный (`#4CAF50`).
  - Ошибки: красный (`#F44336`).
  - Предупреждения: жёлтый (`#FFEB3B`).

#### Пример: Управление светом
1. В главном меню выберите «Управление источниками света» (`w`/`s`/`Enter`).
2. Выберите «Добавить источник света», введите имя, например, «Лампа1»:
   ```
   Добавление источника света...
   Введите имя источника света: Лампа1
   Источник света 'Лампа1' добавлен.
   Нажмите Enter для возврата в меню...
   ```
3. Выберите «Изменить яркость», выберите «Лампа1»:
   ```
   === Выбор источника света ===
   > Лампа1 (Включено, яркость: 50%, температура: neutral)
   Используйте 'w' (вверх), 's' (вниз), Enter (выбор)
   ```
4. Введите яркость `75`:
   ```
   Введите яркость (0-100): 75
   Яркость для 'Лампа1' установлена: 75%.
   Нажмите Enter для возврата в меню...
   ```
5. Выберите «Показать все компоненты дома»:
   ```
   === Состояние умного дома ===
   Источники света:
     - Лампа1: Включено, яркость: 75%, температура: neutral
   Термостаты: нет устройств.
   Розетки: нет устройств.
   Кислородные мониторы: нет устройств.
   Двери: нет устройств.
   ============================
   Нажмите Enter для возврата в меню...
   ```

#### Пример: Управление дверью
1. Добавьте дверь «Дверь1».
2. Выберите «Заблокировать дверь»:
   ```
   === Выбор двери ===
   > Дверь1 (Разблокирована, автоблокировка: Выключена)
   Используйте 'w' (вверх), 's' (вниз), Enter (выбор)
   ```
3. Выберите «Дверь1»:
   ```
   Дверь 'Дверь1' заблокирована.
   Нажмите Enter для возврата в меню...
   ```

### GUI
- Запустите приложение без флага `--cli`.
- Используйте мышь для взаимодействия с кнопками.
- Цветовая схема: фиолетовые кнопки (`#6A1B9A`), зелёные акценты (`#4CAF50`), тёмный фон (`#2A2A2E`).

## Структура проекта

```
smart-home/
├── src/
│   ├── cli/
│   │   └── cli.py          # Логика интерфейса командной строки
│   ├── contoller/
│   │   └── controller.py      
│   ├── view/
│   │   └── gui.py          # Логика графического интерфейса
│   ├── model/
│   │   ├── light.py        # Модель источника света
│   │   ├── thermostat.py   # Модель термостата
│   │   ├── socket.py       # Модель розетки
│   │   ├── oxygen_monitor.py # Модель кислородного монитора
│   │   ├── door.py         # Модель двери
│   │   ├── device.py       
│   │   ├── smarthome.py
│   └── main.py             # Точка входа
├── .venv/                  # Виртуальная среда
├── README.md               # Этот файл
└── requirements.txt      
```

## Технологии

- **Python 3.8+**: Основной язык.
- **colorama**: Цветной вывод в CLI.
- **curses**: Интерактивное меню в CLI (Linux/macOS, Windows с `windows-curses`).
- **GUI библиотека**:  `PyQt6`
- **ООП**: Модели устройств реализованы как классы в `src/model`.

