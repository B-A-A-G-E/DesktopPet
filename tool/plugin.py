from PySide6.QtCore import QObject, Signal, QEvent

from typing import TYPE_CHECKING
import importlib

from tool import data
from tool.data import LogType

if TYPE_CHECKING:
    from window.petWindow import PetWindow

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
        self.stopped.emit()
    
    def eventFilter(self, obj, event: QEvent) -> bool:
        """事件过滤器"""
        return False

class PluginManager(QObject):
    pluginLoadSucceeded = Signal(str)
    pluginError = Signal(str)
    
    currentPluginChanged = Signal(str, str)

    def __init__(self, petWindow):
        super().__init__()

        self.plugins: dict[str, Plugin] = {}
        self._currentPlugin: Plugin | None = None # 正在运行的非自启动插件
        self._petWindow = petWindow
    
    @property
    def currentPlugin(self) -> Plugin | None:
        return self._currentPlugin
    
    @currentPlugin.setter
    def currentPlugin(self, plugin: Plugin | None) -> None:
        if not plugin or plugin in self.plugins.values():
            # 停止上一个插件
            if self._currentPlugin:
                prevPlugin = self._currentPlugin
                self._currentPlugin = None
                prevPlugin.stop()
                if prevPlugin.teardownImmed:
                    prevPlugin.teardown()
            
            if plugin:
                # 运行新插件
                self._currentPlugin = plugin
                self._currentPlugin.setup(self._petWindow)
                self._currentPlugin.start()

    def loadAllPlugins(self) -> None:
        ids = self.sortPlugins()
        for id in ids:
            self.loadPlugin(id)
    
    def loadPlugin(self, id: str) -> Plugin:
        try:
            # 检查是否启用
            if not data.plugin[id]["enabled"]:
                return
            
            # 检查是否已加载
            if id in self.plugins:
                return
            
            module = importlib.import_module(data.plugin[id]["path"])
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
            self.pluginError.emit(f"failed to load plugin \"{id}\": {e}")
            return None
    
    def sortPlugins(self) -> list[str]:
        """通过检查依赖项对插件加载顺序排序"""
        # 1. 构建依赖图
        graph = {}  # {插件ID: [依赖的插件ID列表]}
        inDegree = {}  # {插件ID: 入度（依赖它的插件数量）}
        ids = set(data.plugin.keys())
        
        # 初始化所有插件
        for id in ids:
            deps = data.plugin.get(id, {}).get("dependencies", [])
            graph[id] = deps
            inDegree[id] = 0  # 初始入度为0
        
        # 计算入度：对于每个插件A，所有依赖它的插件B，B的入度+1
        for id, deps in graph.items():
            for dep in deps:
                if dep in inDegree:
                    inDegree[dep] = inDegree.get(dep, 0) + 1
                else:
                    # 依赖的插件未注册，报错
                    self.pluginError.emit(f"Plugin \"{id}\" depends on unregistered plugin \"{dep}\"")
        
        # 2. Kahn 算法主体
        queue = []  # 存储所有入度为0的节点（可加载的插件）
        for id, degree in inDegree.items():
            if degree == 0:
                queue.append(id)
        
        result = []  # 最终的加载顺序
        sortedPlugins = set()  # 已处理的插件
        
        while queue:
            # 从队列取出一个入度为0的节点
            current = queue.pop(0)
            result.append(current)
            sortedPlugins.add(current)
            
            # 找到所有依赖 current 的插件，将其入度减1
            for id, deps in graph.items():
                if current in deps and id not in sortedPlugins:
                    inDegree[id] -= 1
                    if inDegree[id] == 0:
                        queue.append(id)
        
        # 3. 检测循环依赖
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
            if self._currentPlugin == plugin:
                self.currentPlugin = None
            else:
                plugin.stop()
                if plugin.teardownImmed:
                    plugin.teardown()
