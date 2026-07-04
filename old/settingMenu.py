from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QTabWidget, QToolBox, QLineEdit, QPushButton, QCheckBox
from PySide6.QtCore import Signal

import json
from tool import data

class SettingMenu(QWidget):
    dataUpdated = Signal()

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Setting Menu")
        self.resize(600, 450)
        
        self.lyt = QVBoxLayout()
        self.tabw = QTabWidget()
        self.initPage1()
        self.initPage2()
        self.initpage3()
        self.initPage4()
        self.initPage5()
        self.applyBtn = QPushButton("应用")
        self.cancelBtn = QPushButton("取消")
        self.lyt.addWidget(self.tabw)
        self.lyt.addWidget(self.applyBtn)
        self.lyt.addWidget(self.cancelBtn)
        self.setLayout(self.lyt)
        
        self.bind()
    
    def initPage1(self) -> None:
        """初始化page1（基础项）"""
        self.pg1 = QWidget()
        self.pg1.lyt = QFormLayout()
        
        self.pg1.logEdit = QLineEdit(text = data.base["log-path"])
        self.pg1.failEdit = QLineEdit(text = data.base["load-failed-img-path"])
        self.pg1.numEdit = QLineEdit(text = str(data.base["quesSelecter-item-count"]))
        self.pg1.idleEdit = QLineEdit(text = str(data.base["idle-time"]))
        self.pg1.idleMoveTimeEdit = QLineEdit(text = str(data.base["idle-move-time"]))
        self.pg1.moveMinStepEdit = QLineEdit(text = str(data.base["move-min-step"]))
        self.pg1.moveMaxStepEdit = QLineEdit(text = str(data.base["move-max-step"]))
        self.pg1.moveStepTimeEdit = QLineEdit(text = str(data.base["move-step-time"]))
        self.pg1.moveSpeedEdit = QLineEdit(text = str(data.base["move-speed"]))
        
        self.pg1.lyt.addRow("日志保存路径", self.pg1.logEdit)
        self.pg1.lyt.addRow("加载失败图片路径", self.pg1.failEdit)
        self.pg1.lyt.addRow("询问框最大问题数", self.pg1.numEdit)
        self.pg1.lyt.addRow("待机判定时间（毫秒）", self.pg1.idleEdit)
        self.pg1.lyt.addRow("待机移动时间（毫秒）", self.pg1.idleMoveTimeEdit)
        self.pg1.lyt.addRow("移动最小步长", self.pg1.moveMinStepEdit)
        self.pg1.lyt.addRow("移动最大步长", self.pg1.moveMaxStepEdit)
        self.pg1.lyt.addRow("移动步进时间（毫秒）", self.pg1.moveStepTimeEdit)
        self.pg1.lyt.addRow("移动速度（像素/步）", self.pg1.moveSpeedEdit)
        self.pg1.setLayout(self.pg1.lyt)
        self.tabw.addTab(self.pg1, "基础项")
    
    def initPage2(self) -> None:
        """初始化page2（动画）"""
        self.pg2 = QWidget()
        self.pg2.lyt = QVBoxLayout()
        self.pg2.box = QToolBox()

        self.pg2.box.w = {}
        for k, v in data.anime.items():
            # 创建布局及控件: k:{"w":QWidget,"f":QFormLayout,"path":QLineEdit,"fps":QLineEdit,"loop":QCheckBox}
            self.pg2.box.w[k] = {}
            self.pg2.box.w[k]["w"] = QWidget()
            self.pg2.box.w[k]["f"] = QFormLayout()
            self.pg2.box.w[k]["path"] = QLineEdit(v["path"])
            self.pg2.box.w[k]["fps"] = QLineEdit(str(v["fps"]))
            self.pg2.box.w[k]["loop"] = QCheckBox("")
            self.pg2.box.w[k]["loop"].setChecked(v["loop"])
            # 向布局添加控件
            self.pg2.box.w[k]["f"].addRow("Path:", self.pg2.box.w[k]["path"])
            self.pg2.box.w[k]["f"].addRow("Fps:", self.pg2.box.w[k]["fps"])
            self.pg2.box.w[k]["f"].addRow("Loop:", self.pg2.box.w[k]["loop"])
            self.pg2.box.w[k]["w"].setLayout(self.pg2.box.w[k]["f"])
            # 向pg2.box 添加页面
            self.pg2.box.addItem(self.pg2.box.w[k]["w"], k)
        
        self.pg2.lyt.addWidget(self.pg2.box)
        self.pg2.setLayout(self.pg2.lyt)
        self.tabw.addTab(self.pg2, "动画")

    def initpage3(self) -> None:
        """初始化page3（碰撞体）"""
        self.pg3 = QWidget()
        self.pg3.lyt = QVBoxLayout()
        self.pg3.box = QToolBox()

        self.pg3.box.w = {}
        for k, v in data.collision.items():
            # 创建布局及控件: k:{"w":QWidget,"f":QFormLayout,"path":QLineEdit,"fps":QLineEdit,"loop":QCheckBox}
            self.pg3.box.w[k] = {}
            self.pg3.box.w[k]["w"] = QWidget()
            self.pg3.box.w[k]["f"] = QFormLayout()
            self.pg3.box.w[k]["left"] = QLineEdit(str(v["left"]))
            self.pg3.box.w[k]["top"] = QLineEdit(str(v["top"]))
            self.pg3.box.w[k]["width"] = QLineEdit(str(v["width"]))
            self.pg3.box.w[k]["height"] = QLineEdit(str(v["height"]))
            # 向布局添加控件
            self.pg3.box.w[k]["f"].addRow("Left:", self.pg3.box.w[k]["left"])
            self.pg3.box.w[k]["f"].addRow("Top:", self.pg3.box.w[k]["top"])
            self.pg3.box.w[k]["f"].addRow("Width:", self.pg3.box.w[k]["width"])
            self.pg3.box.w[k]["f"].addRow("Height:", self.pg3.box.w[k]["height"])
            self.pg3.box.w[k]["w"].setLayout(self.pg3.box.w[k]["f"])
            # 向pg3.box 添加页面
            self.pg3.box.addItem(self.pg3.box.w[k]["w"], k)
        
        self.pg3.lyt.addWidget(self.pg3.box)
        self.pg3.setLayout(self.pg3.lyt)
        self.tabw.addTab(self.pg3, "碰撞体")

    def initPage4(self) -> None:
        """初始化page4（反应文本）"""
        self.pg4 = QWidget()
        self.pg4.lyt = QVBoxLayout()
        self.pg4.box = QToolBox()

        self.pg4.box.w = {}
        for k, v in data.action.items():
            # 创建布局及控件: k:{"w":QWidget,"c":QVBoxLayout,"r":list[QHBoxLayout],"txt":list[QLineEdit],"rmb":list[QPushButton]}
            self.pg4.box.w[k] = {}
            self.pg4.box.w[k]["w"] = QWidget()
            self.pg4.box.w[k]["c"] = QVBoxLayout()
            self.pg4.box.w[k]["r"] = []
            self.pg4.box.w[k]["txt"] = []
            self.pg4.box.w[k]["rmb"] = []
            for i in range(len(v)):
                self.pg4.box.w[k]["r"].append(QHBoxLayout())
                
                self.pg4.box.w[k]["txt"].append(QLineEdit(v[i]))
                self.pg4.box.w[k]["rmb"].append(QPushButton("移除"))
                
                self.pg4.box.w[k]["r"][i].addWidget(self.pg4.box.w[k]["txt"][i])
                self.pg4.box.w[k]["r"][i].addWidget(self.pg4.box.w[k]["rmb"][i])

                self.pg4.box.w[k]["adb"] = QPushButton("新建回复")

                self.pg4.box.w[k]["c"].addLayout(self.pg4.box.w[k]["r"][i])
                self.pg4.box.w[k]["c"].addWidget(self.pg4.box.w[k]["adb"])

            self.pg4.box.w[k]["w"].setLayout(self.pg4.box.w[k]["c"])
            # 向pg4.box 添加页面
            self.pg4.box.addItem(self.pg4.box.w[k]["w"], k)
        
        self.pg4.lyt.addWidget(self.pg4.box)
        self.pg4.setLayout(self.pg4.lyt)
        self.tabw.addTab(self.pg4, "反应文本")
    
    def initPage5(self) -> None:
        """初始化page4（对话文本）"""
        self.pg5 = QWidget()
        self.pg5.lyt = QVBoxLayout()
        self.pg5.box = QToolBox()

        self.pg5.box.w = {}
        self.pg5.lyt.addWidget(self.pg5.box)
        self.pg5.setLayout(self.pg5.lyt)
        self.tabw.addTab(self.pg5, "对话文本")
    
    def bind(self) -> None:
        # 应用&取消按钮
        self.applyBtn.clicked.connect(self.apply)
        self.cancelBtn.clicked.connect(self.cancel)
        
        # page4
        for k in data.action.keys():
            for i in range(len(self.pg4.box.w[k]["rmb"])):
                pass
                #self.pg4.box.w[k]["rmb"][i].clicked.connect()
                #self.pg4.box.w[k]["adb"].clicked.connect()
    
    def apply(self) -> None:
        # 更新数据
        # page1
        data.base["log-path"] = self.pg1.logEdit.text()
        data.base["load-failed-img-path"] = self.pg1.failEdit.text()
        data.base["quesSelecter-item-count"] = int(self.pg1.numEdit.text())
        data.base["idle-time"] = int(self.pg1.idleEdit.text())
        data.base["idle-move-time"] = int(self.pg1.idleMoveTimeEdit.text())
        data.base["move-min-step"] = int(self.pg1.moveMinStepEdit.text())
        data.base["move-max-step"] = int(self.pg1.moveMaxStepEdit.text())
        data.base["move-step-time"] = int(self.pg1.moveStepTimeEdit.text())
        data.base["move-speed"] = int(self.pg1.moveSpeedEdit.text())
        # page2
        for k in data.anime.keys():
            data.anime[k]["path"] = self.pg2.box.w[k]["path"].text()
            data.anime[k]["fps"] = int(self.pg2.box.w[k]["fps"].text())
            data.anime[k]["loop"] = self.pg2.box.w[k]["loop"].isChecked()
        # page3
        for k in data.collision.keys():
            data.collision[k]["left"] = int(self.pg3.box.w[k]["left"].text())
            data.collision[k]["top"] = int(self.pg3.box.w[k]["top"].text())
            data.collision[k]["width"] = int(self.pg3.box.w[k]["width"].text())
            data.collision[k]["height"] = int(self.pg3.box.w[k]["height"].text())
        # page4
        for k in data.action.keys():
            data.action[k] = []
            for txt in self.pg4.box.w[k]["txt"]:
                data.action[k].append(txt.text())

        # 保存数据
        with open("./data/base.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data.base))
        with open("./data/anime.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data.anime))
        with open("./data/collision.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data.collision))
        with open("./data/action.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data.action))
        with open("./data/dialog.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data.dialog))
        
        self.dataUpdated.emit()
        self.close()

    def cancel(self) -> None:
        self.close()
