## 环境依赖
1. PySide6
## 项目结构
```
|-README.md
|-.gitignore
|-log.log
|-main.py
|-data
| |-base.json
| |-anime.json
| |-collision.json
| |-state.json
| |-dialog.json
|-img
| |-load_failed.png
| |-entre
| |-exit
| |-idle
| |-stroke
| |-drag
| |-after-stroke
| |-after-drag
|-tool
| |-anime.py
| |-data.py
| |-conv.py
|-window
| |-petWindow.py
| |-dialogMenu.py
| |-stateMenu.py
| |-settingMenu.py
| |-action
| | |-import.json
```

## "act-event"类型事件的自定义
1. 新建.py文件，为统一格式，文件名最好为 **"act-\[事件名\].py"**
2. 在 **"action-import-json-path"（位于./data/base.json内）** 中配置好路径的json文件中**添加要导入模块（包含start与stop槽函数）相对于main.py的名称**
3. （可选）在./data/state.json中新建 **"act-\[事件名\]"** 状态
4. 在新建的文件内输入基础模板
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
5. 自定义事件逻辑

---

### 例:  
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

### v0.1
1. 新建项目并实现基本功能  
（时间较久远，记不清修改）

### v0.2
1. 加入待机时随即移动的功能
2. 加入"after-event"类型事件
3. 丰富日志系统
4. 修复动画切换异常等bug
5. 俗手偶得，获得更多bug
6. 借助ai完善设置界面
7. 基本确保自定义功能稳定运行
8. 用ai给几个我也看不懂的地方写注释
9. 晚上可乐配饺子

### v0.3
1. 加入行动自定义功能与行动面板
2. 将部分含"action"的变量/函数等的命名规范为"state"
3. 丰富日志系统
4. 优化判定，防崩溃
