import random

from tool import data

def replyText(type: str, act: str) -> str:
    if type == "state":
        if act in data.state:
            return data.state[act][random.randint(0, len(data.state[act]) - 1)]
    elif type == "dialog":
        if act in data.dialog:
            return data.dialog[act][random.randint(0, len(data.dialog[act]) - 1)]
    return ""
