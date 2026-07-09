from PySide6.QtCore import Qt, QEvent, QPoint
from PySide6.QtGui import QMouseEvent

from tool.plugin import Plugin
from tool import mouse

class Action(Plugin):
    def __init__(self):
        super().__init__()
        
        self.id = "act-stroke"
        self.state = "stroke"
        self.auto = True
    
    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.mouseReleaseEvent(event)
        return super().eventFilter(obj, event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.window.state == "idle":
            collision = mouse.getCollision(self.window, event.position().toPoint())
            if self.window.state != "act-drag" and self.window.state != self.state and collision == "head":
                event.accept()
                self.window.replyState(self.state)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.window.state == self.state:
            self.window.replyState("idle", True)
