from PySide6.QtWidgets import QApplication

import qtvscodestyle

from window.petWindow import PetWindow
from tool.data import LogType

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qtvscodestyle.load_stylesheet(qtvscodestyle.Theme.LIGHT_VS))

    window = PetWindow()
    app.aboutToQuit.connect(window.aboutToQuit.emit)
    window.show()
    app.exec()
    
    window.operateState("exit", "exit", isAsync = False)
    window.stateMenu.log("Succeeded to exit", LogType.Exit)
