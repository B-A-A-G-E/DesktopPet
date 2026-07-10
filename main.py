from PySide6.QtWidgets import QApplication

from qt_material import apply_stylesheet

from window.petWindow import PetWindow
from tool.data import LogType

if __name__ == "__main__":
    app = QApplication([])
    apply_stylesheet(app, theme = "light_cyan_500.xml")

    window = PetWindow()
    app.aboutToQuit.connect(window.aboutToQuit.emit)
    window.show()
    app.exec()
    
    window.operateState("exit", "exit", isAsync = False)
    window.stateMenu.log("Succeeded to exit", LogType.Exit)
