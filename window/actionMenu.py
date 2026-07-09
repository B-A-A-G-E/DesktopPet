from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

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

        for k, v in self.petWindow.pluginManager.plugins.items():
            if v.auto:
                continue

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
        for k, v in self.petWindow.pluginManager.plugins.items():
            if not v.auto:
                self.actBtn[k].clicked.connect(lambda clicked, id = k: self.petWindow.startAct(id))

        def stopCurrentAct() -> None:
            if self.petWindow.currentAct:
                self.petWindow.stopCurrentAct()
        self.stopBtn.clicked.connect(stopCurrentAct)
