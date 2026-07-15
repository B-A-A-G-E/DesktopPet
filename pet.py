import PySide6.QtWidgets

import sys

import tool
from window.pet.petWindow import PetWindow

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(-1)
    app = PySide6.QtWidgets.QApplication([])

    print(sys.argv[1])
    petWindow = PetWindow(sys.argv[1])
    app.aboutToQuit.connect(petWindow.aboutToQuit.emit)
    petWindow.show()
    app.exec()
    
    petWindow.operateState("exit", "exit", isAsync = False)
    petWindow.stateMenu.log("Succeeded to exit", tool.config.LogType.Exit)
