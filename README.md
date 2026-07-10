# 桌面宠物

## 目录
- [项目简介](#项目简介)
- [适宜人群](#适宜人群)
- [环境依赖](#环境依赖)
- [项目结构](#项目结构)
- [API](#api)
- [操作简介（宠物本体）](#操作简介宠物本体)
- [核心机制](#核心机制)
- [自定义](#自定义)
    - [base.json 基础配置](#basejson-基础配置)
    - [anime.json 动画配置](#animejson-动画配置)
    - [collision.json 碰撞体配置](#collisionjson-碰撞体配置)
    - [state.json 状态反馈文本配置](#statejson-状态反馈文本配置)
    - [dialog.json 对话文本配置](#dialogjson-对话文本配置)
    - [自定义行动（插件开发）](#自定义行动插件开发)
- [更新日志](#更新日志)

---

## 项目简介

基于 PySide6 框架开发的桌面宠物项目，支持自定义动画、状态反馈、对话和扩展行为（插件）。宠物会随机移动、响应点击拖拽、通过对话菜单互动，并能执行自定义行动（插件）。

## 适宜人群

- 准备好动画/对话文本，希望通过简单配置直接使用
- 有基本的 python、PySide6 编程能力，但不想从0开始制作
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
├── main.py                 # 程序入口
├── log.log                 # 运行日志
├── README.md
├── API.md                  # API 文档
├── customization.md        # 自定义教程
├── .gitignore
├── .gitattributes
│
├── data/                   # 配置文件目录
│   ├── base.json           # 基础配置
│   ├── plugin.json         # 插件注册配置
│   ├── anime.json          # 动画配置
│   ├── collision.json      # 碰撞体配置
│   ├── state.json          # 状态反馈文本
│   └── dialog.json         # 对话文本
│
├── img/                    # 图片资源目录
│   ├── entre/              # 入场动画帧
│   ├── exit/               # 退场动画帧
│   ├── idle/               # 待机动画帧
│   ├── stroke/             # 抚摸动画帧
│   ├── drag/               # 拖拽动画帧
│   ├── after-stroke/       # 抚摸后动画帧
│   ├── using-fan/          # 吹风扇动画帧
│   └── turn-off-fan/       # 关风扇动画帧
│
├── tool/                   # 工具模块
│   ├── anime.py            # 动画播放引擎
│   ├── data.py             # 数据加载与全局变量
│   ├── conv.py             # 对话回复生成器
│   ├── mouse.py            # 鼠标交互辅助
│   ├── stateMachine.py     # 状态机
│   └── plugin.py           # 插件基类与插件管理器
│
├── window/                 # 窗口模块
│   ├── petWindow.py        # 主窗口（宠物本体）
│   ├── dialogMenu.py       # 对话面板
│   ├── stateMenu.py        # 状态日志面板
│   ├── actionMenu.py       # 行动面板
│   └── settingMenu.py      # 设置面板
│
└── plugin/                 # 自定义行动（插件）目录
    ├── stroke.py           # 抚摸事件
    ├── drag.py             # 拖拽事件
    ├── move-randomly/      # 随机移动事件目录
    │   ├── move_randomly.py  # 随机移动事件
    │   └── data.json       # 配置文件
    ├── use_fan.py          # 吹风扇行动
    └── attr/               # 属性系统插件目录
        ├── attr.py         # 属性系统主文件
        └── data.json       # 属性配置文件
```

## API

详见 [API.md](./API.md)。

## 操作简介（宠物本体）

| 操作 | 反馈 |
| :---: | :---: |
| 左键拖拽 | 切换 `drag` 状态，宠物跟随鼠标移动 |
| 左键点击 `head` 碰撞区 | 触发 `stroke` 状态 |
| 闲置等待 | 自动进入 `idle` 状态，随机移动 |
| 右键菜单 | 打开对话/状态/行动/设置面板 |

## 核心机制

1. 动画系统
    - 基于帧序列图片播放，支持循环/单次播放
    - 窗口自动适应图片大小
    - 支持异步（定时器驱动）和同步（阻塞）两种播放模式
2. 状态机
    - 状态切换时触发对应的反馈文本和动画
    - 支持 `after-state` 后续事件（如抚摸后播放特殊动画）
3. 对话系统
    - 随机从 `dialog.json` 抽取问题选项
    - 反馈文本从 `state.json` 随机选取
    - 回复文本从 `dialog.json` 随机选取
4. 自定义行动（插件系统）
    - 通过 `plugin/` 目录添加插件模块
    - 在 `plugin.json` 中注册后即可在行动面板调用
    - 插件须继承 `tool.plugin.Plugin` 基类，类名必须为 `Action`
    - 支持自动启动插件（`auto = True`）
    - 支持插件依赖排序（通过 `dependencies` 字段）
    - 支持插件热卸载（`teardownImmed` 控制是否立即卸载）
5. 设置面板
    - 可视化编辑所有 JSON 配置文件（后续添加的 JSON 需在 `SettingMenu.addPage` 新建编辑页）
    - 支持动态增删状态/对话文本条目

## 自定义

桌面宠物通过插件系统支持自定义行为，详细教程请参阅 [customization.md](./customization.md)。

### base.json 基础配置

| 键 | 说明 | 默认值 |
| :---: | :---: | :---: |
| `log-path` | 日志保存路径 | `./log.log` |
| `quesSelecter-item-count` | 对话面板最大显示问题数 | `10` |
| `idle-time` | 待机判定时间（毫秒） | `10000` |

---

### anime.json 动画配置

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
> - 动画名建议使用小写字母和连字符（如 `using-fan`），以保持风格统一
> - 帧图片需按数字顺序命名（如 `0.png`, `1.png`, `2.png`...）
> - 若需在 `PetWindow.replyState` 中自动播放，动画名需与状态名一致

---

### collision.json 碰撞体配置

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

### state.json 状态反馈文本配置

``` json
"状态名": [
    "反馈1",
    "反馈2"
]
```

- 状态切换时从对应数组中随机选取一条回复
- 若状态不需要回复，设置为空数组即可

---

### dialog.json 对话文本配置

``` json
"问题": [
    "回复1",
    "回复2"
]
```

- 用户在对话面板选择问题后，从对应回复数组中随机选取一条

---

### 自定义行动（插件开发）

**快速上手**：

1. 在 `plugin/` 目录新建 Python 文件（如 `action.py`）
2. 编写继承自 `tool.plugin.Plugin` 的类 `Action`
3. 在 `./data/plugin.json` 中注册插件
4. （可选）配置动画、碰撞体和状态反馈文本

**插件基础模板**：

``` python
# plugin/action.py
from tool.plugin import Plugin

class Action(Plugin):
    def __init__(self):
        super().__init__()
        self.id = "action"
        self.name = "Action"
        self.description = "This is an action"
        self.state = "state"
        self.auto = False
        self.teardownImmed = True

    def start(self):
        # do something here
        super().start()

    def stop(self):
        # do something here
        super().stop()
```

> **注意**：
> - 行动开始后会暂停其他状态切换，直至调用 `stop` 或点击"结束"按钮
> - 可通过 `self.window` 访问主窗口的公开方法
> - 设置 `self.auto = True` 可使插件在程序启动后自动运行
> - **初始化中涉及主窗口的操作应移至 `setup`，并先调用 `super().setup(window)`**
> - 插件 ID 须与 `plugin.json` 中的键一致
> - **类名必须为 `Action`**
> - `teardownImmed` 控制插件停止后是否立即卸载，默认为 `True`。若不希望卸载（如用于后续复用），可设为 `False`
> - 如需在状态面板中添加自定义属性页，可调用 `StateMenu.addPage`

---

## 更新日志

详见 [CHANGELOG.md](./CHANGELOG.md)。
