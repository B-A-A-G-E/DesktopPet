from PySide6.QtWidgets import QApplication

import sys

import tool
from tool.config import ConfigManager

from window.pet.petWindow import PetWindow
from window.manager.mainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    window = None
    
    default = ConfigManager.settings["default-pet"]
    if len(sys.argv) == 1:
            window = MainWindow()
    elif sys.argv[1] == "-default":
        if default == "":
            print("default pet name is not exist")
            input("pause")
            sys.exit(-1)
        
        window = PetWindow(default, ConfigManager.pets[default])
        ConfigManager.default = True
    else:
        window = PetWindow(sys.argv[1], ConfigManager.pets[sys.argv[1]])
    
    if ConfigManager.default:
        app.aboutToQuit.connect(window.aboutToQuit)
    
    window.show()
    app.exec()
    
    if ConfigManager.default:
        window.operateState("exit", "exit", isAsync = False)
        window.stateMenu.log("Succeeded to exit", tool.config.LogType.Exit)
