from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QMouseEvent

from tool.plugin import Plugin
from tool.mouse import getCollision

class UseFan(Plugin):
    def __init__(self):
        super().__init__()
        self.id = "act-use-fan"
        self.name = "吹风扇"
        self.description = "吹风扇，点风扇开关关闭风扇"

    def start(self):
        self.window().changeAnime("using-fan")
        super().start()

    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.MouseButtonPress:
            mouseEvent: QMouseEvent = event
            if mouseEvent.button() == Qt.MouseButton.LeftButton and getCollision(self.window(), mouseEvent.position().toPoint()):
                self.window().changeAnime("turn-off-fan", isAsync = False)
                self.stop()
        return super().eventFilter(obj, event)
