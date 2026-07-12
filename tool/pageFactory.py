from PySide6.QtWidgets import (
    QWidget, QLayout, QVBoxLayout, QHBoxLayout, QFormLayout,
    QToolBox, QLineEdit, QPushButton, QCheckBox, QSpinBox,
    QDoubleSpinBox, QFileDialog
)
from PySide6.QtCore import Signal, Slot

from typing import Any

def deleteLyt(lyt: QLayout) -> None:
    """
    递归删除布局及其所有子控件和子布局。

    该函数会遍历布局中的所有项，如果是控件则调用 deleteLater() 标记删除，
    如果是子布局则递归调用 deleteLyt() 进行深度清理，最后将布局自身标记删除。

    参数:
        lyt: 要删除的 QLayout 对象
    """
    if lyt is not None:
        while lyt.count():
            item = lyt.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                deleteLyt(item.layout())
        lyt.deleteLater()

def clearLyt(lyt: QLayout) -> None:
    """
    清空布局中的所有子项（控件或子布局）。

    与 deleteLyt 类似，但不删除布局本身，仅移除并删除其所有子项。
    适用于需要重用布局对象但清空其内容的场景。

    参数:
        lyt: 要清空的 QLayout 对象
    """
    while lyt.count():
        item = lyt.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
        elif item.layout():
            deleteLyt(item.layout())

def getVal(edit: Any, dataType: str) -> Any:
    """
    根据数据类型从编辑控件中提取值。

    支持的数据类型:
        - "bool": 从 QCheckBox 获取选中状态
        - "int"/"float": 从 QSpinBox/QDoubleSpinBox 获取数值
        - "str": 从 QLineEdit 获取文本
        - "file"/"folder": 从 FileSelecter 获取路径

    参数:
        edit: 编辑控件实例
        dataType: 数据类型字符串

    返回:
        提取出的值，类型根据 dataType 而定

    异常:
        TypeError: 当 dataType 不在支持列表中时抛出
    """
    match dataType:
        case "bool":
            return edit.isChecked()
        case "int" | "float":
            return edit.value()
        case "str":
            return edit.text()
        case "file" | "folder":
            return edit.getFile()
        case _:
            raise TypeError(f"invalid type: {dataType}")

def setVal(edit: Any, dataType: str, val: Any) -> None:
    """
    根据数据类型将值设置到编辑控件中。

    支持的数据类型及对应的设置方式同 getVal()。

    参数:
        edit: 编辑控件实例
        dataType: 数据类型字符串
        val: 要设置的值，类型需与 dataType 匹配

    异常:
        TypeError: 当 dataType 不在支持列表中时抛出
    """
    match dataType:
        case "bool":
            edit.setChecked(val)
        case "int" | "float":
            edit.setValue(val)
        case "str":
            edit.setText(val)
        case "file" | "folder":
            edit.setFile(val)
        case _:
            raise TypeError(f"invalid type: {dataType}")

def createEdit(dataType: str) -> QWidget | None:
    """
    根据数据类型工厂方法，创建对应的编辑器控件。

    参数:
        dataType: 数据类型字符串，支持 "bool", "int", "float", "str", "file", "folder"

    返回:
        对应类型的 QWidget 子类实例，若类型不支持则返回 None
    """
    edit = None
    match dataType:
        case "bool":
            edit = QCheckBox()
        case "int":
            edit = QSpinBox()
            edit.setRange(-99999, 99999)
        case "float":
            edit = QDoubleSpinBox()
            edit.setRange(-99999, 99999)
        case "str":
            edit = QLineEdit()
        case "file":
            edit = FileSelecter("file")
        case "folder":
            edit = FileSelecter("folder")
    return edit

class FileSelecter(QWidget):
    """
    文件/文件夹选择器控件。

    组合了一个 QLineEdit 用于显示路径，和一个按钮用于触发文件对话框。
    支持文件选择和文件夹选择两种模式。
    """
    textChanged = Signal(str)  # 当路径文本发生变化时发送信号

    def __init__(self, mode: str = "file"):
        """
        初始化文件选择器。

        参数:
            mode: 选择模式，"file" 表示文件选择，"folder" 表示文件夹选择
        """
        super().__init__()
        self.edit = QLineEdit()
        self.btn = QPushButton("📁")
        self.lyt = QHBoxLayout()
        self.mode = mode

        self.lyt.addWidget(self.edit)
        self.lyt.addWidget(self.btn)
        self.setLayout(self.lyt)

        self.bind()

    def bind(self) -> None:
        """绑定信号与槽，连接按钮点击事件到文件对话框。"""
        self.edit.textChanged.connect(self.textChanged)
        if self.mode == "file":
            self.btn.clicked.connect(lambda: self.edit.setText(
                QFileDialog.getOpenFileName(self, "选择文件", ".", "所有文件(*);;JSON(*.json)")[0]
            ))
        elif self.mode == "folder":
            self.btn.clicked.connect(lambda: self.edit.setText(
                QFileDialog.getExistingDirectory(self, "选择文件夹", ".")
            ))

    def getFile(self) -> str:
        """获取当前选中的路径。"""
        return self.edit.text()

    def setFile(self, file: str) -> None:
        """设置当前路径文本。"""
        self.edit.setText(file)

class RemovableRow(QHBoxLayout):
    """
    可删除的行布局，包含一个编辑器和一个删除按钮。

    常用于动态列表中的单行条目，点击删除按钮会从父布局中移除自身并清理资源。
    """
    aboutToRemove = Signal()  # 在行被移除前发出信号

    def __init__(self, parent: QLayout, dataType: str, rmBtnText: str = "删除"):
        """
        初始化可删除行。

        参数:
            parent: 父布局，行将被添加到该布局中
            dataType: 编辑器数据类型
            rmBtnText: 删除按钮上的文本
        """
        super().__init__()
        self._parent = parent
        self.dataType = dataType
        self.edit = createEdit(dataType)
        if self.edit is None:
            raise TypeError(f"invalid type: {dataType}")

        self.btn = QPushButton(rmBtnText)

        self.addWidget(self.edit)
        self.addWidget(self.btn)
        parent.addLayout(self)

        self.bind()

    def bind(self) -> None:
        """绑定删除按钮的点击信号。"""
        self.btn.clicked.connect(self.onBtnClicked)

    def deleteLater(self) -> None:
        """递归清理行内的控件，然后调用父类 deleteLater()。"""
        if hasattr(self, "edit") and self.edit is not None:
            self.edit.deleteLater()
        if hasattr(self, "btn"):
            self.btn.deleteLater()
        super().deleteLater()

    def getVal(self) -> Any:
        """获取当前编辑器中的值。"""
        return getVal(self.edit, self.dataType)

    def setVal(self, val: Any) -> None:
        """设置当前编辑器的值。"""
        setVal(self.edit, self.dataType, val)

    @Slot()
    def onBtnClicked(self) -> None:
        """删除按钮的槽函数：触发移除信号，从父布局移除自身并清理。"""
        self.aboutToRemove.emit()
        self._parent.removeItem(self)
        deleteLyt(self)

class PageFactory(QWidget):
    """
    创建 QTabWidget 标签页的工厂基类。

    提供页面构建、数据更新和清理的通用接口，子类需实现具体的 buildContent()、updateTab() 和 getData()。
    """
    valChanged = Signal(str, Any)  # key, value — 当数据变更时发出
    dataUpdated = Signal()         # 当整个数据被更新时发出

    def __init__(self, lyt: QLayout, data):
        """
        初始化页面工厂。

        参数:
            lyt: 页面的根布局
            data: 页面绑定的数据对象
        """
        super().__init__()
        self.lyt = lyt
        self.setLayout(self.lyt)

        self._data = data

    def build(self) -> None:
        """构建页面：调用 buildContent() 并初始化数据到界面。"""
        self.buildContent()
        self.updateTab(self._data)

    def buildContent(self) -> None:
        """构建页面内容，子类必须重写。"""
        pass

    def updateTab(self, data) -> None:
        """用给定的数据更新界面，子类必须重写。"""
        pass

    def getData(self) -> Any:
        """从界面收集数据并返回，子类必须重写。"""
        pass

    def setData(self, data) -> None:
        """设置新数据并刷新界面，同时发出 dataUpdated 信号。"""
        self._data = data
        self.updateTab(data)
        self.dataUpdated.emit()

    def clear(self) -> None:
        """清空页面布局中的所有子项。"""
        clearLyt(self.lyt)

class FormFactory(PageFactory):
    """
    表单工厂，用于创建基于 QFormLayout 的编辑页面。

    根据字段定义（名称、键、类型）生成对应的编辑器，并自动绑定数据更新信号。
    """
    def __init__(self, fields: list[tuple[str, str, str]], data: dict):
        """
        初始化表单工厂。

        参数:
            fields: 字段定义列表，每个元素为 (显示名称, 数据键, 数据类型)
            data: 初始数据字典，键应与 fields 中的键对应
        """
        super().__init__(QFormLayout(), data)
        self.fields = fields
        self.edits: dict[str, QWidget] = {}

    def buildContent(self) -> None:
        """根据字段定义创建编辑器并添加到表单布局。"""
        for name, key, dataType in self.fields:
            edit = createEdit(dataType)
            if edit is None:
                raise TypeError(f"invalid type: {dataType}")
            self.edits[key] = edit
            self.lyt.addRow(name, edit)
            self.bindEditSignal(key, dataType)

    def updateTab(self, data: dict) -> None:
        """用数据字典更新所有编辑器。"""
        for _, key, dataType in self.fields:
            setVal(self.edits[key], dataType, data[key])

    def getData(self) -> dict[str, Any]:
        """从所有编辑器收集数据，返回字典。"""
        return {key: getVal(self.edits[key], dataType) for _, key, dataType in self.fields}

    def bindEditSignal(self, key: str, dataType: str) -> None:
        """
        绑定编辑器值变更信号，将变更同步到 _data 并发出 valChanged。

        参数:
            key: 数据键
            dataType: 数据类型，用于确定监听哪个信号
        """
        edit = self.edits[key]
        match dataType:
            case "bool":
                edit.checkStateChanged.connect(lambda state, k=key: self.onValChanged(k, state != 0))
            case "int":
                edit.valueChanged.connect(lambda val, k=key: self.onValChanged(k, val))
            case "float":
                edit.valueChanged.connect(lambda val, k=key: self.onValChanged(k, val))
            case "str":
                edit.textChanged.connect(lambda text, k=key: self.onValChanged(k, text))
            case "file":
                edit.textChanged.connect(lambda text, k=key: self.onValChanged(k, text))

    @Slot(str, Any)
    def onValChanged(self, key: str, val: Any) -> None:
        """值变更槽函数，更新 _data 并发出信号。"""
        self._data[key] = val
        self.valChanged.emit(key, val)

class DynamicListFactory(PageFactory):
    """
    动态字符串列表工厂，允许添加和删除条目。

    内部维护一个 RemovableRow 列表，每个条目包含一个文本编辑器和一个删除按钮。
    """
    def __init__(self, data: list[str], rmBtnText: str = "删除", addBtnText: str = "新建"):
        """
        初始化动态列表工厂。

        参数:
            data: 初始字符串列表
            rmBtnText: 删除按钮文本
            addBtnText: 添加按钮文本
        """
        super().__init__(QVBoxLayout(), data)
        self.rmBtnText = rmBtnText
        self.addBtnText = addBtnText
        self.addBtn = QPushButton(self.addBtnText)
        self.edits: list[RemovableRow] = []

    def buildContent(self) -> None:
        """根据初始数据创建所有行，并添加"新建"按钮。"""
        for i in self._data:
            self.createRow(i)

        self.lyt.addWidget(self.addBtn)

        self.bind()

    def updateTab(self, data) -> None:
        """用新数据重建列表，清空原有内容。"""
        # 清空
        while len(self.edits) > 0:
            self.edits.pop(0)
        clearLyt(self.lyt)

        for i in data:
            self.createRow(i)

        self.addBtn = QPushButton(self.addBtnText)

        self.lyt.addWidget(self.addBtn)

        self.bind()

    def getData(self) -> list[str]:
        """从所有行收集字符串数据，返回列表。"""
        if len(self.edits) > 0:
            return [edit.getVal() for edit in self.edits]
        else:
            return []

    def bind(self) -> None:
        """绑定添加按钮的点击事件，并为每行绑定移除时的清理逻辑。"""
        self.addBtn.clicked.connect(lambda: self.createRow(""))
        for edit in self.edits:
            edit.aboutToRemove.connect(lambda e=edit: self.edits.remove(e))

    def createRow(self, val: Any) -> None:
        """
        创建一个新的可删除行，将其插入到"新建"按钮之前，并设置初始值。

        参数:
            val: 行的初始值
        """
        self.lyt.removeWidget(self.addBtn)
        edit = RemovableRow(self.lyt, "str", self.rmBtnText)
        self.lyt.addWidget(self.addBtn)
        edit.setVal(val)
        self.edits.append(edit)

class FormBoxFactory(PageFactory):
    """
    工具箱（QToolBox）页面工厂，每个页面包含一个表单。

    用于组织多个表单，每个表单在一个独立的工具页中。
    """
    formValChanged = Signal(str, str, Any)  # key, form's key, value
    formDataUpdated = Signal(str)           # key

    def __init__(self, fields: list[tuple[str, str, list[tuple[str, str, str]]]], data: dict):
        """
        初始化表单工具箱工厂。

        参数:
            fields: 字段定义列表，每个元素为 (页面名称, 数据键, FormFactory.fields)
            data: 数据字典，每个键对应一个表单的数据
        """
        super().__init__(QVBoxLayout(), data)
        self.box: QToolBox = QToolBox()
        self.lyt.addWidget(self.box)
        self.fields = fields
        self.forms: dict[FormBoxFactory] = {}

    def buildContent(self) -> None:
        """为每个字段创建一个 FormFactory，并添加到工具箱中。"""
        for name, key, v in self.fields:
            form = FormFactory(v, self._data[key])
            form.build()
            form.valChanged.connect(lambda formK, val, k=key: self.onFormValChanged(k, formK, val))
            form.dataUpdated.connect(lambda k=key: self.formDataUpdated.emit(k))
            self.box.addItem(form, name)
            self.forms[key] = form

    def updateTab(self, data: dict) -> None:
        """更新所有表单的数据。"""
        for _, key, _ in self.fields:
            form = self.forms[key]
            form.data = data[key]

    def getData(self) -> dict[str, dict[str, Any]]:
        """从所有表单收集数据，返回嵌套字典。"""
        return {key: self.forms[key].getData() for _, key, _ in self.fields}

    @Slot(str, str, Any)
    def onFormValChanged(self, k: str, formK: str, val: Any) -> None:
        """表单内值变更的槽函数，更新 _data 并转发信号。"""
        self._data[k][formK] = val
        self.formValChanged.emit(k, formK, val)

class ListBoxFactory(PageFactory):
    """
    工具箱（QToolBox）页面工厂，每个页面包含一个动态字符串列表。

    用于组织多个动态列表，每个列表在一个独立的工具页中。
    """
    listDataUpdated = Signal(str)  # key

    def __init__(self, fields: list[tuple[str, str]], data: dict):
        """
        初始化列表工具箱工厂。

        参数:
            fields: 字段定义列表，每个元素为 (页面名称, 数据键)
            data: 数据字典，每个键对应一个列表数据
        """
        super().__init__(QVBoxLayout(), data)
        self.box: QToolBox = QToolBox()
        self.lyt.addWidget(self.box)
        self.fields = fields
        self.lists: dict = {}

    def buildContent(self) -> None:
        """为每个字段创建一个 DynamicListFactory，并添加到工具箱中。"""
        for name, key in self.fields:
            list = DynamicListFactory(self._data[key])
            list.build()
            list.dataUpdated.connect(lambda k=key: self.listDataUpdated.emit(k))
            self.box.addItem(list, name)
            self.lists[key] = list

    def updateTab(self, data: dict) -> None:
        """更新所有列表的数据。"""
        for _, key in self.fields:
            l = self.lists[key]
            l.data = data[key]

    def getData(self) -> dict[str, list[str]]:
        """从所有列表收集数据，返回字典。"""
        return {key: self.lists[key].getData() for _, key in self.fields}
