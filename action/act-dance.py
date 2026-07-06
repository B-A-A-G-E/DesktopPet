from tool.plugin import Plugin

class Dance(Plugin):
    def __init__(self):
        super().__init__()
        
        self.id = "act-dance"
        self.name = "跳舞"
        self.description = "播放跳舞动画"
    
    def start(self):
        self.window.changeAnime(self.id)
    
    def stop(self):
        pass
