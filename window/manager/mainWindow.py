from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QStackedWidget, QSpacerItem, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt

from typing import TYPE_CHECKING

from tool.widgetFactory import SearchStackFactory

from window.pet.petWindow import PetWindow
from window.manager.managerPage import ManagerPage
from window.manager.pluginPage import PluginPage
from window.manager.docPage import DocPage
from window.manager.settingPage import SettingPage

if TYPE_CHECKING:
    from window.pet.petWindow import PetWindow

class SidebarButton(QPushButton):
    def __init__(self, text: str, toolTipText: str | None = None):
        super().__init__()
        self.setMinimumSize(60, 60)
        self.setMaximumSize(60, 60)
        self.setText(text)
        if toolTipText is not None:
            self.setToolTip(toolTipText)
        self.setStyleSheet("""
            QPushButton {
                font-size: 30px;
            }
            """)

class MainWindow(QWidget):
    pets: list["PetWindow"] = []

    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
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

        self.bind()
    
    def initSidebar(self) -> None:
        self.sbLyt = QVBoxLayout()

        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #0098ff
            }
        """)
        texts = [("🐱", "桌宠管理"), ("🧩", "插件管理"), ("📄", "文档查阅"), ("⚙", "管理器设置")]
        
        for text, toolTipText in texts:
            if text == "⚙":
                self.sbLyt.addItem(QSpacerItem(60, 0, vData = QSizePolicy.Expanding))
            
            sbBtn = SidebarButton(text, toolTipText)
            self.sbBtns.append(sbBtn)
            self.sbLyt.addWidget(sbBtn)

        self.sidebar.setLayout(self.sbLyt)
        self.mainLyt.addWidget(self.sidebar)
    
    def initStack(self) -> None:
        self.pages.append(ManagerPage(self))
        self.pages.append(PluginPage())
        self.pages.append(DocPage())
        self.pages.append(SettingPage())
        
        for page in self.pages:
            page.build()
            self.stack.addWidget(page)
        
        self.mainLyt.addWidget(self.stack)
    
    def bind(self) -> None:
        for i in range(len(self.sbBtns)):
            self.fields.append((self.sbBtns[i], self.pages[i]))
            self.sbBtns[i].clicked.connect(lambda clicked, index = i: self.stack.setCurrentIndex(index))
    
    def closeEvent(self, event) -> None:
        """管理器关闭时，关闭所有打开的宠物窗口"""
        for pet in MainWindow.pets[:]:
            pet.close()
        MainWindow.pets.clear()
        event.accept()
    
    @staticmethod
    def getPet(name: str) -> list["PetWindow"] | None:
        petList: list["PetWindow"] = []
        for pet in MainWindow.pets:
            if pet.name == name:
                petList.append(pet)
        return None if len(petList) == 0 else petList
