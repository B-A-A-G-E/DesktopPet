from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, QDir, Slot, Signal, QObject

import time

from tool import data

def getPixNames(folderPath: str):
    """获取文件夹内所有文件名（不包括子目录）"""
    dir = QDir(folderPath)
    files = dir.entryList(QDir.Files | QDir.NoDotAndDotDot)
    def extract_number(fileName):
        # 去掉扩展名，转为整数
        nameWithoutExt = fileName.split('.')[0]
        return int(nameWithoutExt) if nameWithoutExt.isdigit() else -1
    
    # 按数值排序，过滤掉非纯数字的文件
    numericFiles = [f for f in files if f.split('.')[0].isdigit()]
    numericFiles.sort(key=extract_number)
    
    return numericFiles


def fitImgSize(window, widget):
        """窗口适应图片"""
        # 调整窗口大小以适应图片
        pixmap = widget.pixmap()
        if pixmap and not pixmap.isNull():
            window.resize(pixmap.size())
            widget.resize(pixmap.size())
        else:
            showLoadFailedMsg(window, widget)

def showLoadFailedMsg(window, widget, path: str = ""):
    operation = QMessageBox.critical(window, "Fail to Load", f"Can't load file {path}.", QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Close)
    if operation == QMessageBox.StandardButton.Ok:
        # 加载默认图片
        window.resize(200, 200)
        widget.resize(200, 200)
        widget.setPixmap(QPixmap(data.base["load-failed-img-path"]))
    elif operation == QMessageBox.StandardButton.Close:
        #退出程序
        window.close()

class Anime(QObject):
    finished = Signal() # 一轮动画播放完成信号
    overed = Signal() # 动画播放结束信号
    loadErr = Signal(str)

    def __init__(self, path: str, fps: int, loop: bool, window, widget):
        super().__init__()
        
        self.path = path # 存放帧的文件夹的路径
        self.fps = fps # 帧率
        self.loop = loop # 是否循环播放
        self.window = window # 窗体
        self.widget = widget # 存储帧的容器
        
        self.imgNames = getPixNames(self.path)
        self.index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextImg)
    
    def play(self, isContinue: bool = False, isAsync: bool = True) -> None:
        """开始或继续播放动画"""
        if not isContinue:
            self.index = 0
        
        if isAsync:
            self.timer.start(1000 // self.fps)
        else:
            for imgName in self.imgNames:
                try:
                    self.widget.setPixmap(QPixmap(f"{self.path}/{imgName}"))
                    fitImgSize(self.window, self.widget) # 调整窗口大小以适应图片
                except:
                    self.loadErr.emit(f"Can't load file {self.path}.")
                    showLoadFailedMsg(self.window, self.widget, self.path)
                time.sleep(1 / self.fps)
                QApplication.processEvents()  # 允许界面更新
            self.finished.emit()
            self.overed.emit()
    
    def stop(self) -> None:
        self.timer.stop()
    
    def over(self) -> None:
        self.index = 0
        self.timer.stop()
        self.overed.emit()
    
    def replay(self) -> None:
        self.index = 0
        self.timer.stop()
        self.timer.start(1000 // self.fps)
    
    @Slot()
    def nextImg(self) -> None:
        try:
            self.widget.setPixmap(QPixmap(f"{self.path}/{self.imgNames[self.index]}")) # 更新帧
            fitImgSize(self.window, self.widget) # 调整窗口大小以适应图片
        except:
            self.loadErr.emit(f"Can't load file {self.path}.")
            showLoadFailedMsg(self.window, self.widget, self.path)
        self.index += 1
        if self.index == len(self.imgNames):
            self.index = 0
            if not self.loop:
                self.over()
