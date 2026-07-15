from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QStackedWidget, QSpacerItem, QFrame, QSizePolicy
)
from PySide6.QtCore import Signal, Slot, QObject

from tool.widgetFactory import SearchStackFactory

from window.manager.managerPage import ManagerPage

class SidebarButton(QPushButton):
    def __init__(self, text: str):
        super().__init__()
        self.setMinimumSize(60, 60)
        self.setMaximumSize(60, 60)
        self.setText(text)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1000, 600)
        self.mainLyt = QHBoxLayout()

        self.sbBtns: list[SidebarButton] = [] # 侧边栏按钮
        self.pages: list[SearchStackFactory] = [] # 页面

        self.sidebar = QFrame()
        self.stack = QStackedWidget()

        self.fields: list[tuple[SidebarButton, SearchStackFactory]] = [] # (sbBtn, page)

        self.initSidebar()
        self.initStack()

        self.setLayout(self.mainLyt)
    
    def initSidebar(self) -> None:
        self.sbLyt = QVBoxLayout()

        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #0098ff
            }
        """)
        texts = ["🐱", "🧩", "📄", "⚙"]
        
        for text in texts:
            if text == "⚙":
                self.sbLyt.addItem(QSpacerItem(60, 0, vData = QSizePolicy.Expanding))
            
            sbBtn = SidebarButton(text)
            self.sbBtns.append(sbBtn)
            self.sbLyt.addWidget(sbBtn)

        self.sidebar.setLayout(self.sbLyt)
        self.mainLyt.addWidget(self.sidebar)
    
    def initStack(self) -> None:
        self.pages.append(ManagerPage())
        
        for page in self.pages:
            page.build()
            self.stack.addWidget(page)
        self.mainLyt.addWidget(self.stack)
    
    def bind(self) -> None:
        for i in range(len(self.sbBtns)):
            self.fields.append((self.sbBtns[i], self.pages[i]))
            self.sbBtns[i].clicked.connect(lambda index = i: self.stack.setCurrentIndex(index))
