# 桌宠管理器 API

## 目录
- [桌宠管理器 API](#桌宠管理器-api)
  - [目录](#目录)
  - [概述](#概述)
  - [模块 window.manager](#模块-windowmanager)
    - [类 MainWindow(QWidget)](#类-mainwindowqwidget)
      - [属性](#属性)
      - [信号](#信号)
      - [方法 __init__()](#方法-__init__)
      - [方法 initSidebar() -> None](#方法-initsidebar---none)
      - [方法 initStack() -> None](#方法-initstack---none)
      - [方法 bind() -> None](#方法-bind---none)
      - [方法 closeEvent()](#方法-closeevent)
    - [类 SidebarButton(QPushButton)](#类-sidebarbuttonqpushbutton)
      - [属性](#属性-1)
      - [信号](#信号-1)
      - [方法 __init__()](#方法-__init__-1)
    - [类 ManagerPage(SearchStackFactory)](#类-managerpagesearchstackfactory)
      - [属性](#属性-2)
      - [信号](#信号-2)
      - [方法 __init__()](#方法-__init__-2)
      - [方法 _loadAll() -> None](#方法-_loadall---none)
      - [方法 _bindPetSignals() -> None](#方法-_bindpetsignals---none)
      - [方法 reload() -> None](#方法-reload---none)
      - [方法 initConfigPage() -> QWidget](#方法-initconfigpage---qwidget)
      - [方法 initSettingPage() -> QWidget](#方法-initsettingpage---qwidget)
      - [槽函数 onContextMenu() -> None](#槽函数-oncontextmenu---none)
      - [槽函数 renamePet() -> None](#槽函数-renamepet---none)
      - [槽函数 apply() -> None](#槽函数-apply---none)
      - [槽函数 cancel() -> None](#槽函数-cancel---none)
      - [槽函数 openPet() -> None](#槽函数-openpet---none)
      - [槽函数 delPet() -> None](#槽函数-delpet---none)
      - [槽函数 launchPet() -> None](#槽函数-launchpet---none)
    - [类 TempPage(SearchStackFactory)](#类-temppagesearchstackfactory)
      - [属性](#属性-3)
      - [信号](#信号-3)
      - [方法 __init__()](#方法-__init__-3)
      - [方法 loadTemps() -> None](#方法-loadtemps---none)
      - [方法 initInfoPage() -> QWidget](#方法-initinfopage---qwidget)
      - [方法 bind() -> None](#方法-bind---none-1)
      - [方法 refreshManager() -> None](#方法-refreshmanager---none)
      - [槽函数 onContextMenu() -> None](#槽函数-oncontextmenu---none-1)
      - [槽函数 onItemDoubleClicked() -> None](#槽函数-onitemdoubleclicked---none)
      - [方法 instantiatePet() -> None](#方法-instantiatepet---none)
      - [方法 findInstances() -> list[str]](#方法-findinstances---liststr)
      - [方法 deleteTemp() -> None](#方法-deletetemp---none)
    - [类 NameInputDialog(QDialog)](#类-nameinputdialogqdialog)
      - [属性](#属性-4)
      - [信号](#信号-4)
      - [方法 __init__()](#方法-__init__-4)
      - [方法 bind() -> None](#方法-bind---none-2)
      - [槽函数 onOk() -> None](#槽函数-onok---none)
      - [方法 getName() -> str](#方法-getname---str)
    - [类 PluginPage(SearchStackFactory)](#类-pluginpagesearchstackfactory)
      - [属性](#属性-5)
      - [信号](#信号-5)
      - [方法 __init__()](#方法-__init__-5)
    - [类 DocPage(SearchStackFactory)](#类-docpagesearchstackfactory)
      - [属性](#属性-6)
      - [信号](#信号-6)
      - [方法 __init__()](#方法-__init__-6)
    - [类 SettingPage(SearchStackFactory)](#类-settingpagesearchstackfactory)
      - [属性](#属性-7)
      - [信号](#信号-7)
      - [方法 __init__()](#方法-__init__-7)
      - [方法 bind() -> None](#方法-bind---none-3)
      - [槽函数 apply() -> None](#槽函数-apply---none-1)
      - [槽函数 cancel() -> None](#槽函数-cancel---none-1)

---

## 概述

本文档描述桌宠管理器（`window/manager/`）的 API，涵盖主窗口、侧边栏按钮及五个管理页面：`ManagerPage`、`TempPage`、`PluginPage`、`DocPage`、`SettingPage`。管理器用于集中管理多个宠物配置、模板实例化，提供可视化编辑、启动与删除功能。

---

## 模块 window.manager

桌宠管理器模块，包含主窗口、各管理页面及侧边栏按钮。

### 类 MainWindow(QWidget)

管理器主窗口，包含侧边栏和堆叠页面。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `pets` | list[PetWindow] | 当前已打开的宠物窗口列表（类变量） |
| `mainLyt` | QHBoxLayout | 主布局 |
| `sbBtns` | list[SidebarButton] | 侧边栏按钮列表 |
| `pages` | list[SearchStackFactory] | 页面列表 |
| `sidebar` | QFrame | 侧边栏容器 |
| `stack` | QStackedWidget | 堆叠页面容器 |
| `fields` | list[tuple[SidebarButton, SearchStackFactory]] | 按钮与页面的配对列表 |
| `sbLyt` | QVBoxLayout | 侧边栏布局 |

#### 信号

无自定义信号。

#### 方法 __init__()

```python
def __init__(self)
```

初始化主窗口。

- **说明**
  - 设置 `WA_DeleteOnClose` 属性
  - 设置窗口大小为 1000x600
  - 调用 `initSidebar()` 和 `initStack()` 构建界面
  - 调用 `bind()` 绑定信号

#### 方法 initSidebar() -> None

初始化侧边栏，创建侧边栏按钮。

- **说明**
  - 按钮文本依次为 `"🐱"`（桌宠管理）、`"</>"`（模板管理）、`"🧩"`（插件管理）、`"📄"`（文档查阅）、`"⚙"`（管理器设置）
  - `"⚙"` 按钮前插入弹簧（`QSpacerItem`），将其推至底部
  - 每个按钮均设置相应的工具提示文本
  - 侧边栏背景色为 `#0098ff`

#### 方法 initStack() -> None

初始化堆叠页面容器。

- **说明**
  - 依次创建 `ManagerPage`、`TempPage`、`PluginPage`、`DocPage`、`SettingPage` 实例
  - 调用每个页面的 `build()` 方法后添加到堆叠
  - `ManagerPage` 和 `TempPage` 构造时传入 `self`（主窗口引用）

#### 方法 bind() -> None

绑定侧边栏按钮与堆叠页面的切换信号。

- **说明**
  - 遍历侧边栏按钮，为每个按钮绑定点击事件，切换到对应索引的页面
  - 将按钮与页面配对存入 `fields` 列表

#### 方法 closeEvent()

```python
def closeEvent(self, event) -> None
```

管理器关闭事件处理。

- **行为**
  - 遍历 `MainWindow.pets` 列表，关闭所有已打开的宠物窗口
  - 清空 `MainWindow.pets` 列表
  - 接受关闭事件

---

### 类 SidebarButton(QPushButton)

侧边栏按钮，用于在管理器主窗口中切换页面。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `text` | str | 按钮显示的文本（通常为 Emoji 图标） |
| `toolTipText` | str \| None | 鼠标悬浮时显示的工具提示文本 |
| `minimumSize` | QSize | 最小尺寸，固定为 60x60 |
| `maximumSize` | QSize | 最大尺寸，固定为 60x60 |

#### 信号

继承自 `QPushButton` 的 `clicked` 信号。

#### 方法 __init__()

```python
def __init__(self, text: str, toolTipText: str | None = None)
```

初始化侧边栏按钮。

- **参数**
  - `text`: 按钮显示的文本
  - `toolTipText`: 工具提示文本（可选）
- **说明**
  - 按钮尺寸固定为 60x60 像素
  - 字体大小为 30 像素
  - 若提供 `toolTipText`，则设置工具提示

---

### 类 ManagerPage(SearchStackFactory)

桌宠管理页面，包含宠物列表、配置编辑和启动功能。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `_mainWindow` | MainWindow | 主窗口实例引用 |
| `_data` | dict[str, dict] | 宠物元信息字典，键为宠物名 |
| `_petConfigs` | dict[str, ConfigManager] | 宠物配置管理器实例字典 |
| `_intro` | dict[str, str] | 宠物介绍文档内容字典 |
| `configPages` | dict[str, tuple[QWidget, list[WidgetFactory], QPushButton, QPushButton]] | 配置页面信息：`(widget, pages, applyBtn, cancelBtn)` |
| `settingPages` | dict[str, tuple[QPushButton, QPushButton]] | 设置页面信息：`(openBtn, delBtn)` |
| `pages` | dict[str, tuple[QListWidgetItem, QTextEdit, QTabWidget, QFormLayout]] | 页面组件：`(listItem, introPg, configPg, setPg)` |

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `saveError(str, str)` | 保存配置失败时发射，携带宠物名和错误信息 |
| `launchError(str, str)` | 启动宠物失败时发射，携带宠物名和错误信息 |
| `delError(str, str)` | 删除宠物失败时发射，携带宠物名和错误信息 |
| `dataUpdated(str)` | 数据更新时发射，携带宠物名 |
| `updateCancelled(str)` | 取消更新时发射，携带宠物名 |

#### 方法 __init__()

```python
def __init__(self, mainWindow: "MainWindow")
```

初始化桌宠管理页面。

- **参数**
  - `mainWindow`: 主窗口实例
- **说明**
  - 初始化各数据字典
  - 调用 `_loadAll()` 加载所有宠物
  - 调用 `_bindPetSignals()` 绑定宠物信号
  - 绑定列表项双击事件（启动宠物）
  - 设置列表右键菜单策略为 `CustomContextMenu`，并连接 `customContextMenuRequested` 信号到 `onContextMenu`

#### 方法 _loadAll() -> None

从 `ConfigManager.pets` 加载所有宠物并构建页面。

- **行为**
  - 遍历 `ConfigManager.pets`，为每个宠物创建 `ConfigManager` 实例
  - 读取 `info.json` 和 `./temp/{temp}/introduction.md`
  - 为每个宠物创建列表项（含图标）、介绍页（`MarkdownView`）、配置页和设置页
  - 使用 `controller.addPage` 将标签页注册到搜索堆叠中
  - 加载失败时跳过该宠物

#### 方法 _bindPetSignals() -> None

为每个宠物的配置页按钮绑定信号。

- **行为**
  - 绑定 `ConfigManager.saveError` 到 `saveError` 信号
  - 绑定配置页「应用」按钮到 `apply` 槽函数
  - 绑定配置页「取消」按钮到 `cancel` 槽函数
  - 绑定设置页「打开」按钮到 `openPet` 槽函数
  - 绑定设置页「删除」按钮到 `delPet` 槽函数

#### 方法 reload() -> None

重新从磁盘加载宠物列表与配置，重建全部页面。

- **行为**
  1. 调用 `controller.clearAll()` 清空现有 UI
  2. 清空内存数据（`_data`、`_petConfigs`、`_intro`、`configPages`、`settingPages`、`pages`）
  3. 调用 `_loadAll()` 重新加载
  4. 调用 `_bindPetSignals()` 重新绑定信号

#### 方法 initConfigPage() -> QWidget

```python
def initConfigPage(self, name: str) -> QWidget
```

创建宠物的配置编辑页面。

- **参数**
  - `name`: 宠物名
- **返回**
  - 配置页面控件
- **说明**
  - 页面包含六个标签页：基础项、动画、碰撞体、状态反馈文本、对话文本、插件状态
  - 使用 `FormFactory`、`FormBoxFactory`、`ListBoxFactory` 构建各标签页
  - 包含「应用」和「取消」按钮
  - 将配置页面信息存入 `configPages`

**配置页面结构**：

| 标签页 | 工厂类 | 数据来源 |
| :--- | :--- | :--- |
| 基础项 | `FormFactory` | `config.base` |
| 动画 | `FormBoxFactory` | `config.anime` |
| 碰撞体 | `FormBoxFactory` | `config.collision` |
| 状态反馈文本 | `ListBoxFactory` | `config.state` |
| 对话文本 | `ListBoxFactory` | `config.dialog` |
| 插件状态 | `FormFactory` | `config.pluginState` |

#### 方法 initSettingPage() -> QWidget

```python
def initSettingPage(self, name: str) -> QWidget
```

创建宠物的设置页面。

- **参数**
  - `name`: 宠物名
- **返回**
  - 设置页面控件
- **说明**
  - 显示宠物元信息（名称、版本、作者）
  - 包含「在文件资源管理器中打开」和「删除桌宠」按钮
  - 将设置页面信息存入 `settingPages`

#### 槽函数 onContextMenu() -> None

```python
def onContextMenu(self, pos: QPoint) -> None
```

显示右键菜单。

- **参数**
  - `pos`: 鼠标位置
- **行为**
  - 获取点击位置的列表项，若无效则返回
  - 创建右键菜单，包含「重命名」动作和红色「删除桌宠」项（`QWidgetAction` + `QLabel`）
  - 在鼠标全局位置弹出菜单

#### 槽函数 renamePet() -> None

```python
def renamePet(self, oldName: str) -> None
```

重命名桌宠。

- **参数**
  - `oldName`: 原宠物名
- **行为**
  1. 检查是否有运行中的实例，若有则提示用户关闭
  2. 弹出输入对话框获取新名称
  3. 校验新名称（非空、不重复、目录不存在）
  4. 重命名磁盘目录（`os.rename`）
  5. 更新 `info.json` 中的 `name` 字段
  6. 更新 `./pet/config.json` 注册表
  7. 更新 `ConfigManager.pets`
  8. 调用 `reload()` 重建页面
  9. 失败时回滚磁盘重命名

#### 槽函数 apply() -> None

```python
def apply(self, name: str) -> None
```

应用配置更改。

- **参数**
  - `name`: 宠物名
- **行为**
  - 从所有配置页面收集数据
  - 更新 `ConfigManager` 对应属性（`base`、`anime`、`collision`、`state`、`dialog`、`pluginState`）
  - 调用 `saveConfig(ConfigManager.SaveMode.Common)` 保存到文件
  - 发射 `dataUpdated` 信号

#### 槽函数 cancel() -> None

```python
def cancel(self, name: str) -> None
```

取消配置更改。

- **参数**
  - `name`: 宠物名
- **行为**
  - 从 `ConfigManager` 重新加载数据到所有配置页面
  - 调用 `repaint()` 刷新界面
  - 发射 `updateCancelled` 信号

#### 槽函数 openPet() -> None

```python
def openPet(self, name: str) -> None
```

在文件资源管理器中打开宠物文件夹。

- **参数**
  - `name`: 宠物名
- **行为**
  - 获取宠物目录的绝对路径
  - 根据操作系统调用相应的文件管理器打开：
    - Windows：`os.startfile`
    - macOS：`subprocess.Popen(['open', absPath])`
    - Linux：`subprocess.Popen(['xdg-open', absPath])`

#### 槽函数 delPet() -> None

```python
def delPet(self, name: str) -> None
```

从系统中删除宠物。

- **参数**
  - `name`: 宠物名
- **行为**
  1. 检查是否有运行中的实例，若有则提示用户关闭
  2. 弹出确认对话框
  3. 从 `./pet/config.json` 注册文件中移除
  4. 更新 `ConfigManager.pets`
  5. 删除宠物文件夹（使用 `shutil.rmtree`）
  6. 调用 `reload()` 重建页面
  7. 提示删除成功
- **信号**
  - `delError(str, str)`: 删除失败时发射

#### 槽函数 launchPet() -> None

```python
def launchPet(self, name: str) -> None
```

启动指定宠物。

- **参数**
  - `name`: 宠物名
- **行为**
  1. 检查是否已有同名实例，若有则提示用户
  2. 创建 `PetWindow` 实例
  3. 设置 `WA_DeleteOnClose` 属性
  4. 显示窗口
  5. 将窗口添加到 `MainWindow.pets` 列表
- **信号**
  - `launchError(str, str)`: 启动失败时发射

---

### 类 TempPage(SearchStackFactory)

模板管理页面，用于浏览、实例化和删除宠物模板。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `_mainWindow` | MainWindow | 主窗口实例引用 |
| `_data` | dict[str, dict] | 模板信息字典，键为模板目录名 |
| `_intro` | dict[str, str] | 模板介绍文档内容字典 |

#### 信号

无自定义信号。

#### 方法 __init__()

```python
def __init__(self, mainWindow=None)
```

初始化模板管理页面。

- **参数**
  - `mainWindow`: 主窗口实例（可选）
- **说明**
  - 初始化 `_data` 和 `_intro` 字典
  - 调用 `loadTemps()` 加载所有模板
  - 调用 `bind()` 绑定信号

#### 方法 loadTemps() -> None

加载 `./temp/` 下所有模板。

- **行为**
  - 遍历 `./temp/` 下的所有目录
  - 读取每个模板的 `info.json` 和 `introduction.md`
  - 创建列表项（含图标），图标路径为 `./temp/{name}/icon.png`
  - 列表项通过 `setData(Qt.ItemDataRole.UserRole, name)` 存储模板目录名
  - 创建详情页，包含介绍页（`MarkdownView`）和信息页
  - 使用 `controller.addPage` 注册到搜索堆叠中

#### 方法 initInfoPage() -> QWidget

```python
def initInfoPage(self, name: str) -> QWidget
```

创建模板信息页面。

- **参数**
  - `name`: 模板目录名
- **返回**
  - 信息页面控件
- **说明**
  - 显示模板名称、版本、模板目录、作者

#### 方法 bind() -> None

绑定信号与槽。

- **说明**
  - 绑定列表项双击事件到 `onItemDoubleClicked`
  - 设置列表右键菜单策略为 `CustomContextMenu`，并连接 `customContextMenuRequested` 信号到 `onContextMenu`

#### 方法 refreshManager() -> None

通知主窗口中的各页刷新。

- **行为**
  - 遍历 `_mainWindow.pages`，对具有 `reload` 方法的页面调用 `reload()`

#### 槽函数 onContextMenu() -> None

```python
def onContextMenu(self, pos: QPoint) -> None
```

显示右键菜单。

- **参数**
  - `pos`: 鼠标位置
- **行为**
  - 获取点击位置的列表项，若无效则返回
  - 创建右键菜单，包含「实例化」动作和红色「删除模板」项（`QWidgetAction` + `QLabel`）
  - 在鼠标全局位置弹出菜单

#### 槽函数 onItemDoubleClicked() -> None

```python
def onItemDoubleClicked(self, item: QListWidgetItem) -> None
```

双击列表项，实例化宠物。

- **参数**
  - `item`: 被双击的列表项
- **行为**
  - 获取模板目录名，调用 `instantiatePet(tempName)`

#### 方法 instantiatePet() -> None

```python
def instantiatePet(self, tempName: str) -> None
```

实例化宠物：复制模板资源到 `./pet/` 下。

- **参数**
  - `tempName`: 模板目录名
- **行为**
  1. 弹出命名对话框，获取宠物名称
  2. 创建 `./pet/{name}` 目录
  3. 复制 `info.json` 到宠物目录
  4. 复制 `config/` 目录到宠物目录
  5. 写入 `name` 和 `temp` 字段到 `info.json`
  6. 新建 `log.log` 文件
  7. 注册到 `./pet/config.json` 列表
  8. 更新 `ConfigManager.pets`
  9. 调用 `refreshManager()` 通知管理器刷新
  10. 失败时删除已创建的宠物目录

#### 方法 findInstances() -> list[str]

```python
def findInstances(self, tempName: str) -> list[str]
```

查找使用指定模板的所有宠物实例名。

- **参数**
  - `tempName`: 模板目录名
- **返回**
  - 宠物实例名列表
- **行为**
  - 遍历 `ConfigManager.pets`，读取每个宠物的 `info.json`
  - 若 `info["temp"] == tempName`，则加入结果列表

#### 方法 deleteTemp() -> None

```python
def deleteTemp(self, tempName: str) -> None
```

删除模板（及其所有实例）。

- **参数**
  - `tempName`: 模板目录名
- **行为**
  - 调用 `findInstances()` 查找使用该模板的所有实例
  - 若有实例，询问是否删除所有实例及模板
    - 确定：从 `./pet/config.json` 中移除实例，删除实例目录
    - 取消：不做任何操作
  - 若无实例，确认删除模板
  - 删除模板目录
  - 从 UI 中移除（`controller.removePage`）
  - 从内存数据中移除
  - 调用 `refreshManager()` 通知管理器刷新

---

### 类 NameInputDialog(QDialog)

宠物命名对话框，用于实例化模板时输入宠物名称。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `lyt` | QVBoxLayout | 主布局 |
| `formLyt` | QFormLayout | 表单布局 |
| `nameEdit` | QLineEdit | 名称输入框 |
| `btnLyt` | QHBoxLayout | 按钮布局 |
| `okBtn` | QPushButton | 确认按钮 |
| `cancelBtn` | QPushButton | 取消按钮 |

#### 信号

无自定义信号。

#### 方法 __init__()

```python
def __init__(self, parent=None)
```

初始化命名对话框。

- **参数**
  - `parent`: 父窗口（可选）
- **说明**
  - 设置窗口标题为 "命名桌宠"，大小为 300x120
  - 创建名称输入框、确认按钮和取消按钮
  - 调用 `bind()` 绑定信号

#### 方法 bind() -> None

绑定信号与槽。

- **说明**
  - 绑定确认按钮到 `onOk`
  - 绑定取消按钮到 `reject`

#### 槽函数 onOk() -> None

```python
def onOk(self) -> None
```

确认按钮槽函数。

- **行为**
  1. 获取输入的名称并去除首尾空格
  2. 校验名称（非空、不重复、目录不存在）
  3. 校验通过则调用 `accept()`

#### 方法 getName() -> str

```python
def getName(self) -> str
```

获取输入的名称。

- **返回**
  - 去除首尾空格的名称字符串

---

### 类 PluginPage(SearchStackFactory)

插件管理页面。

#### 属性

继承自 `SearchStackFactory` 的属性。

#### 信号

继承自 `SearchStackFactory` 的信号。

#### 方法 __init__()

```python
def __init__(self)
```

初始化插件管理页面。

- **说明**
  - 当前为空实现（占位页面），待后续完善
  - 继承自 `SearchStackFactory`，具备搜索列表与堆叠页面的联动能力

---

### 类 DocPage(SearchStackFactory)

文档查阅页面。

#### 属性

继承自 `SearchStackFactory` 的属性。

#### 信号

继承自 `SearchStackFactory` 的信号。

#### 方法 __init__()

```python
def __init__(self)
```

初始化文档查阅页面。

- **说明**
  - 当前为空实现（占位页面），待后续完善
  - 继承自 `SearchStackFactory`，具备搜索列表与堆叠页面的联动能力

---

### 类 SettingPage(SearchStackFactory)

管理器设置页面，用于编辑全局配置。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `form` | FormFactory | 设置表单工厂，包含三个设置项 |
| `applyBtn` | QPushButton | 应用按钮 |
| `cancelBtn` | QPushButton | 取消按钮 |

**设置项**：

| 显示名称 | 键 | 数据类型 |
| :--- | :--- | :--- |
| 默认桌宠 | `default-pet` | str（选项为 `[""] + [key for key in ConfigManager.pets]`） |
| 控制器颜色主题 | `manager-color-subject` | str（选项为 `["Light", "Dark"]`） |
| 开机自启动 | `auto-start` | bool |

#### 信号

无自定义信号。

#### 方法 __init__()

```python
def __init__(self)
```

初始化设置页面。

- **说明**
  - 创建 `FormFactory` 表单，绑定 `ConfigManager.settings`
  - 添加「应用」和「取消」按钮
  - 使用 `controller.addPage` 将页面注册到搜索堆叠中，标签为 "管理器设置"
  - 调用 `bind()` 绑定信号

#### 方法 bind() -> None

绑定信号与槽。

- **说明**
  - 绑定「应用」按钮到 `apply` 槽函数
  - 绑定「取消」按钮到 `cancel` 槽函数

#### 槽函数 apply() -> None

```python
def apply(self) -> None
```

应用管理器设置更改。

- **行为**
  - 从表单收集数据
  - 更新 `ConfigManager.settings`
  - 调用 `ConfigManager.saveStaticConfigs()` 保存到文件

#### 槽函数 cancel() -> None

```python
def cancel(self) -> None
```

取消管理器设置更改。

- **行为**
  - 从 `ConfigManager.settings` 重新加载数据到表单
  - 调用 `repaint()` 刷新界面
