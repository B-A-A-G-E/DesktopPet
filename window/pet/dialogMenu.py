from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QTextEdit
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal, Slot

import random

from tool.config import ConfigManager
from tool import conv

class DialogMenu(QWidget):
    def __init__(self, petWindow):
        super().__init__()

        self.setWindowTitle("Dialog Menu")
        self.resize(400, 200)

        self._petWindow = petWindow
        
        self.lyt = QVBoxLayout()
        self.sendLyt = QHBoxLayout()

        self.quesSelecter = QComboBox()
        self.sendBtn = QPushButton("发送")
        self.sendLyt.addWidget(self.quesSelecter)
        self.sendLyt.addWidget(self.sendBtn)

        self.replyBox = QTextEdit(readOnly = True, placeholderText = "The pet will reply here.")
        
        self.lyt.addLayout(self.sendLyt)
        self.lyt.addWidget(self.replyBox)
        self.setLayout(self.lyt)

        # replyBox添加清空上下文菜单
        self.replyBox.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.replyBox.clearAct = QAction("清空")
        self.replyBox.addAction(self.replyBox.clearAct)
        
        self.resetQuesSelecter()
        
        self.bind()

    def bind(self) -> None:
        self.sendBtn.clicked.connect(self.reply)
        self.replyBox.clearAct.triggered.connect(self.replyBox.clear)
    
    def resetQuesSelecter(self) -> None:
        """重置quesSelect"""
        self.quesSelecter.clear()
        vals = list(self._petWindow.configManager.dialog.keys())
        result = random.sample(vals, min(self._petWindow.configManager.base["quesSelecter-item-count"], len(vals)))
        for item in result:
            self.quesSelecter.addItem(item)

    def addLine(self, content: str) -> None:
        if content != "":
            self.replyBox.setText(self.replyBox.toPlainText() + '\n' + content)
    
    @Slot()
    def reply(self) -> None:
        question = self.quesSelecter.currentText()
        reply = conv.replyText("dialog", question, self._petWindow.configManager)
        self.replyBox.append("\nQ: " + question + "\nA: " + reply) # 写入replyBox
        self._petWindow.replyed.emit("dialog", question, reply)
        self.quesSelecter.removeItem(self.quesSelecter.findText(question)) # 删除用过的问题
        # 添加未使用的新问题（包括刚才quesSelecter移除的）
        vals = list(self._petWindow.configManager.dialog.keys())
        using = [self.quesSelecter.itemText(i) for i in range(self.quesSelecter.count())]
        dif = [i for i in vals if i not in using]
        self.quesSelecter.addItem(dif[random.randint(0, len(dif) - 1)])
