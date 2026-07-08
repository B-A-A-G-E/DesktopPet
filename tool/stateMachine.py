from PySide6.QtCore import QObject, Signal, Slot, QTimer

class StateMachine(QObject):
    stateChanged = Signal(str, str) # prevState, currentState
    stateUndefined = Signal(str)
    stateTimeout = Signal(str) # 超时状态名

    def __init__(self, stateList: list, idleTime: int, state: str = "idle"):
        super().__init__()

        self._stateList: list[str] = stateList
        self._currentState: str = state
        self._idleTime: int = idleTime

        self._idleTimer: QTimer = QTimer()
    
    @property
    def stateList(self) -> list:
        return self._stateList
    
    @stateList.setter
    def stateList(self, value: list[str]) -> list[str]:
        self._stateList = value
        return value
    
    @property
    def currentState(self) -> str:
        return self._currentState
    
    @currentState.setter
    def currentState(self, state: str) -> bool:
        """更新状态"""
        if self._currentState != state or (state == "idle" and self._currentState == "idle"):
            if state not in self._stateList:
                self.stateUndefined.emit(state)
                return False
            
            # 切换计时器状态
            if state != "idle":
                self._idleTimer.stop()
            else:
                self._idleTimer.start(self._idleTime)
            
            # 更新状态
            prevState = self._currentState
            self._currentState = state
            self.stateChanged.emit(prevState, self._currentState)
            return True
        return False
    
    @property
    def idleTime(self) -> int:
        return self._idleTime
    
    @idleTime.setter
    def idleTime(self, time: int) -> int:
        self._idleTime = time
        self._idleTimer.start(time)

    def addState(self, state: str) -> None:
        """添加新状态到状态列表"""
        if state not in self._stateList:
            self._stateList.append(state)
    
    def removeState(self, state: str) -> bool:
        """删除状态"""
        if state in self._stateList:
            self._stateList.remove(state)
            return True
        else:
            self.stateUndefined.emit(state)
            return False

    @Slot()
    def onIdleTimeout(self) -> None:
        self.currentState = "idle"
