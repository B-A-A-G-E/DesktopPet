from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Slot, Signal, QRect

import importlib

from tool import data
from tool import conv
from tool import anime
from tool.stateMachine import StateMachine
from tool.data import LogType

from tool.plugin import Plugin

from window.dialogMenu import DialogMenu
from window.stateMenu import StateMenu
from window.actionMenu import ActionMenu
from window.settingMenu import SettingMenu

class PetWindow(QWidget):
    pluginLoadSucceeded = Signal(str)
    pluginInheritError = Signal(str)
    pluginLoadFailed = Signal(str)

    stateChanged = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        # 无边框及透明背景
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 添加控件
        self.imgLb = QLabel() # 存放图片

        # 添加上下文菜单
        self.imgLb.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.imgLb.dialogAct = QAction("对话")
        self.imgLb.stateAct = QAction("状态")
        self.imgLb.actAct = QAction("行动")
        self.imgLb.setAct = QAction("设置")
        self.imgLb.exitAct = QAction("退出")
        self.imgLb.addAction(self.imgLb.dialogAct)
        self.imgLb.addAction(self.imgLb.stateAct)
        self.imgLb.addAction(self.imgLb.actAct)
        self.imgLb.addAction(self.imgLb.setAct)
        self.imgLb.addAction(self.imgLb.exitAct)

        # 设置布局并填入控件
        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(self.imgLb)
        self.setLayout(self.mainlayout)

        # 辅助变量
        self.stateMachine = StateMachine([k for k in data.state.keys()], data.base["idle-time"], "idle")

        # 添加动画
        self.animes = { k: anime.Anime(v["path"], v["fps"], v["loop"], self, self.imgLb) for k, v in data.anime.items()}
        self.currentAnime = self.animes["idle"]

        # 添加碰撞体
        self.collisions = { k: QRect(v["left"], v["top"], v["width"], v["height"]) for k, v in data.collision.items()}

        # 添加自定义行动（插件）
        self.acts: dict[str, Plugin] = {}
        self.autoActs: dict[str, Plugin] = {}
        self.currentAct: Plugin | None = None
        self.loadPlugins()

        # 安装事件过滤器来捕获所有输入事件
        self.installEventFilter(self)
        self.setMouseTracking(True)

        self.bind()

        # 入场并切换待机
        self.stateMenu.log("Succeeded to entre", LogType.Entre)
        #self.replyState("entre", isAsync = False)
        self.replyState("idle")

        # 安装并开始行动
        for act in self.autoActs.values():
            act.setup(self)
            act.start()

    def bind(self) -> None:
        """绑定子窗口及信号"""
        self.dialogMenu = DialogMenu()
        self.stateMenu = StateMenu()
        self.actionMenu = ActionMenu(self)
        self.settingMenu = SettingMenu()

        self.settingMenu.dataUpdated.connect(self.updateData)
        
        self.pluginLoadSucceeded.connect(lambda text: self.stateMenu.log(text, LogType.PluginLoaded))
        self.pluginInheritError.connect(lambda text: self.stateMenu.log(text, LogType.Error))
        self.pluginLoadFailed.connect(lambda text: self.stateMenu.log(text, LogType.Error))

        # 绑定上下文菜单
        self.imgLb.dialogAct.triggered.connect(self.dialogMenu.show)
        self.imgLb.stateAct.triggered.connect(self.stateMenu.show)
        self.imgLb.setAct.triggered.connect(self.settingMenu.show)
        self.imgLb.actAct.triggered.connect(self.actionMenu.show)
        self.imgLb.exitAct.triggered.connect(QApplication.quit)

        self.stateMachine.stateChanged.connect(self.onStateChanged)
        self.stateMachine.stateUndefined.connect(lambda state: self.stateMenu.log(f"Undefined state \"{state}\"", LogType.Error))

        # 绑定动画加载失败信号
        for anime in self.animes.values():
            anime.loadErr.connect(lambda text: self.stateMenu.log(text, LogType.Error))
    
    @property
    def state(self) -> str:
        """获取当前状态"""
        return self.stateMachine.currentState
    
    @state.setter
    def state(self, value: str) -> None:
        """设置当前状态"""
        self.stateMachine.currentState = value
    
    def replyState(self, state: str, afterEvent: bool = False, isContinue: bool = False, isAsync: bool = True) -> None:
        """
        执行对应行动时进行响应\n
        若afterEvent为True，则先响应当前状态的after-state事件（动画只能同步播放）\n
        """
        currentState = self.stateMachine.currentState
        
        if currentState != state or (state == "idle" and currentState == "idle"):
            if afterEvent and f"after-{currentState}" in self.animes.keys():
                self.replyState(f"after-{currentState}", isAsync = False)
            # 更新状态
            self.stateMachine.currentState = state
            # 在dialogMenu回复
            self.dialogMenu.addLine(conv.replyText("state", state))
            # 切换动画
            self.changeAnime(state, isContinue, isAsync)
    
    def changeAnime(self, name: str, isContinue: bool = False, isAsync: bool = True) -> None:
        """切换动画"""
        if name in self.animes.keys():
            self.currentAnime.over()
            self.currentAnime = self.animes[name]
            self.currentAnime.play(isContinue, isAsync)
    
    def loadPlugins(self) -> None:
        for id in data.plugin.keys():
            self.loadPlugin(id)

    def loadPlugin(self, id: str) -> bool:
        try:
            if not data.plugin[id]["enabled"]:
                return False
            
            # 检查是否已加载
            if id in self.acts or id in self.autoActs:
                return True
            
            module = importlib.import_module(data.plugin[id]["path"])
            pluginClass = None
            for attrName in dir(module):
                attr = getattr(module, attrName)
                
                if isinstance(attr, type) and issubclass(attr, Plugin) and attr is not Plugin:
                    pluginClass = attr
                    break
            
            if pluginClass:
                plugin = pluginClass()
                plugin.stopped.connect(lambda: self.onActStopped(plugin.id))
                
                if plugin.auto:
                    self.autoActs[id] = plugin
                else:
                    self.acts[id] = plugin
                
                self.pluginLoadSucceeded.emit(f"succeeded to load plugin \"{id}\"")
                return True
            else:
                self.pluginInheritError.emit(f"plugin \"{id}\" is not based on the base class \"Plugin\"")
                return False
        except Exception as e:
            self.pluginLoadFailed.emit(f"failed to load plugin \"{id}\": {e}")
            return False
    
    def deletePlugin(self, id: str) -> bool:
        """删除插件"""
        if id in self.acts:
            # 停止并卸载非自启动插件
            if self.currentAct and self.currentAct.id == id:
                self.currentAct.stop()
                self.currentAct.teardown()
                self.currentAct = None
            self.acts.pop(id)
            return True
        elif id in self.autoActs:
            # 停止并卸载自启动插件
            self.autoActs[id].stop()
            self.autoActs[id].teardown()
            self.autoActs.pop(id)
            return True
        return False

    def act(self, id: str) -> None:
        """执行行动"""
        if id != self.stateMachine.currentState:
            # 停止上一个行动
            if id in self.acts and self.currentAct:
                self.currentAct.stop()
            
            # 更新状态
            self.state = id
            
            # 开始新行动
            self.currentAct = self.acts[id]
            self.currentAct.setup(self) # 安装插件，安装事件过滤器
            self.currentAct.start()
        
    def getAct(self, id: str) -> Plugin | None:
        for k, v in self.acts.items():
            if k == id:
                return v
        for k, v in self.autoActs.items():
            if k == id:
                return v
        return None

    @Slot(str, str)
    def onStateChanged(self, prevState: str, currentState: str) -> None:
        self.stateMenu.log(self.state, LogType.StateChanged)
        if prevState == "idle" and currentState == "idle":
            # 在dialogMenu回复
            self.dialogMenu.addLine(conv.replyText("state", currentState))
        self.stateChanged.emit(currentState)

    @Slot(str, str)
    def onActStopped(self, id: str) -> None:
        if self.currentAct and self.currentAct.id == id:
            self.currentAct.teardown()
            self.currentAct = None
        self.replyState("idle")

    @Slot()
    def updateData(self) -> None:
        """更新数据"""
        # petWindow
        self.stateMachine.idleTime = data.base["idle-time"]
        self.animes = { k: anime.Anime(v["path"], v["fps"], v["loop"], self, self.imgLb) for k, v in data.anime.items()}
        self.collisions = { k: QRect(v["left"], v["top"], v["width"], v["height"]) for k, v in data.collision.items()}
        # dialogWindow
        self.dialogMenu.resetQuesSelecter()
        self.stateMenu.log("Data is updated", LogType.Set)
