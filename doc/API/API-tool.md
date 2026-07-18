# 桌面宠物 API（工具模块）

## 目录
- [桌面宠物 API（工具模块）](#桌面宠物-api工具模块)
  - [目录](#目录)
  - [概述](#概述)
  - [模块 tool.anime](#模块-toolanime)
    - [函数 getPixNames()](#函数-getpixnames)
    - [函数 fitImgSize()](#函数-fitimgsize)
    - [函数 showLoadFailedMsg()](#函数-showloadfailedmsg)
    - [类 Anime](#类-anime)
      - [信号](#信号)
      - [初始化 __init__()](#初始化-__init__)
      - [方法 play()](#方法-play)
      - [方法 stop()](#方法-stop)
      - [方法 over()](#方法-over)
      - [方法 replay()](#方法-replay)
      - [槽函数 nextImg()](#槽函数-nextimg)
  - [模块 tool.config](#模块-toolconfig)
    - [枚举 LogType](#枚举-logtype)
    - [类 ConfigManager](#类-configmanager)
      - [嵌套类 SaveMode](#嵌套类-savemode)
      - [属性（类变量）](#属性类变量)
      - [属性（实例变量）](#属性实例变量)
      - [信号](#信号-1)
      - [方法 \_\_init__()](#方法-__init__)
      - [方法 loadConfig()](#方法-loadconfig)
      - [方法 saveConfig()](#方法-saveconfig)
      - [方法 saveAllConfigs()](#方法-saveallconfigs)
      - [静态方法 saveStaticConfigs()](#静态方法-savestaticconfigs)
      - [方法 saveCommonConfigs()](#方法-savecommonconfigs)
      - [静态方法 save()](#静态方法-save)
    - [函数 loadPets()](#函数-loadpets)
  - [模块 tool.conv](#模块-toolconv)
    - [函数 replyText()](#函数-replytext)
  - [模块 tool.collision](#模块-toolcollision)
    - [函数 pointAt()](#函数-pointAt)
  - [模块 tool.plugin](#模块-toolplugin)
    - [类 Plugin](#类-plugin)
      - [属性](#属性)
      - [属性（Property）](#属性property)
      - [信号](#信号-2)
      - [方法 setup()](#方法-setup)
      - [方法 teardown()](#方法-teardown)
      - [方法 start()](#方法-start)
      - [方法 stop()](#方法-stop)
      - [方法 eventFilter()](#方法-eventfilter)
    - [类 PluginManager](#类-pluginmanager)
      - [信号](#信号-3)
      - [属性](#属性-1)
      - [属性（Property）](#属性property-1)
      - [方法 \_\_init__()](#方法-__init__-1)
      - [方法 loadAllPlugins()](#方法-loadallplugins)
      - [方法 loadPlugin()](#方法-loadplugin)
      - [方法 importModule()](#方法-importmodule)
      - [方法 sortPlugins()](#方法-sortplugins)
      - [方法 startAutoPlugins()](#方法-startautoplugins)
      - [方法 getPlugin()](#方法-getplugin)
      - [方法 startPlugin()](#方法-startplugin)
      - [方法 stopPlugin()](#方法-stopplugin)
  - [模块 tool.stateMachine](#模块-toolstatemachine)
    - [类 StateMachine](#类-statemachine)
      - [信号](#信号-4)
      - [属性](#属性-2)
      - [属性（Property）](#属性property-2)
      - [方法 \_\_init__()](#方法-__init__-2)
      - [方法 addState()](#方法-addstate)
      - [方法 removeState()](#方法-removestate)
  - [模块 tool.widgetFactory](#模块-toolwidgetfactory)
    - [函数 deleteLyt()](#函数-deletelyt)
    - [函数 clearLyt()](#函数-clearlyt)
    - [函数 getVal()](#函数-getval)
    - [函数 setVal()](#函数-setval)
    - [函数 createEdit()](#函数-createedit)
    - [类 FileSelecter](#类-fileselecter)
      - [信号](#信号-5)
      - [方法 \_\_init__()](#方法-__init__-3)
      - [方法 bind()](#方法-bind)
      - [方法 getFile()](#方法-getfile)
      - [方法 setFile()](#方法-setfile)
    - [类 SearchBox](#类-searchbox)
      - [信号](#信号-6)
      - [属性](#属性-3)
      - [方法 \_\_init__()](#方法-__init__-4)
      - [方法 bind()](#方法-bind-1)
      - [槽函数 changeMode()](#槽函数-changemode)
    - [类 SearchableList](#类-searchablelist)
      - [信号](#信号-7)
      - [属性](#属性-4)
      - [方法 \_\_init__()](#方法-__init__-5)
      - [方法 bind()](#方法-bind-2)
      - [方法 setItems()](#方法-setitems)
      - [方法 getSelected()](#方法-getselected)
      - [槽函数 filterItems()](#槽函数-filteritems)
    - [类 RemovableRow](#类-removablerow)
      - [信号](#信号-8)
      - [方法 \_\_init__()](#方法-__init__-6)
      - [方法 bind()](#方法-bind-3)
      - [方法 deleteLater()](#方法-deletelater)
      - [方法 getVal()](#方法-getval-1)
      - [方法 setVal()](#方法-setval-1)
      - [槽函数 onBtnClicked()](#槽函数-onbtnclicked)
    - [类 WidgetFactory](#类-widgetfactory)
      - [信号](#信号-9)
      - [方法 \_\_init__()](#方法-__init__-7)
      - [方法 build()](#方法-build)
      - [方法 buildContent()](#方法-buildcontent)
      - [方法 updateTab()](#方法-updatetab)
      - [方法 getData()](#方法-getdata-1)
      - [方法 setData()](#方法-setdata-1)
      - [方法 clear()](#方法-clear)
    - [类 FormFactory](#类-formfactory)
      - [方法 \_\_init__()](#方法-__init__-8)
      - [方法 buildContent()](#方法-buildcontent-1)
      - [方法 updateTab()](#方法-updatetab-1)
      - [方法 getData()](#方法-getdata-2)
      - [方法 bindEditSignal()](#方法-bindeditsignal)
      - [槽函数 onValChanged()](#槽函数-onvalchanged)
    - [类 DynamicListFactory](#类-dynamiclistfactory)
      - [方法 \_\_init__()](#方法-__init__-9)
      - [方法 buildContent()](#方法-buildcontent-2)
      - [方法 updateTab()](#方法-updatetab-2)
      - [方法 getData()](#方法-getdata-3)
      - [方法 bind()](#方法-bind-4)
      - [方法 createRow()](#方法-createrow)
    - [类 FormBoxFactory](#类-formboxfactory)
      - [信号](#信号-10)
      - [方法 \_\_init__()](#方法-__init__-10)
      - [方法 buildContent()](#方法-buildcontent-3)
      - [方法 updateTab()](#方法-updatetab-3)
      - [方法 getData()](#方法-getdata-4)
      - [槽函数 onFormValChanged()](#槽函数-onformvalchanged)
    - [类 ListBoxFactory](#类-listboxfactory)
      - [信号](#信号-11)
      - [方法 \_\_init__()](#方法-__init__-11)
      - [方法 buildContent()](#方法-buildcontent-4)
      - [方法 updateTab()](#方法-updatetab-4)
      - [方法 getData()](#方法-getdata-5)
    - [类 SearchStackController](#类-searchstackcontroller)
      - [信号](#信号-12)
      - [方法 \_\_init__()](#方法-__init__-12)
      - [方法 bind()](#方法-bind-5)
      - [属性（Property）](#属性property-3)
      - [方法 addPage()](#方法-addpage)
      - [方法 addfields()](#方法-addfields)
      - [方法 removePage()](#方法-removepage)
      - [方法 changePageByKey()](#方法-changepagebykey)
      - [方法 changePageByIndex()](#方法-changepagebyindex)
      - [槽函数 onItemSelected()](#槽函数-onitemselected)
    - [类 SearchStackFactory](#类-searchstackfactory)
      - [方法 \_\_init__()](#方法-__init__-13)
      - [方法 buildContent()](#方法-buildcontent-5)

---

## 概述

本文档描述桌面宠物程序的工具模块 API，涵盖动画控制、配置管理、对话生成、碰撞检测、插件系统、状态机和页面工厂。这些模块为宠物本体和管理器提供底层支持。

---

## 模块 tool.anime

动画播放引擎，负责帧序列的加载、播放控制和窗口自适应。

### 函数 getPixNames()

```python
def getPixNames(folderPath: str) -> list[str]
```

获取指定文件夹内所有纯数字命名的图片文件名（不含子目录），并按数字升序排序。

- **参数**
  - `folderPath`: 文件夹路径
- **返回**
  - 排序后的文件名列表，如 `["0.png", "1.png", "2.png"]`
- **说明**
  - 自动过滤非纯数字命名的文件

### 函数 fitImgSize()

```python
def fitImgSize(window: QWidget, widget: QLabel) -> None
```

将窗口和标签控件调整为当前图片的尺寸。

- **参数**
  - `window`: 父窗口
  - `widget`: 存放图片的 QLabel
- **说明**
  - 若 pixmap 为空或无效，调用 `showLoadFailedMsg` 显示错误

### 函数 showLoadFailedMsg()

```python
def showLoadFailedMsg(window: QWidget, path: str = "") -> None
```

显示图片加载失败的错误对话框。

- **参数**
  - `window`: 父窗口
  - `path`: 尝试加载的文件路径
- **说明**
  - 显示 `QMessageBox.Critical` 对话框
  - 关闭父窗口

### 类 Anime

```python
class Anime(QObject)
```

动画播放器，支持异步定时器播放和同步阻塞播放两种模式。

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `finished()` | 一轮动画播放完成（仅非循环模式） |
| `overed()` | 动画播放结束（停止或完成） |
| `loadError(str)` | 加载帧图片失败时，携带错误信息 |

#### 初始化 __init__()

```python
def __init__(path: str, fps: int, loop: bool, window: QWidget, widget: QLabel)
```

- **参数**
  - `path`: 帧图片所在文件夹路径
  - `fps`: 播放帧率
  - `loop`: 是否循环播放
  - `window`: 父窗口
  - `widget`: 用于显示图片的 QLabel
- **说明**
  - 调用 `getPixNames` 获取帧列表
  - 创建 `QTimer` 用于驱动动画

#### 方法 play()

```python
def play(isContinue: bool = False, isAsync: bool = True) -> None
```

开始或继续播放动画。

- **参数**
  - `isContinue`: 是否从上一次停止位置继续播放
  - `isAsync`: 是否异步播放（定时器驱动）；若为 `False`，则同步阻塞播放
- **说明**
  - 异步模式：定时器按帧率触发 `nextImg`
  - 同步模式：逐帧加载并调用 `QApplication.processEvents()` 更新界面

#### 方法 stop()

```python
def stop() -> None
```

暂停播放（保留当前帧位置）。

#### 方法 over()

```python
def over() -> None
```

停止播放并重置索引为 0，发射 `overed` 信号。

- **说明**
  - 停止定时器
  - 断开 `timeout` 信号连接
  - 重置索引为 0
  - 发射 `overed` 信号

#### 方法 replay()

```python
def replay() -> None
```

重置索引并从当前帧率重新开始播放。

#### 槽函数 nextImg()

```python
@Slot()
def nextImg() -> None
```

播放下一帧，由定时器驱动触发。

- **说明**
  - 加载当前索引对应的帧图片
  - 调用 `fitImgSize` 调整窗口大小
  - 索引递增，若到达末尾则重置
  - 若非循环模式且到达末尾，调用 `over()`

---

## 模块 tool.config

配置管理模块，负责加载和保存宠物配置。

### 枚举 LogType

```python
class LogType(Enum)
```

日志类型枚举。

| 成员 | 值 | 说明 |
| :--- | :--- | :--- |
| `Error` | 0 | 错误信息 |
| `Entre` | 1 | 入场事件 |
| `Exit` | 2 | 退场事件 |
| `Set` | 3 | 设置更新事件 |
| `StateChanged` | 4 | 状态切换事件 |
| `PluginLoaded` | 5 | 插件加载事件 |

### 类 ConfigManager

```python
class ConfigManager(QObject)
```

配置管理器，管理单个宠物的所有配置。

#### 嵌套类 SaveMode

```python
class SaveMode(Enum)
```

保存模式枚举。

| 成员 | 值 | 说明 |
| :--- | :--- | :--- |
| `All` | 0 | 所有配置 |
| `Static` | 1 | 静态成员变量（pets, plugin, settings） |
| `Common` | 2 | 普通成员变量（base, anime, collision, state, dialog, pluginState） |
| `Pets` | 3 | `./pet/config.json` |
| `Plugin` | 4 | `./pet/plugin.json` |
| `Settings` | 5 | `./settings.json` |
| `Base` | 6 | `base.json` |
| `Anime` | 7 | `anime.json` |
| `Collision` | 8 | `collision.json` |
| `State` | 9 | `state.json` |
| `Dialog` | 10 | `dialog.json` |
| `PluginState` | 11 | `pluginState.json` |

#### 属性（类变量）

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `pets` | dict[str, str] | 宠物注册表，键为宠物名，值为路径 |
| `plugin` | dict[str, dict] | 插件注册表 |
| `settings` | dict | 全局设置 |
| `default` | bool | 是否为默认宠物 |

#### 属性（实例变量）

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `path` | str | 宠物资源包根路径 |
| `base` | dict | 基础配置 |
| `anime` | dict[str, dict] | 动画配置 |
| `collision` | dict | 碰撞体配置 |
| `state` | dict[str, list[str]] | 状态反馈文本配置 |
| `dialog` | dict[str, list[str]] | 对话文本配置 |
| `pluginState` | dict[str, bool] | 插件启用状态 |

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `loadError(str)` | 加载配置失败时发射，携带错误信息 |
| `saveError(str)` | 保存配置失败时发射，携带错误信息 |

#### 方法 __init__()

```python
def __init__(self, path: str)
```

初始化配置管理器。

- **参数**
  - `path`: 宠物资源包根路径
- **说明**
  - 调用 `loadConfig()` 加载所有配置

#### 方法 loadConfig()

```python
def loadConfig() -> None
```

加载所有 JSON 配置文件到对应属性。

- **说明**
  - 依次加载 `base.json`、`anime.json`、`collision.json`、`state.json`、`dialog.json`、`pluginState.json`
  - 若文件不存在，对应属性设为空字典
  - 加载失败时发射 `loadError` 信号

#### 方法 saveConfig()

```python
def saveConfig(mode: SaveMode = SaveMode.All) -> None
```

根据模式保存配置文件。

- **参数**
  - `mode`: 保存模式，默认为 `SaveMode.All`
- **说明**
  - 根据 `mode` 调用不同的保存方法
  - 保存失败时发射 `saveError` 信号

#### 方法 saveAllConfigs()

```python
def saveAllConfigs() -> None
```

保存所有配置（静态 + 普通）。

- **说明**
  - 调用 `saveStaticConfigs()` 和 `saveCommonConfigs()`

#### 静态方法 saveStaticConfigs()

```python
@staticmethod
def saveStaticConfigs() -> None
```

保存静态成员变量（pets, plugin, settings）。

- **说明**
  - 保存到 `./pet/config.json`、`./pet/plugin.json`、`./settings.json`

#### 方法 saveCommonConfigs()

```python
def saveCommonConfigs() -> None
```

保存普通成员变量（base, anime, collision, state, dialog, pluginState）。

- **说明**
  - 保存到 `{path}/config/` 目录下对应的 JSON 文件

#### 静态方法 save()

```python
@staticmethod
def save(filepath, data) -> None
```

将数据写入 JSON 文件。

- **参数**
  - `filepath`: 文件路径
  - `data`: 要写入的数据
- **说明**
  - 自动创建文件所在目录
  - 使用 `ensure_ascii=False` 和 `indent=2` 格式化输出

### 函数 loadPets()

```python
def loadPets() -> None
```

加载 `./pet/config.json`、`./pet/plugin.json`、`./settings.json` 中的配置。

- **说明**
  - 由 `config.py` 在导入时自动调用
  - 结果存入 `ConfigManager` 的类变量
  - 若文件不存在，初始化为空字典

---

## 模块 tool.conv

对话回复生成器，从配置中随机选取回复文本。

### 函数 replyText()

```python
def replyText(type: str, act: str, config: ConfigManager) -> str
```

根据类型和动作名从 `config.state` 或 `config.dialog` 中随机选取一条回复。

- **参数**
  - `type`: 类型，可选 `"state"` 或 `"dialog"`
  - `act`: 动作/状态名或问题键名
  - `config`: `ConfigManager` 实例
- **返回**
  - 随机选取的回复文本；若未匹配则返回空字符串

---

## 模块 tool.collision

鼠标交互辅助函数。

### 函数 pointAt()

```python
def pointAt(point: QPoint, colls: dict[str, QRect]) -> list[str]
```

检测某点是否在某个碰撞体内。

- **参数**
  - `point`: 点位置
  - `colls`: 碰撞体字典
- **返回**
  - 命中的碰撞体名（键名）列表

---

## 模块 tool.plugin

插件基类与插件管理器。

### 类 Plugin

```python
class Plugin(QObject)
```

插件基类。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `id` | str | 插件唯一标识，默认 `"plugin-plugin"` |
| `name` | str | 在行动面板显示的名称，默认 `"未命名插件"` |
| `description` | str | 插件描述 |
| `state` | str | 对应的状态名，默认 `"plugin"` |
| `auto` | bool | 是否自启动，默认 `False` |
| `teardownImmed` | bool | 停止后是否立即卸载，默认 `True` |
| `_window` | PetWindow \| None | 关联的主窗口实例 |

#### 属性（Property）

| 属性 | 类型 | 可访问性 | 说明 |
| :--- | :--- | :--- | :--- |
| `window` | PetWindow \| None | 只读 | 获取关联的主窗口实例 |

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `started()` | `start` 方法被调用时发射 |
| `stopped()` | `stop` 方法被调用时发射 |

#### 方法 setup()

```python
def setup(window: PetWindow) -> None
```

插件安装，关联主窗口。

- **参数**
  - `window`: 主窗口实例

#### 方法 teardown()

```python
def teardown() -> None
```

插件卸载，解除与主窗口的关联。

- **说明**
  - 将 `_window` 设为 `None`

#### 方法 start()

```python
def start() -> None
```

开始行动，安装事件过滤器并发射 `started` 信号。

- **说明**
  - 调用 `_window.installEventFilter(self)` 安装事件过滤器
  - 发射 `started` 信号

#### 方法 stop()

```python
def stop() -> None
```

停止行动，移除事件过滤器并发射 `stopped` 信号。

- **说明**
  - 调用 `_window.removeEventFilter(self)` 移除事件过滤器
  - 将 `window.pluginManager._currentPlugin` 设为 `None`
  - 发射 `stopped` 信号
  - 若 `teardownImmed` 为 `True`，调用 `teardown()`

#### 方法 eventFilter()

```python
def eventFilter(obj, event: QEvent) -> bool
```

事件过滤器，默认返回 `False`。

- **参数**
  - `obj`: 事件目标对象
  - `event`: 事件对象
- **返回**
  - `True` 表示拦截事件，`False` 表示继续传递

---

### 类 PluginManager

```python
class PluginManager(QObject)
```

插件管理器。

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `pluginLoadSucceeded(str)` | 插件加载成功，携带插件 ID |
| `pluginError(str)` | 插件加载或操作失败，携带错误信息 |
| `currentPluginChanged(str, str)` | 当前插件变更时发射，携带旧 ID 和新 ID |

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `plugins` | dict[str, Plugin] | 所有已加载的插件字典 |
| `_currentPlugin` | Plugin \| None | 当前正在运行的非自启动插件 |
| `_petWindow` | PetWindow | 关联的宠物主窗口 |

#### 属性（Property）

| 属性 | 类型 | 可访问性 | 说明 |
| :--- | :--- | :--- | :--- |
| `currentPlugin` | Plugin \| None | 读写 | 获取或设置当前运行的非自启动插件 |

#### 方法 __init__()

```python
def __init__(self, petWindow: "PetWindow")
```

初始化插件管理器。

- **参数**
  - `petWindow`: 宠物主窗口实例

#### 方法 loadAllPlugins()

```python
def loadAllPlugins() -> None
```

加载所有注册的插件。

- **说明**
  - 调用 `sortPlugins()` 获取加载顺序
  - 依次调用 `loadPlugin()` 加载每个插件

#### 方法 loadPlugin()

```python
def loadPlugin(id: str) -> Plugin | None
```

加载指定插件。

- **参数**
  - `id`: 插件 ID
- **返回**
  - 插件实例，若加载失败则返回 `None`
- **说明**
  - 检查 `pluginState[id]` 是否启用
  - 检查是否已加载
  - 调用 `importModule()` 导入模块
  - 获取 `Action` 类并实例化
  - 存入 `plugins` 字典
  - 发射 `pluginLoadSucceeded` 或 `pluginError` 信号

#### 方法 importModule()

```python
def importModule(path: str) -> ModuleType
```

导入指定路径的 Python 模块。

- **参数**
  - `path`: 模块文件路径（支持相对路径和绝对路径）
- **返回**
  - 导入的模块对象
- **异常**
  - `FileNotFoundError`: 路径不存在
  - `ImportError`: 无法加载模块
- **说明**
  - 支持 `./` 开头的相对路径
  - 支持 Windows 绝对路径（如 `C:/...`）
  - 支持 Unix 绝对路径（如 `/home/...`）
  - 使用 `importlib.util` 动态导入

#### 方法 sortPlugins()

```python
def sortPlugins() -> list[str]
```

通过检查依赖项对插件加载顺序进行拓扑排序（Kahn 算法）。

- **返回**
  - 排序后的插件 ID 列表
- **异常**
  - `ValueError`: 检测到循环依赖时抛出
- **说明**
  - 依赖信息从 `ConfigManager.plugin` 的 `deps` 字段获取
  - 若依赖的插件未注册，发射 `pluginError` 信号

#### 方法 startAutoPlugins()

```python
def startAutoPlugins() -> None
```

启动所有自启动插件（`auto = True`）。

- **说明**
  - 遍历 `plugins`，对 `auto` 为 `True` 的插件调用 `setup()` 和 `start()`

#### 方法 getPlugin()

```python
def getPlugin(id: str) -> Plugin | None
```

根据 ID 获取插件实例。

- **参数**
  - `id`: 插件 ID
- **返回**
  - 插件实例，若未找到则返回 `None`

#### 方法 startPlugin()

```python
def startPlugin(id: str) -> None
```

启动指定插件。

- **参数**
  - `id`: 插件 ID
- **说明**
  - 通过 `currentPlugin` setter 启动插件
  - 若插件不存在，发射 `pluginError` 信号

#### 方法 stopPlugin()

```python
def stopPlugin(id: str) -> None
```

停止指定插件。

- **参数**
  - `id`: 插件 ID
- **说明**
  - 若当前运行的插件与指定 ID 匹配，将 `currentPlugin` 设为 `None`
  - 否则调用插件的 `stop()` 方法

---

## 模块 tool.stateMachine

状态机模块。

### 类 StateMachine

```python
class StateMachine(QObject)
```

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `stateChanged(str, str)` | 状态变更时发射，携带前一状态名和新状态名 |
| `stateUndefined(str)` | 尝试切换至未定义状态时发射，携带状态名 |

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `_stateList` | list[str] | 所有已注册状态的列表 |
| `_currentState` | str | 当前状态 |

#### 属性（Property）

| 属性 | 类型 | 可访问性 | 说明 |
| :--- | :--- | :--- | :--- |
| `stateList` | list[str] | 读写 | 状态列表 |
| `currentState` | str | 读写 | 当前状态，设置时会检查是否在 `_stateList` 中 |

#### 方法 __init__()

```python
def __init__(self, stateList: list, state: str = "")
```

初始化状态机。

- **参数**
  - `stateList`: 初始状态列表
  - `state`: 初始状态

#### 方法 addState()

```python
def addState(state: str) -> None
```

添加新状态到状态列表。

- **参数**
  - `state`: 要添加的状态名

#### 方法 removeState()

```python
def removeState(state: str) -> bool
```

从状态列表中移除指定状态。

- **参数**
  - `state`: 要移除的状态名
- **返回**
  - 是否成功移除
- **说明**
  - 若状态不存在，发射 `stateUndefined` 信号

---

## 模块 tool.widgetFactory

页面工厂模块，用于构建设置面板和属性面板的配置界面。

### 函数 deleteLyt()

```python
def deleteLyt(lyt: QLayout) -> None
```

递归删除布局及其所有子控件。

- **参数**
  - `lyt`: 要删除的布局
- **说明**
  - 遍历布局中的所有项，递归删除子布局和控件
  - 最后删除布局自身

### 函数 clearLyt()

```python
def clearLyt(lyt: QLayout) -> None
```

清空布局中的所有子控件。

- **参数**
  - `lyt`: 要清空的布局
- **说明**
  - 与 `deleteLyt` 类似，但不删除布局本身

### 函数 getVal()

```python
def getVal(edit: Any, dataType: str) -> Any
```

从编辑器控件获取值。

- **参数**
  - `edit`: 编辑器控件实例
  - `dataType`: 数据类型
- **支持的数据类型**: `"bool"`, `"int"`, `"float"`, `"str"`, `"file"`, `"folder"`
- **异常**
  - `TypeError`: 不支持的数据类型

### 函数 setVal()

```python
def setVal(edit: Any, dataType: str, val: Any) -> None
```

向编辑器控件设置值。

- **参数**
  - `edit`: 编辑器控件实例
  - `dataType`: 数据类型
  - `val`: 要设置的值
- **支持的数据类型**: `"bool"`, `"int"`, `"float"`, `"str"`, `"file"`, `"folder"`
- **异常**
  - `TypeError`: 不支持的数据类型

### 函数 createEdit()

```python
def createEdit(dataType: str) -> QWidget | None
```

根据数据类型创建对应的编辑器控件。

- **参数**
  - `dataType`: 数据类型
- **返回**
  - 编辑器控件实例，若类型不支持则返回 `None`
- **支持的数据类型**:
  - `"bool"`: `QCheckBox`
  - `"int"`: `QSpinBox`（范围 -99999 ~ 99999）
  - `"float"`: `QDoubleSpinBox`（范围 -99999 ~ 99999）
  - `"str"`: `QLineEdit`
  - `"file"`: `FileSelecter`（文件选择模式）
  - `"folder"`: `FileSelecter`（文件夹选择模式）

### 类 FileSelecter

文件/文件夹选择器控件。

- **信号**: `textChanged(str)` — 路径文本变化时发射
- **方法**:
  - `__init__(mode: str = "file")`: 初始化，`mode` 为 `"file"` 或 `"folder"`
  - `getFile() -> str`: 获取当前路径
  - `setFile(file: str) -> None`: 设置路径

### 类 SearchBox

搜索框控件，包含文本输入、区分大小写和全字匹配开关。

- **信号**:
  - `textChanged(str)`: 搜索文本变化时发射
  - `modeChanged(bool, bool)`: 搜索模式变化时发射，参数为（区分大小写, 全字匹配）
- **属性**: `caseSensitive: bool`, `exactMatch: bool`

### 类 SearchableList

可搜索的列表控件。

- **信号**:
  - `itemSelected(QWidget)`: 列表项被选中时发射
  - `itemDoubleClicked(QWidget)`: 列表项被双击时发射
- **方法**:
  - `setItems(items: list[QWidget])`: 设置列表项
  - `getSelected() -> QWidget | None`: 获取当前选中的项

### 类 RemovableRow

可删除的编辑行（`QHBoxLayout`）。

- **信号**: `aboutToRemove()` — 行被移除前发射
- **方法**:
  - `__init__(parent: QLayout, dataType: str, rmBtnText: str = "删除")`
  - `getVal() -> Any`: 获取编辑器值
  - `setVal(val: Any) -> None`: 设置编辑器值

### 类 WidgetFactory

创建控件的工厂基类。

- **信号**:
  - `valChanged(str, Any)`: 数据变更时发射
  - `dataUpdated()`: 整个数据被更新时发射
- **方法**:
  - `build()`: 构建页面
  - `buildContent()`: 构建页面内容（子类重写）
  - `updateTab(data)`: 用数据更新界面（子类重写）
  - `getData() -> Any`: 从界面收集数据（子类重写）
  - `setData(data)`: 设置新数据并刷新
  - `clear()`: 清空页面布局

### 类 FormFactory

表单工厂，创建键值对编辑页面。

- **参数**:
  - `fields: list[tuple[str, str, str]]`: 字段定义，格式为 `(显示名称, 数据键, 数据类型)`
  - `data: dict`: 初始数据
- **方法**: `getData() -> dict[str, Any]`

### 类 DynamicListFactory

动态列表工厂，创建可增删的字符串列表编辑页面。

- **参数**:
  - `data: list[str]`: 初始数据
  - `rmBtnText: str = "删除"`: 删除按钮文本
  - `addBtnText: str = "新建"`: 添加按钮文本
- **方法**: `getData() -> list[str]`

### 类 FormBoxFactory

表单盒子工厂，创建分组的表单编辑页面（`QToolBox` 容器）。

- **参数**:
  - `fields: list[tuple[str, str, list[tuple[str, str, str]]]]`: 分组定义
  - `data: dict`: 初始数据
- **信号**:
  - `formValChanged(str, str, Any)`: 表单内值变更，参数为（表单键, 字段键, 值）
  - `formDataUpdated(str)`: 表单数据更新
- **方法**: `getData() -> dict[str, dict[str, Any]]`

### 类 ListBoxFactory

列表盒子工厂，创建分组的列表编辑页面（`QToolBox` 容器）。

- **参数**:
  - `fields: list[tuple[str, str]]`: 分组定义，格式为 `(页面名称, 数据键)`
  - `data: dict`: 初始数据
- **信号**: `listDataUpdated(str)` — 列表数据更新
- **方法**: `getData() -> dict[str, list[str]]`

### 类 SearchStackController

搜索列表与堆叠页面的联动控制器。

- **信号**: `pageChanged(str, int, QWidget)` — 页面切换时发射
- **属性（Property）**:
  - `pageCount: int`: 页面总数
  - `keys: list[str]`: 所有页面键
  - `currentPage: tuple | None`: 当前页面信息
- **方法**:
  - `addPage(widget, listItem, key)`: 添加页面
  - `addfields(fields)`: 批量添加页面
  - `removePage(key)`: 移除页面
  - `changePageByKey(key)`: 通过键切换页面
  - `changePageByIndex(index)`: 通过索引切换页面

### 类 SearchStackFactory

搜索列表与堆叠页面的组合工厂。

- **参数**:
  - `data: Any`: 数据
  - `fields: dict[str, tuple[QWidget, QWidget]] | None`: 初始页面
- **属性**:
  - `list: SearchableList`: 搜索列表
  - `stack: QStackedWidget`: 堆叠页面
  - `controller: SearchStackController`: 控制器
