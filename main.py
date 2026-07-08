from PySide6.QtWidgets import QApplication

from window.petWindow import PetWindow
from tool.data import LogType

if __name__ == "__main__":
    app = QApplication([])
    window = PetWindow()
    window.show()
    app.exec()
    window.replyState("exit", isAsync = False)
    window.stateMenu.log("Succeeded to exit", LogType.Exit)
