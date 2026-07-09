from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Slot, Signal, QRect

import importlib

from tool import data
from tool import conv
from tool import anime
from tool.stateMachine import StateMachine
from tool.data import LogType

from tool.plugin import Plugin, PluginManager

from window.dialogMenu import DialogMenu
from window.stateMenu import StateMenu
from window.actionMenu import ActionMenu
from window.settingMenu import SettingMenu

class PetWindow(QWidget):
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

        # 状态机
        self.stateMachine = StateMachine([k for k in data.state.keys()], data.base["idle-time"], "idle")

        # 插件管理器
        self.pluginManager = PluginManager(self)
        self.pluginManager.loadAllPlugins()

        # 添加动画
        self.animes = { k: anime.Anime(v["path"], v["fps"], v["loop"], self, self.imgLb) for k, v in data.anime.items()}
        self.currentAnime = self.animes["idle"]

        # 添加碰撞体
        self.collisions = { k: QRect(v["left"], v["top"], v["width"], v["height"]) for k, v in data.collision.items()}

        # 安装事件过滤器来捕获所有输入事件
        self.installEventFilter(self)
        self.setMouseTracking(True)

        # 绑定子窗口及信号
        self.bind()

        self.pluginManager.startAutoPlugins()

        # 入场并切换待机
        self.stateMenu.log("Succeeded to entre", LogType.Entre)
        #self.replyState("entre", isAsync = False)
        self.replyState("idle")

    def bind(self) -> None:
        """绑定子窗口及信号"""
        self.dialogMenu = DialogMenu()
        self.stateMenu = StateMenu()
        self.actionMenu = ActionMenu(self)
        self.settingMenu = SettingMenu()

        self.settingMenu.dataUpdated.connect(self.updateData)
        
        # 绑定上下文菜单
        self.imgLb.dialogAct.triggered.connect(self.dialogMenu.show)
        self.imgLb.stateAct.triggered.connect(self.stateMenu.show)
        self.imgLb.setAct.triggered.connect(self.settingMenu.show)
        self.imgLb.actAct.triggered.connect(self.actionMenu.show)
        self.imgLb.exitAct.triggered.connect(QApplication.quit)

        # 绑定状态机信号
        self.stateMachine.stateChanged.connect(self.onStateChanged)
        self.stateMachine.stateUndefined.connect(lambda state: self.stateMenu.log(f"Undefined state \"{state}\"", LogType.Error))

        # 绑定插件管理器信号
        self.pluginManager.pluginLoadSucceeded.connect(lambda text: self.stateMenu.log(text, LogType.PluginLoaded))
        self.pluginManager.pluginError.connect(lambda text: self.stateMenu.log(text, LogType.Error))

        # 绑定动画加载失败信号
        for anime in self.animes.values():
            anime.loadError.connect(lambda text: self.stateMenu.log(text, LogType.Error))
    
    @property
    def state(self) -> str:
        """获取当前状态"""
        return self.stateMachine.currentState
    
    @state.setter
    def state(self, value: str) -> None:
        """设置当前状态"""
        self.stateMachine.currentState = value
    
    @property
    def currentAct(self) -> Plugin | None:
        return self.pluginManager.currentPlugin

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

    def startAct(self, id: str) -> None:
        """执行行动"""
        act = self.pluginManager.getPlugin(id)
        if act and act.state != self.stateMachine.currentState:
            self.pluginManager.currentPlugin = act
            self.stateMachine.currentState = act.state
    
    def stopAct(self, id: str) -> None:
        self.pluginManager.stopPlugin(id)
    
    def getAct(self, id: str) -> Plugin | None:
        return self.pluginManager.getPlugin(id)

    @Slot(str, str)
    def onStateChanged(self, prevState: str, currentState: str) -> None:
        self.stateMenu.log(self.state, LogType.StateChanged)
        if prevState == "idle" and currentState == "idle":
            # 在dialogMenu回复
            self.dialogMenu.addLine(conv.replyText("state", currentState))
        self.stateChanged.emit(currentState)

    @Slot(str)
    def onActStopped(self, id: str) -> None:
        if self.pluginManager.currentPlugin and self.pluginManager.currentPlugin.id == id:
            self.pluginManager.currentPlugin = None
        
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
