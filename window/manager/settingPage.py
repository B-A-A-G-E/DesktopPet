from PySide6.QtWidgets import QWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Slot

from tool.config import ConfigManager
from tool.widgetFactory import SearchStackFactory, FormFactory

class SettingPage(SearchStackFactory):
    def __init__(self):
        super().__init__(None, None)

        widget = QWidget()
        lyt = QVBoxLayout()

        self.form = FormFactory([
                ("默认桌宠", "default-pet", "str"),
                ("控制器颜色主题", "manager-color-subject", "str"),
                ("开机自启动", "auto-start", "bool")
            ], ConfigManager.settings)
        self.form.build()
        
        btnLyt = QHBoxLayout()
        self.applyBtn = QPushButton("应用")
        self.cancelBtn = QPushButton("取消")
        btnLyt.addWidget(self.applyBtn)
        btnLyt.addWidget(self.cancelBtn)

        lyt.addWidget(self.form)
        lyt.addLayout(btnLyt)
        widget.setLayout(lyt)
        
        self.controller.addPage(widget, QListWidgetItem("管理器设置"), "manager")
        
        self.bind()
    
    def bind(self) -> None:
        self.applyBtn.clicked.connect(self.apply)
        self.cancelBtn.clicked.connect(self.cancel)

    @Slot()
    def apply(self) -> None:
        ConfigManager.settings = self.form.getData()
        ConfigManager.saveStaticConfigs()
    
    @Slot()
    def cancel(self) -> None:
        self.form.setData(ConfigManager.settings)
        
        self.repaint()
