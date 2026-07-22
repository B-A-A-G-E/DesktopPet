from PySide6.QtCore import QObject, Signal, QEvent

from typing import TYPE_CHECKING
from types import ModuleType
from importlib import util
import sys
import os

from tool.config import ConfigManager

if TYPE_CHECKING:
    from window.pet.petWindow import PetWindow

class Plugin(QObject):
    """插件基类"""
    started = Signal()
    stopped = Signal()
    
    def __init__(self):
        super().__init__()
        self.id: str = "plugin-plugin"
        self.name: str = "未命名插件"
        self.description: str = ""
        self.state: str = "plugin"
        self.auto: bool = False
        self.teardownImmed: bool = True
        
        self._window: "PetWindow | None" = None
    
    @property
    def window(self) -> "PetWindow | None":
        return self._window
    
    def setup(self, window: 'PetWindow') -> None:
        """插件安装，关联主窗口"""
        self._window = window
    
    def teardown(self) -> None:
        """插件卸载，解绑主窗口"""
        if self._window:
            self._window = None
    
    def start(self) -> None:
        """安装事件过滤器，运行插件"""
        self._window.installEventFilter(self)
        self.started.emit()
    
    def stop(self) -> None:
        """卸载事件过滤器，结束插件"""
        if self._window:
            self._window.removeEventFilter(self)
        self.window.pluginManager._currentPlugin = None
        self.stopped.emit()

        if self.teardownImmed:
            self.teardown()
    
    def eventFilter(self, obj, event: QEvent) -> bool:
        """事件过滤器"""
        return False

class PluginManager(QObject):
    pluginLoadSucceeded = Signal(str)
    pluginError = Signal(str)
    
    currentPluginChanged = Signal(str, str)

    def __init__(self, petWindow: "PetWindow"):
        super().__init__()

        self.plugins: dict[str, Plugin] = {}
        self._currentPlugin: Plugin | None = None # 正在运行的非自启动插件
        self._petWindow = petWindow
    
    @property
    def currentPlugin(self) -> Plugin | None:
        return self._currentPlugin
    
    @currentPlugin.setter
    def currentPlugin(self, plugin: Plugin | None) -> None:
        if plugin is None or plugin in self.plugins.values():
            # 停止上一个插件
            if self._currentPlugin:
                prevPlugin = self._currentPlugin
                self._currentPlugin = None
                prevPlugin.stop()
            
            if plugin is not None:
                # 运行新插件
                self._currentPlugin = plugin
                self._currentPlugin.setup(self._petWindow)
                self._currentPlugin.start()

    def loadAllPlugins(self) -> None:
        ids = self.sortPlugins()
        for id in ids:
            self.loadPlugin(id)
    
    def loadPlugin(self, id: str) -> Plugin | None:
        try:
            # 检查是否启用
            if not self._petWindow.configManager.pluginState[id]:
                return
            
            # 检查是否已加载
            if id in self.plugins:
                return
            
            module = self.importModule(ConfigManager.plugin[id]["path"])
            pluginClass = getattr(module, "Action")
            
            if pluginClass and issubclass(pluginClass, Plugin) and pluginClass is not Plugin:
                plugin = pluginClass()
                self.plugins[id] = plugin
                
                self.pluginLoadSucceeded.emit(f"succeeded to load plugin \"{id}\"")
                return plugin
            else:
                self.pluginError.emit(f"plugin \"{id}\" has not inherited from the base class \"Plugin\"")
                return None
        except Exception as e:
            print(e)
            self.pluginError.emit(f"failed to load plugin \"{id}\": {e}")
            return None
    
    def importModule(self, path: str) -> ModuleType:
        if path.startswith("./") or path.startswith(".\\"): # path 为相对路径（Windows/MacOs，Linux 不用处理）
            path = os.path.abspath(os.path.join(os.getcwd(), path[2:])) # 工作目录绝对路径 + 插件相对路径（去掉 ./ 或 .\）
        elif (len(path) > 3 and path[1] == ":") or path.startswith("/"): # path 为绝对路径
            path = os.path.abspath(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"cannot find plugin \"{path}\"")
        
        fileName = os.path.basename(path)
        moduleName = os.path.splitext(fileName)[0]

        spec = util.spec_from_file_location(moduleName, path)
        if spec is None:
            raise ImportError(f"cannot load module from \"path\"")
        
        module = util.module_from_spec(spec)

        # 添加到 sys.modules
        if moduleName not in sys.modules:
            sys.modules[moduleName] = module
        
        spec.loader.exec_module(module)

        return module
        
    def sortPlugins(self) -> list[str]:
        """通过检查依赖项对插件加载顺序排序（Kahn算法）"""
        from collections import deque
        
        ids = set(ConfigManager.plugin.keys())
        if not ids:
            return []
        
        # 构建依赖图和入度
        graph = {}  # {插件ID: [依赖的插件ID列表]}
        inDegree = {pid: 0 for pid in ids}
        
        for pid in ids:
            deps = ConfigManager.plugin.get(pid, {}).get("deps", [])
            validDeos = []
            for dep in deps:
                if dep in ids:
                    validDeos.append(dep)
                else:
                    self.pluginError.emit(f"Plugin \"{pid}\" depends on unregistered plugin \"{dep}\", skipping")
            graph[pid] = validDeos
            inDegree[pid] = len(validDeos)  # 入度 = 依赖数量
        
        # 构建反向图
        reverseGraph = {pid: [] for pid in ids}
        for pid, deps in graph.items():
            for dep in deps:
                reverseGraph[dep].append(pid)
        
        # Kahn算法
        queue = deque([pid for pid in ids if inDegree[pid] == 0])
        result = []
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            for dependent in reverseGraph[current]:
                inDegree[dependent] -= 1
                if inDegree[dependent] == 0:
                    queue.append(dependent)
        
        # 检测循环依赖
        if len(result) != len(ids):
            remaining = ids - set(result)
            raise ValueError(f"检测到循环依赖，无法加载的插件: {remaining}")
        
        return result
    def startAutoPlugins(self) -> None:
        """启动所有自启动插件"""
        for plugin in self.plugins.values():
            if plugin.auto:
                plugin.setup(self._petWindow)
                plugin.start()
    
    def getPlugin(self, id: str) -> Plugin | None:
        return self.plugins.get(id)
    
    def startPlugin(self, id: str) -> None:
        plugin = self.plugins.get(id)
        if plugin:
            self.currentPlugin = plugin
        else:
            self.pluginError.emit(f"cannot find plugin \"{id}\"")
    
    def stopPlugin(self, id: str) -> None:
        plugin = self.plugins.get(id)
        if plugin:
            if self._currentPlugin and self._currentPlugin == plugin:
                self.currentPlugin = None
            else:
                plugin.stop()
