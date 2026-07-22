from PySide6.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit
from PySide6.QtCore import Slot, QEvent, QTimer, QPoint, QRect

import json
import os
import random

from tool.plugin import Plugin
from tool.widgetFactory import FormFactory

class Action(Plugin):
    def __init__(self):
        super().__init__()
    
        self.id = "move-randomly"
        self.auto = True
        self.teardownImmed = False
        
        self.moveTimer = QTimer() # 随机移动触发定时器
        self.stepTimer = QTimer() # 步进定时器
        self.step = 0 # 移动步数
        self.dir = QPoint(0, 0) # 移动方向
        self.screenGeo = None  # 存储屏幕几何信息
        self.data: dict = {}
    
    def setup(self, window) -> None:
        super().setup(window)
        self.loadData()
        self.bind()
        self.addPage()
    
    def teardown(self):
        self.moveTimer.stop()
        self.stepTimer.stop()
        self.moveTimer.deleteLater()
        self.stepTimer.deleteLater()
        return super().teardown()
    
    def start(self) -> None:
        super().start()
        self.moveTimer.start(self.data["idle-move-time"])

    def stop(self) -> None:
        self.step = 0
        self.moveTimer.stop()
        super().stop()
    
    def eventFilter(self, obj, event: QEvent) -> None:
        if event.type() == QEvent.Type.MouseButtonPress:
            # 终止自动移动
            self.step = 0
            self.dir = QPoint(0, 0)
        return super().eventFilter(obj, event)
    
    def bind(self) -> None:
        def stopTimer(prevState: str, state: str) -> None:
            if state != "idle":
                self.moveTimer.stop()
            else:
                if not self.moveTimer.isActive():
                    self.moveTimer.start(self.data["idle-move-time"])
    
        self.moveTimer.timeout.connect(self.moveRandomly)

        # 配置步进定时器
        self.stepTimer.setSingleShot(True)
        self.stepTimer.timeout.connect(self.doStep)

        self.window.stateChanged.connect(stopTimer)
        
        self.window.settingMenu.dataUpdated.connect(self.updateData)
    
    def loadData(self) -> None:
        if os.path.exists(f"{self.window.petPath}/config/move-randomly.json"):
            with open(f"{self.window.petPath}/config/move-randomly.json", "r", encoding = "utf-8") as f:
                self.data = json.load(f)
        else:
            with open(f"{self.window.petPath}/config/move-randomly.json", "w", encoding = "utf-8") as f:
                self.data = {
                    "idle-move-time": 15000,
                    "move-min-step": 200,
                    "move-max-step": 3000,
                    "move-step-time": 20,
                    "move-speed": 10
                }
                json.dump(self.data, f, ensure_ascii = False, indent = 2)

    def addPage(self) -> None:
        page = FormFactory([
                ("待机移动时间（毫秒）", "idle-move-time", "int"),
                ("移动最小步长", "move-min-step", "int"),
                ("移动最大步长", "move-max-step", "int"),
                ("移动步进时间（毫秒）", "move-step-time", "int"),
                ("移动速度（像素/步）", "move-speed", "int"),
            ], self.data
        )
        page.build()
        self.window.settingMenu.addPage(page, "移动配置")
    
    @Slot()
    def moveRandomly(self) -> None:
        if self.window.state == "idle":
            self.moveTimer.stop()
            
            self.screenGeo = QApplication.primaryScreen().availableGeometry()
            
            self.dir = QPoint(0, 0)
            while self.dir.x() == 0 and self.dir.y() == 0:
                self.dir.setX(random.randint(-1, 1))
                self.dir.setY(random.randint(-1, 1))
            
            self.step = random.randint(self.data["move-min-step"], self.data["move-max-step"])
            self.doStep()  # 开始第一步

    @Slot()
    def doStep(self) -> None:
        """执行单步移动"""
        if self.step <= 0 or self.window.state != "idle":
            # 移动结束，回到待机定时器
            if self.moveTimer.isActive():
                self.moveTimer.stop()
            self.moveTimer.start(self.data["idle-move-time"])
            return
        
        width, height = self.window.width(), self.window.height()
        
        # 计算新位置
        speed = self.data["move-speed"] * (0.5 if self.dir.x() != 0 and self.dir.y() != 0 else 1)
        newX = self.window.x() + self.dir.x() * speed
        newY = self.window.y() + self.dir.y() * speed
        
        # 检查边界
        if (self.screenGeo.left() <= newX <= self.screenGeo.right() - width) and \
           (self.screenGeo.top() <= newY <= self.screenGeo.bottom() - height):
            self.window.move(newX, newY)
            self.step -= 1
        else:
            # 改变方向
            self.dir = QPoint(0, 0)
            while self.dir.x() == 0 and self.dir.y() == 0:
                self.dir.setX(random.randint(-1, 1))
                self.dir.setY(random.randint(-1, 1))
        
        # 调度下一步
        self.stepTimer.start(self.data["move-step-time"])
    
    @Slot()
    def updateData(self) -> None:
        self.data = self.window.settingMenu.getPage("移动配置").getData()

        with open(f"{self.window.petPath}/config/move-randomly.json", "w", encoding = "utf-8") as f:
            json.dump(self.data, f, ensure_ascii = False, indent = 2)
