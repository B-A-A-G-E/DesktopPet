# 工具 API

## 目录
- [工具 API](#工具-api)
  - [目录](#目录)
  - [概述](#概述)
  - [模块 tool](#模块-tool)
    - [模块 tool.config](#模块-toolconfig)
      - [枚举 LogType](#枚举-logtype)
      - [类 ConfigManager(QObject)](#类-configmanagerqobject)
        - [枚举 SaveMode](#枚举-savemode)
        - [静态属性](#静态属性)
        - [实例属性](#实例属性)
        - [信号](#信号)
        - [方法 __init__()](#方法-__init__)
        - [方法 loadConfig() -> None](#方法-loadconfig---none)
        - [方法 saveConfig() -> None](#方法-saveconfig---none)
        - [方法 saveAllConfigs() -> None](#方法-saveallconfigs---none)
        - [方法 saveStaticConfigs() -> None](#方法-savestaticconfigs---none)
        - [方法 saveCommonConfigs() -> None](#方法-savecommonconfigs---none)
        - [方法 save() -> None](#方法-save---none)
      - [函数 scanPets() -> list[str]](#函数-scanpets---liststr)
      - [函数 loadPets() -> None](#函数-loadpets---none)
    - [模块 tool.anime](#模块-toolanime)
      - [函数 getPixNames() -> list[str]](#函数-getpixnames---liststr)
      - [函数 fitImgSize() -> None](#函数-fitimgsize---none)
      - [函数 showLoadFailedMsg() -> None](#函数-showloadfailedmsg---none)
      - [类 Anime(QObject)](#类-animeqobject)
        - [属性](#属性)
        - [信号](#信号-1)
        - [方法 __init__()](#方法-__init__-1)
        - [方法 play() -> None](#方法-play---none)
        - [方法 stop() -> None](#方法-stop---none)
        - [方法 over() -> None](#方法-over---none)
        - [方法 replay() -> None](#方法-replay---none)
        - [槽函数 nextImg() -> None](#槽函数-nextimg---none)
    - [模块 tool.audio](#模块-toolaudio)
      - [类 AudioPlayer(QObject)](#类-audioplayerqobject)
        - [属性](#属性-1)
        - [信号](#信号-2)
        - [方法 __init__()](#方法-__init__-2)
        - [方法 bind() -> None](#方法-bind---none)
        - [方法 play() -> None](#方法-play---none-1)
        - [方法 stop() -> None](#方法-stop---none-1)
        - [方法 pause() -> None](#方法-pause---none)
    - [模块 tool.collision](#模块-toolcollision)
      - [函数 pointAt() -> list[str]](#函数-pointat---liststr)
      - [函数 isCollided() -> bool](#函数-iscollided---bool)
      - [函数 getCollision() -> list[str]](#函数-getcollision---liststr)
    - [模块 tool.conv](#模块-toolconv)
      - [函数 replyText() -> str](#函数-replytext---str)
    - [模块 tool.plugin](#模块-toolplugin)
      - [类 Plugin(QObject)](#类-pluginqobject)
        - [属性](#属性-2)
        - [信号](#信号-3)
        - [方法 __init__()](#方法-__init__-3)
        - [方法 setup() -> None](#方法-setup---none)
        - [方法 teardown() -> None](#方法-teardown---none)
        - [方法 start() -> None](#方法-start---none)
        - [方法 stop() -> None](#方法-stop---none-2)
        - [方法 eventFilter() -> bool](#方法-eventfilter---bool)
      - [类 PluginManager(QObject)](#类-pluginmanagerqobject)
        - [属性](#属性-3)
        - [信号](#信号-4)
        - [方法 __init__()](#方法-__init__-4)
        - [方法 loadAllPlugins() -> None](#方法-loadallplugins---none)
        - [方法 loadPlugin() -> Plugin | None](#方法-loadplugin---plugin--none)
        - [方法 importModule() -> ModuleType](#方法-importmodule---moduletype)
        - [方法 sortPlugins() -> list[str]](#方法-sortplugins---liststr)
        - [方法 startAutoPlugins() -> None](#方法-startautoplugins---none)
        - [方法 getPlugin() -> Plugin | None](#方法-getplugin---plugin--none)
        - [方法 startPlugin() -> None](#方法-startplugin---none)
        - [方法 stopPlugin() -> None](#方法-stopplugin---none)
    - [模块 tool.stateMachine](#模块-toolstatemachine)
      - [类 StateMachine(QObject)](#类-statemachineqobject)
        - [属性](#属性-4)
        - [信号](#信号-5)
        - [方法 __init__()](#方法-__init__-5)
        - [方法 addState() -> None](#方法-addstate---none)
        - [方法 removeState() -> bool](#方法-removestate---bool)
    - [模块 tool.widgetFactory](#模块-toolwidgetfactory)
      - [函数 deleteLyt() -> None](#函数-deletelyt---none)
      - [函数 clearLyt() -> None](#函数-clearlyt---none)
      - [函数 getVal() -> Any](#函数-getval---any)
      - [函数 setVal() -> None](#函数-setval---none)
      - [函数 createEdit() -> QWidget | None](#函数-createedit---qwidget--none)
      - [类 FileSelecter(QWidget)](#类-fileselecterqwidget)
        - [属性](#属性-5)
        - [信号](#信号-6)
        - [方法 __init__()](#方法-__init__-6)
        - [方法 bind() -> None](#方法-bind---none-1)
        - [方法 getFile() -> str](#方法-getfile---str)
        - [方法 setFile() -> None](#方法-setfile---none)
      - [类 SearchBox(QWidget)](#类-searchboxqwidget)
        - [属性](#属性-6)
        - [信号](#信号-7)
        - [方法 __init__()](#方法-__init__-7)
        - [方法 bind() -> None](#方法-bind---none-2)
        - [槽函数 changeMode() -> None](#槽函数-changemode---none)
      - [类 SearchableList(QWidget)](#类-searchablelistqwidget)
        - [属性](#属性-7)
        - [信号](#信号-8)
        - [方法 __init__()](#方法-__init__-8)
        - [方法 bind() -> None](#方法-bind---none-3)
        - [方法 setItems() -> None](#方法-setitems---none)
        - [方法 getSelected() -> QWidget | None](#方法-getselected---qwidget--none)
        - [槽函数 filterItems() -> None](#槽函数-filteritems---none)
      - [类 RemovableRow(QHBoxLayout)](#类-removablerowqhboxlayout)
        - [属性](#属性-8)
        - [信号](#信号-9)
        - [方法 __init__()](#方法-__init__-8)
        - [方法 bind() -> None](#方法-bind---none-4)
        - [方法 deleteLater() -> None](#方法-deletelater---none)
        - [方法 getVal() -> Any](#方法-getval---any-1)
        - [方法 setVal() -> None](#方法-setval---none-1)
        - [槽函数 onBtnClicked() -> None](#槽函数-onbtnclicked---none)
      - [类 WidgetFactory(QWidget)](#类-widgetfactoryqwidget)
        - [属性](#属性-9)
        - [信号](#信号-10)
        - [方法 __init__()](#方法-__init__-9)
        - [方法 build() -> None](#方法-build---none)
        - [方法 buildContent() -> None](#方法-buildcontent---none)
        - [方法 updateTab() -> None](#方法-updatetab---none)
        - [方法 getData() -> Any](#方法-getdata---any)
        - [方法 setData() -> None](#方法-setdata---none)
        - [方法 clear() -> None](#方法-clear---none)
      - [类 FormFactory(WidgetFactory)](#类-formfactorywidgetfactory)
        - [属性](#属性-10)
        - [方法 __init__()](#方法-__init__-10)
        - [方法 buildContent() -> None](#方法-buildcontent---none-1)
        - [方法 updateTab() -> None](#方法-updatetab---none-1)
        - [方法 getData() -> dict[str, Any]](#方法-getdata---dictstr-any)
        - [方法 bindEditSignal() -> None](#方法-bindeditsignal---none)
        - [槽函数 onValChanged() -> None](#槽函数-onvalchanged---none)
      - [类 DynamicListFactory(WidgetFactory)](#类-dynamiclistfactorywidgetfactory)
        - [属性](#属性-11)
        - [方法 __init__()](#方法-__init__-11)
        - [方法 buildContent() -> None](#方法-buildcontent---none-2)
        - [方法 updateTab() -> None](#方法-updatetab---none-2)
        - [方法 getData() -> list[str]](#方法-getdata---liststr)
        - [方法 bind() -> None](#方法-bind---none-5)
        - [方法 createRow() -> None](#方法-createrow---none)
      - [类 FormBoxFactory(WidgetFactory)](#类-formboxfactorywidgetfactory)
        - [属性](#属性-12)
        - [信号](#信号-11)
        - [方法 __init__()](#方法-__init__-12)
        - [方法 buildContent() -> None](#方法-buildcontent---none-3)
        - [方法 updateTab() -> None](#方法-updatetab---none-3)
        - [方法 getData() -> dict[str, dict[str, Any]]](#方法-getdata---dictstr-dictstr-any)
        - [槽函数 onFormValChanged() -> None](#槽函数-onformvalchanged---none)
      - [类 ListBoxFactory(WidgetFactory)](#类-listboxfactorywidgetfactory)
        - [属性](#属性-13)
        - [信号](#信号-12)
        - [方法 __init__()](#方法-__init__-13)
        - [方法 buildContent() -> None](#方法-buildcontent---none-4)
        - [方法 updateTab() -> None](#方法-updatetab---none-4)
        - [方法 getData() -> dict[str, list[str]]](#方法-getdata---dictstr-liststr)
      - [类 SearchStackController(QObject)](#类-searchstackcontrollerqobject)
        - [属性](#属性-14)
        - [信号](#信号-13)
        - [方法 __init__()](#方法-__init__-14)
        - [方法 bind() -> None](#方法-bind---none-6)
        - [方法 addPage() -> None](#方法-addpage---none)
        - [方法 addfields() -> None](#方法-addfields---none)
        - [方法 removePage() -> None](#方法-removepage---none)
        - [方法 _reindex() -> None](#方法-_reindex---none)
        - [方法 clearAll() -> None](#方法-clearall---none)
        - [方法 changePageByKey() -> None](#方法-changepagebykey---none)
        - [方法 changePageByIndex() -> None](#方法-changepagebyindex---none)
        - [槽函数 onItemSelected() -> None](#槽函数-onitemselected---none)
      - [类 SearchStackFactory(WidgetFactory)](#类-searchstackfactorywidgetfactory)
        - [属性](#属性-15)
        - [方法 __init__()](#方法-__init__-15)
        - [方法 buildContent() -> None](#方法-buildcontent---none-5)

---

## 概述

本文档描述 `tool/` 包下所有工具模块的 API，包括配置管理、动画播放、音频播放、碰撞检测、文本回复、插件系统、状态机和页面工厂。

---

## 模块 tool

工具包，包含以下子模块：

| 模块 | 说明 |
| :--- | :--- |
| `tool.config` | 配置管理 |
| `tool.anime` | 动画播放 |
| `tool.audio` | 音频播放 |
| `tool.collision` | 碰撞检测 |
| `tool.conv` | 文本回复 |
| `tool.plugin` | 插件系统 |
| `tool.stateMachine` | 状态机 |
| `tool.widgetFactory` | 页面工厂 |

---

### 模块 tool.config

配置管理模块，提供 `ConfigManager` 类和 `loadPets` 函数。

#### 枚举 LogType

`tool.config.LogType`

日志类型枚举。

| 值 | 名称 | 说明 |
| :--- | :--- | :--- |
| 0 | `Error` | 错误 |
| 1 | `Enter` | 进入 |
| 2 | `Exit` | 退出 |
| 3 | `Set` | 设置 |
| 4 | `StateChanged` | 状态变更 |
| 5 | `PluginLoaded` | 插件加载 |

---

#### 类 ConfigManager(QObject)

配置管理器，负责加载、保存和提供桌宠的所有配置。

##### 枚举 SaveMode

`tool.config.ConfigManager.SaveMode`

保存模式枚举。

| 值 | 名称 | 说明 |
| :--- | :--- | :--- |
| 0 | `All` | 所有配置 |
| 1 | `Static` | 静态成员变量（`pets`, `plugin`, `settings`） |
| 2 | `Common` | 普通成员变量（`base`, `anime`, `collision`, `state`, `dialog`, `pluginState`） |
| 3 | `Pets` | `./pet/config.json` |
| 4 | `Plugin` | `./plugin/config.json` |
| 5 | `Settings` | `./settings.json` |
| 6 | `Base` | `base.json` |
| 7 | `Anime` | `anime.json` |
| 8 | `Collision` | `collision.json` |
| 9 | `State` | `state.json` |
| 10 | `Dialog` | `dialog.json` |
| 11 | `PluginState` | `pluginState.json` |

##### 静态属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `pets` | list[str] | 已注册的宠物名称列表 |
| `plugin` | dict[str, dict] | 插件全局配置 |
| `settings` | dict | 全局设置 |
| `default` | bool | 是否为默认桌宠模式 |

##### 实例属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `path` | str | 桌宠目录路径，格式为 `./pet/{name}/` |
| `info` | dict | `info.json` 内容 |
| `base` | dict | `base.json` 内容 |
| `anime` | dict[str, dict] | `anime.json` 内容 |
| `collision` | dict | `collision.json` 内容 |
| `state` | dict[str, list[str]] | `state.json` 内容 |
| `dialog` | dict[str, list[str]] | `dialog.json` 内容 |
| `pluginState` | dict[str, bool] | `pluginState.json` 内容 |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `loadError(str)` | 加载配置失败时发射，携带错误信息 |
| `saveError(str)` | 保存配置失败时发射，携带错误信息 |

##### 方法 __init__()

```python
def __init__(self, name: str)
```

初始化配置管理器。

- **参数**
  - `name`: 桌宠名称
- **说明**
  - 设置 `path` 为 `./pet/{name}/`
  - 初始化所有实例属性为空字典
  - 调用 `loadConfig()` 加载配置

##### 方法 loadConfig() -> None

加载所有配置文件。

- **行为**
  - 依次加载 `info.json`、`base.json`、`anime.json`、`collision.json`、`state.json`、`dialog.json`、`pluginState.json`
  - 文件不存在时初始化为空字典
  - 加载失败时发射 `loadError` 信号

##### 方法 saveConfig() -> None

```python
def saveConfig(self, mode: SaveMode = SaveMode.All) -> None
```

根据模式保存配置文件。

- **参数**
  - `mode`: 保存模式，默认为 `SaveMode.All`
- **行为**
  - 根据模式调用对应的保存方法
  - 保存失败时发射 `saveError` 信号

##### 方法 saveAllConfigs() -> None

保存所有配置（静态 + 普通）。

##### 方法 saveStaticConfigs() -> None

```python
@staticmethod
def saveStaticConfigs() -> None
```

保存静态成员变量（`pets`, `plugin`, `settings`）。

##### 方法 saveCommonConfigs() -> None

保存普通成员变量（`base`, `anime`, `collision`, `state`, `dialog`, `pluginState`）。

##### 方法 save() -> None

```python
@staticmethod
def save(filepath, data) -> None
```

将数据保存为 JSON 文件。

- **参数**
  - `filepath`: 文件路径
  - `data`: 要保存的数据

---

#### 函数 scanPets() -> list[str]

```python
def scanPets() -> list[str]
```

扫描实例

---

#### 函数 loadPets() -> None

```python
def loadPets() -> None
```

全局加载函数，加载宠物相关配置。

- **行为**
  - 加载 `./pet/config.json` 到 `ConfigManager.pets`
  - 加载 `./plugin/config.json` 到 `ConfigManager.plugin`
  - 加载 `./settings.json` 到 `ConfigManager.settings`
  - 文件不存在时初始化为空
  - 其他异常则抛出

---

### 模块 tool.anime

动画模块，提供帧序列动画播放功能。

#### 函数 getPixNames() -> list[str]

```python
def getPixNames(folderPath: str) -> list[str]
```

获取文件夹内所有文件名（不包括子目录），按数值排序。

- **参数**
  - `folderPath`: 文件夹路径
- **返回**
  - 按数值排序的纯数字文件名列表

#### 函数 fitImgSize() -> None

```python
def fitImgSize(window, widget) -> None
```

窗口适应图片。

- **参数**
  - `window`: 宿主窗口
  - `widget`: 显示图片的控件
- **行为**
  - 若图片有效，调整窗口和控件大小以适应图片
  - 若图片无效，调用 `showLoadFailedMsg`

#### 函数 showLoadFailedMsg() -> None

```python
def showLoadFailedMsg(window, path: str = "") -> None
```

显示加载失败消息框并关闭窗口。

- **参数**
  - `window`: 宿主窗口
  - `path`: 文件路径（可选）

---

#### 类 Anime(QObject)

动画类，基于帧序列图片播放动画。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `path` | str | 存放帧的文件夹的路径 |
| `fps` | int | 帧率 |
| `loop` | bool | 是否循环播放 |
| `window` | QWidget | 宿主窗口 |
| `widget` | QLabel | 存储帧的容器 |
| `connected` | bool | 定时器是否已连接 |
| `imgNames` | list[str] | 帧文件名列表 |
| `index` | int | 当前帧索引 |
| `timer` | QTimer | 定时器 |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `finished()` | 一轮动画播放完成时发射 |
| `overed()` | 动画播放结束时发射 |
| `loadError(str)` | 加载帧图片失败时发射 |

##### 方法 __init__()

```python
def __init__(self, path: str, fps: int, loop: bool, window, widget)
```

初始化动画。

- **参数**
  - `path`: 存放帧的文件夹的路径
  - `fps`: 帧率
  - `loop`: 是否循环播放
  - `window`: 宿主窗口
  - `widget`: 存储帧的容器
- **说明**
  - 调用 `getPixNames` 获取帧文件名列表
  - 初始化索引为 0，创建定时器

##### 方法 play() -> None

```python
def play(self, isContinue: bool = False, isAsync: bool = True) -> None
```

开始或继续播放动画。

- **参数**
  - `isContinue`: 是否继续播放（不重置索引），默认 `False`
  - `isAsync`: 是否异步播放，默认 `True`
- **行为**
  - 若 `isContinue` 为 `False`，重置索引并连接定时器
  - 异步模式：启动定时器
  - 同步模式：逐帧设置图片并阻塞，完成后发射 `finished` 和 `overed` 信号

##### 方法 stop() -> None

```python
def stop(self) -> None
```

停止播放动画（不重置索引）。

##### 方法 over() -> None

```python
def over(self) -> None
```

结束动画播放，重置索引，断开定时器连接，发射 `overed` 信号。

##### 方法 replay() -> None

```python
def replay(self) -> None
```

重新播放动画（重置索引）。

##### 槽函数 nextImg() -> None

```python
@Slot()
def nextImg(self) -> None
```

更新到下一帧。

- **行为**
  - 设置当前帧图片并调整窗口大小
  - 索引递增
  - 若到达末尾，根据 `loop` 决定是否循环或调用 `over()`

---

### 模块 tool.audio

音频模块，提供音频播放功能。

#### 类 AudioPlayer(QObject)

音频播放器。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `player` | QMediaPlayer | 媒体播放器 |
| `audio_output` | QAudioOutput | 音频输出 |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `handleError(str)` | 播放出错时发射，携带错误信息 |
| `finished()` | 播放完成时发射 |

##### 方法 __init__()

```python
def __init__(self, path: str)
```

初始化音频播放器。

- **参数**
  - `path`: 音频文件路径
- **异常**
  - `FileNotFoundError`: 音频文件不存在时抛出
- **说明**
  - 创建媒体播放器和音频输出
  - 设置音量并调用 `bind()` 绑定信号

##### 方法 bind() -> None

绑定信号与槽。

- **说明**
  - 绑定 `errorOccurred` 到 `handleError` 信号
  - 绑定 `mediaStatusChanged`，在 `EndOfMedia` 时发射 `finished` 信号

##### 方法 play() -> None

开始播放音频。

##### 方法 stop() -> None

停止播放音频。

##### 方法 pause() -> None

暂停播放音频。

---

### 模块 tool.collision

碰撞检测模块，提供碰撞检测函数。

#### 函数 pointAt() -> list[str]

```python
def pointAt(point: QPoint, colls: dict[str, QRect]) -> list[str]
```

获取指定位置对应的碰撞体。

- **参数**
  - `point`: 位置点
  - `colls`: 碰撞体字典
- **返回**
  - 包含该位置的碰撞体名称列表

#### 函数 isCollided() -> bool

```python
def isCollided(coll1: QRect, coll2: QRect) -> bool
```

判断两个碰撞体是否相交。

- **参数**
  - `coll1`: 碰撞体1
  - `coll2`: 碰撞体2
- **返回**
  - 是否相交

#### 函数 getCollision() -> list[str]

```python
def getCollision(coll: QRect, colls: dict[str, QRect]) -> list[str]
```

获取与指定碰撞体相交的所有碰撞体。

- **参数**
  - `coll`: 碰撞体
  - `colls`: 碰撞体字典
- **返回**
  - 相交的碰撞体名称列表

---

### 模块 tool.conv

文本回复模块。

#### 函数 replyText() -> str

```python
def replyText(type: str, act: str, config: ConfigManager) -> str
```

根据类型和动作获取随机回复文本。

- **参数**
  - `type`: 类型，`"state"` 或 `"dialog"`
  - `act`: 动作名（状态名或问题）
  - `config`: 配置管理器实例
- **返回**
  - 随机选取的回复文本，若不存在则返回空字符串

---

### 模块 tool.plugin

插件系统模块，提供 `Plugin` 基类和 `PluginManager` 类。

#### 类 Plugin(QObject)

插件基类，所有插件必须继承此类。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `id` | str | 插件 ID，默认为 `"plugin-plugin"` |
| `name` | str | 插件显示名称，默认为 `"未命名插件"` |
| `description` | str | 插件描述 |
| `state` | str | 状态名，默认为 `"plugin"` |
| `auto` | bool | 是否自启动，默认为 `False` |
| `teardownImmed` | bool | 是否在停止后立即卸载，默认为 `True` |
| `_window` | PetWindow \| None | 宿主窗口（私有） |
| `window` | PetWindow \| None | 宿主窗口（property，只读） |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `started()` | 插件启动时发射 |
| `stopped()` | 插件停止时发射 |

##### 方法 __init__()

```python
def __init__(self)
```

初始化插件基类。

##### 方法 setup() -> None

```python
def setup(self, window: "PetWindow") -> None
```

插件安装，关联主窗口。

- **参数**
  - `window`: 桌宠主窗口实例

##### 方法 teardown() -> None

插件卸载，解绑主窗口。

##### 方法 start() -> None

安装事件过滤器，运行插件，发射 `started` 信号。

##### 方法 stop() -> None

卸载事件过滤器，结束插件，发射 `stopped` 信号。

- **说明**
  - 若 `teardownImmed` 为 `True`，则调用 `teardown()`

##### 方法 eventFilter() -> bool

```python
def eventFilter(self, obj, event: QEvent) -> bool
```

事件过滤器。重写此方法以捕获输入事件。

- **参数**
  - `obj`: 事件目标对象
  - `event`: 事件对象
- **返回**
  - 返回 `True` 表示拦截事件

---

#### 类 PluginManager(QObject)

插件管理器，负责加载、启动和停止所有插件。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `plugins` | dict[str, Plugin] | 已加载的插件字典 |
| `_currentPlugin` | Plugin \| None | 当前正在运行的非自启动插件（私有） |
| `_petWindow` | PetWindow | 宿主桌宠窗口（私有） |
| `currentPlugin` | Plugin \| None | 当前正在运行的非自启动插件（property，可读写） |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `pluginLoadSucceeded(str)` | 插件加载成功时发射 |
| `pluginError(str)` | 插件加载失败时发射 |
| `currentPluginChanged(str, str)` | 当前插件变更时发射 |

##### 方法 __init__()

```python
def __init__(self, petWindow: "PetWindow")
```

初始化插件管理器。

- **参数**
  - `petWindow`: 宿主桌宠窗口

##### 方法 loadAllPlugins() -> None

加载所有插件（按依赖顺序排序）。

##### 方法 loadPlugin() -> Plugin | None

```python
def loadPlugin(self, id: str) -> Plugin | None
```

加载指定插件。

- **参数**
  - `id`: 插件 ID
- **返回**
  - 插件实例，若加载失败则返回 `None`
- **行为**
  - 检查插件是否启用
  - 检查插件是否已加载
  - 导入模块并获取 `Action` 类
  - 验证 `Action` 类是否继承自 `Plugin`
  - 创建插件实例并存入 `plugins`

##### 方法 importModule() -> ModuleType

```python
def importModule(self, path: str) -> ModuleType
```

导入指定路径的模块。

- **参数**
  - `path`: 模块路径
- **返回**
  - 导入的模块
- **异常**
  - `FileNotFoundError`: 路径不存在时抛出
  - `ImportError`: 无法加载模块时抛出

##### 方法 sortPlugins() -> list[str]

```python
def sortPlugins(self) -> list[str]
```

通过检查依赖项对插件加载顺序排序（Kahn 算法）。

- **返回**
  - 排序后的插件 ID 列表
- **异常**
  - `ValueError`: 检测到循环依赖时抛出

##### 方法 startAutoPlugins() -> None

启动所有自启动插件。

##### 方法 getPlugin() -> Plugin | None

```python
def getPlugin(self, id: str) -> Plugin | None
```

获取指定插件实例。

- **参数**
  - `id`: 插件 ID
- **返回**
  - 插件实例，若不存在则返回 `None`

##### 方法 startPlugin() -> None

```python
def startPlugin(self, id: str) -> None
```

启动指定插件。

- **参数**
  - `id`: 插件 ID

##### 方法 stopPlugin() -> None

```python
def stopPlugin(self, id: str) -> None
```

停止指定插件。

- **参数**
  - `id`: 插件 ID

---

### 模块 tool.stateMachine

状态机模块。

#### 类 StateMachine(QObject)

状态机，管理宠物的所有状态。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `_stateList` | list[str] | 状态列表（私有） |
| `_currentState` | str | 当前状态（私有） |
| `stateList` | list[str] | 状态列表（property，可读写） |
| `currentState` | str | 当前状态（property，可读写） |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `stateChanged(str, str)` | 状态切换时发射，携带 `(prevState, currentState)` |
| `stateUndefined(str)` | 状态未定义时发射 |

##### 方法 __init__()

```python
def __init__(self, stateList: list, state: str = "")
```

初始化状态机。

- **参数**
  - `stateList`: 状态列表
  - `state`: 初始状态，默认为空字符串

##### 方法 addState() -> None

```python
def addState(self, state: str) -> None
```

添加新状态到状态列表。

- **参数**
  - `state`: 状态名

##### 方法 removeState() -> bool

```python
def removeState(self, state: str) -> bool
```

从状态列表中删除状态。

- **参数**
  - `state`: 状态名
- **返回**
  - 是否成功删除

---

### 模块 tool.widgetFactory

页面工厂模块，提供多种工厂类和辅助函数。

#### 函数 deleteLyt() -> None

```python
def deleteLyt(lyt: QLayout) -> None
```

递归删除布局及其所有子控件和子布局。

- **参数**
  - `lyt`: 要删除的 `QLayout` 对象

#### 函数 clearLyt() -> None

```python
def clearLyt(lyt: QLayout) -> None
```

清空布局中的所有子项（控件或子布局），但不删除布局本身。

- **参数**
  - `lyt`: 要清空的 `QLayout` 对象

#### 函数 getVal() -> Any

```python
def getVal(edit: Any, dataType: str) -> Any
```

根据数据类型从编辑控件中提取值。

- **参数**
  - `edit`: 编辑控件实例
  - `dataType`: 数据类型字符串
- **返回**
  - 提取出的值
- **异常**
  - `TypeError`: 当 `dataType` 不在支持列表中时抛出

#### 函数 setVal() -> None

```python
def setVal(edit: Any, dataType: str, val: Any) -> None
```

根据数据类型将值设置到编辑控件中。

- **参数**
  - `edit`: 编辑控件实例
  - `dataType`: 数据类型字符串
  - `val`: 要设置的值
- **异常**
  - `TypeError`: 当 `dataType` 不在支持列表中时抛出

#### 函数 createEdit() -> QWidget | None

```python
def createEdit(dataType: str | dict) -> QWidget | None
```

根据数据类型工厂方法，创建对应的编辑器控件。

- **参数**
  - `dataType`: 数据类型字符串或字典
- **返回**
  - 对应类型的 `QWidget` 子类实例，若类型不支持则返回 `None`

---

#### 类 FileSelecter(QWidget)

文件/文件夹选择器控件。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `edit` | QLineEdit | 显示路径的文本框 |
| `btn` | QPushButton | 触发文件对话框的按钮 |
| `lyt` | QHBoxLayout | 布局 |
| `mode` | str | 选择模式，`"file"` 或 `"folder"` |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `textChanged(str)` | 路径文本发生变化时发射 |

##### 方法 __init__()

```python
def __init__(self, mode: str = "file")
```

初始化文件选择器。

- **参数**
  - `mode`: 选择模式，`"file"` 表示文件选择，`"folder"` 表示文件夹选择
- **说明**
  - 创建文本框和按钮
  - 调用 `bind()` 绑定信号

##### 方法 bind() -> None

绑定信号与槽，连接按钮点击事件到文件对话框。

##### 方法 getFile() -> str

获取当前选中的路径。

- **返回**
  - 路径字符串

##### 方法 setFile() -> None

```python
def setFile(self, file: str) -> None
```

设置当前路径文本。

- **参数**
  - `file`: 路径字符串

---

#### 类 SearchBox(QWidget)

搜索框控件。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `lyt` | QHBoxLayout | 布局 |
| `edit` | QLineEdit | 搜索输入框 |
| `csBtn` | QPushButton | 区分大小写切换按钮 |
| `emBtn` | QPushButton | 全字匹配切换按钮 |
| `caseSensitive` | bool | 是否区分大小写 |
| `exactMatch` | bool | 是否全字匹配 |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `textChanged(str)` | 搜索文本变化时发射 |
| `modeChanged(bool, bool)` | 搜索模式变化时发射，携带 `(caseSensitive, exactMatch)` |

##### 方法 __init__()

```python
def __init__(self)
```

初始化搜索框。

##### 方法 bind() -> None

绑定信号与槽。

##### 槽函数 changeMode() -> None

```python
@Slot(bool, bool)
def changeMode(self, cs: bool, em: bool) -> None
```

切换搜索模式。

- **参数**
  - `cs`: 是否区分大小写
  - `em`: 是否全字匹配

---

#### 类 SearchableList(QWidget)

可搜索列表控件。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `searchBox` | SearchBox | 搜索框 |
| `list` | QListWidget | 列表控件 |
| `lyt` | QVBoxLayout | 布局 |
| `items` | list[QWidget] | 列表项 |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `itemSelected(QWidget)` | 列表项被单击时发射 |
| `itemDoubleClicked(QWidget)` | 列表项被双击时发射 |

##### 方法 __init__()

```python
def __init__(self)
```

初始化可搜索列表。

##### 方法 bind() -> None

绑定信号与槽。

##### 方法 setItems() -> None

```python
def setItems(self, items: list[QWidget]) -> None
```

设置列表项。

- **参数**
  - `items`: 列表项列表

##### 方法 getSelected() -> QWidget | None

获取当前选中的列表项。

- **返回**
  - 选中的列表项，若无则返回 `None`

##### 槽函数 filterItems() -> None

```python
@Slot(str, bool, bool)
def filterItems(self, text: str, cs: bool, em: bool) -> None
```

根据搜索条件过滤列表项。

- **参数**
  - `text`: 搜索文本
  - `cs`: 是否区分大小写
  - `em`: 是否全字匹配

---

#### 类 RemovableRow(QHBoxLayout)

可删除的行布局，包含一个编辑器和一个删除按钮。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `_parent` | QLayout | 父布局（私有） |
| `dataType` | str | 数据类型 |
| `edit` | QWidget | 编辑器控件 |
| `btn` | QPushButton | 删除按钮 |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `aboutToRemove()` | 在行被移除前发射 |

##### 方法 __init__()

```python
def __init__(self, parent: QLayout, dataType: str, rmBtnText: str = "删除")
```

初始化可删除行。

- **参数**
  - `parent`: 父布局
  - `dataType`: 编辑器数据类型
  - `rmBtnText`: 删除按钮上的文本
- **说明**
  - 创建编辑器并添加到布局
  - 调用 `bind()` 绑定信号

##### 方法 bind() -> None

绑定删除按钮的点击信号。

##### 方法 deleteLater() -> None

递归清理行内的控件，然后调用父类 `deleteLater()`。

##### 方法 getVal() -> Any

获取当前编辑器中的值。

- **返回**
  - 编辑器中的值

##### 方法 setVal() -> None

```python
def setVal(self, val: Any) -> None
```

设置当前编辑器的值。

- **参数**
  - `val`: 要设置的值

##### 槽函数 onBtnClicked() -> None

```python
@Slot()
def onBtnClicked(self) -> None
```

删除按钮的槽函数：触发移除信号，从父布局移除自身并清理。

---

#### 类 WidgetFactory(QWidget)

创建控件的工厂基类。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `lyt` | QLayout | 页面的根布局 |
| `_data` | Any | 页面绑定的数据对象（私有） |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `valChanged(str, Any)` | 数据变更时发射，携带 `(key, value)` |
| `dataUpdated()` | 整个数据被更新时发射 |

##### 方法 __init__()

```python
def __init__(self, lyt: QLayout, data: Any)
```

初始化页面工厂。

- **参数**
  - `lyt`: 页面的根布局
  - `data`: 页面绑定的数据对象

##### 方法 build() -> None

构建页面：调用 `buildContent()` 并初始化数据到界面。

##### 方法 buildContent() -> None

构建页面内容。子类需重写此方法。

##### 方法 updateTab() -> None

```python
def updateTab(self, data: Any) -> None
```

用给定的数据更新界面。子类需重写此方法。

- **参数**
  - `data`: 数据对象

##### 方法 getData() -> Any

从界面收集数据并返回。子类需重写此方法。

- **返回**
  - 收集的数据

##### 方法 setData() -> None

```python
def setData(self, data: Any) -> None
```

设置新数据并刷新界面，同时发射 `dataUpdated` 信号。

- **参数**
  - `data`: 新数据

##### 方法 clear() -> None

清空页面布局中的所有子项。

---

#### 类 FormFactory(WidgetFactory)

表单工厂，用于创建基于 `QFormLayout` 的编辑页面。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `fields` | list[tuple[str, str, str]] | 字段定义列表 |
| `edits` | dict[str, QWidget] | 编辑器控件字典 |

##### 方法 __init__()

```python
def __init__(self, fields: list[tuple[str, str, str]], data: dict)
```

初始化表单工厂。

- **参数**
  - `fields`: 字段定义列表，每个元素为 `(显示名称, 数据键, 数据信息)`
  - `data`: 初始数据字典

##### 方法 buildContent() -> None

根据字段定义创建编辑器并添加到表单布局。

##### 方法 updateTab() -> None

```python
def updateTab(self, data: dict) -> None
```

用数据字典更新所有编辑器。

- **参数**
  - `data`: 数据字典

##### 方法 getData() -> dict[str, Any]

从所有编辑器收集数据，返回字典。

- **返回**
  - 数据字典

##### 方法 bindEditSignal() -> None

```python
def bindEditSignal(self, key: str, dataType: str) -> None
```

绑定编辑器值变更信号，将变更同步到 `_data` 并发射 `valChanged`。

- **参数**
  - `key`: 数据键
  - `dataType`: 数据类型

##### 槽函数 onValChanged() -> None

```python
@Slot(str, Any)
def onValChanged(self, key: str, val: Any) -> None
```

值变更槽函数，更新 `_data` 并发射信号。

- **参数**
  - `key`: 数据键
  - `val`: 新值

---

#### 类 DynamicListFactory(WidgetFactory)

动态字符串列表工厂，允许添加和删除条目。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `rmBtnText` | str | 删除按钮文本 |
| `addBtnText` | str | 添加按钮文本 |
| `addBtn` | QPushButton | 添加按钮 |
| `edits` | list[RemovableRow] | 可删除行列表 |

##### 方法 __init__()

```python
def __init__(self, data: list[str], rmBtnText: str = "删除", addBtnText: str = "新建")
```

初始化动态列表工厂。

- **参数**
  - `data`: 初始字符串列表
  - `rmBtnText`: 删除按钮文本
  - `addBtnText`: 添加按钮文本

##### 方法 buildContent() -> None

根据初始数据创建所有行，并添加"新建"按钮。

##### 方法 updateTab() -> None

```python
def updateTab(self, data) -> None
```

用新数据重建列表，清空原有内容。

- **参数**
  - `data`: 新数据列表

##### 方法 getData() -> list[str]

从所有行收集字符串数据，返回列表。

- **返回**
  - 字符串列表

##### 方法 bind() -> None

绑定添加按钮的点击事件，并为每行绑定移除时的清理逻辑。

##### 方法 createRow() -> None

```python
def createRow(self, val: Any) -> None
```

创建一个新的可删除行，将其插入到"新建"按钮之前，并设置初始值。

- **参数**
  - `val`: 行的初始值

---

#### 类 FormBoxFactory(WidgetFactory)

工具箱（`QToolBox`）页面工厂，每个页面包含一个表单。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `box` | QToolBox | 工具箱容器 |
| `fields` | list[tuple[str, str, list[tuple[str, str, str]]]] | 字段定义列表 |
| `forms` | dict[str, FormFactory] | 表单字典 |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `formValChanged(str, str, Any)` | 表单内值变更时发射，携带 `(key, form's key, value)` |
| `formDataUpdated(str)` | 表单数据更新时发射 |

##### 方法 __init__()

```python
def __init__(self, fields: list[tuple[str, str, list[tuple[str, str, str]]]], data: dict)
```

初始化表单工具箱工厂。

- **参数**
  - `fields`: 字段定义列表，每个元素为 `(页面名称, 数据键, FormFactory.fields)`
  - `data`: 数据字典

##### 方法 buildContent() -> None

为每个字段创建一个 `FormFactory`，并添加到工具箱中。

##### 方法 updateTab() -> None

```python
def updateTab(self, data: dict) -> None
```

更新所有表单的数据。

- **参数**
  - `data`: 数据字典

##### 方法 getData() -> dict[str, dict[str, Any]]

从所有表单收集数据，返回嵌套字典。

- **返回**
  - 嵌套字典

##### 槽函数 onFormValChanged() -> None

```python
@Slot(str, str, Any)
def onFormValChanged(self, k: str, formK: str, val: Any) -> None
```

表单内值变更的槽函数，更新 `_data` 并转发信号。

- **参数**
  - `k`: 数据键
  - `formK`: 表单内的键
  - `val`: 新值

---

#### 类 ListBoxFactory(WidgetFactory)

工具箱（`QToolBox`）页面工厂，每个页面包含一个动态字符串列表。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `box` | QToolBox | 工具箱容器 |
| `fields` | list[tuple[str, str]] | 字段定义列表 |
| `lists` | dict | 动态列表字典 |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `listDataUpdated(str)` | 列表数据更新时发射，携带数据键 |

##### 方法 __init__()

```python
def __init__(self, fields: list[tuple[str, str]], data: dict)
```

初始化列表工具箱工厂。

- **参数**
  - `fields`: 字段定义列表，每个元素为 `(页面名称, 数据键)`
  - `data`: 数据字典

##### 方法 buildContent() -> None

为每个字段创建一个 `DynamicListFactory`，并添加到工具箱中。

##### 方法 updateTab() -> None

```python
def updateTab(self, data: dict) -> None
```

更新所有列表的数据。

- **参数**
  - `data`: 数据字典

##### 方法 getData() -> dict[str, list[str]]

从所有列表收集数据，返回字典。

- **返回**
  - 字典，值为字符串列表

---

#### 类 SearchStackController(QObject)

搜索堆叠控制器，管理搜索列表与堆叠页面的联动。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `list` | SearchableList | 可搜索列表 |
| `stack` | QStackedWidget | 堆叠页面容器 |
| `fields` | dict[str, tuple[int, QWidget, QWidget]] | 字段字典，键为标识，值为 `(index, page, listItem)` |
| `pageCount` | int | 页面数量（property，只读） |
| `keys` | list[str] | 所有标识列表（property，只读） |
| `pages` | dict[str, QWidget] | 所有页面字典（property，只读） |
| `listItems` | dict[str, QWidget] | 所有列表项字典（property，只读） |
| `currentPage` | tuple[str, tuple[int, QWidget, QWidget]] \| None | 当前页面信息（property，只读） |

##### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `pageChanged(str, int, QWidget)` | 页面切换时发射，携带 `(标识, 索引, 页面)` |

##### 方法 __init__()

```python
def __init__(self, list: SearchableList, stack: QStackedWidget, fields: dict[str, tuple[QWidget, QWidget]] | None = None)
```

初始化搜索堆叠控制器。

- **参数**
  - `list`: 可搜索列表
  - `stack`: 堆叠页面容器
  - `fields`: 字段字典（可选）

##### 方法 bind() -> None

绑定信号与槽。

##### 方法 addPage() -> None

```python
def addPage(self, widget: QWidget, listItem: QWidget, key: str) -> None
```

添加页面。

- **参数**
  - `widget`: 页面控件
  - `listItem`: 列表项控件
  - `key`: 标识
- **异常**
  - `ValueError`: 标识已存在时抛出

##### 方法 addfields() -> None

```python
def addfields(self, fields: dict[str, tuple[QWidget, QWidget]]) -> None
```

批量添加页面。

- **参数**
  - `fields`: 字段字典

##### 方法 removePage() -> None

```python
def removePage(self, key: str) -> None
```

移除页面。

- **参数**
  - `key`: 标识
- **异常**
  - `ValueError`: 标识不存在时抛出

##### 方法 _reindex() -> None

根据堆叠中控件的实际顺序重建 `fields` 的索引映射。

##### 方法 clearAll() -> None

清空所有页面（用于整体重建）。

##### 方法 changePageByKey() -> None

```python
def changePageByKey(self, key: str) -> None
```

根据标识切换页面。

- **参数**
  - `key`: 标识
- **异常**
  - `ValueError`: 标识不存在时抛出

##### 方法 changePageByIndex() -> None

```python
def changePageByIndex(self, index: int) -> None
```

根据索引切换页面。

- **参数**
  - `index`: 索引
- **异常**
  - `ValueError`: 索引超出范围时抛出

##### 槽函数 onItemSelected() -> None

```python
@Slot(QWidget)
def onItemSelected(self, item: QWidget) -> None
```

列表项选中槽函数。

- **参数**
  - `item`: 选中的列表项

---

#### 类 SearchStackFactory(WidgetFactory)

搜索堆叠工厂，组合 `SearchableList` 和 `QStackedWidget`。

##### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `list` | SearchableList | 可搜索列表 |
| `stack` | QStackedWidget | 堆叠页面容器 |
| `controller` | SearchStackController | 搜索堆叠控制器 |

##### 方法 __init__()

```python
def __init__(self, data: Any, fields: dict[str, tuple[QWidget, QWidget]] | None = None)
```

初始化搜索堆叠工厂。

- **参数**
  - `data`: 数据对象
  - `fields`: 字段字典（可选）

##### 方法 buildContent() -> None

构建页面内容，将列表和堆叠添加到布局。
