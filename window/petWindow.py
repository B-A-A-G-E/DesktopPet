from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QAction, QMouseEvent
from PySide6.QtCore import Qt, Slot, QPoint, QTimer, QRect

import random
import importlib

from tool import data
from tool import conv
from tool import anime
from tool.data import LogType

from window.dialogMenu import DialogMenu
from window.stateMenu import StateMenu
from window.actionMenu import ActionMenu
from window.settingMenu import SettingMenu

class PetWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # 无边框及透明背景
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 添加控件
        self.imgLb = QLabel() # 存放图片

        # 添加上下文菜单
        self.imgLb.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.imgLb.dialogAct = QAction("对话")
        self.imgLb.stateAct = QAction("状态")
        self.imgLb.actAct = QAction("行动")
        self.imgLb.setAct = QAction("设置")
        self.imgLb.exitAct = QAction("退出")
        self.imgLb.addAction(self.imgLb.dialogAct)
        self.imgLb.addAction(self.imgLb.stateAct)
        self.imgLb.addAction(self.imgLb.actAct)
        self.imgLb.addAction(self.imgLb.setAct)
        self.imgLb.addAction(self.imgLb.exitAct)

        # 设置布局并填入控件
        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(self.imgLb)
        self.setLayout(self.mainlayout)

        # 辅助变量
        self.dragPosition = QPoint() # 记录鼠标按下时的位置
        self.state = "idle" # 当前状态（触发特定事件&防止重复触发回复）
        self.idleTimer = QTimer() # 触发闲置（无操作）时间
        self.moveTimer = QTimer() # 触发随机移动时间
        self.step = 0 # 移动步数
        self.dir = QPoint(0, 0) # 移动方向

        # 添加动画
        self.animes = { k: anime.Anime(v["path"], v["fps"], v["loop"], self, self.imgLb) for k, v in data.anime.items()}
        self.currentAnime = self.animes["idle"]

        # 添加碰撞体
        self.collisions = { k: QRect(v["left"], v["top"], v["width"], v["height"]) for k, v in data.collision.items()}

        # 添加自定义事件
        self.acts = { k: importlib.import_module(v["path"]) for k, v in data.actPath.items()}

        # 安装事件过滤器来捕获所有输入事件
        self.installEventFilter(self)
        self.setMouseTracking(True)

        self.bind()

        # 入场并切换待机
        #self.replyState("entre", False, False)
        #self.stateMenu.log("Succeed to entre", LogType.Entre)
        self.replyState("idle")

        # 开始计时
        self.idleTimer.start(data.base["idle-time"])
        self.moveTimer.start(data.base["idle-move-time"])

    def bind(self) -> None:
        """绑定子窗口及信号"""
        self.dialogMenu = DialogMenu()
        self.stateMenu = StateMenu()
        self.actionMenu = ActionMenu()
        self.settingMenu = SettingMenu()

        self.settingMenu.dataUpdated.connect(self.updateData)

        # 绑定actionMenu的按钮
        for k, startBtn in self.actionMenu.actBtn.items():
            def startAct(act = k):
                if k == self.state:
                    self.stateMenu.log("action has been already started")
                else:
                    self.replyState(act)
                    self.acts[act].start(self)
            startBtn.clicked.connect(lambda: startAct())
        
        def stopAct():
            for act in data.actPath.keys():
                self.acts[act].stop(self)
            self.replyState("idle")
        self.actionMenu.stopBtn.clicked.connect(stopAct)

        # 绑定上下文菜单
        self.imgLb.dialogAct.triggered.connect(self.dialogMenu.show)
        self.imgLb.stateAct.triggered.connect(self.stateMenu.show)
        self.imgLb.setAct.triggered.connect(self.settingMenu.show)
        self.imgLb.actAct.triggered.connect(self.actionMenu.show)
        self.imgLb.exitAct.triggered.connect(QApplication.quit)

        # 绑定idle相关计时器
        self.idleTimer.timeout.connect(lambda: self.replyState("idle"))
        self.moveTimer.timeout.connect(self.moveRandomly)

        # 绑定动画加载失败信号
        for anime in self.animes.values():
            anime.loadErr.connect(lambda text: self.stateMenu.log(text, LogType.Error))
    
    def replyState(self, state: str, afterEvent: bool = False, isAsync: bool = True) -> None:
        """
        执行对应行动时进行响应\n
        若afterEvent为True，则先回应当前状态的after-event事件(动画只能同步播放)\n
        """
        if self.state != state or (state == "idle" and self.state == "idle"):
            # 切换计时器状态
            if state != "idle":
                self.idleTimer.stop()
                self.moveTimer.stop()
            else:
                self.idleTimer.start(data.base["idle-time"])
                if not self.moveTimer.isActive():
                    self.moveTimer.start(data.base["idle-move-time"])
            # 在dialogMenu回复
            self.dialogMenu.addLine(conv.replyText("state", state))
            # 切换动画
            if state in self.animes.keys():
                self.currentAnime.over()
                if afterEvent and f"after-{self.state}" in self.animes.keys():
                    self.replyState(f"after-{self.state}", False, False)
                self.currentAnime = self.animes[state]
                self.currentAnime.play(False, isAsync)
            # 更新状态
            self.state = state
            self.stateMenu.log(self.state, LogType.StateChange)
    
    def getCollision(self, pos: QPoint) -> str | None:
        """获取鼠标点击位置的碰撞体"""
        for k in self.collisions.keys():
            if self.collisions[k].contains(pos):
                return k
        return None

    @Slot()
    def moveRandomly(self) -> None:
        if self.state == "idle":
            self.moveTimer.stop()

            currentGeo = self.geometry()
            width, height = currentGeo.width(), currentGeo.height()

            self.dir = QPoint(0, 0)
            while self.dir.x() == 0 and self.dir.y() == 0:
                self.dir.setX(random.randint(-1, 1))
                self.dir.setY(random.randint(-1, 1))

            # 获取当前屏幕的可用区域（排除任务栏）
            screenGeo = QApplication.primaryScreen().availableGeometry()

            # 生成移动距离
            self.step = random.randint(data.base["move-min-step"], data.base["move-max-step"])

            self.moveWindow(width, height, screenGeo)

    @Slot(int, int, QRect)
    def moveWindow(self, width: int, height: int, screenGeo: QRect) -> None:
        if self.step > 0 and self.state == "idle":
            # 控制斜向移动与水平/竖直移动速度相同
            newX = self.x() + self.dir.x() * data.base["move-speed"] * (0.5 if self.dir.x() != 0 and self.dir.y() != 0 else 1)
            newY = self.y() + self.dir.y() * data.base["move-speed"] * (0.5 if self.dir.x() != 0 and self.dir.y() != 0 else 1)

            # 检查新位置是否在屏幕范围内
            if (screenGeo.left() <= newX <= screenGeo.right() - width) and (screenGeo.top() <= newY <= screenGeo.bottom() - height):
                self.move(newX, newY)
                self.step -= 1
            else:
                self.dir = QPoint(0, 0)
                while self.dir.x() == 0 and self.dir.y() == 0:
                    self.dir.setX(random.randint(-1, 1))
                    self.dir.setY(random.randint(-1, 1))
            QTimer.singleShot(data.base["move-step-time"], lambda: self.moveWindow(width, height, screenGeo))
        else:
            self.moveTimer.start(data.base["idle-move-time"])
    
    @Slot()
    def updateData(self) -> None:
        """更新数据"""
        # petWindow
        self.animes = { k: anime.Anime(v["path"], v["fps"], v["loop"], self, self.imgLb) for k, v in data.anime.items()}
        self.collisions = { k: QRect(v["left"], v["top"], v["width"], v["height"]) for k, v in data.collision.items()}
        # dialogWindow
        self.dialogMenu.resetQuesSelecter()
        self.stateMenu.log("Data is updated", LogType.Set)

    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下时记录位置"""
        self.moveTimer.start(data.base["idle-move-time"])
        self.step = 0
        self.dir = QPoint(0, 0)
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPosition = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            collision = self.getCollision(event.position().toPoint())
            if self.state != "drag" and collision:
                event.accept()
                self.replyState(collision)
            else:
                self.move(event.globalPosition().toPoint() - self.dragPosition)
                event.accept()
                self.replyState("drag")
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.state != "idle":
            self.replyState("idle", True)
        return super().mouseReleaseEvent(event)
