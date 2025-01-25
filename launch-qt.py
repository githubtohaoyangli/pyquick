import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog, QTabWidget, QCheckBox, QPushButton, QLineEdit, QMessageBox,QCompleter,QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from qfluentwidgets import PushButton, LineEdit, CheckBox, StrongBodyLabel, QColor, BodyLabel
import getpass
import find
from find import finde
import os
def refresh_versions():
    print("版本已刷新")

class MainWindow(QWidget):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Pyquick Launcher 2.0' )
        #self.resize(400, 300)
        # 主窗格布局
        stands_base1 = list(finde("/Users", "python_tool"))
        stands_base2 = list(finde("/Users", "pyquick"))
        stands_b2 = []

        for i in stands_base1:
            j=i.split("/")
            print(j)
            k=""
            for i in j:
                if ("Contents" not in  i) and ("MacOS" not in i) and (i != "python_tool")  :
                    k+=i+"/"
            stands_b2.append(k)
        for i in stands_base2:
            j2=i.split("/")
            print(j2)
            k2=""
            for i in j:
                if ("Contents" not in  i) and ("MacOS" not in i) and (i != "python_tool")  :
                    k2+=i+"/"
            stands_b2.append(k2)
        stands=stands_b2
        print(stands)
        # 写一个选择文件函数，仅允许打开app文件
        def select_file(self):
            file_path, _ = QFileDialog.getOpenFileName(None, "选择文件", "", "App Files (*.app)")
            if file_path:
                # 设置lineedit的文本
                self.lineedit.setText(file_path)

        def start_file(self):
            u=self.lineedit.text()
            if (("python_tool.app" in u) or ("Pyquick.app" in u) or ("Python_tool.app" in u) or ("Pt.app" in u) or (
                    "Python_Tool.app" in u) or ("python_tool.py" in u) or ("pyquick.app" in u) or (
                    "Pyquick.py" in u) or ("pyquick.py" in u)):
                if "python_tool.py" in u:
                    os.system(f"python3 {u}")
                else:
                    os.system(f"open {u}")

                def en():
                    sys.exit(0)
                en()
            else:
                path=f"/Users/{getpass.getuser()}/pt_saved/launch"
                with open(f"{path}/launch.txt", "w") as f:
                    f.write("")
        # 写一个启动app函数，判断是否存在app文件，存在则启动，不存在则提示


        self.not_found_label=BodyLabel("Pyquick.app is not found.")
        self.not_found_label.setTextColor(QColor(255, 0, 0))

        self.lineedit = LineEdit(self)
        self.lineedit.setFixedWidth(600)
        completer = QCompleter(stands, self.lineedit)
        completer.setMaxVisibleItems(10)
        self.lineedit.setCompleter(completer)

        self.button_select = PushButton("select-file", self)
        self.button_select.clicked.connect(lambda: select_file(self))

        self.button_start=PushButton("start", self)
        self.button_start.clicked.connect(lambda: start_file(self))

        layout_main = QVBoxLayout()
        h_main=QHBoxLayout()
        layout_main.addStretch(1)
        layout_main.addWidget(self.not_found_label)
        layout_main.addStretch(1)
        layout_main.addWidget(self.lineedit)
        layout_main.addStretch(1)
        layout_main.addWidget(self.button_select)
        layout_main.addStretch(1)
        layout_main.addWidget(self.button_start)
        layout_main.addStretch(1)

        self.setLayout(layout_main)
        # 设置主窗口布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self)
        self.setLayout(main_layout)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
