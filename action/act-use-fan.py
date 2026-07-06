from tool.plugin import Plugin

class UseFan(Plugin):
    def __init__(self):
        super().__init__()
        
        self.id = "act-use-fan"
        self.name = "吹风扇"
        self.description = "播放吹风扇动画"
    
    def start(self):
        self.window.changeAnime(self.id)
    
    def stop(self):
        pass
