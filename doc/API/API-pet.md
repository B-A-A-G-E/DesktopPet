# 桌宠 API

## 目录
- [桌宠 API](#桌宠-api)
  - [目录](#目录)
  - [概述](#概述)
  - [模块 window.pet](#模块-windowpet)
    - [类 PetWindow(QWidget)](#类-petwindowqwidget)
      - [属性](#属性)
      - [信号](#信号)
      - [方法 __init__()](#方法-__init__)
      - [方法 bind() -> None](#方法-bind---none)
      - [方法 operateState() -> None](#方法-operatestate---none)
      - [方法 changeState() -> None](#方法-changestate---none)
      - [方法 replyState() -> None](#方法-replystate---none)
      - [方法 changeAnime() -> None](#方法-changeanime---none)
      - [方法 startAct() -> None](#方法-startact---none)
      - [方法 stopAct() -> None](#方法-stopact---none)
      - [方法 getAct() -> Plugin | None](#方法-getact---plugin--none)
      - [方法 closeEvent()](#方法-closeevent)
      - [槽函数 onStateChanged() -> None](#槽函数-onstatechanged---none)
      - [槽函数 updateData() -> None](#槽函数-updatedata---none)
    - [类 DialogMenu(QWidget)](#类-dialogmenuqwidget)
      - [属性](#属性-1)
      - [方法 __init__()](#方法-__init__-1)
      - [方法 bind() -> None](#方法-bind---none-1)
      - [方法 resetQuesSelecter() -> None](#方法-resetquesselecter---none)
      - [方法 addLine() -> None](#方法-addline---none)
      - [槽函数 reply() -> None](#槽函数-reply---none)
    - [类 StateMenu(QWidget)](#类-statemenuqwidget)
      - [属性](#属性-2)
      - [方法 __init__()](#方法-__init__-2)
      - [方法 bind() -> None](#方法-bind---none-2)
      - [方法 log() -> None](#方法-log---none)
      - [方法 addPage() -> None](#方法-addpage---none)
      - [方法 getPage() -> QWidget | None](#方法-getpage---qwidget--none)
    - [类 ActionMenu(QWidget)](#类-actionmenuqwidget)
      - [属性](#属性-3)
      - [方法 __init__()](#方法-__init__-3)
      - [方法 bind() -> None](#方法-bind---none-3)
    - [类 SettingMenu(QWidget)](#类-settingmenuqwidget)
      - [属性](#属性-4)
      - [信号](#信号-1)
      - [方法 __init__()](#方法-__init__-4)
      - [方法 initPages() -> None](#方法-initpages---none)
      - [方法 bind() -> None](#方法-bind---none-4)
      - [方法 apply() -> None](#方法-apply---none)
      - [方法 cancel() -> None](#方法-cancel---none)
      - [方法 addPage() -> None](#方法-addpage---none-1)
      - [方法 getPage() -> QWidget | None](#方法-getpage---qwidget--none-1)

---

## 概述

本文档描述桌宠（`window/pet/`）的 API，涵盖桌宠主窗口及其四个子菜单窗口：`PetWindow`、`DialogMenu`、`StateMenu`、`ActionMenu`、`SettingMenu`。桌宠通过 `PetWindow` 统一管理动画、状态机、插件和碰撞体，子菜单窗口分别负责对话、状态日志、行动执行和配置编辑。

---

## 模块 window.pet

桌宠模块，包含主窗口及四个子菜单窗口。

### 类 PetWindow(QWidget)

桌宠主窗口，管理动画、状态机、插件、碰撞体和子菜单。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `name` | str | 桌宠名称，对应 `./pet/` 下的目录名 |
| `imgLb` | QLabel | 存放图片的标签控件 |
| `dialogAct` | QAction | 上下文菜单"对话"动作 |
| `stateAct` | QAction | 上下文菜单"状态"动作 |
| `actAct` | QAction | 上下文菜单"行动"动作 |
| `setAct` | QAction | 上下文菜单"设置"动作 |
| `exitAct` | QAction | 上下文菜单"退出"动作 |
| `mainlayout` | QVBoxLayout | 主布局 |
| `configManager` | ConfigManager | 配置管理器实例 |
| `stateMachine` | StateMachine | 状态机实例 |
| `pluginManager` | PluginManager | 插件管理器实例 |
| `animes` | dict[str, anime.Anime] | 动画字典，键为动画名 |
| `currentAnime` | anime.Anime \| None | 当前正在播放的动画 |
| `collisions` | dict[str, QRect] | 碰撞体字典，键为碰撞体名 |
| `dialogMenu` | DialogMenu | 对话面板 |
| `stateMenu` | StateMenu | 状态面板 |
| `actionMenu` | ActionMenu | 行动面板 |
| `settingMenu` | SettingMenu | 设置面板 |
| `state` | str | 当前状态（property，可读写） |
| `currentAct` | Plugin \| None | 当前正在运行的非自启动插件（property，只读） |

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `replyed(str, str, str)` | 宠物回复时发射，携带 `(kind, stateName/question, reply)` |
| `stateChanged(str, str)` | 状态切换时发射，携带 `(prevState, currentState)` |
| `aboutToQuit()` | 桌宠即将退出时发射 |

#### 方法 __init__()

```python
def __init__(self, name: str)
```

初始化桌宠窗口。

- **参数**
  - `name`: 桌宠名称
- **说明**
  - 设置无边框及透明背景
  - 创建图片标签、上下文菜单和主布局
  - 初始化配置管理器、状态机和插件管理器
  - 加载所有插件并启动自启动插件
  - 根据配置创建动画和碰撞体
  - 安装事件过滤器并调用 `bind()` 绑定信号

#### 方法 bind() -> None

绑定子窗口及信号。

- **说明**
  - 创建 `DialogMenu`、`StateMenu`、`ActionMenu`、`SettingMenu` 实例
  - 绑定 `settingMenu.dataUpdated` 到 `updateData`
  - 绑定上下文菜单动作到对应子窗口的 `show` 方法
  - 退出动作在默认桌宠模式下调用 `QApplication.quit`，否则调用 `close`
  - 绑定状态机的 `stateChanged` 和 `stateUndefined` 信号
  - 绑定插件管理器的 `pluginLoadSucceeded` 和 `pluginError` 信号
  - 绑定所有动画的 `loadError` 信号

#### 方法 operateState() -> None

```python
def operateState(self, state: str, anime: str, isContinue: bool = False, isAsync: bool = True) -> None
```

执行对应行动时进行响应。

- **参数**
  - `state`: 目标状态名
  - `anime`: 动画名，通常与状态名一致
  - `isContinue`: 是否继续播放当前动画（不重置索引），默认 `False`
  - `isAsync`: 是否异步播放，默认 `True`
- **行为**
  - 若状态与当前状态不同，更新状态机状态
  - 调用 `replyState` 显示状态反馈文本
  - 调用 `changeAnime` 切换动画

#### 方法 changeState() -> None

```python
def changeState(self, state: str) -> None
```

更新状态（不切换动画、不显示反馈文本）。

- **参数**
  - `state`: 目标状态名
- **行为**
  - 若状态与当前状态不同，则更新状态机

#### 方法 replyState() -> None

```python
def replyState(self, state: str) -> None
```

回复状态。

- **参数**
  - `state`: 状态名
- **行为**
  - 从 `config.state` 中随机选取一条反馈文本
  - 若有回复，则调用 `dialogMenu.addLine` 显示
  - 发射 `replyed` 信号

#### 方法 changeAnime() -> None

```python
def changeAnime(self, name: str, isContinue: bool = False, isAsync: bool = True) -> None
```

切换动画。

- **参数**
  - `name`: 动画名
  - `isContinue`: 是否继续播放当前动画，默认 `False`
  - `isAsync`: 是否异步播放，默认 `True`
- **说明**
  - 若动画名不存在则不做任何操作
  - 若当前有动画播放，先调用 `over()` 结束
  - 设置 `currentAnime` 并调用 `play()`

#### 方法 startAct() -> None

```python
def startAct(self, id: str) -> None
```

执行行动（插件）。

- **参数**
  - `id`: 插件 ID
- **行为**
  - 若插件存在且插件状态与当前状态不同
  - 设置 `pluginManager.currentPlugin` 为对应插件
  - 更新状态机状态为插件状态

#### 方法 stopAct() -> None

```python
def stopAct(self, id: str) -> None
```

停止行动（插件）。

- **参数**
  - `id`: 插件 ID

#### 方法 getAct() -> Plugin | None

```python
def getAct(self, id: str) -> Plugin | None
```

获取指定插件实例。

- **参数**
  - `id`: 插件 ID
- **返回**
  - 插件实例，若不存在则返回 `None`

#### 方法 closeEvent()

```python
def closeEvent(self, event) -> None
```

窗口关闭事件处理。

- **行为**
  1. 停止所有自启动插件
  2. 停止所有动画定时器并断开信号
  3. 清空插件管理器
  4. 断开状态机和设置面板的信号
  5. 删除所有子窗口
  6. 删除动画对象
  7. 清空碰撞体
  8. 删除状态机和配置管理器
  9. 从 `MainWindow.pets` 中移除自身（非默认模式）
  10. 写入退出日志
  11. 发射 `aboutToQuit` 信号
  12. 调用 `deleteLater()` 删除自身
  13. 接受关闭事件

#### 槽函数 onStateChanged() -> None

```python
def onStateChanged(self, prevState: str, currentState: str) -> None
```

状态切换槽函数。

- **参数**
  - `prevState`: 前一个状态
  - `currentState`: 当前状态
- **行为**
  - 调用 `stateMenu.log` 记录状态变更日志
  - 发射 `stateChanged` 信号

#### 槽函数 updateData() -> None

```python
def updateData(self) -> None
```

更新数据槽函数。

- **行为**
  - 重新加载所有动画
  - 重新加载所有碰撞体
  - 调用 `dialogMenu.resetQuesSelecter()` 重置问题选择器
  - 记录数据更新日志

---

### 类 DialogMenu(QWidget)

对话面板，用户通过此面板向宠物提问并查看回复。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `_petWindow` | PetWindow | 宿主桌宠窗口 |
| `lyt` | QVBoxLayout | 主布局 |
| `sendLyt` | QHBoxLayout | 发送区布局 |
| `quesSelecter` | QComboBox | 问题选择器 |
| `sendBtn` | QPushButton | 发送按钮 |
| `replyBox` | QTextEdit | 回复显示框（只读） |
| `replyBox.clearAct` | QAction | 清空回复框的上下文菜单动作 |

#### 方法 __init__()

```python
def __init__(self, petWindow: PetWindow)
```

初始化对话面板。

- **参数**
  - `petWindow`: 宿主桌宠窗口
- **说明**
  - 设置窗口标题为 "Dialog Menu"，大小为 400x200
  - 创建问题选择器、发送按钮和回复显示框
  - 为回复框添加上下文菜单"清空"动作
  - 调用 `resetQuesSelecter()` 初始化问题
  - 调用 `bind()` 绑定信号

#### 方法 bind() -> None

绑定信号与槽。

- **说明**
  - 绑定发送按钮到 `reply` 槽函数
  - 绑定清空动作到 `replyBox.clear`

#### 方法 resetQuesSelecter() -> None

重置问题选择器。

- **行为**
  - 清空选择器
  - 从 `config.dialog` 中随机选取 `quesSelecter-item-count` 个问题填充

#### 方法 addLine() -> None

```python
def addLine(self, content: str) -> None
```

向回复框添加一行内容。

- **参数**
  - `content`: 要添加的内容
- **说明**
  - 若内容非空，追加到回复框末尾

#### 槽函数 reply() -> None

```python
def reply(self) -> None
```

发送当前选中的问题并显示回复。

- **行为**
  - 获取当前选中的问题
  - 调用 `conv.replyText("dialog", question, configManager)` 获取回复
  - 将问答写入回复框
  - 发射 `_petWindow.replyed` 信号
  - 从选择器中移除已用问题
  - 从未使用的问题中随机补充一个新问题

---

### 类 StateMenu(QWidget)

状态面板，显示日志和插件传入的页面。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `config` | ConfigManager | 配置管理器实例 |
| `pages` | dict[str, QWidget] | 插件传入的页面字典 |
| `lyt` | QVBoxLayout | 主布局 |
| `tabW` | QTabWidget | 标签页容器 |
| `logBox` | QPlainTextEdit | 日志显示框（只读） |
| `clearAct` | QAction | 清空日志的上下文菜单动作 |

#### 方法 __init__()

```python
def __init__(self, config: ConfigManager)
```

初始化状态面板。

- **参数**
  - `config`: 配置管理器实例
- **说明**
  - 设置窗口标题为 "State Menu"，大小为 400x300
  - 创建标签页容器和日志显示框
  - 为日志框添加上下文菜单"清空"动作
  - 调用 `bind()` 绑定信号

#### 方法 bind() -> None

绑定信号与槽。

- **说明**
  - 绑定清空动作到 `logBox.clear`

#### 方法 log() -> None

```python
def log(self, text: str, type: LogType = None) -> None
```

添加日志到日志框并写入日志文件。

- **参数**
  - `text`: 日志内容
  - `type`: 日志类型，默认 `None`
- **行为**
  - 格式化日志行：`{时间}  {类型}:    {文本}`
  - 追加到 `logBox`
  - 写入 `{config.path}/log.log`

#### 方法 addPage() -> None

```python
def addPage(self, page: QWidget, label: str) -> None
```

添加插件页面。

- **参数**
  - `page`: 页面控件
  - `label`: 页面标签
- **说明**
  - 将页面存入 `pages` 字典并添加到标签页容器

#### 方法 getPage() -> QWidget | None

```python
def getPage(self, label: str) -> QWidget | None
```

获取插件页面。

- **参数**
  - `label`: 页面标签
- **返回**
  - 页面控件，若不存在则返回 `None`

---

### 类 ActionMenu(QWidget)

行动面板，列出所有非自启动插件，提供执行和结束按钮。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `_petWindow` | PetWindow | 宿主桌宠窗口 |
| `lyt` | QVBoxLayout | 主布局 |
| `actLyt` | QVBoxLayout | 行动列表布局 |
| `hl` | dict[str, QHBoxLayout] | 行动行布局字典，键为插件 ID |
| `lb` | dict[str, QLabel] | 行动名称标签字典，键为插件 ID |
| `actBtn` | dict[str, QPushButton] | 行动执行按钮字典，键为插件 ID |
| `stopBtn` | QPushButton | 结束按钮 |

#### 方法 __init__()

```python
def __init__(self, petWindow: PetWindow)
```

初始化行动面板。

- **参数**
  - `petWindow`: 宿主桌宠窗口
- **说明**
  - 设置窗口大小为 400x300
  - 遍历 `pluginManager.plugins`，跳过自启动插件
  - 为每个非自启动插件创建名称标签、执行按钮和行布局
  - 创建"结束"按钮
  - 调用 `bind()` 绑定信号

#### 方法 bind() -> None

绑定信号与槽。

- **说明**
  - 为每个非自启动插件的执行按钮绑定到 `_petWindow.startAct(id)`
  - 为结束按钮绑定停止当前行动的逻辑：若 `currentAct` 存在，调用 `_petWindow.stopAct(currentAct.id)`

---

### 类 SettingMenu(QWidget)

设置面板，提供桌宠配置的可视化编辑界面。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `config` | ConfigManager | 配置管理器实例 |
| `pages` | list[WidgetFactory] | 设置界面自带的页面列表 |
| `otherPages` | dict[str, QWidget] | 插件传入的页面字典 |
| `lyt` | QVBoxLayout | 主布局 |
| `tabW` | QTabWidget | 标签页容器 |
| `btnLyt` | QHBoxLayout | 按钮布局 |
| `applyBtn` | QPushButton | 应用按钮 |
| `cancelBtn` | QPushButton | 取消按钮 |

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `dataUpdated()` | 数据更新时发射 |
| `updateCancelled()` | 更新取消时发射 |
| `saveError(str)` | 保存失败时发射，携带错误信息 |

#### 方法 __init__()

```python
def __init__(self, config: ConfigManager)
```

初始化设置面板。

- **参数**
  - `config`: 配置管理器实例
- **说明**
  - 设置窗口标题为 "Setting Menu"，大小为 600x450
  - 调用 `initPages()` 初始化五个标签页
  - 创建"应用"和"取消"按钮
  - 调用 `bind()` 绑定信号

#### 方法 initPages() -> None

初始化设置界面自带的页面。

- **说明**
  - 依次创建五个标签页：
    - 基础项（`FormFactory`，`config.base`）
    - 动画（`FormBoxFactory`，`config.anime`）
    - 碰撞体（`FormBoxFactory`，`config.collision`）
    - 状态反馈文本（`ListBoxFactory`，`config.state`）
    - 对话文本（`ListBoxFactory`，`config.dialog`）
  - 每个页面构建后添加到标签页容器

**设置页面结构**：

| 标签页 | 工厂类 | 数据来源 |
| :--- | :--- | :--- |
| 基础项 | `FormFactory` | `config.base` |
| 动画 | `FormBoxFactory` | `config.anime` |
| 碰撞体 | `FormBoxFactory` | `config.collision` |
| 状态反馈文本 | `ListBoxFactory` | `config.state` |
| 对话文本 | `ListBoxFactory` | `config.dialog` |

#### 方法 bind() -> None

绑定信号与槽。

- **说明**
  - 绑定「应用」按钮到 `apply` 槽函数
  - 绑定「取消」按钮到 `cancel` 槽函数
  - 绑定 `config.saveError` 到 `saveError` 信号

#### 方法 apply() -> None

应用设置更改。

- **行为**
  - 从五个页面收集数据
  - 更新 `config` 的 `base`、`anime`、`collision`、`state`、`dialog` 属性
  - 调用 `config.saveConfig(ConfigManager.SaveMode.Common)` 保存到文件
  - 发射 `dataUpdated` 信号
  - 关闭窗口

#### 方法 cancel() -> None

取消设置更改。

- **行为**
  - 从 `config` 重新加载数据到五个页面
  - 发射 `updateCancelled` 信号
  - 关闭窗口

#### 方法 addPage() -> None

```python
def addPage(self, page: QWidget, label: str) -> None
```

添加插件页面。

- **参数**
  - `page`: 页面控件
  - `label`: 页面标签
- **说明**
  - 将页面存入 `otherPages` 字典并添加到标签页容器

#### 方法 getPage() -> QWidget | None

```python
def getPage(self, label: str) -> QWidget | None
```

获取插件页面。

- **参数**
  - `label`: 页面标签
- **返回**
  - 页面控件，若不存在则返回 `None`
