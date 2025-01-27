import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog, QTabWidget, QCheckBox, QPushButton, QLineEdit, QMessageBox,QCompleter,QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from qfluentwidgets import PushButton, LineEdit, CheckBox, StrongBodyLabel, QColor, BodyLabel,ComboBox 
import getpass
import threading
import time
import os

def finde(path,name) :
    b=[]
    for root, dirs, files in os.walk(path):
        if name in files:
            a= os.path.join(root, name)
            b.append(a)
    return list(b)
def run_base():
    """
    获取所有python_tool和pyquick的安装路径,并保存到文件中"/Users/liexe/pt_saved/launch/stands_base.txt
    """

    # 函数体待补充
    
    #解释代码

    path1="/Users"
    #path2="/Users"
    name1="python_tool"
    #name2="pyquick"
    path3="/Applications"   
    name3="python_tool"
    #path4="/Applications"
    name4="pyquick"
    
    

    def s1():
        stands_base1 = finde(path1,name1)
        return stands_base1
    def s2():
        stands_base2 = finde(path1,name4)
        return stands_base2
    def s3():
        stands_base3 = finde(path3,name3)
        return stands_base3
    def s4():    
        stands_base4 = finde(path3,name4)
        return stands_base4
    stands_base1 = s1()
    stands_base2 = s2()
    stands_base3 = s3()
    stands_base4 = s4()
    #stands_base2 = finde(path2,name2)
    stands_b2 = []
    def run_base1(i):
        j=str(i).split("/")
        #print(j)
        k=""
        for i in j:
            if ("Contents" not in  i) and ("MacOS" not in i) and (i != "python_tool")  :
                k+=i+"/"
        stands_b2.append(k)
    def run_base2(i):
        j2=str(i).split("/")
        #print(j2)
        k2=""
        for i in j2:
            if ("Contents" not in  i) and ("MacOS" not in i) and (i != "pyquick")  :
                k2+=i+"/"
        stands_b2.append(k2)

    for i in stands_base1:
        run_base1(i)
    for i in stands_base2:
        run_base2(i)
    for i in stands_base3:
        run_base1(i)
    for i in stands_base4:
        run_base2(i)
    if os.path.exists(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_base.txt"):
        with open(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_base2.txt", "w") as f:
            for i in stands_b2:
                f.write(i)
                f.write("\n")
    else:
        with open(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_base.txt", "w") as f:
            for i in stands_b2:  
                f.write(i)
                f.write("\n")
    #return stands_b2

        
def run():
    if(os.path.exists(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_base.txt")):
        with open(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_base.txt", "r") as f:
            stands_b2 = f.readlines()
            stands=[]
            if stands_b2 == []:
                with open(f"/Users/{getpass.getuser()}/pt_saved/launch/launch.txt", "w") as f:
                    f.write("Disabled")
                    f.close()
                return None
            
            else:
                for i in stands_b2:
                    i=i.strip("\n")
                    if(os.path.exists(i) and ("python_tool" in i or "pyquick" in i)):
                        stands.append(i)
                        with open(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_base2.txt", "w") as f:
                            f.write(i)
                            f.write("\n")
                        with open(f"/Users/{getpass.getuser()}/pt_saved/launch/launch.txt", "w") as f:
                            f.write("Enabled")
                            f.close()
                return stands
    else:
        stands_b2=run_base()
        if stands_b2 == []:
            with open(f"/Users/{getpass.getuser()}/pt_saved/launch/launch.txt", "w") as f:
                f.write("Disabled")
                f.close()
        else:
            with open(f"/Users/{getpass.getuser()}/pt_saved/launch/launch.txt", "w") as f:
                f.write("Enabled")
                f.close()
        return stands_b2
def run_thread():
    i=1
    while True:
        a=threading.Thread(target=run_base)
        a.start()
        a.join()
        print(f"success:{i}")
        i+=1
        #time.sleep(1.5)
def start():
    if os.path.exists(f"/Users/{getpass.getuser()}/pt_saved/launch"):
        pass
    else:
        os.mkdir(f"/Users/{getpass.getuser()}/pt_saved/launch")
        run()
    if os.path.exists(f"/Users/{getpass.getuser()}/pt_saved/launch/launch.txt"):
        pass
    else:   
        with open(f"/Users/{getpass.getuser()}/pt_saved/launch/launch.txt", "w") as f:
            f.write("")
            f.close()
    if os.path.exists(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_base2.txt"):
        with open(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_base2.txt", "r") as f:
            stands_b2 = f.read()
        with open(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_base.txt", "w") as f: 
            f.write(stands_b2)
            

class Selectpyquick(QWidget): 
    def get_user_add(self):
        try:
            with open(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_user.txt", "r") as f:
                user_add=f.readlines()
                return user_add
        except FileNotFoundError:
            return []
        except Exception :
            return []
    edd=[]
    def save_user_add(self):
        with open(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_base.txt", "r")as f:
            e=f.readlines()
        with open(f"/Users/{getpass.getuser()}/pt_saved/launch/stands_user.txt", "a+") as f:
            ed=f.readlines()
            
            for i in ed:
                self.edd.append(i.strip("\n"))
            for i in e:
                self.edd.append(i.strip("\n"))
            print(self.edd)
            for i in range(len(self.edd)):
                if(self.edd[i]==self.add_pyquick_combobox.text()):
                    print(1)
                    break
                elif(i==len(self.edd)-1):
                    print(2)
                    f.write(self.add_pyquick_combobox.text())
                    f.write("\n")
        self.scan_pyquick_ver()
    def scan_pyquick_ver(self):
        items=run()
        user_add=self.get_user_add()
        version_list=[]
        both=[]
        for i in items:
            try:
                path=i+"/Contents/Resources/versions.txt"  
                with open(path, "r") as f:
                    version_list.append(f.read())
            except FileNotFoundError:
                version_list.append("unknown")
        for i in user_add:
            try:
                path=i.strip("\n")+"/Contents/Resources/versions.txt"  
                with open(path, "r") as f:
                    version_list.append(f.read())
            except FileNotFoundError:
                version_list.append("unknown")
        #print(version_list)
        for i in range(len(items)):
            a=str(items[i])
            b=str(version_list[i])      
            both.append(f"{b}:{a}")
        return both
    def start_file(self):
        u=self.selectbox.currentText().split(":")[1].strip()
        if ("python_tool.app" in u) or ("Pyquick.app" in u) or ("Python_tool.app" in u) or ("Pt.app" in u) or (
                "Python_Tool.app" in u) or ("python_tool.py" in u) or ("pyquick.app" in u) or (
                "Pyquick.py" in u) or ("pyquick.py" in u):
            if "python_tool.py" in u:
                os.system(f"python3 {u}")
            else:
                os.system(f"open {u}")

            def en():
                time.sleep(3)
                sys.exit(0)
                #os.system("killall Pyquick_Launcher_2.0" )
                #os.system("killall Python" )
                #os.system("killall Pthon3" )
                #for i in range(14):
                    #os.system(f"killall Python3.{i}")
                
            en()
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Select App File", "", "App Files (*.app)")
        if file_path:
            # 设置lineedit的文本
            self.add_pyquick_combobox.setText(file_path)
    def __init__(self, parent=None):
        super(Selectpyquick, self).__init__(parent)    
        self.setWindowTitle('Pyquick_Launcher_2.0' )
        layout=QVBoxLayout()
        loyout=QHBoxLayout()
        self.itemss=self.scan_pyquick_ver()
        self.path=run()

        self.not_found_label=BodyLabel("Please select Pyquick.")
        self.not_found_label.setTextColor(QColor(255, 0, 0))

        self.selectbox=ComboBox(self)
        self.selectbox.addItems(self.itemss)

        self.add_pyquick_combobox=LineEdit(self)

        self.add_pyquick_button=PushButton("select_path(pyquick)", self)
        self.add_pyquick_button.setFixedWidth(300)
        self.add_pyquick_button.clicked.connect(self.select_file)

        self.save_button=PushButton("save", self)
        self.save_button.setFixedWidth(80)
        self.save_button.clicked.connect(self.save_user_add)
        

        self.Pushbotton=PushButton("start", self)
        self.Pushbotton.clicked.connect(self.start_file)

        layout.addWidget(self.not_found_label)
        layout.addStretch(1)
        layout.addWidget(self.selectbox)
        layout.addStretch(1)
        layout.addWidget(self.add_pyquick_combobox)
        loyout.addStretch(1)
        loyout.addWidget(self.add_pyquick_button)
        loyout.addStretch(1)
        loyout.addWidget(self.save_button)
        loyout.addStretch(1)
        layout.addLayout(loyout)
        layout.addStretch(1)
        layout.addWidget(self.Pushbotton)
        layout.addStretch(1)
        self.setLayout(layout)




        

class MainWindow(QWidget):

    def __init__(self,parent=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Pyquick_Launcher_2.0' )
        #self.resize(400, 300)
        # 主窗格布局
        
        # 写一个选择文件函数，仅允许打开app文件
        def select_file(self):
            file_path, _ = QFileDialog.getOpenFileName(None, "Select App File", "", "App Files (*.app)")
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
                    os.system("killall Pyquick_Launcher_2.0" )
                    os.system("killall Python" )
                    os.system("killall Pthon3" )
                    for i in range(14):
                        os.system(f"killall Python3.{i}")
                    sys.exit(0)
                en()
        # 写一个启动app函数，判断是否存在app文件，存在则启动，不存在则提示
        
        self.not_found_label=BodyLabel("Pyquick.app is not found.")
        self.not_found_label.setTextColor(QColor(255, 0, 0))

        self.lineedit = LineEdit(self)
        self.lineedit.setFixedWidth(600)
        stands  =run()
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
    threading.Thread(target=run_thread, daemon=True).start()
    app = QApplication(sys.argv)
    with open(f"/Users/{getpass.getuser()}/pt_saved/launch/launch.txt", "r") as f:
        if f.read() == "Enabled":
            window = Selectpyquick()
            window.show()
        else:
            window = MainWindow()
            window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()
    main()
