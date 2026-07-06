from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPoint

def getCollision(widget: QWidget, pos: QPoint) -> str | None:
    """获取鼠标点击位置的碰撞体"""
    for k in widget.collisions.keys():
        if widget.collisions[k].contains(pos):
            return k
    return None
