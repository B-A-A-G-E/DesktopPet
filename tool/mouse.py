from PySide6.QtCore import QPoint

def getCollision(self, pos: QPoint) -> str | None:
    """获取鼠标点击位置的碰撞体"""
    for k in self.collisions.keys():
        if self.collisions[k].contains(pos):
            return k
    return None
