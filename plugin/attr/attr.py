from PySide6.QtWidgets import QWidget, QFormLayout, QProgressBar, QLabel
from PySide6.QtCore import Slot, QTimer

import json

from tool.plugin import Plugin

class Action(Plugin):
    def __init__(self):
        super().__init__()
        self.id = "attr"
        self.name = "Attributes"
        self.auto = True
        self.teardownImmed = False

        self.data: dict = {}
        self.settings: dict = {}
        self.strokeTimer: QTimer = QTimer()

        self.loadData()


    def setup(self, window) -> None:
        super().setup(window)
        self.bind()
        self.addPage()
    
    def stop(self):
        self.strokeTimer.stop()
        return super().stop()
    
    def teardown(self):
        self.strokeTimer.deleteLater()
        return super().teardown()
    
    def bind(self) -> None:
        self.window.aboutToQuit.connect(self.updateData)
        self.window.stateChanged.connect(self.onStateChanged)
        self.strokeTimer.timeout.connect(self.onStrokeTimeout)

    def loadData(self) -> None:
        with open("./plugin/attr/data.json", "r", encoding = "utf-8") as f:
            self.data = json.load(f)
        self.settings = self.data["settings"]
    
    def addPage(self) -> None:
        self.pg = QWidget()
        lyt = QFormLayout()
        
        self.pg.name = QLabel(self.data["name"])
        lyt.addRow("名称:", self.pg.name)
        fields = [
            ("饱食度", "satiety"),
            ("好感度", "fb")
        ]

        self.pg.bars = {}
        for name, key in fields:
            value = self.data[key]
            bar = QProgressBar(minimum = int(value["min"]), maximum = int(value["max"]), value = int(value["value"]))
            bar.setTextVisible(True)
            bar.setFormat(f"{value["min"]} / {value["value"]} / {value["max"]}")
            bar.setTextVisible(True)
            # 确保文本在任何主题下都可见
            bar.setStyleSheet("""
                QProgressBar {
                    color: #000000;
                }
            """)
            lyt.addRow(name, bar)
            self.pg.bars[key] = bar
        
        self.pg.setLayout(lyt)
        self.window.stateMenu.addPage(self.pg, "属性")
    
    @Slot(str, str)
    def onStateChanged(self, prevState: str, currentState: str) -> None:
        if prevState != "stroke" and currentState == "stroke":
            self.strokeTimer.start(self.data["settings"]["stroke"]["time"])
        elif currentState != "stroke":
            self.strokeTimer.stop()

    @Slot()
    def updateData(self) -> None:
        with open("./plugin/attr/data.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(self.data, ensure_ascii = False, indent = 2))
    
    @Slot()
    def onStrokeTimeout(self) -> None:
        fb = self.data["fb"]
        fb["value"] += self.settings["stroke"]["delta"]
        if fb["value"] >= self.data["fb"]["min"] and fb["value"] <= self.data["fb"]["max"]:
            self.pg.bars["fb"].setValue(fb["value"])
            self.pg.bars["fb"].setFormat(f"{fb["min"]} / {fb["value"]} / {fb["max"]}")
            self.data["fb"] = fb
