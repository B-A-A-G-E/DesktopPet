あ# 自定义教程

あ## 目录
あ- [自定义教程](#自定义教程)
あ  - [目录](#目录)
あ  - [概述](#概述)
あ  - [自定义基础配置](#自定义基础配置)
あ  - [自定义动画](#自定义动画)
あ    - [步骤](#步骤)
あ    - [动画配置示例](#动画配置示例)
あ  - [自定义碰撞体](#自定义碰撞体)
あ    - [步骤](#步骤-1)
あ    - [碰撞体配置示例](#碰撞体配置示例)
あ  - [自定义状态反馈文本](#自定义状态反馈文本)
あ    - [步骤](#步骤-2)
あ  - [自定义对话文本](#自定义对话文本)
あ    - [步骤](#步骤-3)
あ  - [自定义行动（插件）](#自定义行动插件)
あ    - [前置知识](#前置知识)
あ    - [步骤概览](#步骤概览)
あ    - [详细步骤](#详细步骤)
あ      - [1. 创建插件文件](#1-创建插件文件)
あ      - [2. 编写插件类](#2-编写插件类)
あ      - [3. 注册插件](#3-注册插件)
あ      - [4. 注册状态并配置状态反馈文本](#4-注册状态并配置状态反馈文本)
あ      - [5. 配置动画（可选）](#5-配置动画可选)
あ      - [6. 配置碰撞体（可选）](#6-配置碰撞体可选)
あ      - [7. 使用页面工厂构建自定义面板（可选）](#7-使用页面工厂构建自定义面板可选)
あ    - [完整示例：跳舞插件](#完整示例跳舞插件)
あ      - [插件代码](#插件代码)
あ      - [注册](#注册)
あ      - [动画配置](#动画配置)
あ      - [状态反馈文本](#状态反馈文本)
あ    - [进阶：自启动插件](#进阶自启动插件)
あ    - [进阶：事件过滤器](#进阶事件过滤器)
あ    - [进阶：插件依赖](#进阶插件依赖)
あ    - [进阶：使用页面工厂扩展设置面板](#进阶使用页面工厂扩展设置面板)
あ    - [进阶：控制插件卸载行为](#进阶控制插件卸载行为)
あ  - [常见问题](#常见问题)

あ---

あ## 概述

あ桌面宠物支持高度的自定义，你可以在不修改核心代码的情况下：

あ- 添加/修改动画
あ- 添加/修改碰撞体
あ- 添加/修改状态反馈文本
あ- 添加/修改对话文本
あ- 开发新的交互行为（插件）
あ- 扩展状态面板（添加属性页等）
あ- 扩展设置面板（添加配置页等）

あ所有配置均通过 JSON 文件管理，插件通过 Python 模块实现。

あ---

あ## 自定义基础配置

あ``` json
あ{
あ  "log-path": "./log.log",
あ  "quesSelecter-item-count": 10,
あ  "idle-time": 10000
あ}
あ```

あ| 键 | 说明 | 默认值 |
あ| :---: | :---: | :---: |
あ| `log-path` | 日志保存路径 | `./log.log` |
あ| `quesSelecter-item-count` | 对话面板最大显示问题数 | `10` |
あ| `idle-time` | 待机判定时间（毫秒） | `10000` |

あ---

あ## 自定义动画

あ### 步骤

あ1. **准备帧图片**：在 `./pet/你的宠物/img/` 下新建文件夹放入帧图片。图片须**按数字顺序命名**（如 `0.png`, `1.png`, `2.png`...）。
あ2. **编辑 `./pet/你的宠物/config/anime.json`**：配置动画，格式如下：

あ### 动画配置示例

あ``` json
あ"动画名": {
あ    "path": "./pet/你的宠物/img/文件夹路径",
あ    "fps": 30,
あ    "loop": true
あ}
あ```

あ| 键 | 类型 | 说明 |
あ| :--- | :--- | :--- |
あ| `path` | str | 帧图片存放文件夹路径 |
あ| `fps` | int | 播放帧率（帧/秒） |
あ| `loop` | bool | 是否循环播放 |

あ> **注意**：
あ> - 动画名建议使用小写字母和连字符（如 `using-fan`），以保持统一风格
あ> - 帧图片需按数字顺序命名（如 `0.png`, `1.png`, `2.png`...）
あ> - 若需在 `PetWindow.replyState` 中自动播放，动画名需与状态名一致

あ---

あ## 自定义碰撞体

あ碰撞体定义鼠标点击宠物的可交互区域。

あ### 步骤

あ1. **确定碰撞区域**：在图片上测量碰撞区相对于图片左上角的偏移和尺寸。
あ2. **编辑 `./pet/你的宠物/config/collision.json`**：配置碰撞体。

あ### 碰撞体配置示例

あ``` json
あ"碰撞体名": {
あ    "left": 11,
あ    "top": 30,
あ    "width": 135,
あ    "height": 30
あ}
あ```

あ| 键 | 类型 | 说明 |
あ| :--- | :--- | :--- |
あ| `left` | int | 碰撞区相对于窗口左上角的 X 偏移（像素） |
あ| `top` | int | 碰撞区相对于窗口左上角的 Y 偏移（像素） |
あ| `width` | int | 碰撞区宽度（像素） |
あ| `height` | int | 碰撞区高度（像素） |

あ---

あ## 自定义状态反馈文本

あ状态反馈文本是宠物切换状态时在对话面板显示的回复。

あ### 步骤

あ1. **编辑 `./pet/你的宠物/config/state.json`**：添加或修改条目。

あ``` json
あ"状态名": [
あ    "反馈1",
あ    "反馈2"
あ]
あ```

あ``` json
あ"状态名": [] // 只注册状态，不显示回复
あ```

あ- 新建的状态必须在此文件内注册，若不希望回复直接设置空数组即可
あ- 用 `PetWindow.operateState` 切换状态时会从对应数组中随机选取一条回复并播放动画
あ- 若状态无对应条目，则不显示回复

あ---

あ## 自定义对话文本

あ对话文本是用户通过对话面板提问时，宠物随机回复的内容。

あ### 步骤

あ1. **编辑 `./pet/你的宠物/config/dialog.json`**：添加或修改条目。

あ``` json
あ"问题": [
あ    "回复1",
あ    "回复2"
あ]
あ```

あ- 用户在对话面板选择问题后，宠物从对应回复数组中随机选取一条
あ- 支持任意数量的问题-回复对

あ---

あ## 自定义行动（插件）

あ插件系统允许向宠物添加新的交互行为，是自由度最高的自定义方式。

あ### 前置知识

あ- Python 面向对象编程（类继承）
あ- PySide6 事件系统基础（可选）

あ### 步骤概览

あ1. 在 `plugin/` 目录下新建 Python 文件
あ2. 编写继承自 `tool.plugin.Plugin` 的类 `Action`
あ3. 在 `./pet/你的宠物/config/plugin.json` 中注册插件
あ4. （可选）配置动画、碰撞体和状态反馈文本

あ### 详细步骤

あ#### 1. 创建插件文件

あ在 `plugin/` 目录下新建 Python 文件，单词间用连字符连接（如 `use-fan.py`）。

あ```
あplugin/
あ├── action.py   # 新插件
あ```

あ#### 2. 编写插件类

あ**模板：**

あ``` python
あ# plugin/action.py
あfrom tool.plugin import Plugin

あclass Action(Plugin):  # 类名必须为 Action
あ    def __init__(self):
あ        super().__init__()

あ        # 必须设置 id
あ        self.id = "action"   # 应与 `plugin.json` 中的键 一致
あ        self.name = "行动"       # 在行动面板显示的名称（非自启动插件必须设置）
あ        self.description = "这是插件的描述"  # 可选，用于行动面板的鼠标悬浮提示
あ        self.state = "action"  # 状态名，用于状态机切换
あ        self.auto = False        # 是否在程序启动时自动运行，默认为 False
あ        self.teardownImmed = True   # 是否在行动停止后立即卸载插件，默认为True

あ    def start(self):
あ        """开始行动"""
あ        # do something here
あ        super().start()

あ    def stop(self):
あ        """停止行动"""
あ        # do something here
あ        super().stop()
あ    
あ    def eventFilter(self, obj, event: QEvent):
あ        """处理输入事件"""
あ        # do something here
あ        return super().eventFilter(obj, event)
あ    
あ    ### 更多功能

あ    def setup(self, window) -> None:
あ        """绑定信号等操作"""
あ        super().setup(window)
あ        # do something here ### 注意：写在super().setup(window)下面
あ    
あ    def teardown(self) -> None:
あ        """信号解绑与释放资源等操作"""
あ        # do something here
あ        super().teardown()
あ```

あ> **关键说明**：
あ> - **类名必须为 `Action`**（便于插件管理器加载与管理）
あ> - `self.window` 关联 `PetWindow` 实例，可调用其公开方法
あ> - 非自启动行动开始后，**会暂停其他状态的自动切换**，直至插件调用 `stop`、用户点击行动面板的"结束"按钮或手动切换状态
あ> - 不需要在 `stop` 中手动切回待机状态（行动结束时会自动切换）
あ> - **初始化中涉及主窗口的操作应移至 `setup`，并先调用 `super().setup(window)`**

あ#### 3. 注册插件

あ编辑 `./pet/你的宠物/config/plugin.json`：

あ``` json
あ"action": {
あ    "path": "./plugin/action.py",
あ    "enabled": true,
あ    "deps": []
あ}
あ```

あ- 键：插件 ID（须与 `self.id` 一致）
あ- 值：
あ    - `path`: 模块导入路径（如 `./plugin/action.py`）
あ    - `enabled`: 是否启用
あ    - `deps`: 依赖的插件 ID 列表（用于控制加载顺序）


あ#### 4. 注册状态并配置状态反馈文本

あ在 `./pet/你的宠物/config/state.json` 中添加状态反馈文本（可选）：

あ``` json
あ"状态名": []  // 只注册状态，不显示回复
あ```

あ``` json
あ"状态名": [
あ    "反馈1",
あ    "反馈2"
あ]
あ```

あ在 `start` 中调用 `self.window.dialogMenu.addLine` 手动显示回复，或通过 `conv.replyText("state", self.id)` 获取随机回复。

あ#### 5. 配置动画（可选）

あ若行动需要播放动画，在 `./pet/你的宠物/config/anime.json` 中添加条目：

あ``` json
あ"动画名": {
あ    "path": "./pet/你的宠物/img/帧文件夹路径",
あ    "fps": 30,
あ    "loop": true
あ}
あ```

あ在 `start` 中调用 `self.window.changeAnime(动画名)` 即可播放。

あ#### 6. 配置碰撞体（可选）

あ在 `./pet/你的宠物/config/collision.json` 中添加碰撞体：

あ``` json
あ"碰撞体名": {
あ    "left": 11,
あ    "top": 30,
あ    "width": 135,
あ    "height": 30
あ}
あ```

あ导入 `tool.mouse.getCollision` 函数获取鼠标所在的碰撞体。

あ#### 7. 使用页面工厂构建自定义面板（可选）

あ页面工厂（`tool.widgetFactory`）提供了四种工厂类，可用于快速构建插件配置界面：

あ- **`FormFactory`**：创建键值对表单
あ- **`DynamicListFactory`**：创建可增删的动态列表
あ- **`FormBoxFactory`**：创建分组表单（`QToolBox` 容器）
あ- **`ListBoxFactory`**：创建分组列表（`QToolBox` 容器）

あ使用示例见下方的 [进阶：使用页面工厂扩展设置面板](#进阶使用页面工厂扩展设置面板)。

あ### 完整示例：跳舞插件

あ#### 插件代码

あ``` python
あ# plugin/dance.py
あfrom tool.plugin import Plugin
あfrom tool import conv

あclass Action(Plugin):
あ    def __init__(self):
あ        super().__init__()

あ        self.id = "dance"
あ        self.state = "dance"
あ        self.name = "跳舞"
あ        self.description = "让宠物跳舞"

あ    def start(self):
あ        # 切换动画
あ        self.window.changeAnime(self.id)
あ        # 获取并显示随机回复
あ        reply = conv.replyText("state", self.id)
あ        self.window.dialogMenu.addLine(reply)
あ        super().start()

あ    def stop(self):
あ        super().stop()
あ```

あ#### 注册

あ``` json
あ// pet/你的宠物/config/plugin.json
あ{
あ    "dance": {
あ        "path": "./plugin/dance.py",
あ        "enabled": true,
あ        "deps": []
あ    }
あ}
あ```

あ#### 动画配置

あ``` json
あ// pet/你的宠物/config/anime.json
あ"dance": {
あ    "path": "./pet/你的宠物/img/dance",
あ    "fps": 20,
あ    "loop": true
あ}
あ```

あ#### 状态反馈文本

あ``` json
あ// pet/你的宠物/config/state.json
あ"dance": [
あ    "喵喵喵！",
あ    "一起来跳舞吧！"
あ]
あ```

あ### 进阶：自启动插件

あ若希望插件在程序启动时自动运行，将 `self.auto` 设置为 `True`：

あ``` python
あclass Action(Plugin):
あ    def __init__(self):
あ        super().__init__()
あ        self.id = "auto"
あ        self.state = "auto"
あ        self.auto = True  # 程序启动时自动运行

あ    def start(self):
あ        # do something here
あ        super().start()

あ    def stop(self):
あ        # do something here
あ        super().stop()
あ```

あ> **注意**：
あ> - 自启动插件会在宠物窗口初始化后自动运行
あ> - 自动插件不会显示在行动面板中
あ> - 自启动插件**不会暂停其他状态的自动切换**

あ### 进阶：事件过滤器

あ若你的插件需要捕获鼠标、键盘等事件，可重写 `eventFilter` 方法：

あ``` python
あfrom PySide6.QtCore import QEvent

あfrom tool.plugin import Plugin

あclass Action(Plugin):
あ    def eventFilter(self, obj, event):
あ        if event.type() == QEvent.Type.MouseButtonPress:
あ            print("鼠标按下了！")
あ            # 返回 True 表示拦截事件，不再传递给窗口
あ            return True
あ        return super().eventFilter(obj, event)
あ```

あ> **注意**：
あ> - 事件过滤器的安装和移除由基类的 `start`/`stop` 自动处理，无需手动操作
あ> - 拦截事件可能影响宠物正常交互，请谨慎使用

あ### 进阶：插件依赖

あ若插件需要依赖其他插件，可在 `plugin.json` 中通过 `deps` 字段声明：

あ``` json
あ"plugin-b": {
あ    "path": "./plugin/plugin_b.py",
あ    "enabled": true,
あ    "deps": ["plugin-a"]
あ}
あ```

あ- 插件管理器会按拓扑顺序加载插件，确保依赖的插件先被加载
あ- 若存在循环依赖，会抛出错误并停止加载

あ### 进阶：使用页面工厂扩展设置面板

あ插件可以通过 `SettingMenu.addPage` 向设置面板添加自定义配置页：

あ``` python
あfrom tool.widgetFactory import FormFactory

あclass Action(Plugin):
あ    def setup(self, window) -> None:
あ        super().setup(window)
あ        
あ        # 使用 FormFactory 创建配置页面
あ        page = FormFactory([
あ            ("配置项1", "config1", "str"),
あ            ("配置项2", "config2", "int"),
あ            ("启用功能", "enabled", "bool"),
あ        ], self.config_data)
あ        page.build()
あ        
あ        # 添加到设置面板
あ        self.window.settingMenu.addPage(page, "我的插件配置")
あ        
あ        # 监听数据更新
あ        page.valChanged.connect(self.onConfigChanged)
あ        self.window.settingMenu.dataUpdated.connect(self.saveConfig)
あ```

あ**页面工厂类型选择**：
あ- **`FormFactory`**：适用于键值对配置
あ- **`DynamicListFactory`**：适用于可增删字符串列表配置
あ- **`FormBoxFactory`**：适用于分组表单配置
あ- **`ListBoxFactory`**：适用于分组列表配置

あ### 进阶：控制插件卸载行为

あ插件提供 `teardownImmed` 属性控制停止后的卸载行为：

あ- `teardownImmed = True`（默认）：插件停止后立即调用 `teardown` 卸载，释放资源
あ- `teardownImmed = False`：插件停止后保留实例，`teardown` 不会立即调用

あ``` python
あclass Action(Plugin):
あ    def __init__(self):
あ        super().__init__()
あ        self.id = "persistent"
あ        self.teardownImmed = False  # 停止后保留实例
あ```

あ适用场景：
あ- 插件需要频繁启动/停止，可避免重复安装开销
あ- 插件需要在停止后保留某些状态供下次使用

あ---

あ## 常见问题

あ**Q: 插件加载失败怎么办？**

: 检查以下几点：
あ1. 文件名和 `plugin.json` 中的键是否一致
あ2. 模块导入路径是否正确（如 `C:/DesktopPet/plugin/xxx.py` 或 `./plugin/xxx.py`）
あ3. 类名是否为 `Action`
あ4. `self.id` 是否与 `plugin.json` 中的键一致

あ**Q: 在 `__init__`/`setup` 中获取主窗口（`self.window`）报错：AttributeError: 'NoneType' object has no attribute 'xxx' 怎么办？**

: 主窗口还未完成初始化。**初始化中涉及主窗口的操作应移至 `setup`，并先调用 `super().setup(window)`**。

あ**Q: 行动开始后宠物不响应鼠标操作？**

: 检查其他插件是否拦截了事件（`eventFilter` 返回了 `True`）。

あ**Q: 如何让行动在结束后自动恢复待机？**

: 调用 `self.window.changeState("idle")` 或有关方法

あ**Q: 动画不播放怎么办？**

: 检查：
あ1. `anime.json` 中是否配置了对应动画
あ2. 帧图片是否按数字顺序命名（`0.png`, `1.png`...）
あ3. 调用 `changeAnime` 时传入的动画名是否正确

あ**Q: 自动启动插件和普通插件有什么区别？**

: `auto = True` 的插件在程序启动时自动运行，不会出现在行动面板中，**不暂停其他状态的自动切换**，适合后台任务；普通插件需要在行动面板中手动点击执行，**会暂停其他状态切换**。

あ**Q: `PluginManager` 和 `PetWindow` 的关系是什么？**

: `PetWindow` 持有 `PluginManager` 实例，通过它管理所有插件的加载、启动和停止。`PetWindow` 的 `startAct`、`stopAct`、`getAct` 等方法是对 `PluginManager` 的封装。

あ**Q: `teardownImmed` 和 `teardown` 有什么区别？**

: `teardownImmed` 是一个控制属性，决定插件停止后是否立即调用 `teardown` 方法。`teardown` 是实际执行资源清理的方法，你可以在其中进行信号解绑、删除临时控件等。
