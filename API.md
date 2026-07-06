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
      - [初始化 \_\_init\_\_(path: str, fps: int, loop: bool, window: QWidget, widget: QLabel)](#初始化-__init__path-str-fps-int-loop-bool-window-qwidget-widget-qlabel)
      - [方法 setFps(fps: int) -> None](#方法-setfpsfps-int---none)
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
  - [窗口类](#窗口类)
    - [ActionMenu](#actionmenu)
    - [DialogMenu](#dialogmenu)
    - [StateMenu](#statemenu)
    - [SettingMenu](#settingmenu)
    - [PetWindow](#petwindow)
      - [核心方法 replyState(state: str, afterEvent: bool = False, isContinue: bool = False, isAsync: bool = True) -> None](#核心方法-replystatestate-str-afterevent-bool--false-iscontinue-bool--false-isasync-bool--true---none)
      - [核心方法 changeState(state: str) -> None](#核心方法-changestatestate-str---none)
      - [核心方法 changeAnime(state: str, afterEvent: bool = False, isContinue: bool = False, isAsync: bool = True) -> None](#核心方法-changeanimestate-str-afterevent-bool--false-iscontinue-bool--false-isasync-bool--true---none)
      - [信号槽绑定](#信号槽绑定)
      - [自定义行动接口](#自定义行动接口)

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

#### 初始化 \_\_init\_\_(path: str, fps: int, loop: bool, window: QWidget, widget: QLabel)

- **参数**
  - `path`: 帧图片所在文件夹路径
  - `fps`: 播放帧率
  - `loop`: 是否循环播放
  - `window`: 父窗口
  - `widget`: 用于显示图片的 QLabel

#### 方法 setFps(fps: int) -> None

更新帧率，并同步调整定时器间隔。

#### 方法 play(isContinue: bool = False, isAsync: bool = True) -> None

开始或继续播放动画。

- **参数**
  - `isContinue`: 是否从上一次停止的位置继续（若为 False，则从第 0 帧开始）
  - `isAsync`: 是否异步播放（定时器驱动），若为 False 则同步阻塞播放
- **说明**
  - 同步模式下，使用 `time.sleep` 控制帧率，并调用 `QApplication.processEvents()` 更新界面
  - 同步播放结束时自动发射 `finished` 和 `overed` 信号

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
| `actPath` | dict | `./data/import.json` |

### 枚举 LogType

日志类型枚举，用于标识日志条目类别。

| 成员 | 值 | 说明 |
| :--- | :--- | :--- |
| `Error` | 0 | 错误信息 |
| `Entre` | 1 | 入场事件 |
| `Exit` | 2 | 退场事件 |
| `Set` | 3 | 设置更新事件 |
| `StateChange` | 4 | 状态切换事件 |

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

## 窗口类

### ActionMenu

行动面板，显示 `data.actPath` 中注册的所有自定义行动按钮。

- **属性**
  - `actBtn`: 字典，键为动作名，值为对应的 `QPushButton`
  - `stopBtn`: 停止按钮

### DialogMenu

对话面板，随机展示问题列表，用户选择后随机回复。

- **关键方法**
  - `resetQuesSelecter()`: 从 `data.dialog` 中随机抽取指定数量的问题填充下拉框
  - `addLine(content: str)`: 向回复框追加一行文本
- **行为**
  - 提问后自动从列表中移除该问题，并从剩余问题中随机补充

### StateMenu

状态日志面板，显示运行日志并支持写入文件。

- **关键方法**
  - `log(text: str, type: LogType = None) -> None`: 添加日志条目，格式为 `时间  LogType.xxx:    文本`

### SettingMenu

设置面板，可视化编辑所有 JSON 配置文件。

- **信号**
  - `dataUpdated()`: 应用配置后发射，用于通知主窗口刷新数据
- **关键方法**
  - `apply()`: 读取所有输入框内容，更新 `data` 全局变量并写回 JSON 文件
  - `cancel()`: 关闭窗口，不保存更改

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

#### 信号槽绑定

- `idleTimer.timeout` → 触发 `replyState("idle")`
- `moveTimer.timeout` → 触发 `moveRandomly()` 随机移动
- 上下文菜单触发对应面板的 `show()`
- 动画 `loadErr` 信号 → 写入状态日志

#### 自定义行动接口

行动模块需放置在 `action/` 目录下，并在 `./data/import.json` 中注册。

**注册格式**
```json
{
  "act-事件名": {
    "name": "显示名称",
    "path": "action.模块名"
  }
}
