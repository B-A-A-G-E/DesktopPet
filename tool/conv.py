import random
from tool import data

def replyText(type: str, act: str) -> str:
    if type == "action":
        if act in data.action:
            return data.action[act][random.randint(0, len(data.action[act]) - 1)]
    elif type == "dialog":
        if act in data.dialog:
            return data.dialog[act][random.randint(0, len(data.dialog[act]) - 1)]
    return ""
