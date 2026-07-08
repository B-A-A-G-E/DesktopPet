from PySide6.QtCore import QObject, Signal, QEvent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from window.petWindow import PetWindow

class Plugin(QObject):
    """插件基类"""
    started = Signal()
    stopped = Signal()
    
    def __init__(self):
        super().__init__()
        self.id: str = "plugin-plugin"
        self.auto: bool = False
        self.name: str = "未命名插件"
        self.description: str = ""
        self._window: "PetWindow | None" = None
    
    @property
    def window(self) -> "PetWindow | None":
        return self._window
    
    def setup(self, window: 'PetWindow') -> None:
        """插件安装，安装事件过滤器"""
        self._window = window
        window.installEventFilter(self)
    
    def teardown(self) -> None:
        """插件卸载，卸载事件过滤器"""
        if self._window:
            self._window.removeEventFilter(self)
            self._window = None
    
    def start(self) -> None:
        """开始行动"""
        self.started.emit()
    
    def stop(self) -> None:
        """停止行动"""
        self.stopped.emit()
    
    def eventFilter(self, obj, event: QEvent) -> bool:
        """事件过滤器"""
        return False
