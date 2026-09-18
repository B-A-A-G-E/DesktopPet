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
        
        self.moveTimer = QTimer() # 随机移动触发定时器（单次触发）
        self.stepTimer = QTimer() # 步进定时器（单次触发）
        self.step = 0 # 剩余移动步数
        self.dir = QPoint(0, 0) # 移动方向
        self.screenGeo = None  # 存储屏幕几何信息
        self.data: dict = {}
        self._moving = False  # 是否正在移动中
    
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
        # 启动待机定时器，等待 idle-move-time 后触发一次随机移动
        self.moveTimer.start(self.data["idle-move-time"])

    def stop(self) -> None:
        # 停止所有移动相关的定时器与状态
        self._moving = False
        self.step = 0
        self.dir = QPoint(0, 0)
        self.moveTimer.stop()
        self.stepTimer.stop()
        super().stop()
    
    def eventFilter(self, obj, event: QEvent) -> bool:
        if event.type() == QEvent.Type.MouseButtonPress:
            # 用户按下鼠标，立即终止自动移动
            self._stopMoving()
            # 不拦截事件，让其他插件（drag/stroke）继续处理
            return False
        return super().eventFilter(obj, event)
    
    def bind(self) -> None:
        def onStateChanged(prevState: str, state: str) -> None:
            if state != "idle":
                # 离开 idle 状态，停止移动与待机定时器
                self._stopMoving()
                self.moveTimer.stop()
            else:
                # 回到 idle 状态，如果不在移动中则重新启动待机定时器
                if not self._moving and not self.moveTimer.isActive():
                    self.moveTimer.start(self.data["idle-move-time"])
        
        # 配置待机触发定时器：单次触发
        self.moveTimer.setSingleShot(True)
        self.moveTimer.timeout.connect(self.moveRandomly)

        # 配置步进定时器：单次触发
        self.stepTimer.setSingleShot(True)
        self.stepTimer.timeout.connect(self.doStep)

        self.window.stateChanged.connect(onStateChanged)
        
        self.window.settingMenu.dataUpdated.connect(self.updateData)
    
    def loadData(self) -> None:
        if os.path.exists(f"{self.window.configManager.path}/config/move-randomly.json"):
            with open(f"{self.window.configManager.path}/config/move-randomly.json", "r", encoding = "utf-8") as f:
                self.data = json.load(f)
        else:
            with open(f"{self.window.configManager.path}/config/move-randomly.json", "w", encoding = "utf-8") as f:
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
    
    def _stopMoving(self) -> None:
        """终止当前移动并复位移动状态"""
        self._moving = False
        self.step = 0
        self.dir = QPoint(0, 0)
        self.stepTimer.stop()
    
    def _pickRandomDir(self) -> None:
        """随机生成一个非零方向"""
        self.dir = QPoint(0, 0)
        while self.dir.x() == 0 and self.dir.y() == 0:
            self.dir.setX(random.randint(-1, 1))
            self.dir.setY(random.randint(-1, 1))
    
    @Slot()
    def moveRandomly(self) -> None:
        """待机定时器触发，开始一次随机移动"""
        if self.window.state != "idle" or self._moving:
            return
        
        self.screenGeo = QApplication.primaryScreen().availableGeometry()
        
        self._pickRandomDir()
        self.step = random.randint(self.data["move-min-step"], self.data["move-max-step"])
        self._moving = True
        self.doStep()  # 开始第一步
    
    @Slot()
    def doStep(self) -> None:
        """执行单步移动"""
        # 移动结束或状态离开 idle
        if not self._moving or self.step <= 0 or self.window.state != "idle":
            self._moving = False
            self.step = 0
            self.stepTimer.stop()
            # 回到待机定时器，等待下一次随机移动
            if self.window.state == "idle" and not self.moveTimer.isActive():
                self.moveTimer.start(self.data["idle-move-time"])
            return
        
        width, height = self.window.width(), self.window.height()
        
        # 计算移动速度（斜向移动减速）
        speed = self.data["move-speed"] * (0.5 if self.dir.x() != 0 and self.dir.y() != 0 else 1)
        newX = self.window.x() + self.dir.x() * speed
        newY = self.window.y() + self.dir.y() * speed
        
        # 边界限制：将新位置限制在屏幕可用区域内
        minX = self.screenGeo.left()
        maxX = self.screenGeo.right() - width
        minY = self.screenGeo.top()
        maxY = self.screenGeo.bottom() - height
        
        clampedX = max(minX, min(newX, maxX))
        clampedY = max(minY, min(newY, maxY))
        
        # 判断是否撞到边界
        hitBoundary = (clampedX != newX) or (clampedY != newY)
        
        # 移动窗口到限制后的位置
        self.window.move(clampedX, clampedY)
        self.step -= 1
        
        if hitBoundary:
            # 撞到边界，本次移动提前结束
            self._moving = False
            self.step = 0
            self.stepTimer.stop()
            if self.window.state == "idle" and not self.moveTimer.isActive():
                self.moveTimer.start(self.data["idle-move-time"])
            return
        
        # 调度下一步
        self.stepTimer.start(self.data["move-step-time"])
    
    @Slot()
    def updateData(self) -> None:
        self.data = self.window.settingMenu.getPage("移动配置").getData()

        with open(f"{self.window.configManager.path}/config/move-randomly.json", "w", encoding = "utf-8") as f:
            json.dump(self.data, f, ensure_ascii = False, indent = 2)
