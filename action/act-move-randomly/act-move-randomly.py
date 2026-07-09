from PySide6.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit
from PySide6.QtCore import Slot, QEvent, QTimer, QPoint, QRect

import json
import random

from tool.plugin import Plugin

class Action(Plugin):
    def __init__(self):
        super().__init__()

        self.id = "act-move-randomly"
        self.auto = True
        
        self.moveTimer = QTimer() # 触发随机移动时间
        self.step = 0 # 移动步数
        self.dir = QPoint(0, 0) # 移动方向
        self.data: dict = {}

        self.loadData()
    
    def setup(self, window) -> None:
        super().setup(window)
        self.bind()
        self.addPage()
    
    def start(self) -> None:
        self.moveTimer.start(self.data["idle-move-time"])
        super().start()

    def eventFilter(self, obj, event: QEvent) -> None:
        if event.type() == QEvent.Type.MouseButtonPress:
            # 终止自动移动
            self.step = 0
            self.dir = QPoint(0, 0)
        return super().eventFilter(obj, event)
    
    def bind(self):
        def stopTimer(state: str) -> None:
            if state != "idle":
                self.moveTimer.stop()
            else:
                if not self.moveTimer.isActive():
                    self.moveTimer.start(self.data["idle-move-time"])
    
        self.moveTimer.timeout.connect(self.moveRandomly)
        self.window.stateChanged.connect(stopTimer)
        
        self.window.settingMenu.dataUpdated.connect(self.updateData)
    
    def loadData(self) -> None:
        with open("./action/act-move-randomly/data.json", "r", encoding = "utf-8") as f:
            self.data = json.load(f)

    def addPage(self) -> None:
        try:
            self.pg = QWidget()
            layout = QFormLayout()

            # 字段配置: (显示名称(label), 数据键(key), 是否整数(isInt))
            fields = [
                ("待机移动时间（毫秒）", "idle-move-time", True),
                ("移动最小步长", "move-min-step", True),
                ("移动最大步长", "move-max-step", True),
                ("移动步进时间（毫秒）", "move-step-time", True),
                ("移动速度（像素/步）", "move-speed", True),
            ]

            self.pg.edits = {}
            for label, key, isInt in fields:
                value = self.data[key]
                edit = QLineEdit(text = str(value) if isInt else value)
                layout.addRow(label, edit)
                self.pg.edits[key] = (edit, isInt)

            self.pg.setLayout(layout)
            self.window.settingMenu.addPage(self.pg, "移动配置")
        except Exception as e:
            print(e)
    @Slot()
    def moveRandomly(self) -> None:
        if self.window.state == "idle":
            self.moveTimer.stop()

            currentGeo = self.window.geometry()
            width, height = currentGeo.width(), currentGeo.height()

            self.dir = QPoint(0, 0)
            while self.dir.x() == 0 and self.dir.y() == 0:
                self.dir.setX(random.randint(-1, 1))
                self.dir.setY(random.randint(-1, 1))

            # 获取当前屏幕的可用区域（排除任务栏）
            screenGeo = QApplication.primaryScreen().availableGeometry()

            # 生成移动距离
            self.step = random.randint(self.data["move-min-step"], self.data["move-max-step"])

            self.moveWindow(width, height, screenGeo)

    @Slot(int, int, QRect)
    def moveWindow(self, width: int, height: int, screenGeo: QRect) -> None:
        if self.step > 0 and self.window.state == "idle":
            # 控制斜向移动与水平/竖直移动速度相同
            newX = self.window.x() + self.dir.x() * self.data["move-speed"] * (0.5 if self.dir.x() != 0 and self.dir.y() != 0 else 1)
            newY = self.window.y() + self.dir.y() * self.data["move-speed"] * (0.5 if self.dir.x() != 0 and self.dir.y() != 0 else 1)

            # 检查新位置是否在屏幕范围内
            if (screenGeo.left() <= newX <= screenGeo.right() - width) and (screenGeo.top() <= newY <= screenGeo.bottom() - height):
                self.window.move(newX, newY)
                self.step -= 1
            else:
                self.dir = QPoint(0, 0)
                while self.dir.x() == 0 and self.dir.y() == 0:
                    self.dir.setX(random.randint(-1, 1))
                    self.dir.setY(random.randint(-1, 1))
            QTimer.singleShot(self.data["move-step-time"], lambda: self.moveWindow(width, height, screenGeo))
        else:
            self.moveTimer.start(self.data["idle-move-time"])
    
    @Slot()
    def updateData(self) -> None:
        self.pg = self.window.settingMenu.getPage("移动配置")
        
        for key, v in self.pg.edits.items():
            edit, isInt = v
            self.data[key] = int(edit.text()) if isInt else edit.text()
        
        with open("./action/act-move-randomly/data.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(self.data, ensure_ascii = False, indent = 2))
