from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QGroupBox
from PySide6.QtGui import Qt, QAction

from datetime import datetime

from tool import data
from tool.data import LogType

class StateMenu(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("State Menu")
        self.resize(400, 300)

        self.lyt = QVBoxLayout()

        self.logLyt = QGroupBox("日志")
        self.logLyt.lyt = QVBoxLayout()

        self.logBox = QPlainTextEdit(readOnly = True)

        self.logLyt.lyt.addWidget(self.logBox)
        self.logLyt.setLayout(self.logLyt.lyt)
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
        with open(data.base["log-path"], "a", encoding = "utf-8") as f:
            f.write(logLine +  '\n')
