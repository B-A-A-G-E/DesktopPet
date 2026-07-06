# 桌面宠物 API

## 目录
- [桌面宠物 API](#桌面宠物-api)
  - [目录](#目录)
  - [概述](#概述)
  - [模块 tool.anime](#模块-toolanime)
    - [函数 getPixNames(folderPath: str) -> list[str]](#函数-getpixnamesfolderpath-str---liststr)
    - [函数 fitImgSize(window: QWidget, widget: QLabel) -> None](#函数-fitimgsizewindow-qwidget-widget-qlabel---none)
    - [函数 showLoadFailedMsg(window: QWidget, widget: QLabel, path: str = "") -> None](#函数-showloadfailedmsgwindow-qwidget-widget-qlabel-path-str----none)
    - [类 Anime(QObject)](#类-animeqobject)
      - [信号](#信号)
      - [初始化 __init__(path: str, fps: int, loop: bool, window: QWidget, widget: QLabel)](#初始化-__init__path-str-fps-int-loop-bool-window-qwidget-widget-qlabel)
      - [方法 play(isContinue: bool = False, isAsync: bool = True) -> None](#方法-playiscontinue-bool--false-isasync-bool--true---none)
      - [方法 stop() -> None](#方法-stop---none)
      - [方法 over() -> None](#方法-over---none)
      - [方法 replay() -> None](#方法-replay---none)
      - [槽函数 nextImg() -> None](#槽函数-nextimg---none)
  - [模块 tool.conv](#模块-toolconv)
    - [函数 replyText(type: str, act: str) -> str](#函数-replytexttype-str-act-str---str)
  - [模块 tool.data](#模块-tooldata)
    - [全局变量](#全局变量)
    - [枚举 LogType](#枚举-logtype)
    - [函数 loadData() -> None](#函数-loaddata---none)
  - [模块 tool.mouse](#模块-toolmouse)
    - [函数 getCollision(widget: QWidget, pos: QPoint) -> str | None](#函数-getcollisionwidget-qwidget-pos-qpoint---str--none)
  - [模块 tool.plugin](#模块-toolplugin)
    - [类 Plugin(QObject)](#类-pluginqobject)
      - [属性](#属性)
      - [方法 setup(window: PetWindow) -> None](#方法-setupwindow-petwindow---none)
      - [方法 teardown() -> None](#方法-teardown---none)
      - [方法 start() -> None](#方法-start---none)
      - [方法 stop() -> None](#方法-stop---none)
      - [方法 eventFilter(obj, event: QEvent) -> bool](#方法-eventfilterobj-event-qevent---bool)
  - [窗口类](#窗口类)
    - [ActionMenu](#actionmenu)
      - [关键属性](#关键属性)
    - [DialogMenu](#dialogmenu)
      - [关键方法](#关键方法)
    - [StateMenu](#statemenu)
      - [关键方法](#关键方法-1)
    - [SettingMenu](#settingmenu)
      - [信号](#信号-1)
      - [关键方法](#关键方法-2)
    - [PetWindow](#petwindow)
      - [核心方法 replyState(state: str, afterEvent: bool = False, isContinue: bool = False, isAsync: bool = True) -> None](#核心方法-replystatestate-str-afterevent-bool--false-iscontinue-bool--false-isasync-bool--true---none)
      - [核心方法 changeState(state: str) -> None](#核心方法-changestatestate-str---none)
      - [核心方法 changeAnime(state: str, afterEvent: bool = False, isContinue: bool = False, isAsync: bool = True) -> None](#核心方法-changeanimestate-str-afterevent-bool--false-iscontinue-bool--false-isasync-bool--true---none)
      - [核心方法 loadPlugins() -> None](#核心方法-loadplugins---none)
      - [核心方法 act(id: str) -> None](#核心方法-actid-str---none)
      - [核心方法 stopAct() -> None](#核心方法-stopact---none)
      - [核心方法 updateData() -> None](#核心方法-updatedata---none)
      - [信号](#信号-2)
      - [属性](#属性-1)

---

## 概述

本文档描述桌面宠物程序的核心 API，涵盖工具模块、窗口类和自定义扩展接口。所有 API 均基于 PySide6 实现。

---

## 模块 tool.anime

动画播放引擎，负责帧序列的加载、播放控制和窗口自适应。

### 函数 getPixNames(folderPath: str) -> list[str]

获取指定文件夹内所有纯数字命名的图片文件名（不含扩展名），并按数字升序排序。

- **参数**
  - `folderPath`: 文件夹路径
- **返回**
  - 排序后的文件名列表，如 `["0", "1", "2"]`
- **说明**
  - 自动过滤非纯数字命名的文件
  - 文件名示例：`0.png`、`1.jpg` 等

### 函数 fitImgSize(window: QWidget, widget: QLabel) -> None

将窗口和标签控件调整为当前图片的尺寸。

- **参数**
  - `window`: 父窗口
  - `widget`: 存放图片的 QLabel
- **说明**
  - 若图片加载失败，自动调用 `showLoadFailedMsg`

### 函数 showLoadFailedMsg(window: QWidget, widget: QLabel, path: str = "") -> None

显示图片加载失败的错误对话框，并提供恢复选项。

- **参数**
  - `window`: 父窗口
  - `widget`: 存放图片的 QLabel
  - `path`: 尝试加载的文件路径（用于错误提示）
- **行为**
  - 点击「确定」：加载占位图，窗口调整为 200x200
  - 点击「关闭」：关闭窗口

### 类 Anime(QObject)

动画播放器，支持异步定时器播放和同步阻塞播放两种模式。

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `finished()` | 一轮动画播放完成（仅非循环模式） |
| `overed()` | 动画播放结束（停止或完成） |
| `loadErr(str)` | 加载帧图片失败时，携带错误信息 |

#### 初始化 __init__(path: str, fps: int, loop: bool, window: QWidget, widget: QLabel)

- **参数**
  - `path`: 帧图片所在文件夹路径
  - `fps`: 播放帧率
  - `loop`: 是否循环播放
  - `window`: 父窗口
  - `widget`: 用于显示图片的 QLabel

#### 方法 play(isContinue: bool = False, isAsync: bool = True) -> None

开始或继续播放动画。

- **参数**
  - `isContinue`: 是否从上一次停止位置继续播放
  - `isAsync`: 是否异步播放（定时器驱动）；若为 `False`，则同步阻塞播放

#### 方法 stop() -> None

暂停播放（保留当前帧位置）。

#### 方法 over() -> None

停止播放并重置索引为 0，发射 `overed` 信号。

#### 方法 replay() -> None

重置索引并从当前帧率重新开始播放。

#### 槽函数 nextImg() -> None

播放下一帧，由定时器驱动触发。

- **行为**
  - 加载并显示当前索引对应的图片
  - 索引自增，到达末尾时根据 `loop` 决定重置或停止

---

## 模块 tool.conv

对话回复生成器，从配置中随机选取回复文本。

### 函数 replyText(type: str, act: str) -> str

根据类型和动作名从 `data.state` 或 `data.dialog` 中随机选取一条回复。

- **参数**
  - `type`: 类型，可选 `"state"` 或 `"dialog"`
  - `act`: 动作/状态名或问题键名
- **返回**
  - 随机选取的回复文本；若未匹配则返回空字符串

---

## 模块 tool.data

数据加载与全局配置管理。

### 全局变量

| 变量 | 类型 | 数据来源 |
| :--- | :--- | :--- |
| `base` | dict | `./data/base.json` |
| `anime` | dict | `./data/anime.json` |
| `collision` | dict | `./data/collision.json` |
| `state` | dict | `./data/state.json` |
| `dialog` | dict | `./data/dialog.json` |
| `actPath` | dict | `./data/plugin.json` |

### 枚举 LogType

日志类型枚举，用于标识日志条目类别。

| 成员 | 值 | 说明 |
| :--- | :--- | :--- |
| `Error` | 0 | 错误信息 |
| `Entre` | 1 | 入场事件 |
| `Exit` | 2 | 退场事件 |
| `Set` | 3 | 设置更新事件 |
| `StateChange` | 4 | 状态切换事件 |
| `PluginLoaded` | 5 | 插件加载事件 |

### 函数 loadData() -> None

加载所有 JSON 配置文件到全局变量。

- **说明**
  - 模块导入时自动执行
  - 文件路径固定为 `./data/` 目录下

---

## 模块 tool.mouse

鼠标交互辅助函数。

### 函数 getCollision(widget: QWidget, pos: QPoint) -> str | None

检测鼠标点击位置是否落在 `widget.collisions` 中定义的某个碰撞体内。

- **参数**
  - `widget`: 包含 `collisions` 属性的窗口对象（通常为 `PetWindow`）
  - `pos`: 相对于 `widget` 的点击位置
- **返回**
  - 命中状态名（键名），若未命中则返回 `None`
- **说明**
  - `collisions` 格式：`{ "状态名": QRect, ... }`

---

## 模块 tool.plugin

插件基类，用于实现自定义行动。

### 类 Plugin(QObject)

所有自定义行动插件须继承此类并重写 `start` 和 `stop` 方法。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `id` | str | 插件唯一标识，应与文件名一致 |
| `name` | str | 在行动面板显示的名称 |
| `description` | str | 插件描述，用于行动面板的鼠标悬浮提示 |
| `auto` | bool | 是否在程序启动时自动运行，默认为 `False` |
| `_window` | PetWindow \| None | 关联的主窗口实例（内部使用，通过 `window()` 访问） |

#### 方法 setup(window: PetWindow) -> None

插件安装，将插件与主窗口关联并安装事件过滤器。

- **参数**
  - `window`: 主窗口实例
- **说明**
  - 由 `PetWindow.loadPlugins` 自动调用，无需手动调用

#### 方法 teardown() -> None

插件卸载，移除事件过滤器并解除与主窗口的关联。

#### 方法 start() -> None

开始行动。

- **说明**
  - **必须重写**
  - 在此实现行动开始时的逻辑（如切换动画、播放回复等）
  - 可通过 `self.window()` 访问主窗口的公开方法

#### 方法 stop() -> None

停止行动。

- **说明**
  - **必须重写**
  - 在此实现行动结束时的清理逻辑
- **注意**
  - 不需要在 `stop` 中手动切回待机状态（行动结束时会自动切换）

#### 方法 eventFilter(obj, event: QEvent) -> bool

事件过滤器，用于捕获并处理窗口事件。

- **参数**
  - `obj`: 事件目标对象
  - `event`: 事件对象
- **返回**
  - `True` 表示事件已被处理，不再传递；`False` 表示继续传递
- **说明**
  - 默认返回 `False`，子类可按需重写
  - 事件过滤器的安装和卸载由基类的 `setup`/`teardown` 自动处理

---

## 窗口类

### ActionMenu

行动面板，显示 `data.actPath` 中注册的所有自定义行动按钮。

#### 关键属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `actBtn` | dict | 键为动作 ID，值为对应的 `QPushButton` |
| `stopBtn` | QPushButton | 停止按钮 |
| `lb` | dict | 键为动作 ID，值为对应的 `QLabel`（显示插件名称） |

- **说明**
  - 插件名称显示在 `QLabel` 中，鼠标悬浮时显示 `description` 作为提示

### DialogMenu

对话面板，随机展示问题列表，用户选择后随机回复。

#### 关键方法

| 方法 | 说明 |
| :--- | :--- |
| `resetQuesSelecter()` | 从 `data.dialog` 中随机抽取指定数量的问题填充下拉框 |
| `addLine(content: str)` | 向回复框追加一行文本 |

- **行为**
  - 提问后自动从列表中移除该问题，并从剩余问题中随机补充

### StateMenu

状态日志面板，显示运行日志并支持写入文件。

#### 关键方法

| 方法 | 说明 |
| :--- | :--- |
| `log(text: str, type: LogType = None)` | 添加日志条目，格式为 `时间  LogType.xxx:    文本` |

### SettingMenu

设置面板，可视化编辑所有 JSON 配置文件。

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `dataUpdated()` | 应用配置后发射，用于通知主窗口刷新数据 |

#### 关键方法

| 方法 | 说明 |
| :--- | :--- |
| `apply()` | 读取所有输入框内容，更新 `data` 全局变量并写回 JSON 文件 |
| `cancel()` | 关闭窗口，不保存更改 |

### PetWindow

主窗口（宠物本体），集成动画、状态机、碰撞检测、拖拽移动等核心功能。

#### 核心方法 replyState(state: str, afterEvent: bool = False, isContinue: bool = False, isAsync: bool = True) -> None

执行状态切换响应，包含回复文本、切换动画和更新状态。

- **参数**
  - `state`: 目标状态名
  - `afterEvent`: 是否先播放当前状态的 `after-{state}` 后续动画（仅同步模式）
  - `isContinue`: 切换动画时是否从上一次停止位置继续
  - `isAsync`: 动画是否异步播放
- **行为**
  - 调用 `conv.replyText("state", state)` 获取回复并写入对话面板
  - 调用 `changeAnime` 切换动画
  - 调用 `changeState` 更新状态

#### 核心方法 changeState(state: str) -> None

更新状态并管理计时器（闲置计时器和随机移动计时器）。

- **行为**
  - 非 `idle` 状态：停止所有闲置计时器
  - `idle` 状态：启动闲置计时器和随机移动计时器
  - 记录状态变更日志

#### 核心方法 changeAnime(state: str, afterEvent: bool = False, isContinue: bool = False, isAsync: bool = True) -> None

切换动画，停止当前动画并播放目标动画。

- **参数**
  - 同 `replyState`
- **说明**
  - 若 `afterEvent` 为 True，在切换前尝试播放 `after-{当前状态}` 动画（同步阻塞）

#### 核心方法 loadPlugins() -> None

加载 `data.actPath` 中注册的所有插件。

- **行为**
  - 遍历 `actPath`，导入模块并实例化 `Plugin` 子类
  - 普通插件存入 `self.acts`，自动插件存入 `self.autoActs` 并立即启动
  - 发射 `pluginLoadSucceeded`、`pluginInheritError` 或 `pluginLoadFailed` 信号

#### 核心方法 act(id: str) -> None

执行指定 ID 的行动。

- **参数**
  - `id`: 插件 ID
- **行为**
  - 停止当前正在运行的行动
  - 安装新插件并调用其 `start` 方法

#### 核心方法 stopAct() -> None

停止当前正在运行的行动，切换回 `idle` 状态。

#### 核心方法 updateData() -> None

重新加载配置数据并刷新动画和碰撞体。

- **说明**
  - 由 `SettingMenu.dataUpdated` 信号触发调用

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `pluginLoadSucceeded(str)` | 插件加载成功，携带插件 ID |
| `pluginInheritError(str)` | 插件未继承 Plugin 基类，携带错误信息 |
| `pluginLoadFailed(str)` | 插件加载失败，携带异常信息 |

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `state` | str | 当前状态 |
| `animes` | dict | 动画对象字典，键为状态名 |
| `collisions` | dict | 碰撞体字典，键为状态名 |
| `acts` | dict | 普通插件字典，键为插件 ID |
| `autoActs` | dict | 自动启动插件字典，键为插件 ID |
| `currentAct` | Plugin \| None | 当前正在运行的插件 |

> ### 详细教程请参阅 [customization.md](./customization.md)。