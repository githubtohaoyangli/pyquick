import sys
from qfluentwidgets import PushButton, VBoxLayout,PillPushButton,PrimaryPushButton,TogglePushButton,CalendarPicker, FluentTranslator
from PyQt5.QtWidgets import  QWidget,QMainWindow,QApplication,QVBoxLayout
from enum import Enum
class MainWindow(QMainWindow):

    def __init__(self):

        """
        构造函数，初始化主窗口
        """
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle("PyQt5 Example")
        # 设置窗口位置和大小
        #self.setGeometry(100, 100, 300, 200)

        # 创建一个按钮
        self.buttona = PushButton("hello", self)
        # 将按钮的点击事件连接到 on_click 槽函数
        self.buttona.clicked.connect(self.on_click)
        self.buttonb=TogglePushButton("you",self)
        self.buttonb.clicked.connect(self.on_click)
        self.cale=CalendarPicker(self)
        # 创建一个布局管理器
        layout = QVBoxLayout()
        # 将按钮添加到布局管理器中
        layout.addWidget(self.buttona)
        layout.addWidget(self.buttonb)
        layout.addWidget(self.cale)

        # 创建一个中心部件并将布局添加到其中
        container = QWidget()
        container.setLayout(layout)

        # 设置中心部件
        self.setCentralWidget(container)

    def on_click(self):
        """
        按钮点击事件的槽函数
        当按钮被点击时，打印一条消息到控制台
        """
        print("Button clicked!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
