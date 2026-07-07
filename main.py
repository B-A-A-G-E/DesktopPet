from PySide6.QtWidgets import QApplication

from window.petWindow import PetWindow

if __name__ == "__main__":
    app = QApplication([])
    window = PetWindow()
    app.aboutToQuit.connect(lambda: window.replyState("exit", isAsync = False))
    window.show()
    app.exec()
