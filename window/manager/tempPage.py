from PySide6.QtWidgets import (
    QWidget, QListWidgetItem, QTabWidget, QVBoxLayout,
    QDialog, QLineEdit, QPushButton, QHBoxLayout, QLabel,
    QMessageBox, QFormLayout, QMenu, QWidgetAction
)
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt, Slot, QPoint

from QMarkdownView import MarkdownView

import os
import json
import shutil

from tool.config import ConfigManager
from tool.widgetFactory import SearchStackFactory


class NameInputDialog(QDialog):
    """宠物命名对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("命名桌宠")
        self.resize(300, 120)

        self.lyt = QVBoxLayout()
        self.formLyt = QFormLayout()

        self.nameEdit = QLineEdit()
        self.nameEdit.setPlaceholderText("请输入桌宠名称")
        self.formLyt.addRow("名称:", self.nameEdit)

        self.btnLyt = QHBoxLayout()
        self.okBtn = QPushButton("确认")
        self.cancelBtn = QPushButton("取消")
        self.btnLyt.addWidget(self.okBtn)
        self.btnLyt.addWidget(self.cancelBtn)

        self.lyt.addLayout(self.formLyt)
        self.lyt.addLayout(self.btnLyt)
        self.setLayout(self.lyt)

        self.bind()

    def bind(self) -> None:
        self.okBtn.clicked.connect(self.onOk)
        self.cancelBtn.clicked.connect(self.reject)

    @Slot()
    def onOk(self) -> None:
        name = self.nameEdit.text().strip()
        if not name:
            QMessageBox.warning(self, "警告", "名称不能为空")
            return
        if name in ConfigManager.pets:
            QMessageBox.warning(self, "警告", f"桌宠 \"{name}\" 已存在，请使用其他名称")
            return
        if os.path.exists(f"./pet/{name}"):
            QMessageBox.warning(self, "警告", f"目录 \"./pet/{name}\" 已存在，请使用其他名称")
            return
        self.accept()

    def getName(self) -> str:
        return self.nameEdit.text().strip()


class TempPage(SearchStackFactory):
    def __init__(self, mainWindow=None):
        super().__init__(None, None)

        self._mainWindow = mainWindow

        self._data: dict[str, dict] = {}   # 模板目录名 -> info
        self._intro: dict[str, str] = {}   # 模板目录名 -> 介绍文档

        self.loadTemps()

        self.bind()

    def loadTemps(self) -> None:
        """加载 ./temp/ 下所有模板"""
        tempDir = "./temp"
        if not os.path.exists(tempDir):
            return

        for name in os.listdir(tempDir):
            tempPath = os.path.join(tempDir, name)
            if not os.path.isdir(tempPath):
                continue

            infoPath = os.path.join(tempPath, "info.json")
            introPath = os.path.join(tempPath, "introduction.md")

            if not os.path.exists(infoPath):
                continue

            try:
                with open(infoPath, "r", encoding="utf-8") as f:
                    info = json.load(f)
            except Exception as e:
                print(f"failed to load template info {name}: {e}")
                continue

            # 读取介绍文档
            if os.path.exists(introPath):
                with open(introPath, "r", encoding="utf-8") as f:
                    self._intro[name] = f.read()
            else:
                self._intro[name] = ""

            self._data[name] = info

            # 创建列表项
            iconPath = os.path.join(tempPath, "icon.png")
            if os.path.exists(iconPath):
                listItem = QListWidgetItem(QPixmap(iconPath), info.get("name", name))
            else:
                listItem = QListWidgetItem(info.get("name", name))
            listItem.setData(Qt.ItemDataRole.UserRole, name)  # 存储模板目录名

            # 创建详情页
            tabW = QTabWidget()

            introPg = MarkdownView()
            introPg.setExtensions(["markdown.extensions.tables", "markdown.extensions.extra"])
            introPg.loadFinished.connect(
                lambda finished, n=name: introPg.setValue(self._intro[n])
            )

            infoPg = self.initInfoPage(name)

            tabW.addTab(introPg, "介绍")
            tabW.addTab(infoPg, "信息")

            self.controller.addPage(tabW, listItem, name)

    def initInfoPage(self, name: str) -> QWidget:
        """创建模板信息页面"""
        widget = QWidget()
        lyt = QVBoxLayout()
        form = QFormLayout()

        info = self._data[name]
        form.addRow("名称:", QLabel(str(info.get("name", name))))
        form.addRow("版本:", QLabel(str(info.get("version", "未知"))))
        form.addRow("模板目录:", QLabel(name))

        authors = info.get("author", [])
        if isinstance(authors, list):
            authors = ", ".join(authors)
        form.addRow("作者:", QLabel(str(authors)))

        lyt.addLayout(form)
        lyt.addStretch()
        widget.setLayout(lyt)

        return widget

    def bind(self) -> None:
        self.list.itemDoubleClicked.connect(self.onItemDoubleClicked)
        # 右键菜单
        self.list.list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list.list.customContextMenuRequested.connect(self.onContextMenu)

    def refreshManager(self) -> None:
        """通知主窗口中的各页刷新"""
        if self._mainWindow is None:
            return
        for page in getattr(self._mainWindow, "pages", []):
            if hasattr(page, "reload"):
                try:
                    page.reload()
                except Exception as e:
                    print(f"failed to reload page: {e}")

    # ========== 右键菜单 ==========

    @Slot(QPoint)
    def onContextMenu(self, pos: QPoint) -> None:
        """显示右键菜单"""
        item = self.list.list.itemAt(pos)
        if item is None:
            return

        tempName = item.data(Qt.ItemDataRole.UserRole)
        if tempName is None:
            return

        menu = QMenu(self)

        instantiateAct = QAction("实例化", self)
        instantiateAct.triggered.connect(lambda: self.instantiatePet(tempName))
        menu.addAction(instantiateAct)

        menu.addSeparator()

        # 红色删除项：QWidgetAction + QLabel
        delWidgetAct = QWidgetAction(menu)
        delLabel = QLabel("  删除模板")
        delLabel.setStyleSheet("color: red; padding: 4px 24px;")
        delLabel.setCursor(Qt.CursorShape.PointingHandCursor)
        delLabel.mousePressEvent = lambda e: (menu.close(), self.deleteTemp(tempName))
        delWidgetAct.setDefaultWidget(delLabel)
        menu.addAction(delWidgetAct)

        menu.exec(self.list.list.mapToGlobal(pos))

    # ========== 双击实例化 ==========

    @Slot(QWidget)
    def onItemDoubleClicked(self, item: QListWidgetItem) -> None:
        """双击列表项，实例化宠物"""
        tempName = item.data(Qt.ItemDataRole.UserRole)
        if tempName is None:
            return
        self.instantiatePet(tempName)

    # ========== 实例化 ==========

    def instantiatePet(self, tempName: str) -> None:
        """实例化宠物：复制模板资源到 ./pet/ 下"""
        dialog = NameInputDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        name = dialog.getName()
        tempPath = os.path.join("./temp", tempName)
        petPath = os.path.join("./pet", name)

        try:
            os.makedirs(petPath, exist_ok=True)

            # 复制 info.json
            infoSrc = os.path.join(tempPath, "info.json")
            infoDst = os.path.join(petPath, "info.json")
            if os.path.exists(infoSrc):
                shutil.copy2(infoSrc, infoDst)

            # 复制 config/
            configSrc = os.path.join(tempPath, "config")
            configDst = os.path.join(petPath, "config")
            if os.path.exists(configSrc):
                shutil.copytree(configSrc, configDst, dirs_exist_ok=True)

            # 写入 name 与 temp 字段到 info.json
            if os.path.exists(infoDst):
                with open(infoDst, "r", encoding="utf-8") as f:
                    info = json.load(f)
                info["name"] = name
                info["temp"] = tempName   # 记录来源模板，供删除模板时查找实例
                with open(infoDst, "w", encoding="utf-8") as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)

            # 新建 log.log
            logPath = os.path.join(petPath, "log.log")
            with open(logPath, "w", encoding="utf-8") as f:
                pass

            # 注册到 ./pet/config.json（列表结构）
            with open("./pet/config.json", "r", encoding="utf-8") as f:
                petsConfig = json.load(f)

            if name not in petsConfig:
                petsConfig.append(name)

            with open("./pet/config.json", "w", encoding="utf-8") as f:
                json.dump(petsConfig, f, ensure_ascii=False, indent=2)

            ConfigManager.pets = petsConfig

            # 通知管理器刷新
            self.refreshManager()

            QMessageBox.information(self, "实例化成功", f"桌宠 \"{name}\" 已成功创建")

        except Exception as e:
            print(e)
            QMessageBox.critical(self, "实例化失败", f"创建桌宠 \"{name}\" 失败：\n{e}")
            if os.path.exists(petPath):
                shutil.rmtree(petPath, ignore_errors=True)

    # ========== 删除模板 ==========

    def findInstances(self, tempName: str) -> list[str]:
        """查找使用指定模板的所有宠物实例名"""
        instances: list[str] = []
        for petName in ConfigManager.pets:
            infoPath = f"./pet/{petName}/info.json"
            if not os.path.exists(infoPath):
                continue
            try:
                with open(infoPath, "r", encoding="utf-8") as f:
                    info = json.load(f)
            except Exception:
                continue
            if info.get("temp") == tempName:
                instances.append(petName)
        return instances

    def deleteTemp(self, tempName: str) -> None:
        """删除模板（及其所有实例）"""
        instances = self.findInstances(tempName)
        tempPath = os.path.join("./temp", tempName)

        if instances:
            # 有实例，询问是否删除所有实例
            reply = QMessageBox.question(
                self, "确认删除",
                f"模板 \"{tempName}\" 当前有以下 {len(instances)} 个实例：\n"
                f"{', '.join(instances)}\n\n"
                f"是否删除所有实例及模板？\n"
                f"（选择\"No\"将不做任何操作）",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return  # 取消：不做任何操作

            # 确定：先删除所有实例
            try:
                # 从注册表中移除
                with open("./pet/config.json", "r", encoding="utf-8") as f:
                    petsConfig = json.load(f)

                for instName in instances:
                    if instName in petsConfig:
                        petsConfig.remove(instName)

                with open("./pet/config.json", "w", encoding="utf-8") as f:
                    json.dump(petsConfig, f, ensure_ascii=False, indent=2)

                ConfigManager.pets = petsConfig

                # 删除实例目录
                for instName in instances:
                    instPath = f"./pet/{instName}"
                    if os.path.exists(instPath):
                        shutil.rmtree(instPath, ignore_errors=True)

            except Exception as e:
                print(e)
                QMessageBox.critical(self, "删除失败", f"删除实例失败：\n{e}")
                return
        else:
            # 无实例，确认删除模板
            reply = QMessageBox.question(
                self, "确认删除",
                f"是否确认删除模板 \"{tempName}\"？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        # 删除模板目录
        try:
            if os.path.exists(tempPath):
                shutil.rmtree(tempPath, ignore_errors=True)

            # 从 UI 中移除
            self.controller.removePage(tempName)

            # 从内存数据中移除
            self._data.pop(tempName, None)
            self._intro.pop(tempName, None)

            # 通知管理器刷新
            self.refreshManager()

            QMessageBox.information(self, "删除成功", f"模板 \"{tempName}\" 已成功删除")
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "删除失败", f"删除模板失败：\n{e}")
