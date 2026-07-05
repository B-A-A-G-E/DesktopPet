# 桌面宠物

## 项目简介
基于 PySide6 开发的桌面电子宠物程序，支持自定义动画、交互反馈和扩展行为。宠物会随机移动、响应点击拖拽、通过对话菜单互动，并能执行自定义动作

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
├── .gitignore
│
├── data/                   # 配置文件目录
│   ├── base.json           # 基础配置
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
│   └── after-drag/         # 拖拽后动画帧
│
├── tool/                   # 工具模块
│   ├── anime.py            # 动画播放引擎
│   ├── data.py             # 数据加载与全局变量
│   └── conv.py             # 对话回复生成器
│
├── window/                 # 窗口模块
│   ├── petWindow.py        # 主窗口（宠物本体）
│   ├── dialogMenu.py       # 对话菜单
│   ├── stateMenu.py        # 状态日志菜单
│   ├── actionMenu.py       # 行动菜单
│   └── settingMenu.py      # 设置菜单
│
└── action/                 # 自定义动作模块
    ├── import.json         # 动作导入配置
```

## 操作简介（宠物本体）
操作|反馈
:---:|:---:
左键拖拽|切换 `drag` 状态，宠物跟随鼠标移动
左键点击`stroke`碰撞区并拖拽|触发 `stroke` 状态（可配置碰撞体）
闲置等待|自动进入 `idle` 状态，随机移动
右键菜单|打开对话/状态/行动/设置面板

## 核心机制
1. 动画系统
    - 基于帧序列图片播放，支持循环/单次播放
    - 窗口自动适应窗口大小
2. 状态机
    - 状态切换时触发对应的反馈文本和动画
    - 支持 after-{state} 后置事件（如抚摸后播放特殊动画）

3. 对话系统
    - 随机从 dialog.json 抽取问题选项
    - 回复文本从 state.json 或 dialog.json 随机选取
4. 自定义行动
    - 通过 action/ 目录添加 Python 模块
    - 在 import.json 中注册后即可在行动面板调用
5. 设置菜单
    - 可视化编辑所有 JSON 配置文件
    - 支持动态增删状态/对话文本条目

## 自定义
### base.json 基础配置
键|说明|默认值
:---:|:---:|:---:
log-path|日志保存路径|./log.log
load-failed-img-path|加载失败占位图|./img/load_failed.png
action-import-json-path|动作导入配置路径|./action/import.json
quesSelecter-item-count|对话菜单显示问题数|10
idle-time|待机判定时间(ms)|10000
idle-move-time|随机移动间隔(ms)|15000
move-min-step|移动最小步长|200
move-max-step|移动最大步长|3000
move-step-time|步进间隔(ms)|20
move-speed|移动速度(px/步)|10

---

### anime.json 动画配置
```json
"状态名": {
    "path": "文件夹路径",   // 帧图片存放路径
    "fps": 30,                  // 播放帧率
    "loop": true                // 是否循环播放
}
```
> 帧图片需按数字顺序命名（如 0.png, 1.png, 2.png...）

---

### collision.json 碰撞体配置
```json
"状态名": {
    "left": 11,     // 碰撞区相对于窗口左上角的X偏移
    "top": 30,      // 碰撞区相对于窗口左上角的Y偏移
    "width": 135,   // 碰撞区宽度
    "height": 30    // 碰撞区高度
}
```

---

### "act-event"类型事件（行动）的自定义
1. 新建.py文件，为统一格式，文件名最好为 **"act-\[事件名\].py"**
2. 在 **"action-import-json-path"（位于./data/base.json内）** 中配置好路径的json文件中**添加要导入模块（包含start与stop槽函数）相对于main.py的名称**
3. （可选）在./data/state.json中新建 **"act-\[事件名\]"** 状态
4. （可选）在./data/anime.json中新建 **"act-\[事件名\]"** 动画(**注意在设定的路径下先添加好动画**)
5. 在新建的文件内输入基础模板
    ``` python
    from PySide6.QtWidgets import QWidget
    from PySide6.QtCore import Slot

    @Slot(QWidget)
    def start(window: QWidget):
        """开始行动时调用"""
        pass

    @Slot(QWidget)
    def stop(window: QWidget):
        """结束行动时调用"""
        pass
    ```
6. 自定义事件逻辑

---

#### 例:  
./data/base.json中，`"action-import-json-path": "./action/import.json"`  

./data/state.json中，`"act-dance": ["I'm dancing~"]`

./action/import.json:
``` json
{
    "act-dance": 
    {   "name": "跳舞",
        "path": "action.act-dance"
    }
}
```

./action/act-dance.py:
``` python
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Slot

@Slot(QWidget)
def start(window: QWidget):
    """开始行动时调用"""
    print("dancing now")

@Slot(QWidget)
def stop(window: QWidget):
    """结束行动时调用"""
    print("stoped dancing")
```

## 更新日志
版本号格式：**主版本号.次版本号\[.修订版本号\]**

### v0.3.1 （最新）
1. 加入行动自定义功能与行动面板
2. 将部分含"action"的变量/函数等的命名规范为"state"
3. 丰富日志系统
4. 优化判定，防崩溃
5. 重写了readme文件
6. 吃点泡面凑合凑合

### v0.2
1. 加入待机时随机移动的功能
2. 加入"after-event"类型事件
3. 丰富日志系统
4. 修复动画切换异常等bug
5. 俗手偶得，获得更多bug
6. 借助ai完善设置界面
7. 基本确保自定义功能稳定运行
8. 用ai给几个我也看不懂的地方写注释
9. 晚上可乐配饺子

### v0.1
1. 新建项目并实现基本功能  
（时间较久远，记不清修改）
