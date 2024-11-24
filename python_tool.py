import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import os
import threading
import requests
import sv_ttk
import time
import wget
import logging

# 禁用 SSL 警告
requests.packages.urllib3.disable_warnings()

# 获取当前工作目录
my_path = os.getcwd()

# 如果保存目录不存在，则创建它
if not os.path.exists(f"{my_path}\\saved"):
    os.mkdir(f"{my_path}\\saved")

# 可供选择的 Python 版本列表
VERSIONS = [
    "3.12.0",
    "3.11.0",
    "3.10.0",
    "3.9.0",
    "3.8.0",
    "3.7.0",
    "3.6.0",
    "3.5.0"
]

# 清除界面中的状态标签和包标签的文本内容
def clear():
    status_label.config(text="")
    package_label.config(text="Enter Package Name:")

# 选择目标文件夹的函数
def select_destination():
    # 打开文件对话框让用户选择目录
    destination_path = filedialog.askdirectory()
    
    # 如果用户选择了目录，则更新GUI中的目标路径显示
    if destination_path:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, destination_path)

# 下载选定版本的 Python 安装程序
def download_file(selected_version, destination_path):
    file_name = f"python-{selected_version}-amd64.exe"
    destination = os.path.join(destination_path, file_name)
    
    # 如果文件已存在，则删除它
    if os.path.exists(destination):
        os.remove(destination)
    
    def progress_bar_hook(current, total, width=80):
        progress = int(current / total * 100)
        progress_bar['value'] = progress
        downloaded_mb = current / (1024 * 1024)
        status_label.config(text=f"Downloading: {downloaded_mb:.2f} MB / {total / (1024 * 1024):.2f} MB")
        root.update_idletasks()

    try:
        url = f"https://www.python.org/ftp/python/{selected_version}/python-{selected_version}-amd64.exe"
        # 使用 wget 下载文件
        wget.download(url, out=destination, bar=progress_bar_hook)
        status_label.config(text="Download Complete!")
        time.sleep(5)
        clear()
    except Exception as e:
        status_label.config(text=f"Download Failed: {str(e)}")
        time.sleep(5)
        clear()

# 获取当前 pip 版本
def get_pip_version():
    try:
        return subprocess.check_output(["pip", "--version"], creationflags=subprocess.CREATE_NO_WINDOW).decode().strip().split()[1]
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
        return None

# 获取最新 pip 版本
def get_latest_pip_version():
    try:
        r = requests.get("https://pypi.org/pypi/pip/json", verify=True)  # 启用证书验证
        return r.json()["info"]["version"]
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return None

# 更新 pip
def update_pip():
    try:
        subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"], creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
        return False

# 检查并更新 pip 版本
def check_pip_version():
    current_version = get_pip_version()
    if current_version is None:
        package_label.config(text="Error: Failed to get current pip version")
        time.sleep(5)
        clear()
        return

    latest_version = get_latest_pip_version()
    if latest_version is None:
        package_label.config(text="Error: Failed to get latest pip version")
        time.sleep(5)
        clear()
        return

    if current_version != latest_version:
        message = f"Current pip version: {current_version}\nLatest pip version: {latest_version}\nUpdating pip..."
        package_label.config(text=message)
        if update_pip():
            package_label.config(text=f"pip has been updated! {latest_version}")
            time.sleep(5)
            clear()
        else:
            package_label.config(text="Error: Failed to update pip")
            time.sleep(5)
            clear()
    else:
        package_label.config(text=f"pip is up to date: {current_version}")
        time.sleep(5)
        clear()

# 下载选定版本的 Python
def download_selected_version():
    selected_version = version_combobox.get()
    destination_path = destination_entry.get()
    
    if not os.path.exists(destination_path):
        status_label.config(text="Invalid path!")
        time.sleep(5)
        clear()
        return
    
    download_thread = threading.Thread(target=download_file, args=(selected_version, destination_path))
    download_thread.start()

# 升级 pip
def upgrade_pip():
    try:
        subprocess.check_output(["python", "--version"], creationflags=subprocess.CREATE_NO_WINDOW)
        upthread = threading.Thread(target=check_pip_version, daemon=True)
        upthread.start()
    except FileNotFoundError:
        package_label.config(text="Python is not installed.")
        time.sleep(5)
        clear()
    except Exception as e:
        package_label.config(text=f"Error: {str(e)}")
        time.sleep(5)
        clear()

# 安装指定的包
def install_package():
    try:
        subprocess.check_output(["python", "--version"], creationflags=subprocess.CREATE_NO_WINDOW)
        package_name = package_entry.get()
        
        def install_package_thread():
            try:
                result = subprocess.run(["python", "-m", "pip", "install", package_name], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                installed = subprocess.check_output(["python", "-m", "pip", "list", "--format=columns"], text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if "Successfully installed" in result.stdout:
                    package_label.config(text=f"Package '{package_name}' has been installed successfully!")
                    time.sleep(5)
                    clear()
                elif package_name.lower() in installed.lower():
                    package_label.config(text=f"Package {package_name} is already installed.")
                    time.sleep(5)
                    clear()
                else:
                    package_label.config(text=f"Error installing package '{package_name}': {result.stderr}")
                    time.sleep(5)
                    clear()
            except Exception as e:
                package_label.config(text=f"Error installing package '{package_name}': {str(e)}")
                time.sleep(5)
                clear()
        
        install_thread = threading.Thread(target=install_package_thread)
        install_thread.start()
    except FileNotFoundError:
        package_label.config(text="Python is not installed.")
        time.sleep(5)
        clear()
    except Exception as e:
        package_label.config(text=f"Error: {str(e)}")
        time.sleep(5)
        clear()

# 卸载指定的包
def uninstall_package():
    try:
        subprocess.check_output(["python", "--version"], creationflags=subprocess.CREATE_NO_WINDOW)
        package_name = package_entry.get()
        
        try:
            installed_packages = subprocess.check_output(["python", "-m", "pip", "list", "--format=columns"], text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if package_name.lower() in installed_packages.lower():
                result = subprocess.run(["python", "-m", "pip", "uninstall", "-y", package_name], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if "Successfully uninstalled" in result.stdout:
                    package_label.config(text=f"Package '{package_name}' has been uninstalled successfully!")
                    time.sleep(5)
                    clear()
                else:
                    package_label.config(text=f"Error uninstalling package '{package_name}': {result.stderr}")
                    time.sleep(5)
                    clear()
            else:
                package_label.config(text=f"Package '{package_name}' is not installed.")
                time.sleep(5)
                clear()
        except Exception as e:
            package_label.config(text=f"Error uninstalling package '{package_name}': {str(e)}")
            time.sleep(5)
            clear()
    except FileNotFoundError:
        package_label.config(text="Python is not installed.")
        time.sleep(5)
        clear()
    except Exception as e:
        package_label.config(text=f"Error: {str(e)}")
        time.sleep(5)
        clear()

# 检查 Python 是否已安装
def check_python_installation():
    try:
        subprocess.check_output(["python", "--version"], creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        status_label.config(text="Python is not installed.")
        pip_upgrade_button.config(state="disabled")
        install_button.config(state="disabled")
        uninstall_button.config(state="disabled")
        time.sleep(5)
        clear()

# 切换主题
def switch_theme():
    if switch.get():
        sv_ttk.set_theme("dark")
        with open(f"{my_path}\\saved\\theme.txt", "w") as a:
            a.write("dark")
    else:
        sv_ttk.set_theme("light")
        with open(f"{my_path}\\saved\\theme.txt", "w") as a:
            a.write("light")

# 加载保存的主题设置
def load_theme():
    try:
        with open(f"{my_path}\\saved\\theme.txt", "r") as r:
            theme = r.read()
        if theme == "dark":
            switch.set(True)
            sv_ttk.set_theme("dark")
        elif theme == "light":
            switch.set(False)
            sv_ttk.set_theme("light")
    except Exception:
        sv_ttk.set_theme("light")

# 检查更新
def update():
    r = requests.get("https://githubtohaoyangli.github.io/info/info.json")
    ver = r.json()["releases"]["release1"]["version"]
    myver = "1.1.0"
    if int(ver) > int(myver):
        pass

# 创建主窗口
root = tk.Tk()
root.title("Python_Tool")
root.resizable(False, False)
root.iconbitmap('pythontool.ico')

# 创建 Notebook
note = ttk.Notebook(root)

# 创建框架
frame = ttk.Frame(root, padding="10")
framea = ttk.Frame(root, padding="10")

# 添加框架到 Notebook
note.add(frame, text="Python Download")
note.add(framea, text="pip Management")
note.grid(padx=10, pady=10, row=0, column=0)

# Python 下载页面
version_label = ttk.Label(frame, text="Select Python Version:")
version_label.grid(row=0, column=0, pady=10, sticky="e")

selected_version = tk.StringVar()
version_combobox = ttk.Combobox(frame, textvariable=selected_version, values=VERSIONS, state="readonly")
version_combobox.grid(row=0, column=1, pady=10, padx=10, sticky="w")
version_combobox.current(0)

destination_label = ttk.Label(frame, text="Select Destination:")
destination_label.grid(row=1, column=0, pady=10, sticky="e")

destination_entry = ttk.Entry(frame, width=40)
destination_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")

select_button = ttk.Button(frame, text="Select Path", command=select_destination)
select_button.grid(row=1, column=2, pady=10, padx=10, sticky="w")

download_button = ttk.Button(frame, text="Download Selected Version", command=download_selected_version)
download_button.grid(row=2, column=0, columnspan=3, pady=10, padx=10)

progress_bar = ttk.Progressbar(frame, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=3, column=0, columnspan=3, pady=10, padx=10)

status_label = ttk.Label(frame, text="", padding="10")
status_label.grid(row=4, column=0, columnspan=3, pady=10, padx=10)

# pip 管理页面
pip_upgrade_button = ttk.Button(framea, text="Upgrade pip", command=upgrade_pip)
pip_upgrade_button.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
upgrade_pip_button = pip_upgrade_button  # 别名，用于后续禁用/启用

package_label = ttk.Label(framea, text="Enter Package Name:")
package_label.grid(row=1, column=0, pady=10, padx=10, sticky="e")

package_entry = ttk.Entry(framea, width=40)
package_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")

install_button = ttk.Button(framea, text="Install Package", command=install_package)
install_button.grid(row=2, column=0, columnspan=3, pady=10, padx=10)

uninstall_button = ttk.Button(framea, text="Uninstall Package", command=uninstall_package)
uninstall_button.grid(row=3, column=0, columnspan=3, pady=10, padx=10)

package_status_label = ttk.Label(framea, text="", padding="10")
package_status_label.grid(row=4, column=0, columnspan=3, pady=10, padx=10)

# 主题切换按钮
switch = tk.BooleanVar()  # 创建一个 BooleanVar 变量，用于检测复选框状态
themes = ttk.Checkbutton(root, text="Dark Mode", variable=switch, style="Switch.TCheckbutton", command=switch_theme)
themes.grid(row=1, column=0, pady=10, padx=10, sticky="w")

# 加载保存的主题设置
load_theme()

# 设置 sv_ttk 主题
switch_theme()

# 检查 Python 是否已安装
check_python_installation()

# 运行主循环
root.mainloop()