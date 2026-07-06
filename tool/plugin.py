# tool/plugin_base.py
from typing import TYPE_CHECKING
from PySide6.QtCore import QObject, QEvent

if TYPE_CHECKING:
    from window.petWindow import PetWindow

class Plugin(QObject):
    """插件基类"""
    
    def __init__(self):
        super().__init__()
        self.id: str = "plugin-plugin"
        self.auto: bool = False
        self.name: str = "未命名插件"
        self.description: str = ""
        self._window: "PetWindow | None" = None
    
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
        raise NotImplementedError("function \"start(self, window: PetWindow) should be overrided\"")
    
    def stop(self) -> None:
        """停止行动"""
        raise NotImplementedError("function \"stop(self, window: PetWindow) should be overrided\"")
    
    def eventFilter(self, obj, event: QEvent) -> bool:
        return False
