from PySide6.QtCore import Qt, QEvent, QPoint, QRect, QTimer
from PySide6.QtGui import QCursor

from tool.plugin import Plugin
from tool.audio import AudioPlayer

class Action(Plugin):
    def __init__(self):
        super().__init__()
        self.id = "dagou-integ-plugin"
        self.auto = True
        self.timer: QTimer | None = None

    def setup(self, window):
        super().setup(window)

        self.bark = AudioPlayer(r".\plugin\dagou-integ-plugin\audio\bark.mp3")

    def teardown(self):
        if self.timer:
            self.timer.stop()
            self.timer = None
        super().teardown()

    def start(self):
        super().start()
        
        # 使用定时器轮询鼠标位置
        self.timer = QTimer()
        self.timer.timeout.connect(self.checkMouse)
        self.timer.start(20)  # 50fps，平衡性能和响应速度
        
        self.window.operateState("idle", "idle")

    def stop(self):
        if self.timer:
            self.timer.stop()
            self.timer = None
        super().stop()

    def eventFilter(self, obj, event: QEvent):
        # 处理鼠标按下事件
        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
                if self.timer:
                    self.timer.stop()
                    self.timer = None
                
                self.window.changeState("idle")
                self.window.changeAnime("idle")
        else:
            if self.timer is None and event.type() != QEvent.Type.MouseButtonRelease:
                if self.window.state != "drag":
                    self.timer = QTimer()
                    self.timer.timeout.connect(self.checkMouse)
                    self.timer.start(20)
        
        return super().eventFilter(obj, event)

    def checkMouse(self) -> None:
        """定时检查鼠标位置"""
        if not self.window or not self.window.isVisible():
            return
        
        # 获取鼠标全局位置
        mousePos = QCursor.pos()
        geo = self.window.geometry()
        
        # 计算距离
        distance = self.getDistance(mousePos, geo)
        
        # 更新状态
        if geo.contains(mousePos):
            self.bark.play()
            self.window.operateState("bark", "bark")
        elif 0 < distance < 200:
            self.bark.stop()
            self.window.operateState("heyiwei", "heyiwei")
        else:
            self.bark.stop()
            self.window.operateState("idle", "idle")

    def getDistance(self, point: QPoint, rect: QRect) -> float:
        """计算点到矩形的最短距离"""
        dx = 0
        dy = 0
        
        if point.x() < rect.x():
            dx = rect.x() - point.x()
        elif point.x() > rect.x() + rect.width():
            dx = point.x() - (rect.x() + rect.width())
        
        if point.y() < rect.y():
            dy = rect.y() - point.y()
        elif point.y() > rect.y() + rect.height():
            dy = point.y() - (rect.y() + rect.height())
        
        if dx == 0 and dy == 0:
            return 0.0
        return (dx ** 2 + dy ** 2) ** 0.5
