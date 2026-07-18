# 桌面宠物

## 目录
- [项目简介](#项目简介)
- [适宜人群](#适宜人群)
- [环境依赖](#环境依赖)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [API 文档](#api-文档)
- [操作简介（宠物本体）](#操作简介宠物本体)
- [桌宠管理器](#桌宠管理器)
- [核心机制](#核心机制)
- [自定义](#自定义)
- [更新日志](#更新日志)

---

## 项目简介

基于 PySide6 框架开发的桌面宠物项目，支持多宠物并行管理与独立配置。能执行自定义行动（插件系统）。配套的桌宠管理器提供了图形化界面，便于管理宠物及其配置。

## 适宜人群

- **内容创作者**：准备好动画和对话文本，希望通过简单配置快速生成桌宠。
- **开发者**：具备基础的 Python 和 PySide6 编程能力，希望基于成熟框架进行二次开发或功能扩展。
- **学习者**：希望深入了解 PySide6 应用开发、状态机模式或插件系统架构的开发者。

## 环境依赖

- Python 3.10+
- PySide6
- QMarkdownView

```shell
pip install pyside6
pip install qmarkdownview
```

## 快速开始

1.  **克隆或下载项目**。
2.  **运行桌宠**：
    - 运行桌宠管理器:
        ```shell
        python main.py
        # 或
        main.exe # 需打包
        ```
    - 运行默认桌宠（需提前配置）:
        ```shell
        python main.py -default
        # 或
        main.exe -default # 需打包
        ```
    - 运行指定名称的桌宠（需提前配置）
        ```shell
        python main.py <桌宠名>
        # 或
        main.exe <桌宠名> # 需打包
        ```
    在桌宠管理器的图形界面中可以查看所有已注册的宠物、编辑配置，双击启动宠物。

## 项目结构

```
.
├── pet.py                    # 程序入口
├── README.md                 # 项目说明文档
│
├── doc/                      # 详细文档
├── API/                      # API接口文档
│
├── customization.md          # 插件开发指南
├── CHANGELOG.md              # 更新日志
│
├── pet/                      # 宠物资源包
│   ├── config.json           # 宠物注册表
│   └── Mutumi/               # 示例宠物
│       ├── info.json         # 元信息
│       ├── introduction.md   # 介绍文档
│       ├── img/              # 动画帧图片
│       └── config/           # 行为配置
│           ├── base.json     # 基础设置
│           ├── anime.json    # 动画序列
│           ├── collision.json# 碰撞区域
│           ├── dialog.json   # 对话库
│           ├── state.json    # 状态反馈
│           └── pluginState.json # 插件状态
│
├── plugin/                   # 插件系统
│   ├── idle.py               # 待机管理
│   ├── drag.py               # 拖拽交互
│   ├── stroke.py             # 抚摸交互
│   ├── move-randomly/        # 随机移动
│   │   ├── move-randomly.py
│   │   └── data.json
│   ├── use-fan.py            # 风扇互动
│   └── attr/                 # 属性面板
│       ├── attr.py
│       └── data.json
│
├── tool/                     # 核心工具
│   ├── config.py             # 配置管理
│   ├── anime.py              # 动画引擎
│   ├── stateMachine.py       # 状态机
│   ├── plugin.py             # 插件管理器
│   ├── widgetFactory.py      # UI工厂
│   ├── conv.py               # 对话生成
│   └── collision.py              # 碰撞检测
│
└── window/                   # GUI界面
    ├── manager/              # 管理后台
    │   ├── mainWindow.py     # 主窗口
    │   ├── managerPage.py    # 桌宠管理
    │   ├── pluginPage.py     # 插件管理
    │   ├── docPage.py        # 文档查阅
    │   └── settingPage.py    # 设置
    └── pet/                  # 宠物窗口
        ├── petWindow.py      # 主窗口
        ├── dialogMenu.py     # 对话面板
        ├── stateMenu.py      # 状态面板
        ├── actionMenu.py     # 行动面板
        └── settingMenu.py    # 设置面板
```

## API 文档

- [Pet](./doc/API/API-pet.md)
- [Pet Managet](./doc/API/API-manager.md)
- [包：tool](./doc/API/API-tool.md)

## 操作简介（宠物本体）

| 操作 | 反馈 |
| :---: | :--- |
| **左键拖拽** | 切换至 `drag` 状态，宠物跟随鼠标移动 |
| **左键点击头部** (碰撞区) | 触发 `stroke` 状态，播放抚摸动画与反馈 |
| **闲置等待** | 自动进入 `idle` 状态，触发随机移动与待机回复 |
| **右键菜单** | 打开对话/状态/行动/设置面板 |

## 桌宠管理器

管理器（`manager.py`）提供了一个统一的图形界面，用于集中管理所有已注册的宠物。

**主要功能**：
- **宠物管理**：
    - 左侧列表展示所有已注册宠物，支持搜索筛选。
    - 查看 `introduction.md` 中的宠物介绍。
    - **可视化编辑**所有配置文件（基础项、动画、碰撞体、状态文本、对话文本、插件状态）。
    - **快速启动**：双击列表项或点击“启动”按钮。
    - **打开文件夹**：在文件资源管理器中定位宠物资源。
    - **删除桌宠**：从系统中移除宠物及其所有资源。
- **插件管理** (开发中)
- **文档查阅** (开发中)
- **管理器设置**：配置默认宠物、界面主题等。

**宠物注册**：
在 `./pet/config.json` 中注册宠物：
```json
{
    "宠物名": "./pet/宠物名/"
}
```
每个宠物目录必须包含 `info.json`、`introduction.md`、`config/` 和 `img/` 目录。

## 核心机制

1.  **多宠物架构**：
    - 每个宠物拥有独立的配置文件、图片资源和插件状态。
    - 通过 `pet/config.json` 注册，实例由管理器的 `MainWindow` 统一管理。
    - 支持从管理器或命令行独立启动。

2.  **动画系统** (`tool.anime`)：
    - 基于帧序列图片，支持循环/单次播放。
    - 窗口自适应图片尺寸。
    - 提供异步（定时器驱动）和同步（阻塞）两种播放模式。

3.  **状态机** (`tool.stateMachine`)：
    - 管理宠物的所有状态（如 `idle`, `drag`, `stroke`）。
    - 状态切换时自动触发对应的反馈文本和动画。

4.  **插件系统** (`tool.plugin`)：
    - 基于 `Plugin` 基类，支持自定义行动扩展。
    - 支持自启动插件（`auto=True`）和手动触发插件。
    - **插件依赖排序**：通过 `deps` 字段确保加载顺序。
    - **完整生命周期**：`setup` -> `start` -> `stop` -> `teardown`。
    - 插件可扩展设置面板和状态面板（通过 `addPage`）。

5.  **页面工厂** (`tool.widgetFactory`)：
    - 提供 `FormFactory`、`DynamicListFactory`、`FormBoxFactory`、`ListBoxFactory`、`SearchStackFactory` 等。
    - 用于快速、标准化地构建配置界面，实现数据与UI的双向绑定。

## 自定义

提供了从配置到代码的多层次自定义能力。

- **配置层面**：直接编辑 JSON 文件即可添加动画、碰撞体、对话和状态反馈。
- **代码层面**：通过开发插件（Plugin），可以实现任何复杂的交互逻辑，并扩展管理器的设置界面。

详细的教程和示例，请参阅 [customization.md](./doc/customization.md)。

## 更新日志

详见 [CHANGELOG.md](./doc/CHANGELOG.md)。
