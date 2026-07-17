from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QGroupBox, QTabWidget
from PySide6.QtGui import Qt, QAction

from datetime import datetime

from tool.config import ConfigManager
from tool.config import LogType

class StateMenu(QWidget):
    def __init__(self, config: ConfigManager):
        super().__init__()
        
        self.setWindowTitle("State Menu")
        self.resize(400, 300)

        self.config = config

        self.pages: dict[str, QWidget] = {} # 插件传入的页面

        self.lyt = QVBoxLayout()
        self.tabW = QTabWidget()

        self.logBox = QPlainTextEdit(readOnly = True)

        self.lyt.addWidget(self.tabW)
        self.lyt.addWidget(self.logBox)
        self.setLayout(self.lyt)

        # logBox添加清空上下文菜单
        self.logBox.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.logBox.clearAct = QAction("清空")
        self.logBox.addAction(self.logBox.clearAct)

        self.bind()
    
    def bind(self) -> None:
        self.logBox.clearAct.triggered.connect(self.logBox.clear)
    
    def log(self, text: str, type: LogType = None) -> None:
        logLine = f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  {type}:    {text}"
        # 向logBox添加日志
        self.logBox.appendPlainText(logLine)
        # 写入日志文件
        with open(self.config.base["log-path"], "a", encoding = "utf-8") as f:
            f.write(logLine + '\n')
    
    def addPage(self, page: QWidget, label: str) -> None:
        self.pages[label] = page
        self.tabW.addTab(page, label)
    
    def getPage(self, label: str):
        return self.pages.get(label)
