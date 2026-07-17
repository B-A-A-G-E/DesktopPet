from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Slot, Signal, QRect

from tool.config import ConfigManager
from tool.config import LogType
from tool import conv
from tool import anime
from tool.stateMachine import StateMachine
from tool.plugin import Plugin, PluginManager

from window.pet.dialogMenu import DialogMenu
from window.pet.stateMenu import StateMenu
from window.pet.actionMenu import ActionMenu
from window.pet.settingMenu import SettingMenu

class PetWindow(QWidget):
    stateChanged = Signal(str, str)
    aboutToQuit = Signal()
    
    def __init__(self, name: str, petPath: str):
        super().__init__()
        
        # 无边框及透明背景
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.name: str = name
        
        # 添加控件
        self.imgLb: QLabel = QLabel() # 存放图片

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

        # 配置管理器
        self.configManager: ConfigManager = ConfigManager(petPath)
        
        # 状态机
        self.stateMachine: StateMachine = StateMachine([k for k in self.configManager.state.keys()])

        # 插件管理器
        self.pluginManager: PluginManager = PluginManager(self)
        self.pluginManager.loadAllPlugins()

        # 添加动画
        self.animes: dict[str, anime.Anime] = { k: anime.Anime(v["path"], v["fps"], v["loop"], self, self.imgLb) for k, v in self.configManager.anime.items()}
        self.currentAnime: anime.Anime = self.animes["idle"]

        # 添加碰撞体
        self.collisions: dict[str, QRect] = { k: QRect(v["left"], v["top"], v["width"], v["height"]) for k, v in self.configManager.collision.items()}

        # 安装事件过滤器来捕获所有输入事件
        self.installEventFilter(self)
        self.setMouseTracking(True)

        # 绑定子窗口及信号
        self.bind()

        self.pluginManager.startAutoPlugins()

    def bind(self) -> None:
        """绑定子窗口及信号"""
        self.dialogMenu = DialogMenu(self.configManager)
        self.stateMenu = StateMenu(self.configManager)
        self.actionMenu = ActionMenu(self)
        self.settingMenu = SettingMenu(self.configManager)

        self.settingMenu.dataUpdated.connect(self.updateData)
        
        # 绑定上下文菜单
        self.imgLb.dialogAct.triggered.connect(self.dialogMenu.show)
        self.imgLb.stateAct.triggered.connect(self.stateMenu.show)
        self.imgLb.setAct.triggered.connect(self.settingMenu.show)
        self.imgLb.actAct.triggered.connect(self.actionMenu.show)
        self.imgLb.exitAct.triggered.connect(QApplication.quit if ConfigManager.default else self.close)

        # 绑定状态机信号
        self.stateMachine.stateChanged.connect(self.onStateChanged)
        self.stateMachine.stateUndefined.connect(lambda state: self.stateMenu.log(f"Undefined state \"{state}\"", LogType.Error))

        # 绑定插件管理器信号
        self.pluginManager.pluginLoadSucceeded.connect(lambda text: self.stateMenu.log(f"succeeded to load plugin \"{text}\"", LogType.PluginLoaded))
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

    def operateState(self, state: str, anime: str, isContinue: bool = False, isAsync: bool = True) -> None:
        """执行对应行动时进行响应"""
        currentState = self.stateMachine.currentState
        
        if currentState != state:
            # 更新状态
            self.stateMachine.currentState = state
            # 在dialogMenu回复
            self.replyState(state)
            # 切换动画
            self.changeAnime(anime, isContinue, isAsync)
    
    def changeState(self, state: str) -> None:
        """更新状态"""
        currentState = self.stateMachine.currentState
        if currentState != state:
                self.stateMachine.currentState = state
    
    def replyState(self, state: str) -> None:
        """回复状态"""
        self.dialogMenu.addLine(conv.replyText("state", state, self.configManager))

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

    def closeEvent(self, event) -> None:
        try:
            # 1. 停止所有插件
            for plugin in self.pluginManager.plugins.values():
                if plugin.auto:
                    try:
                        plugin.stop()
                        if not plugin.teardownImmed:
                            plugin.teardown()
                    except Exception as e:
                        print(f"failed to stop plugin {plugin.id}: {e}")
            self.pluginManager.currentPlugin = None
            
            # 2. 停止所有动画定时器
            for anime in self.animes.values():
                anime.stop()  # 停止定时器
                # 断开所有信号连接
                try:
                    anime.loadError.disconnect()
                except (RuntimeError, TypeError):
                    pass
            
            # 3. 清空插件管理器
            self.pluginManager.plugins.clear()
            self.pluginManager.deleteLater()

            # 4. 断开所有信号连接
            try:
                self.stateMachine.stateChanged.disconnect()
                self.stateMachine.stateUndefined.disconnect()
                self.settingMenu.dataUpdated.disconnect()
            except (RuntimeError, TypeError):
                pass
            
            # 5. 删除所有子窗口
            for menu in [self.dialogMenu, self.stateMenu, self.actionMenu, self.settingMenu]:
                if menu:
                    try:
                        menu.close()
                        menu.deleteLater()
                    except Exception:
                        pass
            
            # 6. 删除动画对象
            for key in list(self.animes.keys()):
                anime = self.animes.pop(key)
                try:
                    anime.deleteLater()
                except Exception:
                    pass
            
            # 7. 清空碰撞体
            self.collisions.clear()
            
            # 8. 删除状态机和配置管理器
            self.stateMachine.deleteLater()
            self.configManager.deleteLater()
            
            # 9. 从主窗口的宠物列表中移除
            if not ConfigManager.default:
                from window.manager.mainWindow import MainWindow
                if self in MainWindow.pets:
                    MainWindow.pets.remove(self)
            
            # 10. 写入日志
            with open(self.configManager.base["log-path"], "a", encoding = "utf-8") as f:
                from datetime import datetime
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {LogType.Exit}:    Succeeded to exit\n")
            
            # 11. 发射退出信号
            self.aboutToQuit.emit()
            
            # 12. 最后删除自身
            self.deleteLater()
            
        except Exception as e:
            print(f"Error in closeEvent: {e}")
        
        event.accept()
    
    @Slot(str, str)
    def onStateChanged(self, prevState: str, currentState: str) -> None:
        self.stateMenu.log(self.state, LogType.StateChanged)
        self.stateChanged.emit(prevState, currentState)

    @Slot()
    def updateData(self) -> None:
        """更新数据"""
        # petWindow
        self.animes = { k: anime.Anime(v["path"], v["fps"], v["loop"], self, self.imgLb) for k, v in self.configManager.anime.items()}
        self.collisions = { k: QRect(v["left"], v["top"], v["width"], v["height"]) for k, v in self.configManager.collision.items()}
        # dialogWindow
        self.dialogMenu.resetQuesSelecter()
        self.stateMenu.log("Data is updated", LogType.Set)
