from PySide6.QtCore import Slot, QTimer

from tool.plugin import Plugin

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
    
    def teardown(self):
        self.idleTimer.deleteLater()
        return super().teardown()
    
    def start(self) -> None:
        # 入场并切换待机
        super().start()
        #self.window.operateState("entre", "entre", isAsync = False)
        self.window.operateState("idle", "idle")
        self.idleTimer.start(self.idleTime)
    
    def stop(self) -> None:
        self.idleTimer.stop()
    
    def bind(self) -> None:
        self.window.stateChanged.connect(self.onStateChanged)
        self.idleTimer.timeout.connect(lambda: self.window.replyState(self.state))
    
    @Slot(str, str)
    def onStateChanged(self, prevState: str, currentState: str) -> None:
        if currentState != self.state:
            self.idleTimer.stop()
        else:
            self.idleTimer.start(self.idleTime)
