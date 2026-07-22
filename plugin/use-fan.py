from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QMouseEvent

from tool.plugin import Plugin
from tool.collision import pointAt

class Action(Plugin):
    def __init__(self):
        super().__init__()
        self.id = "use-fan"
        self.name = "吹风扇"
        self.description = "吹风扇，点风扇开关关闭风扇"
        self.state = "use-fan"


    def start(self) -> None:
        super().start()
        self.window.changeAnime("using-fan")
    
    def stop(self) -> None:
        self.window.changeAnime("turn-off-fan", isAsync = False)
        self.window.changeState("idle")
        self.window.changeAnime("idle")
        super().stop()

    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.MouseButtonPress:
            mouseEvent: QMouseEvent = event
            if mouseEvent.button() == Qt.MouseButton.LeftButton and \
                "fan-switch" in pointAt(mouseEvent.position().toPoint(), self.window.collisions):
                self.stop()
        return super().eventFilter(obj, event)
