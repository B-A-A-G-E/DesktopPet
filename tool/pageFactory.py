from PySide6.QtWidgets import (
    QWidget, QLayout, QVBoxLayout, QHBoxLayout, QFormLayout,
    QToolBox, QLineEdit, QPushButton, QCheckBox, QSpinBox,
    QDoubleSpinBox, QFileDialog
)
from PySide6.QtCore import Signal, Slot

from typing import Any

def deleteLyt(lyt: QLayout) -> None:
    """递归删除布局"""
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
    while lyt.count():
        item = lyt.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
        elif item.layout():
            deleteLyt(item.layout())

def getVal(edit: Any, dataType: str) -> Any:
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
    """根据类型创建编辑器控件"""
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
    """文件选择器"""
    textChanged = Signal(str)

    def __init__(self, mode: str = "file"):
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
        return self.edit.text()
    
    def setFile(self, file: str) -> None:
        self.edit.setText(file)

class RemovableRow(QHBoxLayout):
    aboutToRemove = Signal()

    def __init__(self, parent: QLayout, dataType: str, rmBtnText: str = "删除"):
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
        self.btn.clicked.connect(self.onBtnClicked)
    
    def deleteLater(self) -> None:
        if hasattr(self, "edit") and self.edit is not None:
            self.edit.deleteLater()
        if hasattr(self, "btn"):
            self.btn.deleteLater()
        super().deleteLater()
    
    def getVal(self) -> Any:
        return getVal(self.edit, self.dataType)
    
    def setVal(self, val: Any) -> None:
        setVal(self.edit, self.dataType, val)

    @Slot()
    def onBtnClicked(self) -> None:
        self.aboutToRemove.emit()
        self._parent.removeItem(self)
        deleteLyt(self)

class PageFactory(QWidget):
    """创建QTabWidget标签页的工厂基类"""
    valChanged = Signal(str, Any) # key, value
    dataUpdated = Signal()

    def __init__(self, lyt: QLayout, data):
        super().__init__()
        self.lyt = lyt
        self.setLayout(self.lyt)
        
        self._data = data

    def build(self) -> None:
        """构建页面"""
        self.buildContent()
        self.updateTab(self._data)

    def buildContent(self) -> None:
        """构建页面内容"""
        pass

    def updateTab(self, data) -> None:
        """更新界面"""
        pass
    
    def getData(self) -> Any:
        """返回更新后的数据"""
        pass

    def setData(self, data) -> None:
        self._data = data
        self.updateTab(data)
        self.dataUpdated.emit()
    
    def clear(self) -> None:
        clearLyt(self.lyt)

class FormFactory(PageFactory):
    def __init__(self, fields: list[tuple[str, str, str]], data: dict):
        """
        fields = [(name, key, type)]
        """
        super().__init__(QFormLayout(), data)
        self.fields = fields
        self.edits: dict[str, QWidget] = {}
    
    def buildContent(self) -> None:
        for name, key, dataType in self.fields:
            edit = createEdit(dataType)
            if edit is None:
                raise TypeError(f"invalid type: {dataType}")
            self.edits[key] = edit
            self.lyt.addRow(name, edit)
            self.bindEditSignal(key, dataType)
    
    def updateTab(self, data: dict) -> None:
        for _, key, dataType in self.fields:
            setVal(self.edits[key], dataType, data[key])

    def getData(self) -> dict[str, Any]:
        return { key: getVal(self.edits[key], dataType) for _, key, dataType in self.fields }

    def bindEditSignal(self, key: str, dataType: str) -> None:
        edit = self.edits[key]
        match dataType:
            case "bool":
                edit.checkStateChanged.connect(lambda state, k = key: self.onValChanged(k, state != 0))
            case "int":
                edit.valueChanged.connect(lambda val, k = key: self.onValChanged(k, val))
            case "float":
                edit.valueChanged.connect(lambda val, k = key: self.onValChanged(k, val))
            case "str":
                edit.textChanged.connect(lambda text, k = key: self.onValChanged(k, text))
            case "file":
                edit.textChanged.connect(lambda text, k = key: self.onValChanged(k, text))

    @Slot(str, Any)
    def onValChanged(self, key: str, val: Any) -> None:
        self._data[key] = val
        self.valChanged.emit(key, val)

class DynamicListFactory(PageFactory):
    """可以动态添加/删除的字符串编辑列表"""
    def __init__(self, data: list[str], rmBtnText: str = "删除", addBtnText: str = "新建"):
        """
        data = [text, text]
        """
        super().__init__(QVBoxLayout(), data)
        self.rmBtnText = rmBtnText
        self.addBtnText = addBtnText
        self.addBtn = QPushButton(self.addBtnText)
        self.edits: list[RemovableRow] = []
    
    def buildContent(self) -> None:
        for i in self._data:
            self.createRow(i)
        
        self.lyt.addWidget(self.addBtn)
        
        self.bind()

    def updateTab(self, data) -> None:
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
        if len(self.edits) > 0:
            return [ edit.getVal() for edit in self.edits ]
        else:
            return []

    def bind(self) -> None:
        self.addBtn.clicked.connect(lambda: self.createRow(""))
        for edit in self.edits:
            edit.aboutToRemove.connect(lambda e = edit: self.edits.remove(e))
    
    def createRow(self, val: Any) -> None:
            self.lyt.removeWidget(self.addBtn)
            edit = RemovableRow(self.lyt, "str", self.rmBtnText)
            self.lyt.addWidget(self.addBtn)
            edit.setVal(val)
            self.edits.append(edit)

class FormBoxFactory(PageFactory):
    formValChanged = Signal(str, str, Any) # key, form's key, value
    formDataUpdated = Signal(str) # key

    def __init__(self, fields: list[tuple[str, str, list[tuple[str, str, str]]]], data: dict):
        """
        fields = [(name, key, FormFactory.fields)]
        """
        super().__init__(QVBoxLayout(), data)
        self.box: QToolBox = QToolBox()
        self.lyt.addWidget(self.box)
        self.fields = fields
        self.forms: dict[FormBoxFactory] = {}
    
    def buildContent(self) -> None:
        for name, key, v in self.fields:
            form = FormFactory(v, self._data[key])
            form.build()
            form.valChanged.connect(lambda formK, val, k = key: self.onFormValChanged(k, formK, val))
            form.dataUpdated.connect(lambda k = key: self.formDataUpdated.emit(k))
            self.box.addItem(form, name)
            self.forms[key] = form
    
    def updateTab(self, data: dict) -> None:
        for _, key, _ in self.fields:
            form = self.forms[key]
            form.data = data[key]
    
    def getData(self) -> dict[str, dict[str, Any]]:
        return { key: self.forms[key].getData() for _, key, _ in self.fields }

    @Slot(str, str, Any)
    def onFormValChanged(self, k: str, formK: str, val: Any) -> None:
        self._data[k][formK] = val
        self.formValChanged.emit(k, formK, val)

class ListBoxFactory(PageFactory):
    listDataUpdated = Signal(str) # key

    def __init__(self, fields: list[tuple[str, str]], data: dict):
        """
        fields = [(name, key)]
        """
        super().__init__(QVBoxLayout(), data)
        self.box: QToolBox = QToolBox()
        self.lyt.addWidget(self.box)
        self.fields = fields
        self.lists: dict = {}
    
    def buildContent(self) -> None:
        for name, key in self.fields:
            list = DynamicListFactory(self._data[key])
            list.build()
            list.dataUpdated.connect(lambda k = key: self.listDataUpdated.emit(k))
            self.box.addItem(list, name)
            self.lists[key] = list
    
    def updateTab(self, data: dict) -> None:
        for _, key in self.fields:
            l = self.lists[key]
            l.data = data[key]
    
    def getData(self) -> dict[str, list[str]]:
        return { key: self.lists[key].getData() for _, key in self.fields }
