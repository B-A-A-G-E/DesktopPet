"""
idle 作为基础状态其插件必须启用，最先加载
"""
from PySide6.QtCore import Slot, QTimer

from tool.plugin import Plugin
from tool.config import LogType

class Action(Plugin):
    def __init__(self):
        super().__init__()

        self.id = "idle"
        self.state = "idle"
        self.auto = True
        self.teardownImmed = False
        
        self.anime: str = "idle"
    
    def setup(self, window) -> None:
        super().setup(window)

        self.idleTime: int = window.configManager.base["idle-time"]
        self.idleTimer: QTimer = QTimer()

        self.bind()
    
    def start(self) -> None:
        # 入场并切换待机
        self.window.stateMenu.log("Succeeded to entre", LogType.Entre)
        #self.window.operateState("entre", "entre", isAsync = False)
        self.window.operateState("idle", "idle")
        self.idleTimer.start(self.idleTime)
        super().start()
    
    def bind(self) -> None:
        self.idleTimer.timeout.connect(lambda: self.window.replyState(self.state))
        for v in self.window.pluginManager.plugins.values():
            if v != self:
                v.stopped.connect(lambda: self.window.operateState(self.state, self.anime))
    
    @Slot(str)
    def onActStopped(self, id: str) -> None:
        if id != self.id:
            self.window.pluginManager.getPlugin(id).stopped.connect(lambda:
                self.window.operateState(self.state, self.anime))
    
    @Slot(str, str)
    def onStateChanged(self, prevState: str, currentState: str) -> None:
        if currentState != self.state:
            self.idleTimer.stop()
        else:
            self.idleTimer.start(self.idleTime)
