from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QTextEdit, QListWidgetItem, QTabWidget, QFormLayout,
    QLabel, QMessageBox, QMenu, QWidgetAction, QInputDialog
)
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Signal, Slot, Qt, QPoint
from QMarkdownView import MarkdownView

from typing import TYPE_CHECKING
import json
import subprocess
import sys
import os
import shutil

from tool.config import ConfigManager, scanPets
from tool.widgetFactory import WidgetFactory, SearchStackFactory, ListBoxFactory, FormFactory, FormBoxFactory

from window.pet.petWindow import PetWindow

if TYPE_CHECKING:
    from window.manager.mainWindow import MainWindow


class ManagerPage(SearchStackFactory):
    saveError = Signal(str, str)       # name, error
    launchError = Signal(str, str)     # name, error
    delError = Signal(str, str)        # name, error
    dataUpdated = Signal(str)          # name
    updateCancelled = Signal(str)      # name

    def __init__(self, mainWindow: "MainWindow"):
        super().__init__(None, None)

        self._mainWindow = mainWindow

        # 加载信息
        self._data: dict[str, dict] = {}                 # name -> info
        self._petConfigs: dict[str, ConfigManager] = {}  # name -> ConfigManager
        self._intro: dict[str, str] = {}                 # name -> introduction
        self.configPages: dict[str, tuple[QWidget, list[WidgetFactory], QPushButton, QPushButton]] = {}
        self.settingPages: dict[str, tuple[QPushButton, QPushButton]] = {}
        self.pages: dict[str, tuple[QListWidgetItem, QTextEdit, QTabWidget, QFormLayout]] = {}

        self._loadAll()
        self._bindPetSignals()

        # 列表项双击启动
        self.list.itemDoubleClicked.connect(lambda item: self.launchPet(item.text()))

        # 右键菜单
        self.list.list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list.list.customContextMenuRequested.connect(self.onContextMenu)

    # ========== 加载与绑定 ==========

    def _loadAll(self) -> None:
        """从 ConfigManager.pets 加载所有宠物并构建页面"""
        for name in ConfigManager.pets:
            path = "./pet/" + name
            try:
                self._petConfigs[name] = ConfigManager(name)
                with open(f"{path}/info.json", "r", encoding="utf-8") as f:
                    info = json.load(f)
                    self._data[name] = info
                with open(f"./temp/{info['temp']}/introduction.md", "r", encoding="utf-8") as f:
                    self._intro[name] = f.read()
            except Exception as e:
                print(f"failed to load pet {name}: {e}")
                self._petConfigs.pop(name, None)
                continue

        for k, v in self._data.items():
            listItem = QListWidgetItem(QPixmap(f"./temp/{v['temp']}/icon.png"), v["name"])
            tabW = QTabWidget()

            introPg = MarkdownView()
            introPg.setExtensions(["markdown.extensions.tables", "markdown.extensions.extra"])
            introPg.loadFinished.connect(lambda finished, name = k: introPg.setValue(self._intro[name]))

            configPg = self.initConfigPage(k)
            setPg = self.initSettingPage(k)

            tabW.addTab(introPg, "介绍")
            tabW.addTab(configPg, "配置")
            tabW.addTab(setPg, "设置")

            self.controller.addPage(tabW, listItem, k)

            self.pages[k] = (listItem, introPg, configPg, setPg)

    def _bindPetSignals(self) -> None:
        """为每个宠物的配置页按钮绑定信号"""
        for name, config in self._petConfigs.items():
            config.saveError.connect(lambda e, k = name: self.saveError.emit(k, e))

        for name, (_, _, applyBtn, cancelBtn) in self.configPages.items():
            applyBtn.clicked.connect(lambda clicked, k = name: self.apply(k))
            cancelBtn.clicked.connect(lambda clicked, k = name: self.cancel(k))

        for name, (openBtn, delBtn) in self.settingPages.items():
            openBtn.clicked.connect(lambda clicked, k = name: self.openPet(k))
            delBtn.clicked.connect(lambda clicked, k = name: self.delPet(k))

    def reload(self) -> None:
        """重新从磁盘加载宠物列表与配置，重建全部页面"""
        # 1. 清空现有 UI
        self.controller.clearAll()

        # 2. 清空内存数据
        self._data.clear()
        self._petConfigs.clear()
        self._intro.clear()
        self.configPages.clear()
        self.settingPages.clear()
        self.pages.clear()

        # 3. 重新加载
        self._loadAll()
        self._bindPetSignals()

    # ========== 配置页构建 ==========

    def initConfigPage(self, name: str) -> QWidget:
        widget = QWidget()
        lyt = QVBoxLayout()
        tabW = QTabWidget()
        pages: list[WidgetFactory] = []

        # page1 (基础项)
        f1 = [
            ("对话面板最大显示问题数", "quesSelecter-item-count", {"type": "int", "min": 1}),
            ("待机判定时间（毫秒）", "idle-time", {"type": "int", "min": 0})
        ]
        pages.append(FormFactory(f1, self._petConfigs[name].base))
        pages[0].build()
        tabW.addTab(pages[0], "基础项")

        # page2 (动画)
        f2F = [
            ("帧率", "fps", {"type": "int", "min": 1}),
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
        form.addRow("版本:", QLabel(str(info.get("version", ""))))
        authors: str = ""
        for author in info.get("author", []):
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

    # ========== 右键菜单 ==========

    @Slot(QPoint)
    def onContextMenu(self, pos: QPoint) -> None:
        """显示右键菜单"""
        item = self.list.list.itemAt(pos)
        if item is None:
            return

        name = item.text()
        if name not in self._data:
            return

        menu = QMenu(self)

        renameAct = QAction("重命名", self)
        renameAct.triggered.connect(lambda: self.renamePet(name))
        menu.addAction(renameAct)

        menu.addSeparator()

        # 红色删除项：QWidgetAction + QLabel
        delWidgetAct = QWidgetAction(menu)
        delLabel = QLabel("  删除桌宠")
        delLabel.setStyleSheet("color: red; padding: 4px 24px;")
        delLabel.setCursor(Qt.CursorShape.PointingHandCursor)
        delLabel.mousePressEvent = lambda e: (menu.close(), self.delPet(name))
        delWidgetAct.setDefaultWidget(delLabel)
        menu.addAction(delWidgetAct)

        menu.exec(self.list.list.mapToGlobal(pos))

    # ========== 重命名 ==========

    @Slot(str)
    def renamePet(self, oldName: str) -> None:
        from window.manager.mainWindow import MainWindow

        for pet in MainWindow.pets:
            if getattr(pet, "name", None) == oldName:
                QMessageBox.critical(
                    self, "无法重命名",
                    "有正在运行中的实例，请先关闭此桌宠的所有实例后再尝试重命名",
                    QMessageBox.StandardButton.Ok
                )
                return

        newName, ok = QInputDialog.getText(self, "重命名桌宠", "请输入新名称:", text=oldName)
        if not ok:
            return

        newName = newName.strip()
        if not newName:
            QMessageBox.warning(self, "警告", "名称不能为空")
            return
        if newName == oldName:
            return
        if os.path.exists(f"./pet/{newName}"):
            QMessageBox.warning(self, "警告", f"目录 \"./pet/{newName}\" 已存在，请使用其他名称")
            return

        oldPath = os.path.abspath(f"./pet/{oldName}")
        newPath = os.path.abspath(f"./pet/{newName}")

        try:
            os.rename(oldPath, newPath)

            # 更新 info.json 的 name 字段（可选，仅作显示）
            infoPath = os.path.join(newPath, "info.json")
            if os.path.exists(infoPath):
                with open(infoPath, "r", encoding="utf-8") as f:
                    info = json.load(f)
                info["name"] = newName
                with open(infoPath, "w", encoding="utf-8") as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)

            # 不再更新 ./pet/config.json，改为刷新缓存
            ConfigManager.pets = scanPets()   # 或直接 self.reload() 内部会重新读

            self.reload()
            QMessageBox.information(self, "重命名成功", f"桌宠已重命名为 \"{newName}\"")

        except Exception as e:
            print(e)
            try:
                if os.path.exists(newPath) and not os.path.exists(oldPath):
                    os.rename(newPath, oldPath)
            except Exception:
                pass
            QMessageBox.critical(self, "重命名失败", f"重命名桌宠失败：\n{e}")
    
    # ========== 配置应用/取消 ==========

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

    # ========== 打开 / 删除 ==========

    @Slot(str)
    def openPet(self, name: str) -> None:
        absPath = os.path.abspath(f"./pet/{name}")
        if sys.platform == 'win32':        # Windows
            os.startfile(absPath)
        elif sys.platform == 'darwin':     # MacOS
            subprocess.Popen(['open', absPath])
        else:                              # Linux
            subprocess.Popen(['xdg-open', absPath])

    @Slot(str)
    def delPet(self, name: str) -> None:
        from window.manager.mainWindow import MainWindow

        # 有运行中的实例时禁止删除
        for pet in MainWindow.pets:
            if getattr(pet, "name", None) == name:
                QMessageBox.critical(
                    self, "无法删除",
                    "有正在运行中的实例，请先关闭此桌宠的所有实例后再尝试删除",
                    QMessageBox.StandardButton.Ok
                )
                return
        if QMessageBox.question(
                self, "确认操作",
                f"是否确认删除桌宠 \"{name}\"？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
            return
        try:
            absPath = os.path.abspath(f"./pet/{name}")
            if os.path.exists(absPath) and os.path.isdir(absPath):
                shutil.rmtree(absPath)
            else:
                QMessageBox.warning(self, "警告", f"宠物文件夹 \"{absPath}\" 不存在或不是目录")

            # 不再更新 ./pet/config.json
            ConfigManager.pets = scanPets()
            self.reload()
            QMessageBox.information(self, "删除成功", f"桌宠 \"{name}\" 已成功删除")
        except Exception as e:
            print(e)
            self.delError.emit(name, e)
    
    # ========== 启动 ==========

    @Slot(str)
    def launchPet(self, name: str) -> None:
        try:
            from window.manager.mainWindow import MainWindow
            # 检查是否已有同名实例
            for pet in MainWindow.pets:
                if getattr(pet, "name", None) == name:
                    QMessageBox.critical(self, "桌宠正在运行", "已有正在运行的桌宠实例，请关闭后再试")
                    return
            pet = PetWindow(name)
            pet.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            pet.show()
            MainWindow.pets.append(pet)
        except Exception as e:
            print(e)
            self.launchError.emit(name, e)
