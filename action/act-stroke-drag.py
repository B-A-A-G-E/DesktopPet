### 偷懒写的，不要学，一个行动（插件）应该只放一个事件
from PySide6.QtCore import Qt, QEvent, QPoint
from PySide6.QtGui import QMouseEvent

from tool.plugin import Plugin
from tool import data
from tool import mouse

class Stroke_Drag(Plugin):
    def __init__(self):
        super().__init__()
        
        self.id = "act-stroke-drag"
        self.auto = True
        
        self.dragPosition = QPoint() # 记录鼠标按下时的位置
    
    def start(self):
        pass
    
    def stop(self):
        pass

    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.MouseButtonPress:
            self.mousePressEvent(event)
        elif event.type() == QEvent.Type.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.mouseReleaseEvent(event)
        return False
    
    def mousePressEvent(self, event: QMouseEvent):
        self.window().moveTimer.start(data.base["idle-move-time"])
        self.window().step = 0
        self.window().dir = QPoint(0, 0)
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPosition = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and "act-" not in self.window().state and "after-" not in self.window().state:
            collision = mouse.getCollision(self.window(), event.position().toPoint())
            if self.window().state != "drag" and collision:
                event.accept()
                self.window().replyState(collision)
            else:
                self.window().move(event.globalPosition().toPoint() - self.dragPosition)
                event.accept()
                self.window().replyState("drag")
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.window().state != "idle" and "act-" not in self.window().state and "after-" not in self.window().state:
            self.window().replyState("idle", True)
