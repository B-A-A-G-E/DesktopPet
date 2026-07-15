import random

from tool.config import ConfigManager

def replyText(type: str, act: str, config: ConfigManager) -> str:
    if type == "state":
        if act in config.state:
            return config.state[act][random.randint(0, len(config.state[act]) - 1)]
    elif type == "dialog":
        if act in config.dialog:
            return config.dialog[act][random.randint(0, len(config.dialog[act]) - 1)]
    return ""
