# 桌面宠物

## 目录
- [项目简介](#项目简介)
- [适宜人群](#适宜人群)
- [环境依赖](#环境依赖)
- [项目结构](#项目结构)
- [API](#api)
- [操作简介（宠物本体）](#操作简介宠物本体)
- [桌宠管理器](#桌宠管理器)
- [核心机制](#核心机制)
- [自定义](#自定义)
    - [配置说明](#配置说明)
        - [base.json 基础配置](#basejson-基础配置)
        - [anime.json 动画配置](#animejson-动画配置)
        - [collision.json 碰撞体配置](#collisionjson-碰撞体配置)
        - [state.json 状态反馈文本配置](#statejson-状态反馈文本配置)
        - [dialog.json 对话文本配置](#dialogjson-对话文本配置)
        - [plugin.json 插件注册配置](#pluginjson-插件注册配置)
        - [pluginState.json 插件启用状态配置](#pluginstatejson-插件启用状态配置)
    - [自定义行动（插件开发）](#自定义行动插件开发)
- [更新日志](#更新日志)

---

## 项目简介

基于 PySide6 框架开发的桌面宠物项目，支持多宠物配置、自定义动画、状态反馈、对话和扩展行为（插件）。宠物会随机移动、响应点击拖拽、通过对话菜单互动，并能执行自定义行动（插件）。桌宠管理器可在同一程序中管理多个宠物配置，并通过命令行启动不同宠物。

## 适宜人群

- 准备好动画/对话文本，希望通过简单配置直接使用
- 有基本的 Python、PySide6 编程能力，但不想从 0 开始制作
- 需要较自由的自定义功能
- PySide6 学习者
- 想要制作桌宠项目，希望得到一些灵感

## 环境依赖

- Python 3.10+
- PySide6

``` shell
pip install pyside6
```

## 项目结构

```
.
├── .gitattributes                # Git 属性配置
├── .gitignore                    # Git 忽略文件列表
├── API-manager.md                # 管理器 API 接口文档
├── API-pet.md                    # 桌宠 API 接口文档
├── CHANGELOG.md                  # 版本更新日志
├── customization.md              # 自定义/定制化指南
├── manager.py                    # 桌宠管理器入口文件
├── pet.py                        # 桌宠本体入口文件
├── README.md                     # 项目介绍与快速开始
│
├── pet/                          # 宠物资源包根目录
│   ├── config.json               # 宠物路径配置文件
│   └── Mutumi/                   # 具体宠物角色（Mutumi）资源包（此为示例）
│       ├── info.json             # 宠物元信息
│       ├── introduction.md       # 宠物介绍
│       ├── log.log               # 运行时日志文件
│       ├── config/               # 宠物行为配置文件
│       │   ├── anime.json        # 动画序列配置
│       │   ├── base.json         # 基础属性
│       │   ├── collision.json    # 碰撞检测参数
│       │   ├── dialog.json       # 对话/气泡文本配置
│       │   ├── pluginState.json  # 插件启用状态配置
│       │   └── state.json        # 状态反馈文本配置
│       └── img/                  # 动画帧图片资源
│           ├── after-stroke/     # 抚摸后反应动画帧
│           ├── drag/             # 拖拽中动画帧
│           ├── entre/            # 入场动画帧
│           ├── exit/             # 退场动画帧
│           ├── idle/             # 待机动画帧
│           ├── stroke/           # 被抚摸时动画帧
│           ├── turn-off-fan/     # 关闭风扇动作帧
│           └── using-fan/        # 使用风扇动作帧
│
├── plugin/                       # 插件系统（行为扩展）
│   ├── attr/                     # 属性系统插件
│   │   ├── attr.py               # 属性管理逻辑
│   │   └── data.json             # 属性数据
│   ├── move_randomly/            # 随机移动插件
│   │   ├── data.json             # 移动参数
│   │   └── move_randomly.py      # 随机移动实现
│   ├── drag.py                   # 拖拽行为插件
│   ├── idle.py                   # 待机行为插件（必须启用）
│   ├── stroke.py                 # 抚摸交互插件
│   └── use_fan.py                # 使用风扇道具插件
│
├── tool/                         # 通用工具/辅助模块
│   ├── __init__.py               # 工具包初始化
│   ├── anime.py                  # 动画控制
│   ├── config.py                 # 配置读取与管理
│   ├── conv.py                   # 回复文本生成
│   ├── mouse.py                  # 鼠标碰撞检测
│   ├── plugin.py                 # 插件基类与插件管理器
│   ├── stateMachine.py           # 状态机核心实现
│   └── widgetFactory.py          # 页面工厂
│
└── window/                       # GUI 窗口模块
    ├── manager/                  # 管理器窗口
    │   ├── mainWindow.py         # 管理器主窗口
    │   └── managerPage.py        # 管理器页面
    └── pet/                      # 宠物相关窗口
        ├── actionMenu.py         # 动作菜单
        ├── dialogMenu.py         # 对话菜单
        ├── petWindow.py          # 宠物主窗口
        ├── settingMenu.py        # 设置菜单
        └── stateMenu.py          # 状态菜单
```

## API

- [API-pet.md](./API-pet.md) — 宠物本体 API
- [API-manager.md](./API-manager.md) — 桌宠管理器 API

## 操作简介（宠物本体）

| 操作 | 反馈 |
| :---: | :---: |
| 左键拖拽 | 切换 `drag` 状态，宠物跟随鼠标移动 |
| 左键点击 `head` 碰撞区 | 触发 `stroke` 状态 |
| 闲置等待 | 自动进入 `idle` 状态，随机移动 |
| 右键菜单 | 打开对话/状态/行动/设置面板 |

## 桌宠管理器

管理器（`manager.py`）提供了一个图形化界面，用于集中管理所有已注册的宠物。

**主要功能**：

- 桌宠管理
    1. **宠物列表**：左侧列表显示所有已注册的宠物，支持搜索筛选
    2. **宠物介绍**：查看宠物的 `introduction.md` 介绍文档
    3. **配置编辑**：可视化编辑宠物的所有配置文件（基础项、动画、碰撞体、状态反馈文本、对话文本、插件状态）
    4. **快速启动**：双击宠物列表项即可启动对应宠物
    5. **打开桌宠文件**：在文件资源管理器中打开宠物文件夹
    6. **宠物删除**：从系统中移除宠物（功能待完善）
- 插件管理（未完成）
- 官方文档查看（未完成）
- 管理器设置（未完成）

**宠物注册**：

在 `./pet/config.json` 中注册宠物：

``` json
{
    "宠物名": "./pet/宠物名/"
}
```

每个宠物目录需包含：
- `info.json`：宠物元信息（名称、图标、版本、作者）
- `introduction.md`：宠物介绍文档
- `config/`：所有配置文件
- `img/`：动画帧图片

## 核心机制

1. **多宠物支持**
    - 通过 `./pet/config.json` 注册多个宠物
    - 每个宠物拥有独立的配置、图片和插件状态
    - 通过桌宠管理器可视化管理所有宠物

2. **动画系统**
    - 基于帧序列图片播放，支持循环/单次播放
    - 窗口自动适应图片大小
    - 支持异步（定时器驱动）和同步（阻塞）两种播放模式

3. **状态机**
    - 状态切换时触发对应的反馈文本和动画

4. **对话系统**
    - 随机从 `dialog.json` 抽取问题选项
    - 反馈文本从 `state.json` 随机选取
    - 回复文本从 `dialog.json` 随机选取

5. **自定义行动（插件系统）**
    - 通过 `./plugin/` 目录添加插件模块
    - 在 `plugin.json` 中注册，在 `pluginState.json` 中决定是否启用
    - 插件须继承 `tool.plugin.Plugin` 基类，类名必须为 `Action`
    - 支持自动启动插件（`auto = True`）
    - 支持插件依赖排序（通过 `deps` 字段）
    - 支持插件热卸载（`teardownImmed` 控制是否立即卸载）

6. **页面工厂**
    - 提供 `FormFactory`、`DynamicListFactory`、`FormBoxFactory`、`ListBoxFactory`、`SearchStackFactory` 等工厂类
    - 用于快速构建设置面板和插件属性面板
    - 支持数据绑定、自动信号转发和值同步

## 自定义

### 配置说明

#### base.json 基础配置

| 键 | 说明 | 类型 |
| :---: | :---: | :---: |
| `log-path` | 日志保存路径 | str |
| `quesSelecter-item-count` | 对话面板最大显示问题数 | int |
| `idle-time` | 待机判定时间（毫秒） | int |

---

#### anime.json 动画配置

``` json
"动画名": {
    "path": "文件夹路径",
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
> - 动画名建议使用小写字母和连字符（如 `using-fan`）
> - 帧图片需按数字顺序命名（如 `0.png`、`1.png`、`2.png`...）

---

#### collision.json 碰撞体配置

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

#### state.json 状态反馈文本配置

``` json
"状态名": [
    "反馈1",
    "反馈2"
]
```

- 状态切换时从对应数组中随机选取一条回复
- 若状态不需要回复，设置为空数组即可
- **新建的状态必须在此文件内注册**

---

#### dialog.json 对话文本配置

``` json
"问题": [
    "回复1",
    "回复2"
]
```

- 用户在对话面板选择问题后，从对应回复数组中随机选取一条

---

#### plugin.json 插件注册配置

位于 `./pet/plugin.json`（全局插件注册表）。

``` json
"插件ID": {
    "path": "./plugin/xxx.py",
    "deps": []
}
```

| 键 | 类型 | 说明 |
| :--- | :--- | :--- |
| `path` | str | 插件文件路径（相对于项目根目录） |
| `deps` | list[str] | 依赖的插件 ID 列表，用于控制加载顺序 |

> **注意**：
> - 插件 ID 须与插件类中 `self.id` 一致
> - 插件启用状态在 `pluginState.json` 中单独管理

---

#### pluginState.json 插件启用状态配置

位于 `./pet/你的宠物/config/pluginState.json`。

``` json
{
    "插件1ID": true,
    "插件2ID": false
}
```

- `true` 表示启用，`false` 表示禁用

---

### 自定义行动（插件开发）

**快速上手**：

1. 在 `plugin/` 目录新建 Python 文件（如 `dance.py`）
2. 编写继承自 `tool.plugin.Plugin` 的类 `Action`
3. 在 `./pet/plugin.json` 中注册插件
4. 在 `./pet/你的宠物/config/pluginState.json` 中启用插件
5. （可选）配置动画、碰撞体和状态反馈文本

**插件基础模板**：

``` python
# plugin/dance.py
from tool.plugin import Plugin
from tool import conv

class Action(Plugin):
    def __init__(self):
        super().__init__()
        self.id = "dance"           # 须与 plugin.json 中的键一致
        self.name = "跳舞"           # 在行动面板显示的名称
        self.description = "让宠物跳舞" # 鼠标悬浮提示
        self.state = "dance"        # 对应的状态名
        self.auto = False           # 是否自启动
        self.teardownImmed = True   # 停止后是否立即卸载

    def setup(self, window) -> None:
        """安装插件，关联主窗口（涉及主窗口的初始化请放在此处）"""
        super().setup(window)
        # 在此绑定信号、添加页面等

    def teardown(self) -> None:
        """卸载插件，清理资源"""
        # 在此解绑信号、删除临时控件等
        super().teardown()

    def start(self):
        """开始行动"""
        self.window.changeAnime(self.id)
        reply = conv.replyText("state", self.id, self.window.configManager)
        self.window.dialogMenu.addLine(reply)
        super().start()

    def stop(self):
        """停止行动"""
        super().stop()
```

> **注意**：
> - 行动开始后会暂停其他状态切换，直至调用 `stop` 或点击"结束"按钮
> - 可通过 `self.window` 访问主窗口的公开方法
> - 设置 `self.auto = True` 可使插件在程序启动后自动运行（不会出现在行动面板）
> - **初始化中涉及主窗口的操作应移至 `setup`，并先调用 `super().setup(window)`**
> - **类名必须为 `Action`**
> - `teardownImmed` 控制插件停止后是否立即卸载，默认为 `True`
> - 在插件中可使用 `tool.widgetFactory` 提供的工厂类快速构建设置页面或属性面板

**常见插件示例**：

- **`idle.py`**：待机状态管理，定时触发回复
- **`stroke.py`**：点击头部触发抚摸状态
- **`drag.py`**：拖拽移动宠物
- **`move_randomly/move_randomly.py`**：待机时随机移动
- **`use_fan.py`**：点击风扇开关切换状态
- **`attr/attr.py`**：属性系统（好感度、饱腹度），在状态面板显示进度条

---

## 更新日志

详见 [CHANGELOG.md](./CHANGELOG.md)。
