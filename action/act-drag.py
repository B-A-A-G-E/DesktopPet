from PySide6.QtCore import Qt, QEvent, QPoint
from PySide6.QtGui import QMouseEvent

from tool.plugin import Plugin
from tool import mouse

class Drag(Plugin):
    def __init__(self):
        super().__init__()
        
        self.id = "act-drag"
        self.auto = True
        
        self.dragPosition = QPoint() # 记录鼠标按下时的位置
    
    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.MouseButtonPress:
            self.mousePressEvent(event)
        elif event.type() == QEvent.Type.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.mouseReleaseEvent(event)
        return super().eventFilter(obj, event)
    
    def mousePressEvent(self, event: QMouseEvent):
        # 记录左键按下时的窗口坐标
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
            self.dragPosition = event.globalPosition().toPoint() - self.window.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and "after-" not in self.window.state:
            collision = mouse.getCollision(self.window, event.position().toPoint())
            if not collision:
                event.accept()
                if self.window.state != self.id:
                    self.window.replyState(self.id)
                self.window.move(event.globalPosition().toPoint() - self.dragPosition)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.window.state == self.id:
            self.window.replyState("idle", False)
