# 桌宠管理器 API

## 目录
- [桌宠管理器 API](#桌宠管理器-api)
  - [目录](#目录)
  - [概述](#概述)
  - [模块 window.manager](#模块-windowmanager)
    - [类 MainWindow(QWidget)](#类-mainwindowqwidget)
      - [属性](#属性)
      - [方法 initSidebar() -> None](#方法-initsidebar---none)
      - [方法 initStack() -> None](#方法-initstack---none)
      - [方法 bind() -> None](#方法-bind---none)
    - [类 ManagerPage(SearchStackFactory)](#类-managerpagesearchstackfactory)
      - [属性](#属性-1)
      - [信号](#信号)
      - [方法 initConfigPage(name: str) -> QWidget](#方法-initconfigpagename-str---qwidget)
      - [方法 initSettingPage(name: str) -> QWidget](#方法-initsettingpagename-str---qwidget)
      - [方法 bind() -> None](#方法-bind---none)
      - [槽函数 apply(name: str) -> None](#槽函数-applyname-str---none)
      - [槽函数 cancel(name: str) -> None](#槽函数-cancelname-str---none)
      - [槽函数 openPet(name: str) -> None](#槽函数-openpetname-str---none)
      - [槽函数 delPet(name: str) -> None](#槽函数-delpetname-str---none)
      - [槽函数 launchPet(name: str) -> None](#槽函数-launchpetname-str---none)

---

## 概述

本文档描述桌宠管理器（`manager.py`）的 API，涵盖窗口类及其方法。管理器用于集中管理多个宠物配置，提供可视化编辑和启动功能。

---

## 模块 window.manager

桌宠管理器模块，包含主窗口和管理页面。

### 类 MainWindow(QWidget)

管理器主窗口，包含侧边栏和堆叠页面。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `mainLyt` | QHBoxLayout | 主布局 |
| `sidebar` | QFrame | 侧边栏容器 |
| `stack` | QStackedWidget | 堆叠页面容器 |
| `sbBtns` | list[SidebarButton] | 侧边栏按钮列表 |
| `pages` | list[SearchStackFactory] | 页面列表 |
| `fields` | list[tuple[SidebarButton, SearchStackFactory]] | 按钮与页面的配对列表 |

#### 方法 initSidebar() -> None

初始化侧边栏，创建侧边栏按钮。

- **说明**
  - 按钮文本依次为 `"🐱"`、`"🧩"`、`"📄"`、`"⚙"`
  - `"⚙"` 按钮前插入弹簧，将其推至底部

#### 方法 initStack() -> None

初始化堆叠页面容器。

- **说明**
  - 创建 `ManagerPage` 实例并添加到堆叠

#### 方法 bind() -> None

绑定侧边栏按钮与堆叠页面的切换信号。

- **说明**
  - 点击侧边栏按钮时，堆叠切换到对应索引的页面

---

### 类 ManagerPage(SearchStackFactory)

管理器页面，包含宠物列表、配置编辑和启动功能。

#### 属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `_data` | dict[str, dict] | 宠物元信息字典，键为宠物名 |
| `_petConfigs` | dict[str, ConfigManager] | 宠物配置管理器实例 |
| `_intro` | dict[str, str] | 宠物介绍文档内容 |
| `configPages` | dict[str, tuple] | 配置页面信息：`(widget, pages, applyBtn, cancelBtn)` |
| `settingPages` | dict[str, tuple] | 设置页面信息：`(openBtn, delBtn)` |
| `pages` | dict[str, tuple] | 页面组件：`(listItem, introPg, configPg, setPg)` |

#### 信号

| 信号 | 触发时机 |
| :--- | :--- |
| `saveError(str, str)` | 保存配置失败时发射，携带宠物名和错误信息 |
| `launchError(str, str)` | 启动宠物失败时发射，携带宠物名和错误信息 |
| `dataUpdated(str)` | 数据更新时发射，携带宠物名 |
| `updateCancelled(str)` | 取消更新时发射，携带宠物名 |

#### 方法 initConfigPage(name: str) -> QWidget

创建宠物的配置编辑页面。

- **参数**
  - `name`: 宠物名
- **返回**
  - 配置页面控件
- **说明**
  - 页面包含六个标签页：基础项、动画、碰撞体、状态反馈文本、对话文本、插件状态
  - 使用 `FormFactory`、`FormBoxFactory`、`ListBoxFactory` 构建各标签页
  - 包含“应用”和“取消”按钮

**配置页面结构**：

| 标签页 | 工厂类 | 数据来源 |
| :--- | :--- | :--- |
| 基础项 | `FormFactory` | `config.base` |
| 动画 | `FormBoxFactory` | `config.anime` |
| 碰撞体 | `FormBoxFactory` | `config.collision` |
| 状态反馈文本 | `ListBoxFactory` | `config.state` |
| 对话文本 | `ListBoxFactory` | `config.dialog` |
| 插件状态 | `FormFactory` | `config.pluginState` |

#### 方法 initSettingPage(name: str) -> QWidget

创建宠物的设置页面。

- **参数**
  - `name`: 宠物名
- **返回**
  - 设置页面控件
- **说明**
  - 显示宠物元信息（名称、版本、作者）
  - 包含「在文件资源管理器中打开」和「删除桌宠」按钮

#### 方法 bind() -> None

绑定所有信号与槽。

- **说明**
  - 绑定配置页面的「应用」和「取消」按钮
  - 绑定设置页面的「打开」和「删除」按钮
  - 绑定宠物列表的双击事件（启动宠物）
  - 绑定 `ConfigManager.saveError` 信号

#### 槽函数 apply(name: str) -> None

应用配置更改。

- **参数**
  - `name`: 宠物名
- **行为**
  - 从所有配置页面收集数据
  - 更新 `ConfigManager` 对应属性
  - 调用 `saveConfig()` 保存到文件
  - 发射 `dataUpdated` 信号

#### 槽函数 cancel(name: str) -> None

取消配置更改。

- **参数**
  - `name`: 宠物名
- **行为**
  - 从 `ConfigManager` 重新加载数据到配置页面
  - 发射 `updateCancelled` 信号

#### 槽函数 openPet(name: str) -> None

在文件资源管理器中打开宠物文件夹。

- **参数**
  - `name`: 宠物名
- **说明**
  - 当前为空实现，待后续完善

#### 槽函数 delPet(name: str) -> None

从系统中删除宠物。

- **参数**
  - `name`: 宠物名
- **说明**
  - 当前为空实现，待后续完善

#### 槽函数 launchPet(name: str) -> None

启动指定宠物。

- **参数**
  - `name`: 宠物名
- **行为**
  - 从 `pets` 全局变量获取宠物路径
  - 使用 `subprocess.Popen` 启动 `pet.py` 或 `pet.exe`
  - 启动失败时发射 `launchError` 信号

**启动逻辑**：

``` python
if sys.executable.endswith('python.exe') or sys.executable.endswith('python'):
    args = ["python", "pet.py", petPath]
else:
    args = ["pet.exe", petPath]
subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```
