import json
from enum import Enum

base: dict
anime: dict
collision: dict
state: dict
dialog: dict
plugin: dict

class LogType(Enum):
    Error = 0
    Entre = 1
    Exit = 2
    Set = 3
    StateChanged = 4
    PluginLoaded = 5


def loadData() -> None:
    global base
    global anime
    global collision
    global state, dialog
    global plugin

    with open("./data/base.json", "r", encoding = "utf-8") as f:
       base = json.load(f)
    with open("./data/anime.json", "r", encoding = "utf-8") as f:
       anime = json.load(f)
    with open("./data/collision.json", "r", encoding = "utf-8") as f:
       collision = json.load(f)
    with open("./data/state.json", "r", encoding = "utf-8") as f:
        state = json.load(f)
    with open("./data/dialog.json", "r", encoding = "utf-8") as f:
        dialog = json.load(f)
    with open("./data/plugin.json", "r", encoding = "utf-8") as f:
        plugin = json.load(f)

loadData()
