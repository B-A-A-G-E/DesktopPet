# 桌面宠物 API（宠物本体）

## 目录
- [桌面宠物 API（宠物本体）](#桌面宠物-api宠物本体)
  - [目录](#目录)
  - [概述](#概述)
  - [窗口类](#窗口类)
    - [PetWindow](#petwindow)
      - [信号](#信号)
      - [属性](#属性)
      - [属性（Property）](#属性property)
      - [方法 \_\_init__()](#方法-__init__)
      - [核心方法 operateState()](#核心方法-operatestate)
      - [核心方法 changeState()](#核心方法-changestate)
      - [核心方法 replyState()](#核心方法-replystate)
      - [核心方法 changeAnime()](#核心方法-changeanime)
      - [核心方法 startAct()](#核心方法-startact)
      - [核心方法 stopAct()](#核心方法-stopact)
      - [核心方法 getAct()](#核心方法-getact)
      - [槽函数 updateData()](#槽函数-updatedata)
      - [槽函数 onStateChanged()](#槽函数-onstatechanged)
      - [方法 bind()](#方法-bind)
      - [方法 closeEvent()](#方法-closeevent)
    - [ActionMenu](#actionmenu)
      - [属性](#属性-1)
      - [方法 \_\_init__()](#方法-__init__-1)
      - [方法 bind()](#方法-bind-1)
    - [DialogMenu](#dialogmenu)
      - [属性](#属性-2)
      - [方法 \_\_init__()](#方法-__init__-2)
      - [方法 resetQuesSelecter()](#方法-resetquesselecter)
      - [方法 addLine()](#方法-addline)
      - [槽函数 addNewOption()](#槽函数-addnewoption)
    - [StateMenu](#statemenu)
      - [属性](#属性-3)
      - [方法 \_\_init__()](#方法-__init__-3)
      - [方法 log()](#方法-log)
      - [方法 addPage()](#方法-addpage)
      - [方法 getPage()](#方法-getpage)
    - [SettingMenu](#settingmenu)
      - [信号](#信号-1)
      - [属性](#属性-4)
      - [方法 \_\_init__()](#方法-__init__-4)
      - [方法 initPages()](#方法-initpages)
      - [方法 apply()](#方法-apply)
      - [方法 cancel()](#方法-cancel)
      - [方法 addPage()](#方法-addpage-1)
      - [方法 getPage()](#方法-getpage-1)

---

## 概述

本文档描述桌面宠物程序的窗口类 API，涵盖宠物主窗口及各子面板。工具模块（`tool/`）的 API 请参阅 [API-tool.md](./API-tool.md)。

---

## 窗口类

### PetWindow

主窗口（宠物本体），集成动画、状态机、碰撞检测、拖拽移动等核心功能。

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `stateChanged(str, str)` | 状态变更时发射，携带前一状态名和新状态名 |
| `aboutToQuit()` | 程序即将退出时发射 |

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `name` | str | 宠物名称 |
| `imgLb` | QLabel | 显示宠物图片的标签 |
| `mainlayout` | QVBoxLayout | 主布局 |
| `animes` | dict[str, Anime] | 动画对象字典，键为状态名 |
| `collisions` | dict[str, QRect] | 碰撞体字典，键为碰撞体名 |
| `currentAnime` | Anime | 当前正在播放的动画对象 |
| `configManager` | ConfigManager | 配置管理器实例 |
| `stateMachine` | StateMachine | 状态机实例 |
| `pluginManager` | PluginManager | 插件管理器实例 |
| `dialogMenu` | DialogMenu | 对话面板实例 |
| `stateMenu` | StateMenu | 状态日志面板实例 |
| `actionMenu` | ActionMenu | 行动面板实例 |
| `settingMenu` | SettingMenu | 设置面板实例 |

#### 属性（Property）

| 属性 | 类型 | 可访问性 | 说明 |
| :--- | :--- | :--- | :--- |
| `state` | str | 读写（getter/setter） | 获取或设置当前状态，通过 setter 调用 `stateMachine.currentState` |
| `currentAct` | Plugin \| None | 只读（getter） | 获取当前正在运行的非自启动插件，通过 `pluginManager.currentPlugin` |

#### 方法 __init__()

```python
def __init__(self, name: str, petPath: str)
```

初始化宠物主窗口。

- **参数**
  - `name`: 宠物名称
  - `petPath`: 宠物资源包路径
- **说明**
  - 设置无边框透明窗口（`FramelessWindowHint` + `WA_TranslucentBackground`）
  - 创建 `ConfigManager` 实例
  - 创建 `StateMachine` 实例（状态列表从 `config.state` 获取）
  - 创建 `PluginManager` 实例并加载所有插件
  - 从配置构建动画对象和碰撞体
  - 安装事件过滤器并启用鼠标跟踪
  - 调用 `bind()` 绑定信号
  - 启动所有自启动插件

#### 核心方法 operateState()

```python
def operateState(state: str, anime: str, isContinue: bool = False, isAsync: bool = True) -> None
```

执行状态切换响应，包含回复文本、切换动画和更新状态。

- **参数**
  - `state`: 目标状态名
  - `anime`: 要播放的动画名（通常与状态名一致）
  - `isContinue`: 切换动画时是否从上一次停止位置继续
  - `isAsync`: 动画是否异步播放
- **行为**
  - 若当前状态与目标状态不同，则调用 `stateMachine.currentState = state` 更新状态
  - 调用 `replyState(state)` 获取并显示回复
  - 调用 `changeAnime(anime, isContinue, isAsync)` 切换动画

#### 核心方法 changeState()

```python
def changeState(state: str) -> None
```

仅更新状态，不触发回复和动画切换。

- **参数**
  - `state`: 目标状态名
- **行为**
  - 若当前状态与目标状态不同，调用 `stateMachine.currentState = state` 更新状态

#### 核心方法 replyState()

```python
def replyState(state: str) -> None
```

仅显示状态回复文本，不切换状态和动画。

- **参数**
  - `state`: 状态名
- **行为**
  - 调用 `conv.replyText("state", state, configManager)` 获取随机回复
  - 通过 `dialogMenu.addLine` 写入对话面板

#### 核心方法 changeAnime()

```python
def changeAnime(name: str, isContinue: bool = False, isAsync: bool = True) -> None
```

切换动画，停止当前动画并播放目标动画。

- **参数**
  - `name`: 目标动画名（须在 `config.anime` 中定义）
  - `isContinue`: 是否从上一次停止位置继续
  - `isAsync`: 动画是否异步播放
- **说明**
  - 若目标动画名存在，则调用 `currentAnime.over()` 停止当前动画
  - 更新 `currentAnime` 并调用 `play()` 开始播放

#### 核心方法 startAct()

```python
def startAct(id: str) -> None
```

执行指定 ID 的行动。

- **参数**
  - `id`: 插件 ID
- **行为**
  - 通过 `pluginManager.getPlugin(id)` 获取插件实例
  - 若插件存在且其状态不等于当前状态，则：
    - 通过 `pluginManager.currentPlugin = act` 切换当前插件
    - 通过 `stateMachine.currentState = act.state` 更新状态

#### 核心方法 stopAct()

```python
def stopAct(id: str) -> None
```

停止指定 ID 的行动。

- **参数**
  - `id`: 插件 ID
- **行为**
  - 调用 `pluginManager.stopPlugin(id)` 停止指定插件

#### 核心方法 getAct()

```python
def getAct(id: str) -> Plugin | None
```

根据 ID 获取插件实例。

- **参数**
  - `id`: 插件 ID
- **返回**
  - 插件实例，若未找到则返回 `None`

#### 槽函数 updateData()

```python
@Slot()
def updateData() -> None
```

重新加载配置数据并刷新动画和碰撞体。由 `SettingMenu.dataUpdated` 信号触发调用。

- **说明**
  - 重新从 `config.anime` 构建动画对象
  - 重新从 `config.collision` 构建碰撞体
  - 调用 `dialogMenu.resetQuesSelecter()` 刷新对话选项
  - 向状态日志面板写入 `"Data is updated"` 日志

#### 槽函数 onStateChanged()

```python
@Slot(str, str)
def onStateChanged(prevState: str, currentState: str) -> None
```

状态变更响应槽函数。由 `stateMachine.stateChanged` 信号触发调用。

- **参数**
  - `prevState`: 前一状态名
  - `currentState`: 新状态名
- **行为**
  - 向状态日志面板写入状态变更日志
  - 发射 `stateChanged` 信号

#### 方法 bind()

```python
def bind() -> None
```

绑定子窗口及信号。

- **说明**
  - 创建 `DialogMenu`、`StateMenu`、`ActionMenu`、`SettingMenu` 实例
  - 绑定设置面板的 `dataUpdated` 信号到 `updateData`
  - 绑定右键菜单各动作到对应的面板显示/退出
  - 绑定状态机的 `stateChanged` 和 `stateUndefined` 信号
  - 绑定插件管理器的 `pluginLoadSucceeded` 和 `pluginError` 信号
  - 绑定所有动画的 `loadError` 信号

#### 方法 closeEvent()

```python
def closeEvent(event) -> None
```

窗口关闭事件处理。

- **行为**
  1. 停止所有插件（自启动和非自启动）
  2. 停止所有动画定时器
  3. 清空插件管理器
  4. 断开所有信号连接
  5. 关闭并删除所有子窗口（dialogMenu, stateMenu, actionMenu, settingMenu）
  6. 删除所有动画对象
  7. 清空碰撞体
  8. 删除状态机和配置管理器
  9. 从 `MainWindow.pets` 列表中移除自身
  10. 写入退出日志
  11. 发射 `aboutToQuit` 信号
  12. 调用 `deleteLater()` 释放自身

---

### ActionMenu

行动面板，显示 `config.plugin` 中注册的所有非自启动行动按钮。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `_petWindow` | PetWindow | 关联的宠物主窗口 |
| `lyt` | QVBoxLayout | 主布局 |
| `actLyt` | QVBoxLayout | 行动按钮布局 |
| `hl` | dict[str, QHBoxLayout] | 行动行布局字典 |
| `lb` | dict[str, QLabel] | 行动名称标签字典 |
| `actBtn` | dict[str, QPushButton] | 行动执行按钮字典 |
| `stopBtn` | QPushButton | 停止按钮 |

- **说明**
  - 窗口大小固定为 400x300
  - 插件名称显示在 `QLabel` 中，鼠标悬浮时显示 `description` 作为提示
  - 仅显示 `auto = False` 的插件（自启动插件不会出现在行动面板中）

#### 方法 __init__()

```python
def __init__(self, petWindow)
```

初始化行动面板。

- **参数**
  - `petWindow`: 宠物主窗口实例
- **说明**
  - 遍历 `petWindow.pluginManager.plugins`，为非自启动插件创建行动按钮
  - 添加「结束」按钮用于停止当前行动

#### 方法 bind()

```python
def bind() -> None
```

绑定信号与槽。

- **说明**
  - 每个行动的「执行」按钮连接到 `PetWindow.startAct`
  - 「结束」按钮连接到停止当前行动的逻辑（调用 `PetWindow.stopAct`）

---

### DialogMenu

对话面板，随机展示问题列表，用户选择后随机回复。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `config` | ConfigManager | 配置管理器实例 |
| `quesSelecter` | QComboBox | 问题下拉选择框 |
| `sendBtn` | QPushButton | 发送按钮 |
| `replyBox` | QTextEdit | 回复显示框（只读） |

#### 方法 __init__()

```python
def __init__(self, config: ConfigManager)
```

初始化对话面板。

- **参数**
  - `config`: 配置管理器实例
- **说明**
  - 窗口大小固定为 400x200
  - 回复框支持右键菜单"清空"

#### 方法 resetQuesSelecter()

```python
def resetQuesSelecter() -> None
```

重置问题下拉框。

- **说明**
  - 从 `config.dialog` 中随机抽取指定数量（由 `base["quesSelecter-item-count"]` 决定）的问题填充下拉框

#### 方法 addLine()

```python
def addLine(content: str) -> None
```

向回复框追加一行文本。

- **参数**
  - `content`: 要添加的文本
- **说明**
  - 若 `content` 非空，则在回复框末尾添加新行

#### 槽函数 addNewOption()

```python
@Slot()
def addNewOption() -> None
```

用户点击"发送"按钮时触发。

- **行为**
  - 获取当前选中的问题文本
  - 在回复框显示 "Q: 问题\nA: 回复"
  - 从下拉框中移除该问题
  - 从剩余问题中随机补充一个新问题

---

### StateMenu

状态日志面板，显示运行日志并支持写入文件。同时作为属性面板的容器，允许插件通过 `addPage` 添加自定义标签页。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `config` | ConfigManager | 配置管理器实例 |
| `pages` | dict[str, QWidget] | 插件传入的页面字典 |
| `tabW` | QTabWidget | 标签页容器 |
| `logBox` | QPlainTextEdit | 日志显示框（只读） |

#### 方法 __init__()

```python
def __init__(self, config: ConfigManager)
```

初始化状态面板。

- **参数**
  - `config`: 配置管理器实例
- **说明**
  - 窗口大小固定为 400x300
  - 日志框支持右键菜单"清空"

#### 方法 log()

```python
def log(text: str, type: LogType = None) -> None
```

添加日志条目。

- **参数**
  - `text`: 日志文本
  - `type`: 日志类型（`LogType` 枚举）
- **行为**
  - 格式为 `时间  LogType.xxx/None:    文本`
  - 同时写入日志文件（由 `config.base["log-path"]` 指定）

#### 方法 addPage()

```python
def addPage(page: QWidget, label: str) -> None
```

由插件调用，添加属性/配置页面到状态面板的标签页中。

- **参数**
  - `page`: 页面控件
  - `label`: 标签页标题

#### 方法 getPage()

```python
def getPage(label: str) -> QWidget | None
```

获取已添加的页面。

- **参数**
  - `label`: 标签页标题
- **返回**
  - 页面控件，若未找到则返回 `None`

---

### SettingMenu

设置面板，可视化编辑所有 JSON 配置文件。

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `dataUpdated()` | 应用配置后发射，用于通知刷新数据 |
| `updateCancelled()` | 取消配置后发射 |
| `saveError(str)` | 保存配置失败时发射，携带错误信息 |

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `config` | ConfigManager | 配置管理器实例 |
| `pages` | list[WidgetFactory] | 设置界面自带的页面 |
| `otherPages` | dict[str, QWidget] | 插件传入的页面 |
| `tabW` | QTabWidget | 标签页容器 |
| `applyBtn` | QPushButton | 应用按钮 |
| `cancelBtn` | QPushButton | 取消按钮 |

#### 方法 __init__()

```python
def __init__(self, config: ConfigManager)
```

初始化设置面板。

- **参数**
  - `config`: 配置管理器实例
- **说明**
  - 窗口大小固定为 600x450
  - 调用 `initPages()` 创建内置页面

#### 方法 initPages()

```python
def initPages() -> None
```

初始化设置面板的内置页面。

- **说明**
  - 创建五个标签页：基础项、动画、碰撞体、状态反馈文本、对话文本
  - 使用 `FormFactory`、`FormBoxFactory`、`ListBoxFactory` 构建各标签页

#### 方法 apply()

```python
def apply() -> None
```

应用配置更改。

- **行为**
  - 从所有内置页面收集数据
  - 更新 `ConfigManager` 对应属性
  - 调用 `saveConfig(ConfigManager.SaveMode.Common)` 保存到文件
  - 发射 `dataUpdated()` 信号
  - 关闭设置面板

#### 方法 cancel()

```python
def cancel() -> None
```

取消配置更改。

- **行为**
  - 从 `ConfigManager` 重新加载数据到各页面
  - 发射 `updateCancelled()` 信号
  - 关闭设置面板

#### 方法 addPage()

```python
def addPage(page: QWidget, label: str) -> None
```

由插件调用，添加自定义配置页面到设置面板的标签页中。

- **参数**
  - `page`: 页面控件
  - `label`: 标签页标题

#### 方法 getPage()

```python
def getPage(label: str) -> QWidget | None
```

获取已添加的页面。

- **参数**
  - `label`: 标签页标题
- **返回**
  - 页面控件，若未找到则返回 `None`
