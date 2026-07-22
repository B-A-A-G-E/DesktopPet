from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QTextEdit, QListWidgetItem, QTabWidget, QFormLayout,
    QLabel, QMessageBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal, Slot, Qt
from QMarkdownView import MarkdownView

from typing import TYPE_CHECKING
import json
import subprocess
import sys
import os
import shutil

from tool.config import ConfigManager, LogType
from tool.widgetFactory import WidgetFactory, SearchStackFactory, ListBoxFactory, FormFactory, FormBoxFactory

from window.pet.petWindow import PetWindow

if TYPE_CHECKING:
    from window.manager.mainWindow import MainWindow

class ManagerPage(SearchStackFactory):
    saveError = Signal(str, str) # name, error
    launchError = Signal(str, str) # name, error
    delError = Signal(str, str) # name, error
    dataUpdated = Signal(str) # name
    updateCancelled = Signal(str) # name

    def __init__(self, mainWindow: "MainWindow"):
        super().__init__(None, None)
        
        self._mainWindow = mainWindow

        # 加载信息
        self._data: dict[str, dict] = {} # name, info
        self._petConfigs: dict[str, ConfigManager] = {}
        self._intro: dict[str, str] = {} # name, introduction
        for name, path in ConfigManager.pets.items():
            self._petConfigs[name] = ConfigManager(path)
            with open(f"{path}info.json", "r", encoding = "utf-8") as f:
                info = json.load(f)
                self._data[info["name"]] = info
            with open(f"{path}introduction.md", "r", encoding = "utf-8") as f:
                self._intro[name] = f.read()
        
        self.configPages: dict[str, tuple[QWidget, list[WidgetFactory], QPushButton, QPushButton]] = {} # name, (widget, [pages], applyBtn, cancelBtn)
        self.settingPages: dict[str, tuple[QPushButton, QPushButton]] = {} # name, (openBtn, delBtn)
        self.pages: dict[str, tuple[QListWidgetItem, QTextEdit, QTabWidget, QFormLayout]] = {} # name, (listItem, tabWidget, introPg, configPg, setPg)
        
        for k, v in self._data.items():
            listItem = QListWidgetItem(QPixmap(v["icon"]), v["name"])
            tabW = QTabWidget()
            
            introPg = MarkdownView() # page1 (介绍)
            introPg.setExtensions(["markdown.extensions.tables", "markdown.extensions.extra"])
            introPg.loadFinished.connect(lambda finished, name = k: introPg.setValue(self._intro[name]))
            
            configPg = self.initConfigPage(k) # page2 (配置)
            setPg = self.initSettingPage(k) # page3 (设置)
            
            tabW.addTab(introPg, "介绍")
            tabW.addTab(configPg, "配置")
            tabW.addTab(setPg, "设置")
            
            self.controller.addPage(tabW, listItem, k)

            self.pages[k] = (listItem, introPg, configPg, setPg)
        
        self.bind()
            
    def initConfigPage(self, name: str) -> QWidget:
        widget = QWidget()
        lyt = QVBoxLayout()
        tabW = QTabWidget()
        pages: list[WidgetFactory] = []
        
        # page1 (基础项)
        f1 = [
            ("日志保存路径", "log-path", "file"),
            ("对话面板最大显示问题数", "quesSelecter-item-count", "int"),
            ("待机判定时间（毫秒）", "idle-time", "int")
        ]
        pages.append(FormFactory(f1, self._petConfigs[name].base))
        pages[0].build()
        tabW.addTab(pages[0], "基础项")

        # page2 (动画)
        f2F = [
            ("路径", "path", "folder"),
            ("帧率", "fps", "int"),
            ("是否循环", "loop", "bool")
        ]
        f2 = [(key, key, f2F) for key in self._petConfigs[name].anime.keys()]
        pages.append(FormBoxFactory(f2, self._petConfigs[name].anime))
        pages[1].build()
        tabW.addTab(pages[1], "动画")

        # page3 (碰撞体)
        f3F = [
            ("左偏移量", "left", "int"),
            ("上偏移量", "top", "int"),
            ("宽度", "width", "int"),
            ("高度", "height", "int")
        ]
        f3 = [(key, key, f3F) for key in self._petConfigs[name].collision.keys()]
        pages.append(FormBoxFactory(f3, self._petConfigs[name].collision))
        pages[2].build()
        tabW.addTab(pages[2], "碰撞体")

        # page4 (状态反馈文本)
        f4 = [(key, key) for key in self._petConfigs[name].state.keys()]
        pages.append(ListBoxFactory(f4, self._petConfigs[name].state))
        pages[3].build()
        tabW.addTab(pages[3], "状态反馈文本")

        # page5 (对话文本)
        f5 = [(key, key) for key in self._petConfigs[name].dialog.keys()]
        pages.append(ListBoxFactory(f5, self._petConfigs[name].dialog))
        pages[4].build()
        tabW.addTab(pages[4], "对话文本")

        # page6 (插件状态)
        f6 = [(key, key, "bool") for key in self._petConfigs[name].pluginState.keys()]
        pages.append(FormFactory(f6, self._petConfigs[name].pluginState))
        pages[5].build()
        tabW.addTab(pages[5], "插件状态")
        
        btnLyt = QHBoxLayout()
        applyBtn = QPushButton("应用")
        cancelBtn = QPushButton("取消")
        btnLyt.addWidget(applyBtn)
        btnLyt.addWidget(cancelBtn)

        lyt.addWidget(tabW)
        lyt.addLayout(btnLyt)
        widget.setLayout(lyt)

        self.configPages[name] = (widget, pages, applyBtn, cancelBtn)

        return widget

    def initSettingPage(self, name: str) -> QWidget:
        widget = QWidget()
        lyt = QVBoxLayout()
        form = QFormLayout()
        
        info = self._data[name]
        form.addRow("名称:", QLabel(info["name"]))
        form.addRow("版本:", QLabel(info["version"]))
        authors: str = ""
        for author in info["author"]:
            authors += author + ", "
        form.addRow("作者:", QLabel(authors))

        openBtn = QPushButton("在文件资源管理器中打开")
        delBtn = QPushButton("删除桌宠")

        lyt.addLayout(form)
        lyt.addWidget(openBtn)
        lyt.addWidget(delBtn)
        widget.setLayout(lyt)
        
        self.settingPages[name] = (openBtn, delBtn)

        return widget
    
    def bind(self) -> None:
        for name, config in self._petConfigs.items():
            config.saveError.connect(lambda e, k = name: self.saveError.emit(k, e))
        
        for name, (_, _, applyBtn, cancelBtn) in self.configPages.items():        
            applyBtn.clicked.connect(lambda clicked, k = name: self.apply(k))
            cancelBtn.clicked.connect(lambda clicked, k = name: self.cancel(k))

        for name, (openBtn, delBtn) in self.settingPages.items():        
            openBtn.clicked.connect(lambda clicked, k = name: self.openPet(k))
            delBtn.clicked.connect(lambda clicked, k = name: self.delPet(k))
        
        self.list.itemDoubleClicked.connect(lambda item: self.launchPet(item.text()))
    
    @Slot(str)
    def apply(self, name: str) -> None:
        self._petConfigs[name].base = self.configPages[name][1][0].getData()
        self._petConfigs[name].anime = self.configPages[name][1][1].getData()
        self._petConfigs[name].collision = self.configPages[name][1][2].getData()
        self._petConfigs[name].state = self.configPages[name][1][3].getData()
        self._petConfigs[name].dialog = self.configPages[name][1][4].getData()
        self._petConfigs[name].pluginState = self.configPages[name][1][5].getData()

        self._petConfigs[name].saveConfig(ConfigManager.SaveMode.Common)
        
        self.dataUpdated.emit(name)

    @Slot(str)
    def cancel(self, name: str) -> None:
        self.configPages[name][1][0].setData(self._petConfigs[name].base)
        self.configPages[name][1][1].setData(self._petConfigs[name].anime)
        self.configPages[name][1][2].setData(self._petConfigs[name].collision)
        self.configPages[name][1][3].setData(self._petConfigs[name].state)
        self.configPages[name][1][4].setData(self._petConfigs[name].dialog)
        self.configPages[name][1][5].setData(self._petConfigs[name].pluginState)
        
        self.repaint()
        
        self.updateCancelled.emit(name)
    
    @Slot(str)
    def openPet(self, name: str) -> None:
        absPath = os.path.abspath(ConfigManager.pets[name])
        if sys.platform == 'win32': # Windows
            os.startfile(absPath)
        elif sys.platform == 'darwin': # MacOS
            subprocess.Popen(['open', absPath])
        else: # Linux
            subprocess.Popen(['xdg-open', absPath])

    @Slot(str)
    def delPet(self, name: str) -> None:
        from window.manager.mainWindow import MainWindow
        
        if MainWindow.getPet(name) is not None:
            QMessageBox.critical(self, "无法删除", f"有正在运行中的实例，请先关闭此桌宠的所有实例后再尝试删除", QMessageBox.StandardButton.Ok)
            return
        if QMessageBox.question(self, "确认操作",
            f"是否确认删除桌宠 \"{name}\"？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
            return
        try:
            absPath = os.path.abspath(ConfigManager.pets[name])

            # 从 UI中移除
            self.controller.removePage(name)

            # 从内存数据中移除
            if name in self._data:
                del self._data[name]
            if name in self._petConfigs:
                del self._petConfigs[name]
            if name in self._intro:
                del self._intro[name]
            if name in self.pages:
                del self.pages[name]
            if name in self.configPages:
                del self.configPages[name]
            if name in self.settingPages:
                del self.settingPages[name]
            
            # 从注册文件中移除
            with open("./pet/config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            
            if name in config:
                del config[name]
            
            with open("./pet/config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii = False, indent = 2)
            
            # 更新ConfigManager.pets
            ConfigManager.pets = config
            
            # 删除文件夹
            if os.path.exists(absPath) and os.path.isdir(absPath):
                shutil.rmtree(absPath)
            else:
                QMessageBox.warning(self, "警告", f"宠物文件夹 \"{absPath}\" 不存在或不是目录")
            
            # 7. 提示成功
            QMessageBox.information(self, "删除成功", f"桌宠 \"{name}\" 已成功删除")
        except Exception as e:
            print(e)
            self.delError.emit(name, e)

    @Slot(str)
    def launchPet(self, name: str) -> None:
        try:
            from window.manager.mainWindow import MainWindow
            pet = PetWindow(name, ConfigManager.pets[name])
            # 设置关闭时删除属性，确保窗口关闭时自动清理
            pet.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            pet.show()
            MainWindow.pets.append(pet)
            pet.stateMenu.log("Succeeded to entre", LogType.Entre)
        except Exception as e:
            print(e)
            self.launchError.emit(name, e)
