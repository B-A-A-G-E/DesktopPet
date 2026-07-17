# 桌宠管理器 API

## 目录
- [桌宠管理器 API](#桌宠管理器-api)
  - [目录](#目录)
  - [概述](#概述)
  - [模块 window.manager](#模块-windowmanager)
    - [类 MainWindow(QWidget)](#类-mainwindowqwidget)
      - [属性](#属性)
      - [方法 \_\_init__()](#方法-__init__)
      - [方法 initSidebar() -> None](#方法-initsidebar---none)
      - [方法 initStack() -> None](#方法-initstack---none)
      - [方法 bind() -> None](#方法-bind---none)
      - [方法 closeEvent()](#方法-closeevent)
      - [静态方法 getPet(name: str) -> list[PetWindow] | None](#静态方法-getpetname-str---listpetwindow--none)
    - [类 ManagerPage(SearchStackFactory)](#类-managerpagesearchstackfactory)
      - [属性](#属性-1)
      - [信号](#信号)
      - [方法 \_\_init__()](#方法-__init__-1)
      - [方法 initConfigPage(name: str) -> QWidget](#方法-initconfigpagename-str---qwidget)
      - [方法 initSettingPage(name: str) -> QWidget](#方法-initsettingpagename-str---qwidget)
      - [方法 bind() -> None](#方法-bind---none-1)
      - [槽函数 apply(name: str) -> None](#槽函数-applyname-str---none)
      - [槽函数 cancel(name: str) -> None](#槽函数-cancelname-str---none)
      - [槽函数 openPet(name: str) -> None](#槽函数-openpetname-str---none)
      - [槽函数 delPet(name: str) -> None](#槽函数-delpetname-str---none)
      - [槽函数 launchPet(name: str) -> None](#槽函数-launchpetname-str---none)
    - [类 PluginPage(SearchStackFactory)](#类-pluginpagesearchstackfactory)
      - [说明](#说明)
    - [类 DocPage(SearchStackFactory)](#类-docpagesearchstackfactory)
      - [说明](#说明-1)
    - [类 SettingPage(SearchStackFactory)](#类-settingpagesearchstackfactory)
      - [属性](#属性-2)
      - [方法 \_\_init__()](#方法-__init__-2)
      - [方法 bind() -> None](#方法-bind---none-2)
      - [槽函数 apply() -> None](#槽函数-apply---none)
      - [槽函数 cancel() -> None](#槽函数-cancel---none)
    - [类 SidebarButton(QPushButton)](#类-sidebarbuttonqpushbutton)
      - [初始化 __init__(text: str, toolTipText: str | None = None)](#初始化-__init__text-str-tooltiptext-str--none--none)

---

## 概述

本文档描述桌宠管理器（`manager.py`）的 API，涵盖主窗口、各管理页面及其方法。管理器用于集中管理多个宠物配置，提供可视化编辑和启动功能。

---

## 模块 window.manager

桌宠管理器模块，包含主窗口、各管理页面及侧边栏按钮。

### 类 MainWindow(QWidget)

管理器主窗口，包含侧边栏和堆叠页面。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `mainLyt` | QHBoxLayout | 主布局 |
| `sidebar` | QFrame | 侧边栏容器 |
| `sbLyt` | QVBoxLayout | 侧边栏布局 |
| `stack` | QStackedWidget | 堆叠页面容器 |
| `sbBtns` | list[SidebarButton] | 侧边栏按钮列表 |
| `pages` | list[SearchStackFactory] | 页面列表 |
| `fields` | list[tuple[SidebarButton, SearchStackFactory]] | 按钮与页面的配对列表 |
| `pets` | list[PetWindow] | 当前已打开的宠物窗口列表（类变量） |

#### 方法 __init__()

```python
def __init__(self)
```

初始化主窗口。

- **说明**
  - 设置窗口大小为 1000x600
  - 设置 `WA_DeleteOnClose` 属性
  - 调用 `initSidebar()` 和 `initStack()` 构建界面
  - 调用 `bind()` 绑定信号

#### 方法 initSidebar() -> None

初始化侧边栏，创建侧边栏按钮。

- **说明**
  - 按钮文本依次为 `"🐱"`（桌宠管理）、`"🧩"`（插件管理）、`"📄"`（文档查阅）、`"⚙"`（管理器设置）
  - `"⚙"` 按钮前插入弹簧，将其推至底部
  - 每个按钮均设置相应的工具提示文本
  - 侧边栏背景色为 `#0098ff`

#### 方法 initStack() -> None

初始化堆叠页面容器。

- **说明**
  - 依次创建 `ManagerPage`、`PluginPage`、`DocPage`、`SettingPage` 实例
  - 调用每个页面的 `build()` 方法后添加到堆叠
  - `ManagerPage` 构造时传入 `self`（主窗口引用）

#### 方法 bind() -> None

绑定侧边栏按钮与堆叠页面的切换信号。

- **说明**
  - 点击侧边栏按钮时，堆叠切换到对应索引的页面
  - 将按钮与页面配对存入 `fields` 列表

#### 方法 closeEvent()

```python
def closeEvent(event) -> None
```

管理器关闭事件处理。

- **行为**
  - 遍历 `MainWindow.pets` 列表，关闭所有已打开的宠物窗口
  - 清空 `MainWindow.pets` 列表
  - 接受关闭事件

#### 静态方法 getPet(name: str) -> list[PetWindow] | None

根据宠物名获取所有已打开的宠物窗口实例。

- **参数**
  - `name`: 宠物名
- **返回**
  - 匹配的宠物窗口列表，若没有匹配项则返回 `None`

---

### 类 ManagerPage(SearchStackFactory)

桌宠管理页面，包含宠物列表、配置编辑和启动功能。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `_mainWindow` | MainWindow | 主窗口实例引用 |
| `_data` | dict[str, dict] | 宠物元信息字典，键为宠物名 |
| `_petConfigs` | dict[str, ConfigManager] | 宠物配置管理器实例 |
| `_intro` | dict[str, str] | 宠物介绍文档内容 |
| `configPages` | dict[str, tuple] | 配置页面信息：`(widget, pages, applyBtn, cancelBtn)` |
| `settingPages` | dict[str, tuple] | 设置页面信息：`(openBtn, delBtn)` |
| `pages` | dict[str, tuple] | 页面组件：`(listItem, introPg, configPg, setPg)` |

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
  - 加载所有宠物的元信息、配置和介绍文档
  - 为每个宠物创建列表项和配置页面
  - 使用 `SearchStackController` 管理列表与页面的联动

#### 方法 initConfigPage(name: str) -> QWidget

创建宠物的配置编辑页面。

- **参数**
  - `name`: 宠物名
- **返回**
  - 配置页面控件
- **说明**
  - 页面包含六个标签页：基础项、动画、碰撞体、状态反馈文本、对话文本、插件状态
  - 使用 `FormFactory`、`FormBoxFactory`、`ListBoxFactory` 构建各标签页
  - 包含"应用"和"取消"按钮

**配置页面结构**：

| 标签页 | 工厂类 | 数据来源 |
| :--- | :--- | :--- |
| 基础项 | `FormFactory` | `config.base` |
| 动画 | `FormBoxFactory` | `config.anime` |
| 碰撞体 | `FormBoxFactory` | `config.collision` |
| 状态反馈文本 | `ListBoxFactory` | `config.state` |
| 对话文本 | `ListBoxFactory` | `config.dialog` |
| 插件状态 | `FormFactory` | `config.pluginState` |

#### 方法 initSettingPage(name: str) -> QWidget

创建宠物的设置页面。

- **参数**
  - `name`: 宠物名
- **返回**
  - 设置页面控件
- **说明**
  - 显示宠物元信息（名称、版本、作者）
  - 包含「在文件资源管理器中打开」和「删除桌宠」按钮

#### 方法 bind() -> None

绑定所有信号与槽。

- **说明**
  - 绑定配置页面的「应用」和「取消」按钮
  - 绑定设置页面的「打开」和「删除」按钮
  - 绑定宠物列表的双击事件（启动宠物）
  - 绑定 `ConfigManager.saveError` 信号

#### 槽函数 apply(name: str) -> None

应用配置更改。

- **参数**
  - `name`: 宠物名
- **行为**
  - 从所有配置页面收集数据
  - 更新 `ConfigManager` 对应属性
  - 调用 `saveConfig(ConfigManager.SaveMode.Common)` 保存到文件
  - 发射 `dataUpdated` 信号

#### 槽函数 cancel(name: str) -> None

取消配置更改。

- **参数**
  - `name`: 宠物名
- **行为**
  - 从 `ConfigManager` 重新加载数据到配置页面
  - 调用 `repaint()` 刷新界面
  - 发射 `updateCancelled` 信号

#### 槽函数 openPet(name: str) -> None

在文件资源管理器中打开宠物文件夹。

- **参数**
  - `name`: 宠物名
- **行为**
  - 获取宠物目录的绝对路径
  - 根据操作系统（Windows/macOS/Linux）调用相应的文件管理器打开

#### 槽函数 delPet(name: str) -> None

从系统中删除宠物。

- **参数**
  - `name`: 宠物名
- **行为**
  1. 检查是否有正在运行的宠物实例，若有则提示用户关闭
  2. 弹出确认对话框
  3. 从 UI 中移除宠物条目（调用 `controller.removePage`）
  4. 从内存数据中移除
  5. 从 `./pet/config.json` 注册文件中移除
  6. 更新 `ConfigManager.pets`
  7. 删除宠物文件夹（使用 `shutil.rmtree`）
  8. 提示删除成功
- **信号**
  - `delError(str, str)`: 删除失败时发射

#### 槽函数 launchPet(name: str) -> None

启动指定宠物。

- **参数**
  - `name`: 宠物名
- **行为**
  - 创建 `PetWindow` 实例
  - 设置 `WA_DeleteOnClose` 属性
  - 显示窗口
  - 将窗口添加到 `MainWindow.pets` 列表
- **信号**
  - `launchError(str, str)`: 启动失败时发射

---

### 类 PluginPage(SearchStackFactory)

插件管理页面。

#### 说明

- 当前为空实现（占位页面），待后续完善
- 继承自 `SearchStackFactory`，具备搜索列表与堆叠页面的联动能力

---

### 类 DocPage(SearchStackFactory)

文档查阅页面。

#### 说明

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
| 默认桌宠 | `default-pet` | str |
| 控制器颜色主题 | `manager-color-subject` | str |
| 开机自启动 | `auto-start` | bool |

#### 方法 __init__()

```python
def __init__(self)
```

初始化设置页面。

- **说明**
  - 创建 `FormFactory` 表单
  - 添加"应用"和"取消"按钮
  - 使用 `controller.addPage` 将页面注册到搜索堆叠中

#### 方法 bind() -> None

绑定信号与槽。

- **说明**
  - 绑定「应用」按钮到 `apply` 槽函数
  - 绑定「取消」按钮到 `cancel` 槽函数

#### 槽函数 apply() -> None

应用管理器设置更改。

- **行为**
  - 从表单收集数据
  - 更新 `ConfigManager.settings`
  - 调用 `ConfigManager.saveStaticConfigs()` 保存到文件

#### 槽函数 cancel() -> None

取消管理器设置更改。

- **行为**
  - 从 `ConfigManager.settings` 重新加载数据到表单
  - 调用 `repaint()` 刷新界面

---

### 类 SidebarButton(QPushButton)

侧边栏按钮，用于在管理器主窗口中切换页面。

#### 初始化 __init__(text: str, toolTipText: str | None = None)

- **参数**
  - `text`: 按钮显示的文本（通常为 Emoji 图标）
  - `toolTipText`: 鼠标悬浮时显示的工具提示文本（可选）
- **说明**
  - 按钮尺寸固定为 60x60 像素
  - 字体大小为 30 像素
  - 按钮最小和最大尺寸均设为 60x60
