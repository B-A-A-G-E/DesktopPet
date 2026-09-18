from PySide6.QtCore import QObject, Signal

import json
from enum import Enum

class LogType(Enum):
    Error = 0
    Enter = 1
    Exit = 2
    Set = 3
    StateChanged = 4
    PluginLoaded = 5

class ConfigManager(QObject):
    class SaveMode(Enum):
        All = 0          # 所有配置
        Static = 1       # 静态成员变量 (pets, plugin, settings)
        Common = 2       # 普通成员变量 (base, anime, collision, state, dialog, pluginState)
        Pets = 3         # pets config
        Plugin = 4       # plugin/config.json
        Settings = 5     # settings.json
        Base = 6         # base.json
        Anime = 7        # anime.json
        Collision = 8    # collision.json
        State = 9        # state.json
        Dialog = 10      # dialog.json
        PluginState = 11 # pluginState.json
    
    loadError = Signal(str)
    saveError = Signal(str)
    
    # 静态成员变量（类变量）
    pets: list[str] = []
    plugin: dict[str, dict] = {}
    settings: dict = {}
    default: bool = False

    def __init__(self, name: str):
        super().__init__()

        self.path = f"./pet/{name}/"
        # 普通成员变量（实例变量）
        self.info: dict = {}
        self.base: dict = {}
        self.anime: dict[str, dict] = {}
        self.collision: dict = {}
        self.state: dict[str, list[str]] = {}
        self.dialog: dict[str, list[str]] = {}
        self.pluginState: dict[str, bool] = {}

        self.loadConfig()

    def loadConfig(self) -> None:
        """加载所有配置文件"""
        configFiles = {
            "info.json": "info",
            "base.json": "base",
            "anime.json": "anime",
            "collision.json": "collision",
            "state.json": "state",
            "dialog.json": "dialog",
            "pluginState.json": "pluginState"
        }
        
        for file, attr in configFiles.items():
            try:
                if attr == "info":
                    with open(f"{self.path}info.json", "r", encoding = "utf-8") as f:
                        setattr(self, attr, json.load(f))
                else:
                    with open(f"{self.path}config/{file}", "r", encoding = "utf-8") as f:
                        setattr(self, attr, json.load(f))
            except FileNotFoundError as e:
                print(f"cannot find file {file}: {e}")
                setattr(self, attr, {})
            except Exception as e:
                print(f"failed to load config {file}: {e}")
                self.loadError.emit(e)

    def saveConfig(self, mode: SaveMode = SaveMode.All) -> None:
        """根据模式保存配置文件"""
        try:
            match mode:
                # 保存所有配置
                case self.SaveMode.All:
                    self.saveAllConfigs()
                
                # 保存静态成员变量 (pets, plugin, settings)
                case self.SaveMode.Static:
                    ConfigManager.saveStaticConfigs()
                
                # 保存普通成员变量 (base, anime, collision, state, dialog, pluginState)
                case self.SaveMode.Common:
                    self.saveCommonConfigs()
                
                # 保存单个配置文件
                case self.SaveMode.Pets:
                    ConfigManager.save("./pet/config.json", self.pets)
                
                case self.SaveMode.Plugin:
                    ConfigManager.save("./plugin/config.json", self.plugin)
                
                case self.SaveMode.Settings:
                    ConfigManager.save("./settings.json", self.settings)
                
                case self.SaveMode.Base:
                    ConfigManager.save(f"{self.path}config/base.json", self.base)
                
                case self.SaveMode.Anime:
                    ConfigManager.save(f"{self.path}config/anime.json", self.anime)
                
                case self.SaveMode.Collision:
                    ConfigManager.save(f"{self.path}config/collision.json", self.collision)
                
                case self.SaveMode.State:
                    ConfigManager.save(f"{self.path}config/state.json", self.state)
                
                case self.SaveMode.Dialog:
                    ConfigManager.save(f"{self.path}config/dialog.json", self.dialog)
                
                case self.SaveMode.PluginState:
                    ConfigManager.save(f"{self.path}config/pluginState.json", self.pluginState)
                
                case _:
                    raise ValueError(f"不支持的保存模式: {mode}")
                    
        except Exception as e:
            print(f"failed to save config: {e}")
            self.saveError.emit(str(e))
    
    def saveAllConfigs(self) -> None:
        """保存所有配置"""
        ConfigManager.saveStaticConfigs()
        self.saveCommonConfigs()
    
    @staticmethod
    def saveStaticConfigs() -> None:
        """保存静态成员变量（类变量）"""
        ConfigManager.save("./pet/config.json", ConfigManager.pets)
        ConfigManager.save("./plugin/config.json", ConfigManager.plugin)
        ConfigManager.save("./settings.json", ConfigManager.settings)
    
    def saveCommonConfigs(self) -> None:
        """保存普通成员变量（实例变量）"""
        ConfigManager.save(f"{self.path}config/base.json", self.base)
        ConfigManager.save(f"{self.path}config/anime.json", self.anime)
        ConfigManager.save(f"{self.path}config/collision.json", self.collision)
        ConfigManager.save(f"{self.path}config/state.json", self.state)
        ConfigManager.save(f"{self.path}config/dialog.json", self.dialog)
        ConfigManager.save(f"{self.path}config/pluginState.json", self.pluginState)
    
    @staticmethod
    def save(filepath, data) -> None:
        with open(filepath, "w", encoding = "utf-8") as f:
            json.dump(data, f, ensure_ascii = False, indent = 2)

# 全局加载函数
def loadPets() -> None:
    """加载宠物相关配置"""
    try:
        with open("./pet/config.json", "r", encoding = "utf-8") as f:
            ConfigManager.pets = json.load(f)
        with open("./plugin/config.json", "r", encoding = "utf-8") as f:
            ConfigManager.plugin = json.load(f)
        with open("./settings.json", "r", encoding = "utf-8") as f:
            ConfigManager.settings = json.load(f)
    except FileNotFoundError as e:
        print(f"cannot find config: {e}")
        # 初始化空配置
        ConfigManager.pets = []
        ConfigManager.plugin = {}
        ConfigManager.settings = {}
    except Exception as e:
        print(f"failed to load config: {e}")
        raise e

loadPets()
