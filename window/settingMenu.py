from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QTabWidget, QToolBox, QLineEdit, QPushButton, QCheckBox, QMessageBox
from PySide6.QtCore import Signal

import json
from tool import data

class PageFactory():
    @staticmethod
    def createPage(dataDict: dict, tabWidget: QTabWidget, tabName: str, addBtnText: str = "新建项"):
        """创建可编辑列表页面"""
        widget = QWidget()
        layout = QVBoxLayout()
        box = QToolBox()

        items = {}
        for k, v in dataDict.items():
            pageWidget = QWidget()
            container = QVBoxLayout()

            rows = []
            for i, text in enumerate(v):
                rowLayout = QHBoxLayout()
                textEdit = QLineEdit(text)
                removeBtn = QPushButton("移除")

                rowLayout.addWidget(textEdit)
                rowLayout.addWidget(removeBtn)
                container.addLayout(rowLayout)

                rows.append({
                    "text": textEdit,
                    "remove": removeBtn,
                    "layout": rowLayout  # 保存布局引用
                })

            addBtn = QPushButton(addBtnText)
            container.addWidget(addBtn)

            pageWidget.setLayout(container)
            box.addItem(pageWidget, k)

            items[k] = {
                "rows": rows,
                "add": addBtn,
                "container": container  # 保存容器布局引用
            }

        layout.addWidget(box)
        widget.setLayout(layout)
        tabWidget.addTab(widget, tabName)

        return widget, items

class SettingMenu(QWidget):
    dataUpdated = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Setting Menu")
        self.resize(600, 450)

        self.otherPages: dict[str, QWidget] = {} # 插件传入的页面

        self.lyt = QVBoxLayout()
        self.tabW = QTabWidget()

        # 初始化所有页面
        self.initPage1()
        self.initPage2()
        self.initPage3()
        self.initPage4()
        self.initPage5()

        self.applyBtn = QPushButton("应用")
        self.cancelBtn = QPushButton("取消")

        self.lyt.addWidget(self.tabW)
        self.lyt.addWidget(self.applyBtn)
        self.lyt.addWidget(self.cancelBtn)
        self.setLayout(self.lyt)

        self.bind()

    def initPage1(self) -> None:
        """初始化page1（基础项）"""
        self.pg1 = QWidget()
        layout = QFormLayout()

        # 字段配置: (显示名称, 数据键, 是否整数)
        fields = [
            ("日志保存路径", "log-path", False),
            ("询问框最大问题数", "quesSelecter-item-count", True),
            ("待机判定时间（毫秒）", "idle-time", True)
        ]

        self.pg1.edits = {}
        for label, key, isInt in fields:
            value = data.base[key]
            edit = QLineEdit(text = str(value) if isInt else value)
            layout.addRow(label, edit)
            self.pg1.edits[key] = (edit, isInt)

        self.pg1.setLayout(layout)
        self.tabW.addTab(self.pg1, "基础项")

    def initPage2(self) -> None:
        """初始化page2（动画）"""
        self.pg2 = QWidget()
        layout = QVBoxLayout()
        box = QToolBox()

        self.pg2.items = {}
        for k, v in data.anime.items():
            widget = QWidget()
            form = QFormLayout()

            pathEdit = QLineEdit(v["path"])
            fpsEdit = QLineEdit(str(v["fps"]))
            loopCheck = QCheckBox("")
            loopCheck.setChecked(v["loop"])

            form.addRow("Path:", pathEdit)
            form.addRow("Fps:", fpsEdit)
            form.addRow("Loop:", loopCheck)
            widget.setLayout(form)
            box.addItem(widget, k)

            self.pg2.items[k] = {
                "path": pathEdit,
                "fps": fpsEdit,
                "loop": loopCheck
            }

        layout.addWidget(box)
        self.pg2.setLayout(layout)
        self.tabW.addTab(self.pg2, "动画")

    def initPage3(self) -> None:
        """初始化page3（碰撞体）"""
        self.pg3 = QWidget()
        layout = QVBoxLayout()
        box = QToolBox()

        self.pg3.items = {}
        for k, v in data.collision.items():
            widget = QWidget()
            form = QFormLayout()

            leftEdit = QLineEdit(str(v["left"]))
            topEdit = QLineEdit(str(v["top"]))
            widthEdit = QLineEdit(str(v["width"]))
            heightEdit = QLineEdit(str(v["height"]))

            form.addRow("Left:", leftEdit)
            form.addRow("Top:", topEdit)
            form.addRow("Width:", widthEdit)
            form.addRow("Height:", heightEdit)
            widget.setLayout(form)
            box.addItem(widget, k)

            self.pg3.items[k] = {
                "left": leftEdit,
                "top": topEdit,
                "width": widthEdit,
                "height": heightEdit
            }

        layout.addWidget(box)
        self.pg3.setLayout(layout)
        self.tabW.addTab(self.pg3, "碰撞体")

    def initPage4(self) -> None:
        self.pg4, self.pg4.items = PageFactory.createPage(
            data.state, self.tabW, "状态反馈文本", "新建回复"
        )

    def initPage5(self) -> None:
        self.pg5, self.pg5.items = PageFactory.createPage(
            data.dialog, self.tabW, "对话文本", "新建对话"
        )

    def bind(self) -> None:
        """绑定信号和槽"""
        # 应用&取消按钮
        self.applyBtn.clicked.connect(self.apply)
        self.cancelBtn.clicked.connect(self.cancel)

        # 绑定page4的动态按钮
        for k, item in self.pg4.items.items():
            # 绑定移除按钮
            for rowIdx, row in enumerate(item["rows"]):
                row["remove"].clicked.connect(
                    lambda clicked, key=k, idx=rowIdx: self.removeStateRow(key, idx)
                )
            # 绑定添加按钮
            item["add"].clicked.connect(
                lambda clicked, key=k: self.addStateRow(key)
            )

        # 绑定page5的动态按钮
        for k, item in self.pg5.items.items():
            for rowIdx, row in enumerate(item["rows"]):
                row["remove"].clicked.connect(
                    lambda clicked, key=k, idx=rowIdx: self.removeDialogRow(key, idx)
                )
            item["add"].clicked.connect(
                lambda clicked, key=k: self.addDialogRow(key)
            )

    def removeStateRow(self, key: str, idx: int) -> None:
        """移除反应文本的一行"""
        item = self.pg4.items[key]
        rows = item["rows"]
        
        # 检查索引是否有效，并且至少保留一行
        if idx < 0 or idx >= len(rows) or len(rows) <= 1:
            QMessageBox.critical(self, "Row Too Few", "Every state must have at least 1 response.", QMessageBox.StandardButton.Ok)
            return
        
        # 获取要删除的行数据
        rowData = rows.pop(idx)
        
        # 从容器布局中移除该行（传入布局对象本身）
        container = item["container"]
        rowLayout = rowData["layout"]
        
        # 清空布局中的控件
        self.clearLayout(rowLayout)
        # 从容器中移除该布局
        container.removeItem(rowLayout)
        
        # 更新所有剩余行的移除按钮绑定
        self.rebindRemoveButtons(key, "state")

    def addStateRow(self, key: str) -> None:
        """为反应文本添加新行"""
        item = self.pg4.items[key]
        container = item["container"]
        # 在"新建回复"按钮前插入（按钮在最后）
        addBtnIndex = container.count() - 1

        rowLayout = QHBoxLayout()
        textEdit = QLineEdit("")
        removeBtn = QPushButton("移除")

        rowLayout.addWidget(textEdit)
        rowLayout.addWidget(removeBtn)

        container.insertLayout(addBtnIndex, rowLayout)

        # 存储新行
        newRow = {"text": textEdit, "remove": removeBtn, "layout": rowLayout}
        item["rows"].append(newRow)

        # 重新绑定所有移除按钮（包括新添加的）
        self.rebindRemoveButtons(key, "state")

    def removeDialogRow(self, key: str, idx: int) -> None:
        """移除对话文本的一行"""
        item = self.pg5.items[key]
        rows = item["rows"]
        
        # 检查索引是否有效，并且至少保留一行
        if idx < 0 or idx >= len(rows) or len(rows) <= 1:
            QMessageBox.critical(self, "Row Too Few", "Every question must have at least 1 answer.", QMessageBox.StandardButton.Ok)
            return
        
        # 获取要删除的行数据
        rowData = rows.pop(idx)
        
        # 从容器布局中移除该行
        container = item["container"]
        rowLayout = rowData["layout"]
        
        # 清空布局中的控件
        self.clearLayout(rowLayout)
        # 从容器中移除该布局
        container.removeItem(rowLayout)
        
        # 更新所有剩余行的移除按钮绑定
        self.rebindRemoveButtons(key, "dialog")

    def addDialogRow(self, key: str) -> None:
        """为对话文本添加新行"""
        item = self.pg5.items[key]
        container = item["container"]
        # 在"新建对话"按钮前插入
        addBtnIndex = container.count() - 1

        rowLayout = QHBoxLayout()
        textEdit = QLineEdit("")
        removeBtn = QPushButton("移除")

        rowLayout.addWidget(textEdit)
        rowLayout.addWidget(removeBtn)

        container.insertLayout(addBtnIndex, rowLayout)

        newRow = {"text": textEdit, "remove": removeBtn, "layout": rowLayout}
        item["rows"].append(newRow)

        # 重新绑定所有移除按钮
        self.rebindRemoveButtons(key, "dialog")

    def rebindRemoveButtons(self, key: str, pageType: str) -> None:
        """重新绑定指定key的所有移除按钮"""
        if pageType == "state":
            item = self.pg4.items[key]
        else:  # dialog
            item = self.pg5.items[key]
        
        rows = item["rows"]
        for idx, row in enumerate(rows):
            # 断开所有已有连接
            try:
                row["remove"].clicked.disconnect()
            except RuntimeError:
                pass  # 如果没有连接则忽略
            
            # 重新绑定
            if pageType == "state":
                row["remove"].clicked.connect(
                    lambda checked, k=key, i=idx: self.removeStateRow(k, i)
                )
            else:
                row["remove"].clicked.connect(
                    lambda checked, k=key, i=idx: self.removeDialogRow(k, i)
                )

    def clearLayout(self, layout) -> None:
        """清空布局中的所有控件"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
            # 删除布局本身
            layout.deleteLater()

    def apply(self) -> None:
        # 更新数据
        # page1
        for key, (edit, isInt) in self.pg1.edits.items():
            value = int(edit.text()) if isInt else edit.text()
            data.base[key] = value

        # page2
        for k in data.anime.keys():
            data.anime[k]["path"] = self.pg2.items[k]["path"].text()
            data.anime[k]["fps"] = int(self.pg2.items[k]["fps"].text())
            data.anime[k]["loop"] = self.pg2.items[k]["loop"].isChecked()

        # page3
        for k in data.collision.keys():
            data.collision[k]["left"] = int(self.pg3.items[k]["left"].text())
            data.collision[k]["top"] = int(self.pg3.items[k]["top"].text())
            data.collision[k]["width"] = int(self.pg3.items[k]["width"].text())
            data.collision[k]["height"] = int(self.pg3.items[k]["height"].text())

        # page4
        for k in data.state.keys():
            data.state[k] = [row["text"].text() for row in self.pg4.items[k]["rows"]]

        # page5
        for k in data.dialog.keys():
            data.dialog[k] = [row["text"].text() for row in self.pg5.items[k]["rows"]]

        # 保存数据
        with open("./data/base.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(data.base, ensure_ascii = False, indent = 2))
        with open("./data/anime.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(data.anime, ensure_ascii = False, indent = 2))
        with open("./data/collision.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(data.collision, ensure_ascii = False, indent = 2))
        with open("./data/state.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(data.state, ensure_ascii = False, indent = 2))
        with open("./data/dialog.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(data.dialog, ensure_ascii = False, indent = 2))

        self.dataUpdated.emit()
        self.close()

    def cancel(self) -> None:
        self.close()

    def addPage(self, page: QWidget, label: str) -> None:
        self.otherPages[label] = page
        self.tabW.addTab(page, label)
    
    def getPage(self, label: str) -> QWidget | None:
        """获取插件传入的页面"""
        return self.otherPages.get(label)
        