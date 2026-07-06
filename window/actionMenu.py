from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from tool import data

class ActionMenu(QWidget):
    def __init__(self, petWindow):
        super().__init__()
        
        self.resize(400, 300)

        self.petWindow = petWindow

        self.lyt = QVBoxLayout()
        self.actLyt = QVBoxLayout()
        self.hl = {}
        self.lb = {}
        self.actBtn = {}

        for k, v in self.petWindow.acts.items():
            self.hl[k] = QHBoxLayout()

            self.lb[k] = QLabel(v.name)
            self.lb[k].setToolTip(v.description)
            self.actBtn[k] = QPushButton("执行")
            
            self.hl[k].addWidget(self.lb[k])
            self.hl[k].addWidget(self.actBtn[k])
            self.actLyt.addLayout(self.hl[k])
        
        self.stopBtn = QPushButton("结束")

        self.lyt.addLayout(self.actLyt)
        self.lyt.addWidget(self.stopBtn)
        self.setLayout(self.lyt)

        self.bind()
    
    def bind(self) -> None:
        for k in self.petWindow.acts.keys():
            self.actBtn[k].clicked.connect(lambda clicked, id = k: self.petWindow.act(id))
        self.stopBtn.clicked.connect(self.petWindow.stopAct)
