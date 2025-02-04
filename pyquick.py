import tkinter as tk
from tkinter import ttk, filedialog,messagebox
import subprocess
import os
import threading
import requests
import getpass
import shutil
import re
import time
from save_path import create_folder,sav_path

import sv_ttk
import shlex
import logging
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import functools
from bs4 import BeautifulSoup
config_path=create_folder.get_path("pyquick","1960")
cancel_event = threading.Event()
create_folder.folder_create("pyquick","1960")
def python_version_reload():
    def thread():
        url=f"https://www.python.org/ftp/python/"
        version_reload.config(text="Reloading...",state="disabled")
        try:
            with requests.get(url,verify=False) as r:
                bs = BeautifulSoup(r.content, "lxml")
                results = []
                for i in bs.find_all("a"):
                    if i.text[0].isnumeric():
                        results.append(i.text[:-1])
                if results:
                    version_reload.config(text="Sorting...")
                    
                    sort_results(results)
        except Exception as e:
            logging.error(f"Python Version Reload Wrong:{e}")
    threadings=threading.Thread(target=thread)
    threadings.start()
def python_file_reload():
    r1=r'\S+/'
    def thread():
        ver=version_combobox.get()
        if ver!="":
            url=f"https://www.python.org/ftp/python/{ver}/"
        else:
            return
        with requests.get(url,verify=False) as r:
            bs = BeautifulSoup(r.content, "lxml")
            results = []
            for i in bs.find_all("a"):
                if(re.match(r1,i.text)==None) and(".exe" not in i.text) and("-embed-"not in i.text):
                    results.append(i.text[:-1])
        choose_file_combobox.configure(values=results)
    while True:
        threading.Thread(target=thread).start()
        time.sleep(0.3)
def read_python_list():
    base1=str(sav_path.read_path(config_path,"python_version_list.txt","readline"))
    base2=base1.strip("[]").split(",")
    base3=[]
    for i in base2:
        j=i.strip("'")
        base3.append(j.strip(" '"))
    version_combobox.configure(values=base3)

class Version:
    def __init__(self, version_str: str):
        self.version = version_str.split('.')
        while len(self.version) < 3:
            self.version.append('0')

    def __lt__(self, other):
        for i in range(3):
            if (v1 := int(self.version[i])) < (v2 := int(other.version[i])):
                return True
            elif v1 > v2:
                return False
        else:
            return False
def sort_results(results: list):
    _results = results.copy()
    length = len(_results)
    for i in range(length):
        for ii in range(0, length - i - 1):
            v1 = Version(_results[ii])
            v2 = Version(_results[ii + 1])
            if v1 < v2:
                _results[ii], _results[ii + 1] = _results[ii + 1], _results[ii]
    version_combobox.configure(values=_results)
    sav_path.save_path(config_path,"python_version_list.txt","w",_results)
    version_reload.config(text="Reload",state="normal")

def check_python_installation(delay=3000):
    """
    检查Python3是否已安装。
    
    本函数尝试执行'python3 --version'命令来检查Python3的安装情况。
    如果命令执行出错，说明Python3未安装，则更新界面标签并禁用相关按钮。
    """
    try:
        # 执行命令并获取输出
        version_output = subprocess.check_output(["python3", "--version"], stderr=subprocess.STDOUT, text=True)
        
        # 验证输出是否包含预期的Python版本信息
        if "Python 3" not in version_output:
            raise ValueError("Unexpected Python version output: " + version_output.strip())
    except subprocess.CalledProcessError:
        # 如果命令执行失败，说明Python3未安装
        status_label.config(text="Python3 is not installed.")
        pip_upgrade_button.config(state="disabled")
        install_button.config(state="disabled")
        uninstall_button.config(state="disabled")
        
        # 延时指定时间后清除当前状态标签的文本
        root.after(delay, clear_a)
    except ValueError as e:
        # 处理其他异常，例如版本输出不符合预期
        status_label.config(text=str(e))
        root.after(delay, clear_a)

def clear_a():
    status_label.config(text="")
    package_label.config(text="")
def select_destination():
    destination_path = filedialog.askdirectory()
    if destination_path:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, destination_path)


    
def download_chunk(url, start, end, destination, chunk_size=1024 * 100):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Range': f'bytes={start}-{end}'
    }
    
    response = requests.get(url, headers=headers, stream=True)
    with open(destination, "r+b") as file:
        file.seek(start)
        for data in response.iter_content(chunk_size=chunk_size):
            file.write(data)
            yield len(data)

def download_file(destination_path, num_threads=8):
    global executor
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    filename=choose_file_combobox.get()
    ver=version_combobox.get()
    url = f"https://www.python.org/ftp/python/{ver}/{filename}/"
    file_name = url.split("/")[-1]
    destination = os.path.join(destination_path, file_name)
    if os.path.exists(destination):
        os.remove(destination)
    download_button.config(state="disabled")
    for attempt in range(3):
        try:
            response = requests.head(url, headers=headers)
            response.raise_for_status()
            file_size = int(response.headers.get('content-length', 0))
            chunk_size = file_size // num_threads
            with open(destination, "wb") as file:
                file.truncate(file_size)
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for i in range(num_threads):
                    start = i * chunk_size
                    end = start + chunk_size - 1 if i < num_threads - 1 else file_size - 1
                    futures.append(executor.submit(download_chunk, url, start, end, destination, chunk_size))

                downloaded = 0
                for future in as_completed(futures):
                    for chunk_size in future.result():
                        downloaded += chunk_size
                        percentage = (downloaded / file_size) * 100
                        downloaded_mb = downloaded / (1024 * 1024)
                        status_label.config(
                            text=f"Downloading: {percentage:.3f}% | {downloaded_mb:.3f} MB | {file_size / (1024 * 1024):.3f} MB ｜ ")
                        status_label.update()
                        download_pb["value"] = percentage
                        download_pb.update()

            status_label.config(text="Download Complete!")
            root.after(3000, clear_a)
            cancel_download_button.config(state="disabled")
            download_button.config(state="normal")
            break
        except Exception as e:
            status_label.config(text=f"Download Failed: {str(e)}. Retrying...")
            time.sleep(2)
    else:
        status_label.config(text="Download Failed after 3 attempts.")
        root.after(3000, clear_a)
        cancel_download_button.config(state="disabled")
        download_button.config(state="normal")

def cancel_download():
    global executor
    cancel_event.set()
    executor.shutdown(wait=False)
    status_label.config(text="Cancelling download...")
    download_pb['value'] = 0  # 重置进度条

    destination_path = destination_entry.get()
    filename=choose_file_combobox.get()
    file_name = filename
    destination = os.path.join(destination_path, file_name)

    if os.path.exists(destination):
        os.remove(destination)
        status_label.config(text="Download cancelled and incomplete file removed.")
        download_button.config(state="normal")
    else:
        status_label.config(text="Download cancelled.")
        download_button.config(state="normal")
    root.after(3000, clear_a)


def download_selected_version():
    destination_path = destination_entry.get()
    num_threads = int(threads_entry.get())

    if not os.path.exists(destination_path):
        status_label.config(text="Invalid path!")
        root.after(2000, clear_a)
        return

    cancel_event.clear()
    cancel_download_button.config(state="enabled")
    down_thread = threading.Thread(target=download_file, args=(destination_path, num_threads), daemon=True)
    down_thread.start()

def disabled_pip():
    install_button.config(state="disabled")
    pip_upgrade_button.config(state="disabled")
    uninstall_button.config(state="disabled")
    package_entry.config(state="disabled")
def return_pip():
    install_button.config(state="normal")
    pip_upgrade_button.config(state="normal")
    uninstall_button.config(state="normal")
    package_entry.config(state="normal")
def get_current_pip_version():
    try:
        result = subprocess.check_output(["python3", "-m", "pip", "--version"])
        version_str = result.decode().strip().split()[1]
        return version_str
    except Exception as e:
        logging.error(f"Error getting pip version: {e}")
        return "Unknown"
def get_latest_pip_version():
    try:
        response = requests.get("https://pypi.org/pypi/pip/json", verify=False)
        data = response.json()
        version_str = data["info"]["version"]
        return version_str
    except Exception as e:
        logging.error(f"Error getting latest pip version: {e}")
        return "Unknown"
def upgrade_pip():
    
    def upgrade_pip_thread():
        try:
            disabled_pip()
            current_version = get_current_pip_version()
            latest_version = get_latest_pip_version()
            if current_version == "Unknown" or latest_version == "Unknown":
                if current_version == "Unknown":
                    package_label.config(text="Error getting current pip version.")
                if latest_version == "Unknown":
                    package_label.config(text="Error getting latest pip version.")
            if current_version == latest_version:
                package_label.config(text=f"Pip is already up-to-date (v{current_version}).")
            else:
                package_label.config(text=f"Upgrading pip from v{current_version} to v{latest_version}...")
                try:
                    subprocess.run(["python3", "-m", "pip", "install", "--upgrade", "pip", "--break-system-packages"], stderr=subprocess.STDOUT, text=True,capture_output=True,shell=True)
                    package_label.config(text=f"Pip has been upgraded to v{latest_version}.")
                except subprocess.CalledProcessError as e:
                    package_label.config(text=f"Error upgrading pip: {e.output}")
        except Exception as e:
            logging.error(f"Error upgrading pip: {e}")
            package_label.config(text=f"Error upgrading pip: {str(e)}")
        return_pip()
        root.after(3000, clear_a)
    upgrade_thread = threading.Thread(target=upgrade_pip_thread, daemon=True)
    upgrade_thread.start()

    

        
#try_update(["python3","-m","pip3", "install", "--upgrade", "pip", "--break-system-packages"])


def install_package():
    def clear_status_label():
        root.after(3000, clear_a)
    package_name = package_entry.get()
    def install_package_thread():
        disabled_pip()
        try:
            installed_packages = subprocess.check_output(["python3", "-m", "pip", "list", "--format=columns"], text=True)
            if package_name.lower() in installed_packages.lower():
                package_label.config(text=f"Package '{package_name}' is already installed.")
            else:
                result = subprocess.run(["python3", "-m", "pip", "install", package_name], capture_output=True, text=True)
                if "Successfully installed" in result.stdout:
                    package_label.config(text=f"Package '{package_name}' has been installed successfully!")
                else:
                    package_label.config(text=f"Error installing package '{package_name}': {result.stderr}")
        except subprocess.CalledProcessError as e:
            status_label.config(text=f"Error running pip command: {e.output}")
        except Exception as e:
            status_label.config(text=f"Error installing package '{package_name}': {str(e)}")
        return_pip()
        clear_status_label()
    install_thread = threading.Thread(target=install_package_thread, daemon=True)
    install_thread.start()
def uninstall_package():
    package_name = package_entry.get()
    def uninstall_package_thread():
        disabled_pip()
        try:
            installed_packages = subprocess.check_output(["python3", "-m", "pip", "list", "--format=columns"], text=True)
            if package_name.lower() in installed_packages.lower():
                result = subprocess.run(["python3", "-m", "pip", "uninstall", "-y", package_name], capture_output=True, text=True)
                if "Successfully uninstalled" in result.stdout:
                    package_label.config(text=f"Package '{package_name}' has been uninstalled successfully!")
                    root.after(3000,clear_a)
                else:
                    package_label.config(text=f"Cannot uninstall package '{package_name}': {result.stderr}")
                    root.after(3000,clear_a)
            else:
                package_label.config(text=f"Package '{package_name}' is not installed.")
                root.after(3000,clear_a)
        except Exception as e:
            package_label.config(text=f"Error uninstalling package '{package_name}': {str(e)}")
            root.after(3000,clear_a)
        return_pip()
    uninstall_thread = threading.Thread(target=uninstall_package_thread, daemon=True)
    uninstall_thread.start()





def show_about():
    time_lim=(datetime.datetime(2025,5,2)-datetime.datetime.now()).days
    if (datetime.datetime.now()>=datetime.datetime(2025,3,1)):
        messagebox.showwarning("About", f"Version: dev\nBuild: 1960\n{time_lim} days left.")
    else:
        messagebox.showinfo("About", f"Version: dev\nBuild: 1960\n{time_lim} days left.")

    
    
#GUI
if __name__ == "__main__":
    #启动laugh = True
    if(datetime.datetime.now()>=datetime.datetime(2025,3,13)):
        messagebox.showerror("Error","You can not open python_tool:exitcode(0x1)")
        exit(1)
    elif(datetime.datetime.now()>=datetime.datetime(2025,3,1)):
        messagebox.showwarning("up","Will cannot open on 2025,5.2")
    
    root = tk.Tk()
    root.title("Pyquick")
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    help_menu = tk.Menu(menu_bar, tearoff=0)
    settings_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_command(label="Settings")
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=show_about)
    help_menu.add_separator()

    #TAB CONTROL
    tab_control = ttk.Notebook(root)
    #MODE TAB
    fmode = ttk.Frame(root, padding="20")
    tab_control.add(fmode,text="Python Download")
    tab_control.grid(row=0, padx=10, pady=10)

    fsettings=ttk.Frame(root,padding="20")
    tab_control.add(fsettings,text="Pip")
    tab_control.grid(row=0, padx=10, pady=10)

    framea_tab = ttk.Frame(fmode)
    framea_tab.pack(padx=20, pady=20)

    settings_tab=ttk.Frame(fsettings)
    settings_tab.pack(padx=20, pady=20)


    #PYTHON VERSION
    version_label = ttk.Label(framea_tab, text="Select Python Version:")
    version_label.grid(row=0, column=0, pady=10, padx=10)


    selected_version = tk.StringVar()
    version_combobox = ttk.Combobox(framea_tab, textvariable=selected_version, values=[], state="read")
    version_combobox.grid(row=0, column=1, pady=10, padx=10)
    version_reload=ttk.Button(framea_tab,text="Reload",command=python_version_reload)
    version_reload.grid(row=0,column=2,pady=10, padx=10)


    
    

    destination_label = ttk.Label(framea_tab, text="Select Destination:")
    destination_label.grid(row=1, column=0, pady=10, padx=10)

    destination_entry = ttk.Entry(framea_tab, width=50)
    destination_entry.grid(row=1, column=1, pady=10, padx=10)

    select_button = ttk.Button(framea_tab, text="Select", command=select_destination)
    select_button.grid(row=1, column=2, pady=10,padx=10)

    threads_label = ttk.Label(framea_tab, text="Number of Threads:")
    threads_label.grid(row=2, column=0, pady=10, padx=10)

    threads = tk.IntVar()
    threads_entry = ttk.Combobox(framea_tab, width=10,textvariable=threads,values=[str(i) for i in range(1, 129)],state="readonly")
    threads_entry.grid(row=2, column=1, pady=10, padx=10)
    threads_entry.current(7)

    choose_label=ttk.Label(framea_tab,text="Choose a File:")
    choose_label.grid(row=3,column=0,pady=10,padx=10)
    choose_file=tk.StringVar()
    choose_file_combobox=ttk.Combobox(framea_tab,textvariable=choose_file,values=[],state="readonly",width=50)
    choose_file_combobox.grid(row=3,column=1,columnspan=3,pady=10,padx=10)
    #DOWNLOAD
    download_button = ttk.Button(framea_tab, text="Download Selected Version", command=download_selected_version)
    download_button.grid(row=4, column=0, columnspan=5, pady=10, padx=10)

    cancel_download_button = ttk.Button(framea_tab, text="Cancel Download", command=cancel_download, state="disabled")
    cancel_download_button.grid(row=5, column=0, columnspan=3, pady=10, padx=10)

    
    download_pb=ttk.Progressbar(framea_tab,length=500,mode="determinate")
    download_pb.grid(row=6,column=0,pady=10,columnspan=3, padx=10)
    
    status_label = ttk.Label(framea_tab, text="", padding="10")
    status_label.grid(row=7, column=0, columnspan=3, pady=10, padx=10)

    #PIP(UPDRADE)
    pip_upgrade_button = ttk.Button(settings_tab, text="Upgrade pip",command=upgrade_pip)
    pip_upgrade_button.grid(row=0, column=0, columnspan=3, pady=20, padx=20)

    upgrade_pip_button = pip_upgrade_button  # Alias for disabling/enabling later
    package_label = ttk.Label(settings_tab, text="Enter Package Name:")
    package_label.grid(row=1, column=0, pady=20, padx=20)

    package_entry = ttk.Entry(settings_tab, width=60)
    package_entry.grid(row=1, column=1, pady=20, padx=20)

    #PIP(INSTALL)
    install_button = ttk.Button(settings_tab, text="Install Package", command=install_package)
    install_button.grid(row=2, column=0, columnspan=3, pady=20, padx=20)

    #PIP(UNINSTALL)
    uninstall_button = ttk.Button(settings_tab, text="Uninstall Package", command=uninstall_package)
    uninstall_button.grid(row=3, column=0, columnspan=3, pady=20, padx=20)

    #progressbar-options:length(number),mode(determinate(从左到右)，indeterminate(来回滚动)),...length=500,mode="indeterminate"
    package_label = ttk.Label(settings_tab, text="", padding="10")
    package_label.grid(row=7, column=0, columnspan=3, pady=20, padx=20)
    
    

    # Set sv_ttk theme
    threading.Thread(target=python_file_reload, daemon=True).start()
    check_python_installation()
    threading.Thread(target=read_python_list, daemon=True).start()
    sv_ttk.set_theme("dark")
    root.resizable(False,False)
    root.mainloop()
    #root.after(3000,)