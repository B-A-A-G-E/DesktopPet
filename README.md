# 桌面宠物

## 目录
- [项目简介](#项目简介)
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
    - [v0.4.2（最新）](#v042最新)
    - [v0.3.2.1](#v0321)
    - [v0.3.1](#v031)
    - [v0.2](#v02)
    - [v0.1](#v01)

---

## 项目简介

基于 PySide6 开发的桌面电子宠物程序，支持自定义动画、交互反馈和扩展行为。宠物会随机移动、响应点击拖拽、通过对话菜单互动，并能执行自定义行动（插件）。

## 环境依赖

- Python 3.8+
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
│   ├── load_failed.png     # 加载失败占位图
│   ├── entre/              # 入场动画帧
│   ├── exit/               # 退场动画帧
│   ├── idle/               # 待机动画帧
│   ├── stroke/             # 抚摸动画帧
│   ├── drag/               # 拖拽动画帧
│   ├── after-stroke/       # 抚摸后动画帧
│   ├── after-drag/         # 拖动后动画帧
│
├── tool/                   # 工具模块
│   ├── anime.py            # 动画播放引擎
│   ├── data.py             # 数据加载与全局变量
│   ├── conv.py             # 对话回复生成器
│   ├── mouse.py            # 鼠标交互辅助
│   └── plugin.py           # 插件基类
│
├── window/                 # 窗口模块
│   ├── petWindow.py        # 主窗口（宠物本体）
│   ├── dialogMenu.py       # 对话面板
│   ├── stateMenu.py        # 状态日志面板
│   ├── actionMenu.py       # 行动面板
│   └── settingMenu.py      # 设置面板
│
└── action/                 # 自定义行动（插件）目录
```

## API

详见 [API.md](./API.md)。

## 操作简介（宠物本体）

| 操作 | 反馈 |
| :---: | :---: |
| 左键拖拽 | 切换 `drag` 状态，宠物跟随鼠标移动 |
| 左键点击 `stroke` 碰撞区并拖拽 | 触发 `stroke` 状态（可配置碰撞体） |
| 闲置等待 | 自动进入 `idle` 状态，随机移动 |
| 右键菜单 | 打开对话/状态/行动/设置面板 |

## 核心机制

1. 动画系统
    - 基于帧序列图片播放，支持循环/单次播放
    - 窗口自动适应图片大小
    - 支持异步（定时器驱动）和同步（阻塞）两种播放模式
2. 状态机
    - 状态切换时触发对应的反馈文本和动画
    - 支持 `after-{state}` 后续事件（如抚摸后播放特殊动画）
3. 对话系统
    - 随机从 `dialog.json` 抽取问题选项
    - 回复文本从 `state.json` 或 `dialog.json` 随机选取
4. 自定义行动（插件系统）
    - 通过 `action/` 目录添加插件模块
    - 在 `plugin.json` 中注册后即可在行动面板调用
    - 插件须继承 `tool.plugin.Plugin` 基类
    - 支持自动启动插件（`auto = True`）
5. 设置面板
    - 可视化编辑所有 JSON 配置文件
    - 支持动态增删状态/对话文本条目

## 自定义

### base.json 基础配置

| 键 | 说明 | 默认值 |
| :---: | :---: | :---: |
| `log-path` | 日志保存路径 | `./log.log` |
| `load-failed-img-path` | 加载失败占位图路径 | `./img/load_failed.png` |
| `quesSelecter-item-count` | 对话面板最大显示问题数 | `10` |
| `idle-time` | 待机判定时间（毫秒） | `10000` |
| `idle-move-time` | 随机移动间隔（毫秒） | `15000` |
| `move-min-step` | 移动最小距离（像素） | `200` |
| `move-max-step` | 移动最大距离（像素） | `3000` |
| `move-step-time` | 步进间隔（毫秒） | `20` |
| `move-speed` | 移动速度（像素/步） | `10` |

---

### anime.json 动画配置

``` json
"状态名": {
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
> - 状态名建议使用小写字母和连字符（如 `act-dance`），以保持统一风格
> - 帧图片需按数字顺序命名（如 `0.png`, `1.png`, `2.png`...）

---

### collision.json 碰撞体配置

``` json
"状态名": {
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

桌面宠物通过插件系统支持自定义交互行为，详细教程请参阅 [customization.md](./customization.md)。

**快速上手**：

1. 在 `action/` 目录新建 Python 文件（如 `act-my-action.py`）
2. 编写继承自 `tool.plugin.Plugin` 的类，重写 `start` 和 `stop` 方法
3. 在 `./data/plugin.json` 中注册插件
4. （可选）配置动画和状态反馈文本

**插件模板**：

``` python
# action/act-action.py
from tool.plugin import Plugin

class MyAction(Plugin):
    def __init__(self):
        super().__init__()
        self.id = "act-action"
        self.name = "Action"
        self.description = "This is an action"  # 可选，用于鼠标悬浮提示

    def start(self):
        pass

    def stop(self):
        pass
```

> **注意**：
> - 行动开始后会阻塞其他状态切换，直至调用 `stop` 或点击"结束"按钮
> - 可通过 `self.window` 访问主窗口的公开方法
> - 设置 `self.auto = True` 可使插件在程序启动时自动运行

---

## 更新日志

版本号格式：**主版本号.次版本号[.修订版本号]**

### v0.4.2（最新）

1. 完全重写插件的实现逻辑（由纯函数改为类继承）
2. 丰富插件功能（事件过滤器、插件生命周期管理）
3. 丰富日志系统（新增 `PluginLoaded` 日志类型）
4. 行动面板新增提示（`ToolTip`）
5. 加入自启动插件
6. 将`stroke`与`drag`事件重写为插件

### v0.3.2.1

1. 拆分了 `PetWindow` 的 `replyAction` 函数
2. 迁移 `plugin.json` 文件到 `./data/`
3. 修复了 `mouse.py` 中 `getCollision` 传参过少导致报错的问题
4. 修复鼠标抬起必定切回待机的 bug
5. 预留了两个行动
6. 让D指导写了篇 API 文档

### v0.3.1

1. 加入行动自定义功能与行动面板
2. 将部分含 "action" 的变量/函数等的命名规范为 "state"
3. 丰富日志系统
4. 优化判定，防崩溃
5. 重写了 README 文件

### v0.2

1. 加入待机时随机移动的功能
2. 加入 "after-state" 类型事件
3. 丰富日志系统
4. 修复动画切换异常等 bug
5. 俗手偶得，获得更多 bug
6. 借助 AI 完善设置界面
7. 基本确保自定义功能稳定运行
8. 用 AI 给几个我也看不懂的地方写注释

### v0.1

1. 新建项目并实现基本功能
（时间较久远，记不清修改）
