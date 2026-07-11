from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton
from PySide6.QtCore import Signal

import json
from tool import data
from tool.data import LogType
from tool.pageFactory import PageFactory, FormFactory, FormBoxFactory, ListBoxFactory

class SettingMenu(QWidget):
    dataUpdated = Signal()
    updateCancelled = Signal()
    saveError = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Setting Menu")
        self.resize(600, 450)

        self.pages: list[PageFactory] = [] # 设置界面自带的页面
        self.otherPages: dict[str, QWidget] = {} # 插件传入的页面

        self.lyt = QVBoxLayout()
        self.tabW = QTabWidget()
        
        self.initPages()

        self.btnLyt = QHBoxLayout()
        self.applyBtn = QPushButton("应用")
        self.cancelBtn = QPushButton("取消")
        self.btnLyt.addWidget(self.applyBtn)
        self.btnLyt.addWidget(self.cancelBtn)

        self.lyt.addWidget(self.tabW)
        self.lyt.addLayout(self.btnLyt)
        self.setLayout(self.lyt)

        self.bind()

    def initPages(self) -> None:
        # page1 (基础项)
        f1 = [
            ("日志保存路径", "log-path", "file"),
            ("对话面板最大显示问题数", "quesSelecter-item-count", "int"),
            ("待机判定时间（毫秒）", "idle-time", "int")
        ]
        self.pages.append(FormFactory(f1, data.base))
        self.pages[0].build()
        self.tabW.addTab(self.pages[0], "基础项")

        # page2 (动画)
        f2F = [
            ("路径", "path", "folder"),
            ("帧率", "fps", "int"),
            ("是否循环", "loop", "bool")
        ]
        f2 = [(key, key, f2F) for key in data.anime.keys()]
        self.pages.append(FormBoxFactory(f2, data.anime))
        self.pages[1].build()
        self.tabW.addTab(self.pages[1], "动画")

        # page3 (碰撞体)
        f3F = [
            ("左偏移量", "left", "int"),
            ("上偏移量", "top", "int"),
            ("宽度", "width", "int"),
            ("高度", "height", "int")
        ]
        f3 = [(key, key, f3F) for key in data.collision.keys()]
        self.pages.append(FormBoxFactory(f3, data.collision))
        self.pages[2].build()
        self.tabW.addTab(self.pages[2], "碰撞体")

        # page4 (状态反馈文本)
        f4 = [(key, key) for key in data.state.keys()]
        self.pages.append(ListBoxFactory(f4, data.state))
        self.pages[3].build()
        self.tabW.addTab(self.pages[3], "状态反馈文本")

        # page5 (对话文本)
        f5 = [(key, key) for key in data.dialog.keys()]
        self.pages.append(ListBoxFactory(f5, data.dialog))
        self.pages[4].build()
        self.tabW.addTab(self.pages[4], "对话文本")

    def bind(self) -> None:
        self.applyBtn.clicked.connect(self.apply)
        self.cancelBtn.clicked.connect(self.cancel)
    
    def apply(self) -> None:
        data.base = self.pages[0].getData()
        data.anime = self.pages[1].getData()
        data.collision = self.pages[2].getData()
        data.state = self.pages[3].getData()
        data.dialog = self.pages[4].getData()

        try:
            with open("./data/base.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(data.base, ensure_ascii = False, indent = 2))
            with open("./data/anime.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(data.anime, ensure_ascii = False, indent = 2))
            with open("./data/collision.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(data.collision, ensure_ascii = False, indent = 2))
            with open("./data/state.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(data.state, ensure_ascii = False, indent = 2))
            with open("./data/dialog.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(data.dialog, ensure_ascii = False, indent = 2))
        except Exception as e:
            print(e)
            self.saveError.emit(e)
        
        self.dataUpdated.emit()

    def cancel(self) -> None:
        self.pages[0].setData(data.base)
        self.pages[1].setData(data.anime)
        self.pages[2].setData(data.collision)
        self.pages[3].setData(data.state)
        self.pages[4].setData(data.dialog)
        
        self.updateCancelled.emit()
        self.close()

    def addPage(self, page: QWidget, label: str) -> None:
        self.otherPages[label] = page
        self.tabW.addTab(page, label)
    
    def getPage(self, label: str) -> QWidget | None:
        """获取插件传入的页面"""
        return self.otherPages.get(label)
        