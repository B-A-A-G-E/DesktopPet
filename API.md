# 桌面宠物 API

## 目录
- [桌面宠物 API](#桌面宠物-api)
  - [目录](#目录)
  - [概述](#概述)
  - [模块 tool.anime](#模块-toolanime)
    - [函数 getPixNames(folderPath: str) -> list[str]](#函数-getpixnamesfolderpath-str---liststr)
    - [函数 fitImgSize(window: QWidget, widget: QLabel) -> None](#函数-fitimgsizewindow-qwidget-widget-qlabel---none)
    - [函数 showLoadFailedMsg(window: QWidget, path: str = "") -> None](#函数-showloadfailedmsgwindow-qwidget-path-str----none)
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
  - [模块 tool.pageFactory](#模块-toolpagefactory)
    - [函数 deleteLyt(lyt: QLayout) -> None](#函数-deletelytlyt-qlayout---none)
    - [函数 clearLyt(lyt: QLayout) -> None](#函数-clearlytlyt-qlayout---none)
    - [函数 getVal(edit: Any, dataType: str) -> Any](#函数-getvaledit-any-datatype-str---any)
    - [函数 setVal(edit: Any, dataType: str, val: Any) -> None](#函数-setvaledit-any-datatype-str-val-any---none)
    - [函数 createEdit(dataType: str) -> QWidget | None](#函数-createeditdatatype-str---qwidget--none)
    - [类 FileSelecter(QWidget)](#类-fileselecterqwidget)
    - [类 RemovableRow(QHBoxLayout)](#类-removablerowqhboxlayout)
    - [类 PageFactory(QWidget)](#类-pagefactoryqwidget)
    - [类 FormFactory(PageFactory)](#类-formfactorypagefactory)
    - [类 DynamicListFactory(PageFactory)](#类-dynamiclistfactorypagefactory)
    - [类 FormBoxFactory(PageFactory)](#类-formboxfactorypagefactory)
    - [类 ListBoxFactory(PageFactory)](#类-listboxfactorypagefactory)
  - [模块 tool.plugin](#模块-toolplugin)
    - [类 Plugin(QObject)](#类-pluginqobject)
      - [属性](#属性)
      - [属性（Property）](#属性property)
      - [信号](#信号-1)
      - [方法 setup(window: PetWindow) -> None](#方法-setupwindow-petwindow---none)
      - [方法 teardown() -> None](#方法-teardown---none)
      - [方法 start() -> None](#方法-start---none)
      - [方法 stop() -> None](#方法-stop---none)
      - [方法 eventFilter(obj, event: QEvent) -> bool](#方法-eventfilterobj-event-qevent---bool)
    - [类 PluginManager(QObject)](#类-pluginmanagerqobject)
      - [信号](#信号-2)
      - [属性](#属性-1)
      - [属性（Property）](#属性property-1)
      - [方法 loadAllPlugins() -> None](#方法-loadallplugins---none)
      - [方法 loadPlugin(id: str) -> Plugin | None](#方法-loadpluginid-str---plugin--none)
      - [方法 sortPlugins() -> list[str]](#方法-sortplugins---liststr)
      - [方法 startAutoPlugins() -> None](#方法-startautoplugins---none)
      - [方法 getPlugin(id: str) -> Plugin | None](#方法-getpluginid-str---plugin--none)
      - [方法 startPlugin(id: str) -> None](#方法-startpluginid-str---none)
      - [方法 stopPlugin(id: str) -> None](#方法-stoppluginid-str---none)
  - [模块 tool.stateMachine](#模块-toolstatemachine)
    - [类 StateMachine(QObject)](#类-statemachineqobject)
      - [信号](#信号-3)
      - [属性](#属性-2)
      - [属性（Property）](#属性property-2)
      - [方法 addState(state: str) -> None](#方法-addstatestate-str---none)
      - [方法 removeState(state: str) -> bool](#方法-removestatestate-str---bool)
  - [窗口类](#窗口类)
    - [ActionMenu](#actionmenu)
      - [关键属性](#关键属性)
    - [DialogMenu](#dialogmenu)
      - [关键方法](#关键方法)
      - [槽函数 addNewOption() -> None](#槽函数-addnewoption---none)
    - [StateMenu](#statemenu)
      - [关键方法](#关键方法-1)
      - [扩展方法](#扩展方法)
    - [SettingMenu](#settingmenu)
      - [信号](#信号-4)
      - [关键方法](#关键方法-2)
      - [扩展方法](#扩展方法-1)
    - [PetWindow](#petwindow)
      - [核心方法 operateState(state: str, anime: str, isContinue: bool = False, isAsync: bool = True) -> None](#核心方法-operatestatestate-str-anime-str-iscontinue-bool--false-isasync-bool--true---none)
      - [核心方法 changeState(state: str) -> None](#核心方法-changestatestate-str---none)
      - [核心方法 replyState(state: str) -> None](#核心方法-replystatestate-str---none)
      - [核心方法 changeAnime(name: str, isContinue: bool = False, isAsync: bool = True) -> None](#核心方法-changeanimename-str-iscontinue-bool--false-isasync-bool--true---none)
      - [核心方法 startAct(id: str) -> None](#核心方法-startactid-str---none)
      - [核心方法 stopAct(id: str) -> None](#核心方法-stopactid-str---none)
      - [核心方法 getAct(id: str) -> Plugin | None](#核心方法-getactid-str---plugin--none)
      - [槽函数 updateData() -> None](#槽函数-updatedata---none)
      - [槽函数 onStateChanged(prevState: str, currentState: str) -> None](#槽函数-onstatechangedprevstate-str-currentstate-str---none)
      - [槽函数 onActStopped(id: str) -> None](#槽函数-onactstoppedid-str---none)
      - [信号](#信号-5)
      - [属性](#属性-3)
      - [属性（Property）](#属性property-3)

---

## 概述

本文档描述桌面宠物程序的核心 API，涵盖工具模块、窗口类和自定义扩展接口。

---

## 模块 tool.anime

动画播放引擎，负责帧序列的加载、播放控制和窗口自适应。

### 函数 getPixNames(folderPath: str) -> list[str]

获取指定文件夹内所有纯数字命名的图片文件名（不含子目录），并按数字升序排序。

- **参数**
  - `folderPath`: 文件夹路径
- **返回**
  - 排序后的文件名列表，如 `["0.png", "1.png", "2.png"]`
- **说明**
  - 自动过滤非纯数字命名的文件
  - 文件名示例：`0.png`、`1.jpg` 等

### 函数 fitImgSize(window: QWidget, widget: QLabel) -> None

将窗口和标签控件调整为当前图片的尺寸。

- **参数**
  - `window`: 父窗口
  - `widget`: 存放图片的 QLabel
- **说明**
  - 若图片加载失败，调用 `showLoadFailedMsg` 弹出错误窗口并退出程序

### 函数 showLoadFailedMsg(window: QWidget, path: str = "") -> None

显示图片加载失败的错误对话框。

- **参数**
  - `window`: 父窗口
  - `path`: 尝试加载的文件路径（用于错误提示）
- **行为**
  - 点击「关闭」：关闭窗口

### 类 Anime(QObject)

动画播放器，支持异步定时器播放和同步阻塞播放两种模式。

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `finished()` | 一轮动画播放完成（仅非循环模式） |
| `overed()` | 动画播放结束（停止或完成） |
| `loadError(str)` | 加载帧图片失败时，携带错误信息 |

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
| `plugin` | dict | `./data/plugin.json` |

### 枚举 LogType

日志类型枚举，用于标识日志条目类别。

| 成员 | 值 | 说明 |
| :--- | :--- | :--- |
| `Error` | 0 | 错误信息 |
| `Entre` | 1 | 入场事件 |
| `Exit` | 2 | 退场事件 |
| `Set` | 3 | 设置更新事件 |
| `StateChanged` | 4 | 状态切换事件 |
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
  - `collisions` 格式：`{ "碰撞体名": QRect, ... }`

---

## 模块 tool.pageFactory

页面工厂模块，用于构建设置面板和属性面板的配置界面。

### 函数 deleteLyt(lyt: QLayout) -> None

递归删除布局及其所有子控件。

- **参数**
  - `lyt`: 要删除的布局

### 函数 clearLyt(lyt: QLayout) -> None

清空布局中的所有子控件。

- **参数**
  - `lyt`: 要清空的布局

### 函数 getVal(edit: Any, dataType: str) -> Any

从编辑器控件获取值。

- **参数**
  - `edit`: 编辑器控件
  - `dataType`: 数据类型，可选 `"bool"`、`"int"`、`"float"`、`"str"`、`"file"`、`"folder"`
- **返回**
  - 控件当前值

### 函数 setVal(edit: Any, dataType: str, val: Any) -> None

向编辑器控件设置值。

- **参数**
  - `edit`: 编辑器控件
  - `dataType`: 数据类型
  - `val`: 要设置的值

### 函数 createEdit(dataType: str) -> QWidget | None

根据数据类型创建对应的编辑器控件。

- **参数**
  - `dataType`: 数据类型
- **返回**
  - 对应的编辑器控件，如 `QCheckBox`、`QSpinBox`、`QLineEdit`、`FileSelecter` 等

### 类 FileSelecter(QWidget)

文件/文件夹选择器控件。

- **信号**
  - `textChanged(str)`: 路径改变时发射
- **方法**
  - `getFile() -> str`: 获取当前路径
  - `setFile(file: str) -> None`: 设置路径

### 类 RemovableRow(QHBoxLayout)

可删除的编辑行，包含一个编辑器控件和一个删除按钮。

- **信号**
  - `aboutToRemove()`: 行被删除前发射
- **方法**
  - `getVal() -> Any`: 获取编辑器的值
  - `setVal(val: Any) -> None`: 设置编辑器的值

### 类 PageFactory(QWidget)

创建标签页的工厂基类。

- **信号**
  - `valChanged(str, Any)`: 值改变时发射，携带键和新值
  - `dataUpdated()`: 数据更新时发射
- **方法**
  - `build() -> None`: 构建页面
  - `updateTab(data) -> None`: 更新界面
  - `getData() -> Any`: 获取更新后的数据
  - `setData(data) -> None`: 设置数据并更新界面
  - `clear() -> None`: 清空页面内容

### 类 FormFactory(PageFactory)

表单工厂，用于创建键值对编辑页面。

- **参数**
  - `fields: list[tuple[str, str, str]]`: 字段列表，每个元素为 `(显示名称, 键, 数据类型)`
  - `data: dict`: 数据字典
- **方法**
  - `getData() -> dict[str, Any]`: 获取所有字段的值

### 类 DynamicListFactory(PageFactory)

动态列表工厂，用于创建可增删的字符串列表编辑页面。

- **参数**
  - `data: list[str]`: 初始数据列表
  - `rmBtnText: str`: 删除按钮文本，默认为 `"删除"`
  - `addBtnText: str`: 添加按钮文本，默认为 `"新建"`
- **方法**
  - `getData() -> list[str]`: 获取列表数据

### 类 FormBoxFactory(PageFactory)

表单盒子工厂，用于创建分组的表单编辑页面（`QToolBox` 容器）。

- **参数**
  - `fields: list[tuple[str, str, list[tuple[str, str, str]]]]`: 字段列表，每个元素为 `(分组名称, 键, FormFactory.fields)`
  - `data: dict`: 数据字典
- **信号**
  - `formValChanged(str, str, Any)`: 表单值改变时发射，携带分组键、表单键和新值
  - `formDataUpdated(str)`: 表单数据更新时发射，携带分组键
- **方法**
  - `getData() -> dict[str, dict[str, Any]]`: 获取所有分组的数据

### 类 ListBoxFactory(PageFactory)

列表盒子工厂，用于创建分组的列表编辑页面（`QToolBox` 容器）。

- **参数**
  - `fields: list[tuple[str, str]]`: 字段列表，每个元素为 `(分组名称, 键)`
  - `data: dict`: 数据字典
- **信号**
  - `listDataUpdated(str)`: 列表数据更新时发射，携带分组键
- **方法**
  - `getData() -> dict[str, list[str]]`: 获取所有分组的列表数据

---

## 模块 tool.plugin

插件基类与插件管理器，用于实现和管理自定义行动。

### 类 Plugin(QObject)

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `id` | str | 插件唯一标识，应与 `plugin.json` 中的键一致 |
| `name` | str | 在行动面板显示的名称 |
| `description` | str | 插件描述，用于行动面板的鼠标悬浮提示 |
| `state` | str | 插件对应的状态名，用于状态机切换 |
| `auto` | bool | 是否在程序启动时自动运行，默认为 `False` |
| `teardownImmed` | bool | 插件停止后是否立即卸载，默认为 `True` |
| `_window` | PetWindow \| None | 关联的主窗口实例（内部使用，通过 `window` 属性访问） |

#### 属性（Property）

| 属性 | 类型 | 可访问性 | 说明 |
| :--- | :--- | :--- | :--- |
| `window` | PetWindow \| None | 只读（getter） | 获取当前关联的主窗口实例。若插件尚未通过 `setup` 安装，则返回 `None`。 |

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `started()` | 插件 `start` 方法被调用时发射 |
| `stopped()` | 插件 `stop` 方法被调用时发射 |

#### 方法 setup(window: PetWindow) -> None

插件安装，将插件与主窗口关联，绑定信号等操作。

- **参数**
  - `window`: 主窗口实例
- **说明**
  - 由 `PetWindow.__init__` 或 `PluginManager` 自动调用，无需手动调用
  - **初始化中涉及主窗口的操作应在此方法中进行，并先调用 `super().setup(window)`**
  - 调用后可通过 `self.window` 属性访问主窗口实例

#### 方法 teardown() -> None

插件卸载，解除与主窗口的关联，信号解绑与释放资源等操作。

- **说明**
  - 由 `PluginManager` 在插件停止且 `teardownImmed` 为 `True` 时自动调用

#### 方法 start() -> None

开始行动。

- **说明**
  - 在此实现行动开始时的逻辑（如切换动画、播放回复等）
  - 可通过 `self.window` 访问主窗口的公开方法
  - 安装事件过滤器并发射 `started` 信号

#### 方法 stop() -> None

停止行动。

- **说明**
  - 在此实现行动结束时的清理逻辑
  - 移除事件过滤器并发射 `stopped` 信号
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
  - 事件过滤器的安装和移除由基类的 `start`/`stop` 自动处理

---

### 类 PluginManager(QObject)

插件管理器，负责插件的加载、排序、生命周期管理和运行状态控制。

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `pluginLoadSucceeded(str)` | 插件加载成功，携带插件 ID |
| `pluginError(str)` | 插件加载或操作失败，携带错误信息 |

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `plugins` | dict[str, Plugin] | 所有已加载的插件字典，键为插件 ID |
| `_currentPlugin` | Plugin \| None | 当前正在运行的非自启动插件（内部存储） |

#### 属性（Property）

| 属性 | 类型 | 可访问性 | 说明 |
| :--- | :--- | :--- | :--- |
| `currentPlugin` | Plugin \| None | 读写（getter/setter） | 获取或设置当前正在运行的非自启动插件。设置新插件时会自动停止上一个插件并启动新插件。 |

#### 方法 loadAllPlugins() -> None

加载 `data.plugin` 中注册的所有插件。

- **行为**
  - 调用 `sortPlugins` 获取排序后的插件 ID 列表
  - 依次调用 `loadPlugin` 加载每个插件

#### 方法 loadPlugin(id: str) -> Plugin | None

加载 `data.plugin` 中注册的指定插件。

- **参数**
  - `id`: 插件 ID
- **行为**
  - 若 `plugin[id]["enabled"]` 为 `False`，直接返回 `None`
  - 若插件已加载，返回已有实例
  - 导入模块并实例化 `Action` 类
  - 发射 `pluginLoadSucceeded` 或 `pluginError` 信号
- **返回**
  - 插件实例，若加载失败则返回 `None`

#### 方法 sortPlugins() -> list[str]

通过检查依赖项对插件加载顺序进行拓扑排序。

- **返回**
  - 排序后的插件 ID 列表
- **行为**
  - 构建依赖图，计算入度
  - 使用 Kahn 算法进行拓扑排序
  - 若检测到循环依赖，发射 `pluginError` 信号

#### 方法 startAutoPlugins() -> None

启动所有自启动插件（`auto = True`）。

- **行为**
  - 遍历所有已加载的插件，对 `auto` 为 `True` 的插件调用 `setup` 和 `start`

#### 方法 getPlugin(id: str) -> Plugin | None

根据 ID 获取插件实例。

- **参数**
  - `id`: 插件 ID
- **返回**
  - 插件实例，若未找到则返回 `None`

#### 方法 startPlugin(id: str) -> None

启动指定 ID 的非自启动插件。

- **参数**
  - `id`: 插件 ID
- **行为**
  - 通过 `currentPlugin` setter 设置当前插件，自动停止上一个插件并启动新插件

#### 方法 stopPlugin(id: str) -> None

停止指定 ID 的插件。

- **参数**
  - `id`: 插件 ID
- **行为**
  - 若该插件为当前正在运行的插件，将 `currentPlugin` 置为 `None` 以停止它
  - 否则调用该插件的 `stop` 方法
  - 若 `teardownImmed` 为 `True`，则同时调用 `teardown`

---

## 模块 tool.stateMachine

状态机模块，管理宠物的状态切换、状态列表。

### 类 StateMachine(QObject)

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `stateChanged(str, str)` | 状态变更时发射，携带前一状态名和新状态名 |
| `stateUndefined(str)` | 尝试切换至未定义状态时发射，携带状态名 |

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `_stateList` | list[str] | 所有已注册状态的列表（内部存储） |
| `_currentState` | str | 当前状态（内部存储） |

#### 属性（Property）

| 属性 | 类型 | 可访问性 | 说明 |
| :--- | :--- | :--- | :--- |
| `stateList` | list[str] | 读写（getter/setter） | 获取或设置所有已注册状态的列表 |
| `currentState` | str | 读写（getter/setter） | 获取或设置当前状态，通过 setter 触发状态切换逻辑 |

#### 方法 addState(state: str) -> None

添加新状态到状态列表。

- **参数**
  - `state`: 要添加的状态名
- **说明**
  - 若状态已存在，不做任何操作

#### 方法 removeState(state: str) -> bool

从状态列表中移除指定状态。

- **参数**
  - `state`: 要移除的状态名
- **返回**
  - 是否成功移除（状态是否存在）
- **说明**
  - 若状态不存在，发射 `stateUndefined` 信号并返回 `False`

---

## 窗口类

### ActionMenu

行动面板，显示 `data.plugin` 中注册的所有非自启动行动按钮。

#### 关键属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `actBtn` | dict | 键为动作 ID，值为对应的 `QPushButton` |
| `stopBtn` | QPushButton | 停止按钮 |
| `lb` | dict | 键为动作 ID，值为对应的 `QLabel`（显示插件名称） |

- **说明**
  - 插件名称显示在 `QLabel` 中，鼠标悬浮时显示 `description` 作为提示
  - 仅显示 `self.auto = False` 的插件（自启动插件不会出现在行动面板中）

### DialogMenu

对话面板，随机展示问题列表，用户选择后随机回复。

#### 关键方法

| 方法 | 说明 |
| :--- | :--- |
| `resetQuesSelecter()` | 从 `data.dialog` 中随机抽取指定数量的问题填充下拉框 |
| `addLine(content: str)` | 向回复框追加一行文本 |

- **行为**
  - 提问后自动从列表中移除该问题，并从剩余问题中随机补充（包括刚刚移除的）

#### 槽函数 addNewOption() -> None

用户点击"发送"按钮时触发，显示选中的问题及随机回复，并从下拉框中移除该问题。

### StateMenu

状态日志面板，显示运行日志并支持写入文件。同时作为属性面板的容器，允许插件通过 `addPage` 添加自定义标签页。

#### 关键方法

| 方法 | 说明 |
| :--- | :--- |
| `log(text: str, type: LogType = None)` | 添加日志条目，格式为 `时间  LogType.xxx/None:    文本` |

#### 扩展方法

| 方法 | 说明 |
| :--- | :--- |
| `addPage(page: QWidget, label: str)` | 由插件调用，添加属性/配置页面到状态面板的标签页中 |
| `getPage(label: str)` | 获取已添加的页面，用于在数据更新时刷新页面内容 |

### SettingMenu

设置面板，可视化编辑所有 JSON 配置文件。

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `dataUpdated()` | 应用配置后发射，用于通知刷新数据 |
| `updateCancelled()` | 取消配置后发射 |
| `saveError()` | 保存配置失败时发射 |

#### 关键方法

| 方法 | 说明 |
| :--- | :--- |
| `apply()` | 读取所有输入框内容，更新 `data` 全局变量并写回 JSON 文件 |
| `cancel()` | 关闭窗口，不保存更改 |

#### 扩展方法

| 方法 | 说明 |
| :--- | :--- |
| `addPage(page: QWidget, label: str)` | 由插件调用，添加自定义配置页面到设置面板的标签页中 |
| `getPage(label: str)` | 获取已添加的页面，用于在数据更新时刷新页面内容 |

### PetWindow

主窗口（宠物本体），集成动画、状态机、碰撞检测、拖拽移动等核心功能。

#### 核心方法 operateState(state: str, anime: str, isContinue: bool = False, isAsync: bool = True) -> None

执行状态切换响应，包含回复文本、切换动画和更新状态。此为 `changeState`、`replyState` 和 `changeAnime` 的组合方法，用于一次性完成状态切换、回复和动画播放。

- **参数**
  - `state`: 目标状态名
  - `anime`: 要播放的动画名（通常与状态名一致）
  - `isContinue`: 切换动画时是否从上一次停止位置继续
  - `isAsync`: 动画是否异步播放
- **行为**
  - 调用 `stateMachine.currentState = state` 更新状态
  - 调用 `replyState(state)` 获取并显示回复
  - 调用 `changeAnime(anime, isContinue, isAsync)` 切换动画
- **说明**
  - 若目标状态与当前状态相同，不执行任何操作

#### 核心方法 changeState(state: str) -> None

仅更新状态，不触发回复和动画切换。

- **参数**
  - `state`: 目标状态名
- **行为**
  - 调用 `stateMachine.currentState = state` 更新状态
- **说明**
  - 若目标状态与当前状态相同，不执行任何操作
  - 通常与 `replyState` 和 `changeAnime` 配合使用

#### 核心方法 replyState(state: str) -> None

仅显示状态回复文本，不切换状态和动画。

- **参数**
  - `state`: 状态名
- **行为**
  - 调用 `conv.replyText("state", state)` 获取随机回复
  - 通过 `dialogMenu.addLine` 写入对话面板
- **说明**
  - 若状态无对应回复文本，则不显示

#### 核心方法 changeAnime(name: str, isContinue: bool = False, isAsync: bool = True) -> None

切换动画，停止当前动画并播放目标动画。

- **参数**
  - `name`: 目标动画名（须在 `data.anime` 中定义）
  - `isContinue`: 是否从上一次停止位置继续
  - `isAsync`: 动画是否异步播放

#### 核心方法 startAct(id: str) -> None

执行指定 ID 的行动。

- **参数**
  - `id`: 插件 ID
- **行为**
  - 通过 `pluginManager.currentPlugin` 切换当前插件（自动停止上一个插件并启动新插件）
  - 通过 `stateMachine.currentState` 更新状态

#### 核心方法 stopAct(id: str) -> None

停止指定 ID 的行动。

- **参数**
  - `id`: 插件 ID
- **行为**
  - 调用 `pluginManager.stopPlugin(id)` 停止指定插件

#### 核心方法 getAct(id: str) -> Plugin | None

根据 ID 获取插件实例。

- **参数**
  - `id`: 插件 ID
- **返回**
  - 插件实例，若未找到则返回 `None`

#### 槽函数 updateData() -> None

重新加载配置数据并刷新动画和碰撞体。由 `SettingMenu.dataUpdated` 信号触发调用。

- **说明**
  - 重新从 `data.anime` 和 `data.collision` 构建动画对象和碰撞体
  - 调用 `dialogMenu.resetQuesSelecter()` 刷新对话选项
  - 记录日志

#### 槽函数 onStateChanged(prevState: str, currentState: str) -> None

状态变更响应槽函数。由 `stateMachine.stateChanged` 信号触发调用。

- **参数**
  - `prevState`: 前一状态名
  - `currentState`: 新状态名
- **行为**
  - 向状态日志面板写入状态变更日志
  - 发射 `stateChanged` 信号

#### 槽函数 onActStopped(id: str) -> None

行动停止响应槽函数。由插件 `stopped` 信号触发调用。

- **参数**
  - `id`: 停止的插件 ID
- **行为**
  - 若当前正在运行的插件 ID 匹配，通过 `pluginManager.currentPlugin = None` 停止

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `stateChanged(str, str)` | 状态变更时发射，携带前一状态名和新状态名 |
| `aboutToQuit()` | 程序即将退出时发射 |

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `animes` | dict | 动画对象字典，键为状态名 |
| `collisions` | dict | 碰撞体字典，键为状态名 |
| `pluginManager` | PluginManager | 插件管理器实例 |
| `dialogMenu` | DialogMenu | 对话面板实例 |
| `stateMenu` | StateMenu | 状态日志面板实例 |
| `actionMenu` | ActionMenu | 行动面板实例 |
| `settingMenu` | SettingMenu | 设置面板实例 |
| `stateMachine` | StateMachine | 状态机实例 |

#### 属性（Property）

| 属性 | 类型 | 可访问性 | 说明 |
| :--- | :--- | :--- | :--- |
| `state` | str | 读写（getter/setter） | 获取或设置当前状态，通过 setter 调用 `stateMachine.currentState` |
| `currentAct` | Plugin \| None | 只读（getter） | 获取当前正在运行的非自启动插件，通过 `pluginManager.currentPlugin` |
