from PySide6.QtCore import QObject, Signal, Slot, QTimer

class StateMachine(QObject):
    stateChanged = Signal(str, str) # prevState, currentState
    stateUndefined = Signal(str)

    def __init__(self, stateList: list, state: str = ""):
        super().__init__()

        self._stateList: list[str] = stateList
        self._currentState: str = state
    
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
        # 防止重复更改
        if self._currentState != state:
            if state not in self._stateList:
                self.stateUndefined.emit(state)
                return False

            # 更新状态
            prevState = self._currentState
            self._currentState = state
            self.stateChanged.emit(prevState, self._currentState)
            return True
        return False

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
