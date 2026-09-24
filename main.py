from PySide6.QtWidgets import QApplication

import sys

from tool.config import ConfigManager

from window.pet.petWindow import PetWindow
from window.manager.mainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    window: MainWindow | PetWindow | None = None
    
    default = ConfigManager.settings["default-pet"]
    if len(sys.argv) == 1:
            window = MainWindow()
    elif sys.argv[1] == "-default":
        if default == "":
            print("default pet does not exist")
            input("pause")
            sys.exit(-1)
        
        ConfigManager.default = True
        window = PetWindow(default)
    else:
        window = PetWindow(sys.argv[1])
    
    if ConfigManager.default:
        app.aboutToQuit.connect(window.aboutToQuit)
    
    window.show()
    app.exec()
