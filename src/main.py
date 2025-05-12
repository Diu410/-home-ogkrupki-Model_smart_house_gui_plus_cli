import argparse
import sys
import os
from PyQt6.QtWidgets import QApplication

# Настраиваем sys.path для корректных импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.controller.controller import SmartHomeController
from src.model.smarthome import SmartHome
from src.view.gui import SmartHomeView
from src.cli.cli import SmartHomeCLI


def main():
    parser = argparse.ArgumentParser(description="Smart Home System")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    args = parser.parse_args()

    smarthome = SmartHome()

    try:
        if args.cli:
            view = SmartHomeCLI()
            controller = SmartHomeController(smarthome, view)
            view.set_controller(controller)
            view.run()
        else:
            app = QApplication([])
            view = SmartHomeView()
            controller = SmartHomeController(smarthome, view)
            view.show()
            app.exec()
    except Exception as e:
        print(f"Ошибка при запуске: {e}")


if __name__ == "__main__":
    main()