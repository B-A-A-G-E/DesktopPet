# 宠物工坊

## 目录
- [项目简介](#项目简介)
- [适宜人群](#适宜人群)
- [环境依赖](#环境依赖)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [API 文档](#api-文档)
- [桌宠管理器](#桌宠管理器)
- [核心机制](#核心机制)
- [自定义](#自定义)
- [更新日志](#更新日志)

---

## 项目简介

基于 PySide6 框架开发的宠物工坊项目，支持多宠物并行管理与独立配置。能执行自定义行动（插件系统）。配套的桌宠管理器提供了图形化界面，便于管理宠物及其配置。

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
├── .gitattributes
├── .gitignore
├── main.py                          # 程序入口
├── README.md                        # 项目说明文档
├── settings.json                    # 全局配置文件
├── doc/                             # 项目文档目录
│   ├── CHANGELOG.md                 # 更新日志
│   ├── customization.md             # 自定义配置说明
│   └── API/                         # API 文档
│       ├── API-manager.md           # 管理器 API
│       ├── API-pet.md               # 桌宠 API
│       └── API-tool.md              # 工具 API
├── pet/                             # 桌宠数据目录
│   ├── Mutumi/                      # 桌宠 Mutumi
│   │   ├── info.json                # 桌宠信息
│   │   ├── log.log                  # 运行日志
│   │   └── config/                  # 桌宠配置
│   │       ├── anime.json           # 动画配置
│   │       ├── attr.json            # 属性配置
│   │       ├── base.json            # 基础配置
│   │       ├── collision.json       # 碰撞配置
│   │       ├── dialog.json          # 对话配置
│   │       ├── move-randomly.json   # 随机移动配置
│   │       ├── pluginState.json     # 插件状态
│   │       └── state.json           # 状态机配置
│   ├── 大狗1/                        # 桌宠 大狗1
│   │   ├── info.json                # 桌宠信息
│   │   ├── log.log                  # 运行日志
│   │   └── config/                  # 桌宠配置
│   │       ├── anime.json           # 动画配置
│   │       ├── base.json            # 基础配置
│   │       ├── collision.json       # 碰撞配置
│   │       ├── dialog.json          # 对话配置
│   │       ├── pluginState.json     # 插件状态
│   │       └── state.json           # 状态机配置
│   └── 大狗2/                        # 桌宠 大狗2
│       ├── info.json                # 桌宠信息
│       ├── log.log                  # 运行日志
│       └── config/                  # 桌宠配置
│           ├── anime.json           # 动画配置
│           ├── base.json            # 基础配置
│           ├── collision.json       # 碰撞配置
│           ├── dialog.json          # 对话配置
│           ├── pluginState.json     # 插件状态
│           └── state.json           # 状态机配置
├── plugin/                          # 插件目录
│   ├── config.json                  # 插件全局配置
│   ├── attr/                        # 属性插件
│   │   └── attr.py                  # 属性插件实现
│   ├── builtin/                     # 内置插件
│   │   ├── drag.py                  # 拖拽
│   │   ├── idle.py                  # 待机
│   │   ├── move-randomly.py         # 随机移动
│   │   └── stroke.py                # 抚摸
│   ├── dagou-integ-plugin/          # 大狗集成插件
│   │   ├── plugin.py                # 插件实现
│   │   └── audio/                   # 音频资源
│   │       └── bark.mp3             # 狗叫音效
│   └── for-mutumi/                  # Mutumi 专用插件
│       └── use-fan.py               # 使用风扇
├── temp/                            # 桌宠模板目录
│   ├── Mutumi/                      # Mutumi 模板
│   │   ├── icon.png                 # 图标
│   │   ├── info.json                # 模板信息
│   │   ├── introduction.md          # 介绍文档
│   │   ├── config/                  # 模板配置
│   │   │   ├── anime.json           # 动画配置
│   │   │   ├── attr.json            # 属性配置
│   │   │   ├── base.json            # 基础配置
│   │   │   ├── collision.json       # 碰撞配置
│   │   │   ├── dialog.json          # 对话配置
│   │   │   ├── move-randomly.json   # 随机移动配置
│   │   │   ├── pluginState.json     # 插件状态
│   │   │   └── state.json           # 状态机配置
│   │   └── img/                     # 图片资源
│   │       ├── after-stroke/        # 抚摸后动画帧
│   │       ├── drag/                # 拖拽动画帧
│   │       ├── entre/               # 进入动画帧
│   │       ├── exit/                # 退出动画帧
│   │       ├── idle/                # 待机动画帧
│   │       ├── stroke/              # 抚摸动画帧
│   │       ├── turn-off-fan/        # 关闭风扇动画帧
│   │       └── using-fan/           # 使用风扇动画帧
│   └── 大狗/                         # 大狗模板
│       ├── icon.png                 # 图标
│       ├── info.json                # 模板信息
│       ├── introduction.md          # 介绍文档
│       ├── config/                  # 模板配置
│       │   ├── anime.json           # 动画配置
│       │   ├── base.json            # 基础配置
│       │   ├── collision.json       # 碰撞配置
│       │   ├── dialog.json          # 对话配置
│       │   ├── pluginState.json     # 插件状态
│       │   └── state.json           # 状态机配置
│       └── img/                     # 图片资源
│           ├── bark/                # 吠叫动画帧
│           ├── heyiwei/             # 何意味动画帧
│           └── idle/                # 待机动画帧
├── tool/                            # 工具模块
│   ├── anime.py                     # 动画工具
│   ├── audio.py                     # 音频工具
│   ├── collision.py                 # 碰撞检测工具
│   ├── config.py                    # 配置工具
│   ├── conv.py                      # 转换工具
│   ├── plugin.py                    # 插件工具
│   ├── stateMachine.py              # 状态机工具
│   ├── widgetFactory.py             # 控件工厂
│   └── __init__.py                  # 包初始化
└── window/                          # 窗口模块
    ├── manager/                     # 管理器窗口
    │   ├── docPage.py               # 文档页面
    │   ├── mainWindow.py            # 主窗口
    │   ├── managerPage.py           # 管理器页面
    │   ├── pluginPage.py            # 插件页面
    │   ├── settingPage.py           # 设置页面
    │   └── tempPage.py              # 模板页面
    └── pet/                         # 桌宠窗口
        ├── actionMenu.py            # 动作菜单
        ├── dialogMenu.py            # 对话菜单
        ├── petWindow.py             # 桌宠窗口
        ├── settingMenu.py           # 设置菜单
        └── stateMenu.py             # 状态菜单
```

## API 文档

- [Pet](./doc/API/API-pet.md)
- [Pet Manager](./doc/API/API-manager.md)
- [包：tool](./doc/API/API-tool.md)

## 桌宠管理器

管理器（`manager.py`）提供了一个统一的图形界面，用于集中管理所有已注册的宠物和模板。

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

**宠物发现**：
程序启动时自动扫描 `./pet/` 目录，任何包含 `info.json` 的子目录都被视为一个已注册宠物。
每个宠物目录包含 `info.json`、`config/`；`introduction.md` 与 `img/` 由模板提供。

## 核心机制

1.  **多宠物架构**：
    - 每个宠物拥有独立的配置文件和插件状态。
    - 宠物通过实例化模板创建，图片资源和文档不会复制，所有同模板宠物共享
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
