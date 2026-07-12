import PySide6.QtWidgets

import tool
from window.petWindow import PetWindow

if __name__ == "__main__":
    app = PySide6.QtWidgets.QApplication([])

    petWindow = PetWindow()
    app.aboutToQuit.connect(petWindow.aboutToQuit.emit)
    petWindow.show()
    app.exec()
    
    petWindow.operateState("exit", "exit", isAsync = False)
    petWindow.stateMenu.log("Succeeded to exit", tool.data.LogType.Exit)
