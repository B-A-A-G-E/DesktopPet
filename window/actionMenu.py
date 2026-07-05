from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QPushButton

from tool import data

class ActionMenu(QWidget):
    def __init__(self):
        super().__init__()
        
        self.resize(400, 300)

        self.lyt = QVBoxLayout()
        self.actLyt = QFormLayout()
        self.actBtn = {}

        for k, v in data.actPath.items():
            self.actBtn[k] = QPushButton("执行")
            self.actLyt.addRow(v["name"], self.actBtn[k])
        
        self.stopBtn = QPushButton("结束")

        self.lyt.addLayout(self.actLyt)
        self.lyt.addWidget(self.stopBtn)
        self.setLayout(self.lyt)
