from PySide6.QtCore import Qt, QEvent, QPoint
from PySide6.QtGui import QMouseEvent

from tool.plugin import Plugin
from tool import mouse

class Stroke(Plugin):
    def __init__(self):
        super().__init__()
        
        self.id = "act-stroke"
        self.auto = True
    
    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.mouseReleaseEvent(event)
        return super().eventFilter(obj, event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and "act-" not in self.window().state and "after-" not in self.window().state:
            collision = mouse.getCollision(self.window(), event.position().toPoint())
            if self.window().state != "act-drag" and self.window().state != self.id and collision == "head":
                event.accept()
                self.window().replyState(self.id)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.window().state == self.id:
            self.window().replyState("idle", True)
