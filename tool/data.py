import json
from enum import Enum

base: dict
anime: dict
collision: dict
action: dict
dialog: dict


class LogType(Enum):
    Error = 0
    Entre = 1
    Exit = 2
    Set = 3
    StateChange = 4


def loadData() -> None:
    global base
    global anime
    global collision
    global action, dialog

    with open("./data/base.json", "r", encoding = "utf-8") as f:
       base = json.load(f)
    with open("./data/anime.json", "r", encoding = "utf-8") as f:
       anime = json.load(f)
    with open("./data/collision.json", "r", encoding = "utf-8") as f:
       collision = json.load(f)
    with open("./data/action.json", "r", encoding = "utf-8") as f:
        action = json.load(f)
    with open("./data/dialog.json", "r", encoding = "utf-8") as f:
        dialog = json.load(f)

loadData()
