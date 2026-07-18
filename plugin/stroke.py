from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QMouseEvent

from tool.plugin import Plugin
from tool.collision import pointAt

class Action(Plugin):
    def __init__(self):
        super().__init__()
        
        self.id = "stroke"
        self.state = "stroke"
        self.auto = True
        self.teardownImmed = False
        
        self.anime = "stroke"
    
    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.mouseReleaseEvent(event)
        return super().eventFilter(obj, event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.window.state == "idle":
            if self.window.state != "drag" and self.window.state != self.state and \
                "head" in pointAt(event.position().toPoint(), self.window.collisions):
                event.accept()
                self.window.operateState(self.state, self.anime)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.window.state == self.state:
            self.window.operateState(f"after-{self.state}", f"after-{self.anime}", isAsync = False)
            self.window.changeState("idle")
            self.window.changeAnime("idle")
