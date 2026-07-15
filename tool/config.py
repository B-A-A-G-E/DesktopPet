from PySide6.QtCore import QObject, Signal

import json
from enum import Enum

pets: dict[str, str]

class LogType(Enum):
    Error = 0
    Entre = 1
    Exit = 2
    Set = 3
    StateChanged = 4
    PluginLoaded = 5

class ConfigManager(QObject):
    saveError = Signal(str)
    def __init__(self, path: str):
        super().__init__()
        self.path = path
        self.base: dict = {}
        self.anime: dict[str, dict] = {}
        self.collision: dict = {}
        self.state: dict[str, list[str]] = {}
        self.dialog: dict[str, list[str]] = {}
        self.pluginState: dict[str, bool] = {}
        self.plugin: dict[str, dict] = {}

        self.loadConfig()

    def loadConfig(self) -> None:
        try:
            with open(f"{self.path}config/base.json", "r", encoding = "utf-8") as f:
                self.base = json.load(f)
            with open(f"{self.path}config/anime.json", "r", encoding = "utf-8") as f:
                self.anime = json.load(f)
            with open(f"{self.path}config/collision.json", "r", encoding = "utf-8") as f:
                self.collision = json.load(f)
            with open(f"{self.path}config/state.json", "r", encoding = "utf-8") as f:
                self.state = json.load(f)
            with open(f"{self.path}config/dialog.json", "r", encoding = "utf-8") as f:
                self.dialog = json.load(f)
            with open(f"{self.path}config/pluginState.json", "r", encoding = "utf-8") as f:
                self.pluginState = json.load(f)
            with open("./pet/plugin.json", "r", encoding = "utf-8") as f:
                self.plugin = json.load(f)
        except Exception as e:
            print(e)
    
    def saveConfig(self) -> None:
        try:
            with open(f"{self.path}config/base.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(self.base, ensure_ascii = False, indent = 2))
            with open(f"{self.path}config/anime.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(self.anime, ensure_ascii = False, indent = 2))
            with open(f"{self.path}config/collision.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(self.collision, ensure_ascii = False, indent = 2))
            with open(f"{self.path}config/state.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(self.state, ensure_ascii = False, indent = 2))
            with open(f"{self.path}config/dialog.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(self.dialog, ensure_ascii = False, indent = 2))
            with open(f"{self.path}config/pluginState.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(self.pluginState, ensure_ascii = False, indent = 2))
            with open("./pet/plugin.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(self.plugin, ensure_ascii = False, indent = 2))
        except Exception as e:
            print(e)
            self.saveError.emit(e)

def loadPets() -> None:
        global pets

        try:
            with open("./pet/config.json", "r", encoding = "utf-8") as f:
                pets = json.load(f)
        except Exception as e:
            print(e)

loadPets()
