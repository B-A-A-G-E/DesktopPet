from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton
from PySide6.QtCore import Signal

from tool.config import ConfigManager
from tool.widgetFactory import WidgetFactory, FormFactory, FormBoxFactory, ListBoxFactory

class SettingMenu(QWidget):
    dataUpdated = Signal()
    updateCancelled = Signal()
    saveError = Signal(str)

    def __init__(self, config: ConfigManager):
        super().__init__()

        self.setWindowTitle("Setting Menu")
        self.resize(600, 450)

        self.config = config
        self.pages: list[WidgetFactory] = [] # 设置界面自带的页面
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
        self.pages.append(FormFactory(f1, self.config.base))
        self.pages[0].build()
        self.tabW.addTab(self.pages[0], "基础项")

        # page2 (动画)
        f2F = [
            ("路径", "path", "folder"),
            ("帧率", "fps", "int"),
            ("是否循环", "loop", "bool")
        ]
        f2 = [(key, key, f2F) for key in self.config.anime.keys()]
        self.pages.append(FormBoxFactory(f2, self.config.anime))
        self.pages[1].build()
        self.tabW.addTab(self.pages[1], "动画")

        # page3 (碰撞体)
        f3F = [
            ("左偏移量", "left", "int"),
            ("上偏移量", "top", "int"),
            ("宽度", "width", "int"),
            ("高度", "height", "int")
        ]
        f3 = [(key, key, f3F) for key in self.config.collision.keys()]
        self.pages.append(FormBoxFactory(f3, self.config.collision))
        self.pages[2].build()
        self.tabW.addTab(self.pages[2], "碰撞体")

        # page4 (状态反馈文本)
        f4 = [(key, key) for key in self.config.state.keys()]
        self.pages.append(ListBoxFactory(f4, self.config.state))
        self.pages[3].build()
        self.tabW.addTab(self.pages[3], "状态反馈文本")

        # page5 (对话文本)
        f5 = [(key, key) for key in self.config.dialog.keys()]
        self.pages.append(ListBoxFactory(f5, self.config.dialog))
        self.pages[4].build()
        self.tabW.addTab(self.pages[4], "对话文本")

    def bind(self) -> None:
        self.applyBtn.clicked.connect(self.apply)
        self.cancelBtn.clicked.connect(self.cancel)
        self.config.saveError.connect(self.saveError)
    
    def apply(self) -> None:
        self.config.base = self.pages[0].getData()
        self.config.anime = self.pages[1].getData()
        self.config.collision = self.pages[2].getData()
        self.config.state = self.pages[3].getData()
        self.config.dialog = self.pages[4].getData()

        self.config.saveConfig()
        
        self.dataUpdated.emit()
        self.close()

    def cancel(self) -> None:
        self.pages[0].setData(self.config.base)
        self.pages[1].setData(self.config.anime)
        self.pages[2].setData(self.config.collision)
        self.pages[3].setData(self.config.state)
        self.pages[4].setData(self.config.dialog)
        
        self.updateCancelled.emit()
        self.close()

    def addPage(self, page: QWidget, label: str) -> None:
        self.otherPages[label] = page
        self.tabW.addTab(page, label)
    
    def getPage(self, label: str) -> QWidget | None:
        """获取插件传入的页面"""
        return self.otherPages.get(label)
        