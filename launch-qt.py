import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox
from qfluentwidgets import PushButton,BodyLabel
def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('launch')
    window.setGeometry(100, 100, 400, 150)
    
    label = BodyLabel('Hello, This is pyquick ', window)
    label.move(100, 30)
    
    # 添加输入框
    line_edit = QLineEdit(window)
    line_edit.move(100, 70)
    line_edit.resize(200, 30)
    
    # 添加按钮
    button = PushButton('Show Message', window)
    button.move(100, 110)
    button.clicked.connect(lambda: show_message(line_edit.text()))
    
    window.show()
    sys.exit(app.exec_())

# 添加槽函数

def show_message(text):
    msg_box = QMessageBox()
    msg_box.setWindowTitle('Message')
    msg_box.setText(text)
    msg_box.exec_()

if __name__ == '__main__':
    main()