from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPoint, QRect

def pointAt(point: QPoint, colls: dict[str, QRect]) -> list[str]:
    """获取鼠标点击位置的碰撞体"""
    collList: list[str] = []
    for k, coll in colls.items():
        if coll.contains(point):
            collList.append(k)
    return collList

def isCollided(coll1: QRect, coll2: QRect) -> bool:
    return coll1.intersects(coll2)

def getCollision(coll: QRect, colls: dict[str, QRect]) -> list[str]:
    collList: list[str] = []
    for k, v in colls.items():
        if coll.intersects(v):
            collList.append(k)
    return collList
