from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyQt 示例')
        self.setGeometry(100, 100, 300, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 创建标签
        self.label = QLabel('点击按钮', self)
        layout.addWidget(self.label)

        # 创建按钮
        self.button = QPushButton('点击我', self)
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        # 设置窗口布局
        self.setLayout(layout)

    def on_click(self):
        self.label.setText('按钮已被点击')

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
