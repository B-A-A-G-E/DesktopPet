# 自定义教程

## 目录
- [自定义教程](#自定义教程)
  - [目录](#目录)
  - [概述](#概述)
  - [自定义基础配置](#自定义基础配置)
  - [自定义动画](#自定义动画)
    - [步骤](#步骤)
    - [动画配置示例](#动画配置示例)
  - [自定义碰撞体](#自定义碰撞体)
    - [步骤](#步骤-1)
    - [碰撞体配置示例](#碰撞体配置示例)
  - [自定义状态反馈文本](#自定义状态反馈文本)
    - [步骤](#步骤-2)
  - [自定义对话文本](#自定义对话文本)
    - [步骤](#步骤-3)
  - [自定义行动（插件）](#自定义行动插件)
    - [前置知识](#前置知识)
    - [步骤概览](#步骤概览)
    - [详细步骤](#详细步骤)
      - [1. 创建插件文件](#1-创建插件文件)
      - [2. 编写插件类](#2-编写插件类)
      - [3. 注册插件](#3-注册插件)
      - [4. 注册状态并配置状态反馈文本](#4-注册状态并配置状态反馈文本)
      - [5. 配置动画（可选）](#5-配置动画可选)
      - [6. 配置碰撞体（可选）](#6-配置碰撞体可选)
    - [完整示例：跳舞插件](#完整示例跳舞插件)
      - [插件代码](#插件代码)
      - [注册](#注册)
      - [动画配置](#动画配置)
      - [状态反馈文本](#状态反馈文本)
    - [进阶：自启动插件](#进阶自启动插件)
    - [进阶：事件过滤器](#进阶事件过滤器)
    - [进阶：插件依赖](#进阶插件依赖)
    - [进阶：扩展设置面板](#进阶扩展设置面板)
    - [进阶：控制插件卸载行为](#进阶控制插件卸载行为)
  - [常见问题](#常见问题)

---

## 概述

桌面宠物支持高度的自定义，你可以在不修改核心代码的情况下：

- 添加/修改动画
- 添加/修改碰撞体
- 添加/修改状态反馈文本
- 添加/修改对话文本
- 开发新的交互行为（插件）

所有配置均通过 JSON 文件管理，插件通过 Python 模块实现。

---

## 自定义基础配置

``` json
{
  "log-path": "./log.log",
  "quesSelecter-item-count": 10,
  "idle-time": 10000
}
```

| 键 | 说明 | 默认值 |
| :---: | :---: | :---: |
| `log-path` | 日志保存路径 | `./log.log` |
| `quesSelecter-item-count` | 对话面板最大显示问题数 | `10` |
| `idle-time` | 待机判定时间（毫秒） | `10000` |

---

## 自定义动画

### 步骤

1. **准备帧图片**：在 `./img/` 下新建文件夹放入帧图片。图片须**按数字顺序命名**（如 `0.png`, `1.png`, `2.png`...）。
2. **编辑 `./data/anime.json`**：配置动画，格式如下：

### 动画配置示例

``` json
"动画名": {
    "path": "./img/文件夹路径",
    "fps": 30,
    "loop": true
}
```

| 键 | 类型 | 说明 |
| :--- | :--- | :--- |
| `path` | str | 帧图片存放文件夹路径 |
| `fps` | int | 播放帧率（帧/秒） |
| `loop` | bool | 是否循环播放 |

> **注意**：
> - 动画名建议使用小写字母和连字符（如 `act-dance`），以保持统一风格
> - 帧图片需按数字顺序命名（如 `0.png`, `1.png`, `2.png`...）
> - 若需在 `PetWindow.replyState` 中自动播放，动画名需与状态名一致

---

## 自定义碰撞体

碰撞体定义鼠标点击宠物的可交互区域。

### 步骤

1. **确定碰撞区域**：在图片上测量碰撞区相对于图片左上角的偏移和尺寸。
2. **编辑 `./data/collision.json`**：配置碰撞体。

### 碰撞体配置示例

``` json
"碰撞体名": {
    "left": 11,
    "top": 30,
    "width": 135,
    "height": 30
}
```

| 键 | 类型 | 说明 |
| :--- | :--- | :--- |
| `left` | int | 碰撞区相对于窗口左上角的 X 偏移（像素） |
| `top` | int | 碰撞区相对于窗口左上角的 Y 偏移（像素） |
| `width` | int | 碰撞区宽度（像素） |
| `height` | int | 碰撞区高度（像素） |

---

## 自定义状态反馈文本

状态反馈文本是宠物切换状态时在对话面板显示的回复。

### 步骤

1. **编辑 `./data/state.json`**：添加或修改条目。

``` json
"状态名": [
    "反馈1",
    "反馈2"
]
```

``` json
"状态名": [] // 只注册状态，不显示回复
```

- 新建的状态必须在此文件内注册，若不希望回复直接设置空数组即可
- 用 `PetWindow.replyState` 切换状态时会从对应数组中随机选取一条回复
- 若状态无对应条目，则不显示回复

---

## 自定义对话文本

对话文本是用户通过对话面板提问时，宠物随机回复的内容。

### 步骤

1. **编辑 `./data/dialog.json`**：添加或修改条目。

``` json
"问题": [
    "回复1",
    "回复2"
]
```

- 用户在对话面板选择问题后，宠物从对应回复数组中随机选取一条
- 支持任意数量的问题-回复对

---

## 自定义行动（插件）

插件系统允许向宠物添加新的交互行为，是自由度最高的自定义方式。

### 前置知识

- Python 面向对象编程（类继承）
- PySide6 事件系统基础（可选）

### 步骤概览

1. 在 `action/` 目录下新建 Python 文件（建议以 `act-` 为前缀）
2. 编写继承自 `tool.plugin.Plugin` 的类 `Action`
3. 在 `./data/plugin.json` 中注册插件
4. （可选）配置动画、碰撞体和状态反馈文本

### 详细步骤

#### 1. 创建插件文件

在 `action/` 目录下新建 Python 文件，文件名建议以 `act-` 为前缀，单词间用连字符连接。

```
action/
├── act-action.py   # 新插件
```

> **命名规范**：文件名中的 `act-` 前缀用于标识行动插件，便于统一管理。

#### 2. 编写插件类

**模板：**

``` python
# action/act-action.py
from tool.plugin import Plugin

class Action(Plugin):  # 类名必须为 Action
    def __init__(self):
        super().__init__()

        # 必须设置 id 和 state
        self.id = "act-action"   # 应与文件名一致
        self.name = "行动"       # 在行动面板显示的名称（非自启动插件必须设置）
        self.description = "这是插件的描述"  # 可选，用于行动面板的鼠标悬浮提示
        self.state = "act-action"  # 状态名，用于状态机切换
        self.auto = False        # 是否在程序启动时自动运行，默认为 False
        self.teardownImmed = True   # 是否在行动停止后立即卸载插件，默认为True

    def start(self):
        """开始行动"""
        # do something here
        super().start()

    def stop(self):
        """停止行动"""
        # do something here
        super().stop()
    
    def eventFilter(self, obj, event: QEvent):
        """处理输入事件"""
        # do something here
        return super().eventFilter(obj, event)
    
    ### 更多功能

    def setup(self, window) -> None:
        """绑定信号等操作"""
        super().setup(window)
        # do something here ### 注意：写在super().setup(window)下面
    
    def teardown(self) -> None:
        """信号解绑与释放资源等操作"""
        # do something here
        super().teardown()
```

> **关键说明**：
> - **类名必须为 `Action`**（便于插件管理器加载与管理）
> - `self.window` 关联 `PetWindow` 实例，可调用其公开方法
> - 非自启动行动开始后，**会暂停其他状态的自动切换**，直至插件调用 `stop`、用户点击行动面板的"结束"按钮或手动切换状态
> - 不需要在 `stop` 中手动切回待机状态（行动结束时会自动切换）
> - **初始化中涉及主窗口的操作应移至 `setup`，并先调用 `super().setup(window)`**

#### 3. 注册插件

编辑 `./data/plugin.json`：

``` json
"act-action": {
    "path": "action.act-action",
    "enabled": true,
    "dependencies": []
}
```

- 键：插件 ID（须与 `self.id` 一致）
- 值：
    - `path`: 模块导入路径（如 `action.act-action`）
    - `enabled`: 是否启用
    - `dependencies`: 依赖的插件 ID 列表（用于控制加载顺序）

#### 4. 注册状态并配置状态反馈文本

在 `./data/state.json` 中添加状态反馈文本（可选）：

``` json
"状态名": []  // 只注册状态，不显示回复
```

``` json
"状态名": [
    "反馈1",
    "反馈2"
]
```

在 `start` 中调用 `self.window.dialogMenu.addLine` 手动显示回复，或通过 `conv.replyText("state", self.id)` 获取随机回复。

#### 5. 配置动画（可选）

若行动需要播放动画，在 `./data/anime.json` 中添加条目：

``` json
"动画名": {
    "path": "./img/帧文件夹路径",
    "fps": 30,
    "loop": true
}
```

在 `start` 中调用 `self.window.changeAnime(self.id)` 即可播放。

#### 6. 配置碰撞体（可选）

在 `./data/collision.json` 中添加碰撞体：

``` json
"碰撞体名": {
    "left": 11,
    "top": 30,
    "width": 135,
    "height": 30
}
```

导入 `tool.mouse.getCollision` 函数获取鼠标所在的碰撞体。

### 完整示例：跳舞插件

#### 插件代码

``` python
# action/act-dance.py
from tool.plugin import Plugin
from tool import conv

class Action(Plugin):
    def __init__(self):
        super().__init__()

        self.id = "act-dance"
        self.state = "dance"
        self.name = "跳舞"
        self.description = "让宠物跳舞"

    def start(self):
        # 切换动画
        self.window.changeAnime(self.id)
        # 获取并显示随机回复
        reply = conv.replyText("state", self.id)
        self.window.dialogMenu.addLine(reply)
        super().start()

    def stop(self):
        super().stop()
```

#### 注册

``` json
// data/plugin.json
{
    "act-dance": {
        "path": "action.act-dance",
        "enabled": true,
        "dependencies": []
    }
}
```

#### 动画配置

``` json
// data/anime.json
"act-dance": {
    "path": "./img/act-dance",
    "fps": 20,
    "loop": true
}
```

#### 状态反馈文本

``` json
// data/state.json
"dance": [
    "喵喵喵！",
    "一起来跳舞吧！"
]
```

### 进阶：自启动插件

若希望插件在程序启动时自动运行，将 `self.auto` 设置为 `True`：

``` python
class Action(Plugin):
    def __init__(self):
        super().__init__()
        self.id = "act-auto"
        self.state = "act-auto"
        self.auto = True  # 程序启动时自动运行

    def start(self):
        # do something here
        super().start()

    def stop(self):
        # do something here
        super().stop()
```

> **注意**：
> - 自启动插件会在宠物窗口初始化后自动运行
> - 自动插件不会显示在行动面板中
> - 自启动插件**不会暂停其他状态的自动切换**

### 进阶：事件过滤器

若你的插件需要捕获鼠标、键盘等事件，可重写 `eventFilter` 方法：

``` python
from PySide6.QtCore import QEvent

from tool.plugin import Plugin

class Action(Plugin):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            print("鼠标按下了！")
            # 返回 True 表示拦截事件，不再传递给窗口
            return True
        return super().eventFilter(obj, event)
```

> **注意**：
> - 事件过滤器的安装和移除由基类的 `start`/`stop` 自动处理，无需手动操作
> - 拦截事件可能影响宠物正常交互，请谨慎使用

### 进阶：插件依赖

若插件需要依赖其他插件，可在 `plugin.json` 中通过 `dependencies` 字段声明：

``` json
"act-plugin-b": {
    "path": "action.act-plugin-b",
    "enabled": true,
    "dependencies": ["act-plugin-a"]
}
```

- 插件管理器会按拓扑顺序加载插件，确保依赖的插件先被加载
- 若存在循环依赖，会抛出错误并停止加载

### 进阶：扩展设置面板

插件可以通过 `SettingMenu.addPage` 向设置面板添加自定义配置页：

``` python
def setup(self, window) -> None:
    super().setup(window)
    
    # 创建自定义设置页面
    self.pg = QWidget()
    layout = QFormLayout()
    self.myEdit = QLineEdit("默认值")
    layout.addRow("我的配置:", self.myEdit)
    self.pg.setLayout(layout)
    
    # 添加到设置面板
    self.window.settingMenu.addPage(self.pg, "我的插件配置")
    
    # 监听数据更新信号以保存配置
    self.window.settingMenu.dataUpdated.connect(self.saveConfig)
```

### 进阶：控制插件卸载行为

插件提供 `teardownImmed` 属性控制停止后的卸载行为：

- `teardownImmed = True`（默认）：插件停止后立即调用 `teardown` 卸载，释放资源
- `teardownImmed = False`：插件停止后保留实例，`teardown` 不会立即调用

``` python
class Action(Plugin):
    def __init__(self):
        super().__init__()
        self.id = "act-persistent"
        self.teardownImmed = False  # 停止后保留实例
```

适用场景：
- 插件需要频繁启动/停止，保留实例可避免重复初始化开销
- 插件需要在停止后保留某些状态供下次使用

---

## 常见问题

**Q: 插件加载失败怎么办？**

A: 检查以下几点：
1. 文件名和 `plugin.json` 中的键是否一致
2. 模块导入路径是否正确（如 `action.act-xxx`）
3. 类名是否为 `Action`
4. `self.id` 是否与 `plugin.json` 中的键一致

**Q: 在 `__init__`/`setup` 中获取主窗口（`self.window`）报错：AttributeError: 'NoneType' object has no attribute 'xxx' 怎么办？**

A: 主窗口还未完成初始化。**初始化中涉及主窗口的操作应移至 `setup`，并先调用 `super().setup(window)`**。

**Q: 行动开始后宠物不响应鼠标操作？**

A: 检查其他插件是否拦截了事件（`eventFilter` 返回了 `True`）。

**Q: 如何让行动在结束后自动恢复待机？**

A: 无需处理，行动结束时会自动切换回 `idle` 状态。

**Q: 动画不播放怎么办？**

A: 检查：
1. `anime.json` 中是否配置了对应动画
2. 帧图片是否按数字顺序命名（`0.png`, `1.png`...）
3. 调用 `changeAnime` 时传入的动画名是否正确

**Q: 自动启动插件和普通插件有什么区别？**

A: `auto = True` 的插件在程序启动时自动运行，不会出现在行动面板中，**不暂停其他状态的自动切换**，适合后台任务；普通插件需要在行动面板中手动点击执行，**会暂停其他状态切换**。

**Q: `PluginManager` 和 `PetWindow` 的关系是什么？**

A: `PetWindow` 持有 `PluginManager` 实例，通过它管理所有插件的加载、启动和停止。`PetWindow` 的 `startAct`、`stopCurrentAct`、`getAct` 等方法是对 `PluginManager` 的封装。

**Q: `teardownImmed` 和 `teardown` 有什么区别？**

A: `teardownImmed` 是一个控制属性，决定插件停止后是否立即调用 `teardown` 方法。`teardown` 是实际执行资源清理的方法，你可以在其中进行信号解绑、删除临时控件等。
