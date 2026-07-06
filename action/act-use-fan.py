from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Slot

@Slot(QWidget)
def start(window: QWidget):
    """开始行动时调用"""
    window.changeAnime("act-use-fan", False, False, True)

@Slot(QWidget)
def stop(window: QWidget):
    """结束行动时调用"""
    pass
