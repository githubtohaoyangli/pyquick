"""
这里对pip进行大改
"""
import datetime
import logging
import os
import re
import sys
import subprocess
import threading
import time
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk, filedialog, messagebox
import ssl
import requests
import sv_ttk
import urllib3
from bs4 import BeautifulSoup
import urllib3
import platform
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def allow_thread():
    def thread():
        with open(os.path.join(config_path, "allowthread.txt"), "r") as r:
            aa=r.readlines()[-1].strip("\n")
            if aa=="True":
                thread_label.grid(row=2, column=0, pady=10,padx=10, sticky="e")
                thread_combobox.grid(row=2, column=1, pady=10, padx=10, sticky="w")
            else:
                thread_label.grid_forget()
                thread_combobox.grid_forget()
    while True:
        threading.Thread(target=thread, daemon=True).start()
        time.sleep(0.3)

def settings():
    global select_python_version_combobox, python_download_mirror, allow_thread_combobox, switch, themes, python_version
    import sv_ttk
    def switch_theme():
        """切换主题"""
        if build>22000:
            if switch.get():
                sv_ttk.set_theme("dark")
                save_theme("dark")
            else:
                sv_ttk.set_theme("light")
                save_theme("light")

    def load_theme():
        """加载主题设置"""
        if build>22000:
            try:
                with open(os.path.join(config_path, "theme.txt"), "r") as r:
                    theme = r.read()
                if theme == "dark":
                    switch.set(True)
                    sv_ttk.set_theme("dark")
                elif theme == "light":
                    switch.set(False)
                    sv_ttk.set_theme("light")
            except:
                sv_ttk.set_theme("light")
    def save_settings():
        def save_thread():
            try:
                with open(os.path.join(config_path, "pythonmirror.txt"), "a") as b:
                    if python_download_mirror.get()!="" or python_download_mirror.get()!=None:
                        b.write(python_download_mirror.get())
                        b.write("\n")
                with open(os.path.join(config_path, "allowthread.txt"), "a") as c:
                    c.write(allow_thread_combobox.get())
                    c.write("\n")
                with open(os.path.join(config_path, "pythonversion.txt"), "a") as d:
                    d.write(select_python_version_combobox.get())
                    d.write("\n")
            except:
                pass
        while True:
            a=threading.Thread(target=save_thread,daemon=True)
            a.start()
            a.join()
            time.sleep(0.2)
    def read_pythonmirror():
        if os.path.exists(os.path.join(config_path, "pythonmirror.txt")):
            with open(os.path.join(config_path, "pythonmirror.txt"), "r") as r:
                aa=r.readlines()
                if len(aa)>0:
                    b=aa[len(aa)-1].strip("\n")
                    for i in range(len(PYTHON_MIRRORS)):
                        if b==PYTHON_MIRRORS[i]:
                            return i
                else:
                    return 0
        else:
            return 0
    def read_allowthread():
        if os.path.exists(os.path.join(config_path, "allowthread.txt")):
            with open(os.path.join(config_path, "allowthread.txt"), "r") as r:
                aa=r.readlines()[-1].strip("\n")
                if aa=="True":
                    return 0
                else:
                    return 1
        else:
            return 1
    def read_py_ver():
        if os.path.exists(os.path.join(config_path, "pythonversion.txt")):
            with open(os.path.join(config_path, "pythonversion.txt"), "r") as r:
                aa=r.readlines()[-1].strip("\n")
                if aa in python_version:
                    for i in range(len(python_version)):
                        if python_version[i]==aa:
                            return i
                else: 
                    return 
        else:
            return
    w=tk.Toplevel(root)
    w.title("Settings")
    w.resizable(False, False)
    icon_path = os.path.join(MY_PATH, 'pyquick.ico')
    if os.path.exists(icon_path):
        w.iconbitmap(icon_path)
    tab_base=ttk.Notebook(w)

    theme_frame = ttk.Frame(tab_base, padding="10")
    python_downlod_frame = ttk.Frame(tab_base, padding="10")
    pip_se_frame = ttk.Frame(tab_base, padding="10")
    tab_base.add(theme_frame, text="Switch Theme")
    tab_base.add(python_downlod_frame, text="Python Download Settings")
    tab_base.add(pip_se_frame, text="Pip Settings")
    tab_base.grid(padx=10, pady=10, row=0, column=0)

    if build>22000:
        switch = tk.BooleanVar()
        themes = ttk.Checkbutton(theme_frame, text="Dark Mode", variable=switch, style="Switch.TCheckbutton", command=switch_theme)
        themes.grid(row=0, column=0, pady=10, padx=10, sticky="w")
    if build<22000:
        warnings=ttk.Label(theme_frame,text="Unless you upgrade to Windows 11(21H2 or later), you can not switch your theme.",foreground="red")
        warnings.grid(row=0, column=0, pady=10, padx=10, sticky="w")
    python_download_key_label = ttk.Label(python_downlod_frame, text="Choose Python Download Mirror:")
    python_download_key_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")

    python_download_mirror=ttk.Combobox(python_downlod_frame,values=PYTHON_MIRRORS)
    python_download_mirror.grid(row=0, column=1, pady=10, padx=10, sticky="w")
    python_download_mirror.current(read_pythonmirror())

    allow_thread_label=ttk.Label(python_downlod_frame,text="Allow Threads During Download:")
    allow_thread_label.grid(row=1, column=0, pady=10, padx=10, sticky="e")

    allow_thread_combobox=ttk.Combobox(python_downlod_frame,values=["True","False"],state="readonly")
    allow_thread_combobox.grid(row=1, column=1, pady=10, padx=10, sticky="w")
    allow_thread_combobox.current(read_allowthread())

    select_python_version_label = ttk.Label(pip_se_frame, text="Select Python Version:")
    select_python_version_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")

    python_version=get_python_version()
    select_python_version_combobox=ttk.Combobox(pip_se_frame,values=python_version,state="readonly")
    select_python_version_combobox.grid(row=0, column=1, pady=10, padx=10, sticky="w")
    select_python_version_combobox.current(read_py_ver())

    if build>22000:
        load_theme()
    threading .Thread(target=save_settings, daemon=True).start()
    w.mainloop()


def on_closing():
    def cancel_download():
        """取消正在进行的下载"""
        global is_downloading
        global canneled
        is_downloading = False
        if executor:
            cancel_button.config(state="disabled")
            download_button.config(state="normal")  # 禁用取消下载按钮
            progress_bar['value'] = 0
            def cancel_threads():
                executor.shutdown(wait=False)   
            canneled=1
            time.sleep(0.1)
            def remove_file():
                os.remove(destination)
            while True:
                try:
                    for i in range(100):
                        cancel_threads()
                    remove_file()
                except FileNotFoundError:
                    break
                except Exception as e:
                    pass
    try:
        if is_downloading:
            messagebox.askokcancel("Exit", "Do you want to quit?")
            cancel_download()
        root.destroy()
        sys.exit(0)
    except:
        os.system("taskkill /IM python.exe /F")
        os.system("taskkill /IM python_tool.exe /F")
        os.system("taskkill /IM pyquick.exe /F")
        os.system("taskkill /IM pythonw.exe /F")


def get_system_build():
    """获取系统版本"""
    system_build=int(str(platform.platform().split("-")[2]).split(".")[2])
    return system_build
build=get_system_build()
#print(build)查看系统build版本是否达标，如果不是Windows11(build>=22000)则无sv_ttk使用权，只能使用ttk 
PYTHON_MIRRORS=[
    "python.org",
    "mirrors.huaweicloud.com"
]
ssl.create_default_context=ssl._create_unverified_context()
# 禁用 SSL 警告
urllib3.disable_warnings()
# 获取当前工作目录
MY_PATH = os.getcwd()
aa=os.path.join(MY_PATH,os.path.basename(__file__))
bb=os.path.basename(__file__).split(".")[0]
py="py"
exe="exe"
pyd="pyd"
pyc="pyc"
if (os.path.exists(os.path.join(MY_PATH,bb+"."+py))) or (os.path.exists(os.path.join(MY_PATH,bb+"."+pyd))) or (os.path.exists(os.path.join(MY_PATH,bb+"."+pyc))):
    version_pyquick="1957_code"
elif (os.path.exists(os.path.join(MY_PATH,bb+exe))):
    version_pyquick="1957"
# 获取用户配置目录
config_path_base = os.path.join(os.environ["APPDATA"], f"pyquick")
config_path=os.path.join(config_path_base,version_pyquick)
if not os.path.exists(os.path.join(config_path,"pythonmirror.txt")):
    with open(os.path.join(config_path,"pythonmirror.txt"),"w") as f:
        pass
if not os.path.exists(os.path.join(config_path,"pipmirror.txt")):
    with open(os.path.join(config_path,"pipmirror.txt"),"w") as f:
        pass

# 如果保存目录不存在，则创建它
if not os.path.exists(config_path):
    os.makedirs(config_path)
if not os.path.exists(os.path.join(config_path, "path.txt")):
    with open(os.path.join(config_path, "path.txt"), "a"):
        pass
if not os.path.exists(os.path.join(config_path, "allowthread.txt")):
    with open(os.path.join(config_path, "allowthread.txt"), "a")as fw:
        fw.write("False")
if not os.path.exists(os.path.join(config_path, "pipmirror.txt")):
    pipmirror=subprocess.run(["pip","config","get","global.index-url"],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW)
    with open(os.path.join(config_path, "pipmirror.txt"), "a")as fw:
        fw.write(pipmirror.stdout.strip("\n"))
with open(os.path.join(config_path, "path.txt"),"r") as f:
    """
    pathed:已有的路径
    """
    #print(os.path.join(config_path_base, "path.txt"))
    pathed=[]
    a=f.readlines()
    for i in a:
        pathed.append(i.strip("\n"))
    writable=True
    
    for j in pathed:
        if str(j)==str(os.path.join(MY_PATH,os.path.basename(__file__))):
            writable=False
            break
    if writable:
        
        if os.path.exists(aa):
            with open(os.path.join(config_path_base, "path.txt"), "a") as f:
                f.write(os.path.join(MY_PATH,os.path.basename(__file__)))
                f.write("\n")
        elif(os.path.exists(os.path.join(MY_PATH,bb+"."+py))):
            with open(os.path.join(config_path_base, "path.txt"), "a") as f:
                f.write(os.path.join(MY_PATH,bb+py))
                f.write("\n")
        elif(os.path.exists(os.path.join(MY_PATH,bb+"."+exe))):
            with open(os.path.join(config_path_base, "path.txt"), "a") as f:
                f.write(os.path.join(MY_PATH,bb+exe))
                f.write("\n")
        elif(os.path.exists(os.path.join(MY_PATH,bb+"."+pyd))):
            with open(os.path.join(config_path_base, "path.txt"), "a") as f:
                f.write(os.path.join(MY_PATH,bb+pyd))
                f.write("\n")
        elif(os.path.exists(os.path.join(MY_PATH,bb+"."+pyc))):
            with open(os.path.join(config_path_base, "path.txt"), "a") as f:
                f.write(os.path.join(MY_PATH,bb+pyc))
                f.write("\n")
        



def show_about():
    """显示关于对话框"""
    if datetime.datetime.now() >= datetime.datetime(2025, 2, 4):
        time_lim = (datetime.datetime(2025, 4, 13) - datetime.datetime.now()).days
        messagebox.showwarning("About",
                               f"Version: Pyquick Magic dev\nBuild: 1957.1000\nExpiration time:2025/4/13\n only {time_lim} days left.")
    else:
        time_lim = (datetime.datetime(2025, 4, 13) - datetime.datetime.now()).days
        messagebox.showinfo("About", f"Version: Pyquick Magic dev\nBuild: 1957.1000\nExpiration time:2025/4/13\n{time_lim} days left.")


# 全局变量
file_size = 0
executor: ThreadPoolExecutor
futures = []
lock = threading.Lock()
downloaded_bytes = [0]
is_downloading = False


def clear():
    """清除状态标签和包标签的文本"""
    status_label.config(text="")
    package_status_label.config(text="")
    package_label.config(text="Enter Package Name:")
    progress_bar['value']=0


def select_destination():
    """选择目标路径"""
    destination_path = filedialog.askdirectory()
    if destination_path:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, destination_path)


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


# 排序版本获取结果
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
    with open(os.path.join(config_path, "version.txt"), "w") as f:
        f.write(str(_results))
def read_python_version():
    try:
        with open(os.path.join(config_path, "version.txt"), "r") as f:
            version1=f.read().strip("[").strip("]").split(",")
            #print(version1)
            version2=[]
            for i in version1:
                version2.append(i.strip("'").strip(" ").strip("'"))
            version_combobox.configure(values=version2)
    except FileNotFoundError:
        pass
def python_dowload_url_reload(url):
    """
    懒得改了
    """
    try:
        r1=r'amd64[a-z]\d+/'
        r3=r'win32[a-z]\d+/'
        r2=r'arm64[a-z]\d+/'
        r4=r'amd64/'
        r5=r'win32/'
        r6=r'arm64/'
        r7=r'amd64[a-z][a-z]\d+/'
        r8=r'win32[a-z][a-z]\d+/'
        r9=r'arm64[a-z][a-z]\d+/'
        r10=r'[a-z]+/'#最有用
        r11=r'\S+/'
        if url!= "https://www.python.org/ftp/python/":
            with requests.get(url,verify=False) as r:
                bs = BeautifulSoup(r.content, "lxml")
                results = []
                for i in bs.find_all("a"):
                    if (i.text != "../" )and(i.text!="previous/")and(re.match(r11,i.text)==None) and(re.match(r10,i.text)==None)and(i.text!="rpms/")and (re.match(r1,i.text)==None)  and (re.match(r2,i.text)==None) and (re.match(r3,i.text)==None)  and (re.match(r4,i.text)==None) and (re.match(r5,i.text)==None)and (re.match(r6,i.text)==None) and ("macos"not in i.text) and (re.match(r7,i.text)==None)  and (re.match(r8,i.text)==None) and (re.match(r9,i.text)==None) and ("mac" not in i.text) and ("Mac" not in i.text) and ("MacOS" not in i.text):
                        results.append(i.text)
                if results:
                    if results:
                        return results
    except Exception as e:
        logging.error(f"Python filename Reload Wrong:{e}")

# 获取可下载版本列表
def python_version_reload():
    def python_version_reload_thread():
        version_reload_button.configure(state="disabled", text="Reloading...")
        root.update()
        url="https://www.python.org/ftp/python/"
        try:
            
            with requests.get(url,verify=False) as r:
                bs = BeautifulSoup(r.content, "lxml")
                results = []
                for i in bs.find_all("a"):
                    if i.text[0].isnumeric():
                        results.append(i.text[:-1])
                if results:
                    version_reload_button.configure(text="Sorting...")
                    sort_results(results)
        except Exception as e:
            logging.error(f"Python Version Reload Wrong:{e}")
        if is_downloading:
            version_reload_button.configure(state="disabled", text="Reload")
        else:
            version_reload_button.configure(state="normal", text="Reload")
        root.update()
    a=threading.Thread(target=python_version_reload_thread, daemon=True)
    a.start()
    


def validate_version(version):
    """
    验证版本号格式是否符合预期的格式

    此函数通过正则表达式检查传入的版本号是否符合 major.minor.patch 的格式，
    其中 major、minor 和 patch 都是数字

    参数:
    version (str): 需要验证的版本号字符串

    返回:
    bool: 如果版本号符合预期格式，则返回 True，否则返回 False
    """
    # 定义版本号的正则表达式模式，确保版本号是 major.minor.patch 的格式
    pattern = r'^\d+\.\d+\.\d+$'
    patten2=r'^\d+\.\d+$'
    # 使用正则表达式匹配版本号，返回匹配结果的布尔值
    if re.match(patten2,version):
        return True
    return bool(re.match(pattern, version))


def validate_path(path):
    """
    验证路径是否存在

    参数:
    path (str): 需要验证的路径

    返回:
    bool: 如果路径存在返回True，否则返回False
    """
    return os.path.isdir(path)


def download_chunk(url, start_byte, end_byte, destination, retries=3):
    """
    下载文件的指定部分

    :param url: 文件的URL
    :param start_byte: 开始下载的字节位置
    :param end_byte: 结束下载的字节位置
    :param destination: 文件保存的目标路径
    :param retries: 最大重试次数,默认为3次
    :return: 如果下载成功返回True,否则返回False
    """
    global is_downloading
    # 构造请求头，指定下载的字节范围
    headers = {'Range': f'bytes={start_byte}-{end_byte}'}
    attempt = 0
    # 尝试下载文件，如果失败则重试
    while attempt < retries:
        try:
            # 发起HTTP请求，包含自定义请求头，启用流式响应，设置超时
            response = requests.get(url, headers=headers, stream=True, timeout=10,verify=False)
            # 检查响应状态码，如果状态码表示错误，则抛出异常
            response.raise_for_status()
            # 使用文件锁确保并发安全，打开文件准备写入
            with lock:
                with open(destination, 'r+b') as f:
                    f.seek(start_byte)
                    # 遍历响应内容，写入到文件中
                    for chunk in response.iter_content(chunk_size=8192):
                        if not is_downloading:
                            return False
                        f.write(chunk)
                        downloaded_bytes[0] += len(chunk)
            return True
        except requests.RequestException as e:
            # 如果发生网络请求异常，更新状态标签并重试
            with lock:
                if canneled!=1:
                    status_label.config(text=f"Download Failed! Retrying... ({attempt + 1}/{retries})")
            attempt += 1
    # 如果重试次数用尽仍然失败，更新状态标签并设置下载状态为False
    with lock:
        status_label.config(text=f"Download Failed! Error: {e}")
        is_downloading = False
    return False
def show_name():
    def show_name_thread():
        select_version=version_combobox.get()
        url=f"https://www.python.org/ftp/python/{select_version}"
        __result=python_dowload_url_reload(url)
        download_file_combobox.configure(values=__result)
    while True:
        a=threading.Thread(target=show_name_thread, daemon=True)
        a.start()
        a.join()
        time.sleep(0.3)

def return_normal():
    with open(os.path.join(config_path,"allowthread.txt"),"r") as f:
        allowthread=f.readlines()[-1].strip("\n")
        if allowthread=="False":
            thread_label.grid_forget()
            thread_combobox.grid_forget()
        else:
            thread_combobox.config(state="normal")
    download_button.config(state="normal")
    version_reload_button.config(state="normal")
    version_combobox.config(state="normal")
    destination_entry.config(state="normal")
    
    download_file_combobox.config(state="normal")
    select_button.config(state="normal")
    cancel_button.grid_forget()
    progress_bar.stop()
    progress_bar.config(mode="determinate")
    progress_bar['value']=0
    progress_bar['maximum']=100
    root.after(5000, clear)
# 定义下载指定版本Python安装程序的函数
def download_file(selected_version, destination_path, num_threads):
    """下载指定版本的Python安装程序"""
    progress_bar.config(mode="indeterminate")
    progress_bar.start(10)
    cancel_button.grid(row=5, column=0, columnspan=3, pady=10, padx=5)
    cancel_button.config(state="disabled")
    
    global file_size, executor, futures, downloaded_bytes, is_downloading, destination
    # 验证版本号是否有效
    if not validate_version(selected_version):
        status_label.config(text="Invalid version number")
        return_normal()
        return

    # 验证目标路径是否有效
    if not validate_path(destination_path):
        status_label.config(text="Invalid destination path")
        return_normal()
        return

    # 构造文件名和目标路径
    file_name = download_file_combobox.get()
    destination = os.path.join(destination_path, file_name)

    # 如果目标文件已存在，尝试删除它
    if os.path.exists(destination):
        try:
            os.remove(destination)
        except (PermissionError, FileNotFoundError) as e:
            status_label.config(text=f"Failed to remove existing file: {str(e)}")
            return_normal()
            return

    # 构造下载URL
    url = f"https://www.python.org/ftp/python/{selected_version}/{file_name}"

    # 获取文件大小
    try:
        response = requests.head(url, timeout=10,verify=False)
        response.raise_for_status()
        file_size = int(response.headers['Content-Length'])
    except requests.RequestException as e:
        status_label.config(text=f"Failed to get file size: {str(e)}")
        return_normal()
        return

    # 尝试创建目标文件
    try:
        with open(destination, 'wb') as f:
            pass
    except IOError as e:
        status_label.config(text=f"Failed to create file: {str(e)}")
        return_normal()
        return

    # 计算每个线程下载的数据块大小
    chunk_size = file_size // num_threads
    futures = []
    downloaded_bytes = [0]
    is_downloading = True
    # 使用线程池执行下载任务
    executor = ThreadPoolExecutor(max_workers=num_threads)
    for i in range(num_threads):
        start_byte = i * chunk_size
        end_byte = start_byte + chunk_size - 1 if i != num_threads - 1 else file_size - 1

        def start():
            futures.append(executor.submit(download_chunk, url, start_byte, end_byte, destination))

        b=threading.Thread(target=start, daemon=True)
        b.start()
        b.join()
    time.sleep(0.2)
    cancel_button.config(state="normal")
    progress_bar.config(mode="determinate")
    progress_bar['value']=0
    progress_bar['maximum']=100
    # 启动一个线程来更新下载进度
    a=threading.Thread(target=update_progress, daemon=True)
    a.start()
    # 启用取消下载按钮
    


def update_progress():
    """更新进度条和状态标签

    通过计算已下载字节数与总文件大小的比例来更新进度条和状态标签的文本。
    此函数在一个单独的线程中运行，以保持UI响应性。
    """
    global file_size, is_downloading
    
    progress_bar.config(mode="indeterminate")
    progress_bar.start(10)
    # 当有任何一个下载任务未完成时，继续更新进度
    while any(not future.done() for future in futures):
        # 如果下载状态为False，则停止更新进度
        if not is_downloading:
            break
        time.sleep(0.2)
        progress_bar.stop()
        progress_bar.config(mode="determinate")
        progress_bar["maximum"]=100
        progress_bar["value"]=0
        # 计算并更新下载进度的百分比
        progress = int(downloaded_bytes[0] / file_size * 100)
        # 将已下载字节数转换为MB
        downloaded_mb = downloaded_bytes[0] / (1024 * 1024)
        # 将总文件大小转换为MB
        total_mb = file_size / (1024 * 1024)
        # 更新状态标签的文本，显示下载进度和已下载/总文件大小
        status_label.config(text=f"Progress: {progress}% ({downloaded_mb:.2f} MB / {total_mb:.2f} MB)")
        # 更新进度条的值
        progress_bar['value'] = progress
        # 暂停0.1秒，减少UI更新频率
        time.sleep(0.05)
    # 如果下载状态为True，则表示下载已完成
    if is_downloading:
        progress_bar['value']=100
        status_label.config(text="Download Complete!")
        return_normal()
    # 如果下载状态为False，则表示下载已取消
    else:
        status_label.config(text="Download Cancelled!")
        return_normal()
    # 将下载状态设置为False，表示下载已完成或已取消
    is_downloading = False
    # 禁用取消下载按钮，防止用户在下载已完成或已取消的情况下点击按钮
    cancel_button.grid_forget()
    root.after(5000,clear)




def cancel_download():
    """取消正在进行的下载"""
    global is_downloading
    global canneled
    is_downloading = False
    if executor:
        cancel_button.config(state="disabled")
        download_button.config(state="normal")  # 禁用取消下载按钮
        progress_bar['value'] = 0
        def cancel_threads():
            executor.shutdown(wait=False)   
        canneled=1
        time.sleep(0.1)
        def remove_file():
            os.remove(destination)
        while True:
            try:
                for i in range(100):
                    cancel_threads()
                remove_file()
            except FileNotFoundError:
                break
            except Exception as e:
                pass


def download_selected_version():
    """开始下载选定的Python版本"""
    selected_version = version_combobox.get()
    destination_path = destination_entry.get()
    num_threads = int(thread_combobox.get())

    if not os.path.exists(destination_path):
        status_label.config(text="Invalid path!")
        root.after(5000, clear)
        return
    if download_file_combobox.get()==None or download_file_combobox.get()=="":
        status_label.config(text="Please choose a file!")
        root.after(5000,clear)
        return
    with open(os.path.join(config_path,"allowthread.txt"),"r") as f:
        allowthread=f.readlines()[-1].strip("\n")
        if allowthread=="False":
            thread_label.grid_forget()
            thread_combobox.grid_forget()
        else:
            thread_combobox.config(state="disabled")
    download_button.config(state="disabled")
    version_combobox.config(state="disabled")
    select_button.config(state="disabled")
    destination_entry.config(state="disabled")
    
    download_file_combobox.config(state="disabled")
    version_reload_button.config(state="disabled")
    cancel_button.grid(row=5, column=0, columnspan=3, pady=10, padx=5)
    cancel_button.config(state="normal")
    clear()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    threading.Thread(target=download_file, args=(selected_version, destination_path, num_threads), daemon=True).start()

def get_python_version():
    """获取当前Python版本"""
    all_versions=[]
    versions_base=subprocess.run(["where","python"],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    python_version=(versions_base.stdout).decode().split("\n")
    name=r"Python\d+"
    for i in python_version:
        j=i.strip("\r")
        
        python_ver=j.split("\\")
        if len(python_ver)>2:
            ver=python_ver[len(python_ver)-2]
        if re.match(name,ver):
            all_versions.append(f"Pip{ver.strip("Python")}")
    return all_versions



def confirm_cancel_download():
    """确认取消下载"""
    if messagebox.askyesno("Confirm", "Are you sure you want to cancel the download?"):
        threading.Thread(target=cancel_download, daemon=True).start()


def get_pip_version():
    """获取当前pip版本"""
    try:
        with open(os.path.join(os.path.join(config_path,"pythonversion.txt")),"r") as f:
            version_pip=f.read()
    except:
        version_pip=""
    
    if version_pip=="":
        return None
    if "Pip3" in version_pip:
        version="."+version_pip.strip("Pip3")
    if "Pip2" in version_pip:
        version="."+version_pip.strip("Pip2")
    
    try:
        return subprocess.check_output([f'pip3{version}.exe', "--version"],
                                       creationflags=subprocess.CREATE_NO_WINDOW).decode().strip().split()[1]
    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e}")
        return None
    except FileNotFoundError:
        return None
    except Exception:
        return None
    

def get_latest_pip_version():
    """获取最新pip版本"""
    try:
        r = requests.get("https://pypi.org/pypi/pip/json", verify=False)
        return r.json()["info"]["version"]
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None


def update_pip():
    """更新pip到最新版本"""
    try:
        subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"],
                       creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e}")
        return False


def check_pip_version():
    global select_python_version_combobox
    """检查并更新pip版本"""
    pip_upgrade_button.config(state="disabled")
    package_entry.config(state="disabled")
    install_button.config(state="disabled")
    uninstall_button.config(state="disabled")
    upgrade_button.config(state="disabled")
    pip_progress_bar.grid(row=5, column=0, columnspan=3, pady=10, padx=10)
    pip_progress_bar.start(10)
    clear()
    current_version = get_pip_version()
    if current_version is None:
        pip_progress_bar.stop()
        pip_progress_bar.grid_forget()
        package_status_label.config(text="Error: Failed to get current pip version")
        pip_upgrade_button.config(state="normal")
        package_entry.config(state="normal")
        install_button.config(state="normal")
        upgrade_button.config(state="normal")
        uninstall_button.config(state="normal")
        root.after(5000, clear)
        return

    latest_version = get_latest_pip_version()
    if latest_version is None:
        pip_progress_bar.stop()
        pip_progress_bar.grid_forget()
        package_status_label.config(text="Error: Failed to get latest pip version")
        pip_upgrade_button.config(state="normal")
        package_entry.config(state="normal")
        install_button.config(state="normal")
        upgrade_button.config(state="normal")
        uninstall_button.config(state="normal")
        root.after(5000, clear)
        return

    if current_version != latest_version:
        message = f"Current pip version: {current_version}\nLatest pip version: {latest_version}\nUpdating pip..."
        package_status_label.config(text=message)
        if update_pip():
            pip_progress_bar.stop()
            pip_progress_bar.grid_forget()
            package_status_label.config(text=f"pip has been updated! {current_version}-->{latest_version}")
            pip_upgrade_button.config(state="normal")
            package_entry.config(state="normal")
            upgrade_button.config(state="normal")
            install_button.config(state="normal")
            uninstall_button.config(state="normal")
            
            root.after(5000, clear)
        else:
            pip_progress_bar.stop()
            pip_progress_bar.grid_forget()
            package_status_label.config(text="Error: Failed to update pip")
            pip_upgrade_button.config(state="normal")
            package_entry.config(state="normal")
            install_button.config(state="normal")
            upgrade_button.config(state="normal")
            uninstall_button.config(state="normal")
            root.after(5000, clear)
    else:
        pip_progress_bar.stop()
        pip_progress_bar.grid_forget()
        package_status_label.config(text=f"pip is up to date: {current_version}")
        pip_upgrade_button.config(state="normal")
        package_entry.config(state="normal")
        install_button.config(state="normal")
        upgrade_button.config(state="normal")
        uninstall_button.config(state="normal")
        root.after(5000, clear)


def upgrade_pip():
    """启动pip版本检查线程"""
    try:
        pip_upgrade_button.config(state="disabled")
        package_entry.config(state="disabled")
        install_button.config(state="disabled")
        uninstall_button.config(state="disabled")
        upgrade_button.config(state="disabled")
        pip_progress_bar.grid(row=5, column=0, columnspan=3, pady=10, padx=10)
        pip_progress_bar.start(10)
        clear()
        subprocess.check_output(["python", "--version"], creationflags=subprocess.CREATE_NO_WINDOW)
        threading.Thread(target=check_pip_version, daemon=True).start()
    except FileNotFoundError:
        package_status_label.config(text="Python is not installed.")
        root.after(5000, clear)
    except Exception as e:
        package_status_label.config(text=f"Error: {str(e)}")
        pip_upgrade_button.config(state="normal")
        package_entry.config(state="normal")
        upgrade_button.config(state="normal")
        install_button.config(state="normal")
        uninstall_button.config(state="normal")
        pip_progress_bar.stop()
        pip_progress_bar.grid_forget()
        root.after(5000, clear)


def install_package():
    """安装指定的Python包"""
    
    package_name = package_entry.get()
    
    clear()
    install_button.config(state="disabled")
    pip_upgrade_button.config(state="disabled")
    package_entry.config(state="disabled")
    uninstall_button.config(state="disabled")
    upgrade_button.config(state="disabled")
    pip_progress_bar.grid(row=5, column=0, columnspan=3, pady=10, padx=10)
    pip_progress_bar.start(10)
    if "=" in package_name or package_name=="" or package_name==None or " " in package_name:
        pip_progress_bar.stop()
        pip_progress_bar.grid_forget()
        package_status_label.config(text=f"Invalid package name: {package_name}")
        uninstall_button.config(state="normal")
        upgrade_button.config(state="normal")
        pip_upgrade_button.config(state="normal")
        package_entry.config(state="normal")
        install_button.config(state="normal")
        root.after(5000, clear)
        return
    def install_package_thread():
        try:
            #PyQt5_sip12.16.1(14)
            
            
            find_packages=subprocess.run(["python", "-m", "pip", "show",package_name], text=True,capture_output=True,
                                                        creationflags=subprocess.CREATE_NO_WINDOW)
            if f"Name: {package_name}" in find_packages.stdout:
                pip_progress_bar.stop()
                pip_progress_bar.grid_forget()
                package_status_label.config(text=f"Package '{package_name}' is already installed.")
                install_button.config(state="normal")
                pip_upgrade_button.config(state="normal")
                upgrade_button.config(state="normal")
                package_entry.config(state="normal")
                uninstall_button.config(state="normal")
                root.after(5000, clear)
                return
            else:
                result = subprocess.run(["python", "-m", "pip", "install", package_name], capture_output=True,
                                        text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if "Successfully installed" in result.stdout:
                    pip_progress_bar.stop()
                    pip_progress_bar.grid_forget()
                    package_status_label.config(text=f"Package '{package_name}' has been installed successfully!")
                    install_button.config(state="normal")
                    pip_upgrade_button.config(state="normal")
                    upgrade_button.config(state="normal")
                    package_entry.config(state="normal")
                    uninstall_button.config(state="normal")                    
                    root.after(5000, clear)
                elif f"ERROR: No matching distribution found for {package_name}" in result.stderr:
                    pip_progress_bar.stop()
                    pip_progress_bar.grid_forget()
                    package_status_label.config(text=f"{package_name} is not found from the Internet.")
                    install_button.config(state="normal")
                    pip_upgrade_button.config(state="normal")
                    upgrade_button.config(state="normal")
                    package_entry.config(state="normal")
                    uninstall_button.config(state="normal")          
                    root.after(5000, clear)
                elif "Invalid requirement" in result.stderr:
                    pip_progress_bar.stop()
                    pip_progress_bar.grid_forget()
                    package_status_label.config(text=f"Invalid package name: {package_name}")
                    uninstall_button.config(state="normal")
                    upgrade_button.config(state="normal")
                    pip_upgrade_button.config(state="normal")
                    package_entry.config(state="normal")
                    install_button.config(state="normal")
                    root.after(5000, clear)
                else:
                    pip_progress_bar.stop()
                    pip_progress_bar.grid_forget()
                    package_status_label.config(text=f"Error installing package '{package_name}': {result.stderr}")
                    install_button.config(state="normal")
                    pip_upgrade_button.config(state="normal")
                    upgrade_button.config(state="normal")
                    package_entry.config(state="normal")
                    uninstall_button.config(state="normal")
                    root.after(5000, clear)
        except Exception as e:
            pip_progress_bar.stop()
            pip_progress_bar.grid_forget()
            package_status_label.config(text=f"Error installing package '{package_name}': {str(e)}")
            install_button.config(state="normal")
            pip_upgrade_button.config(state="normal")
            upgrade_button.config(state="normal")
            package_entry.config(state="normal")
            uninstall_button.config(state="normal")
            root.after(5000, clear)

    threading.Thread(target=install_package_thread,daemon=True).start()


def uninstall_package():
    """卸载指定的Python包"""
    clear()
    package_name = package_entry.get()
    uninstall_button.config(state="disabled")
    upgrade_button.config(state="disabled")
    pip_upgrade_button.config(state="disabled")
    package_entry.config(state="disabled")
    install_button.config(state="disabled")
    pip_progress_bar.grid(row=5, column=0, columnspan=3, pady=10, padx=10)
    pip_progress_bar.start(10)
    if "=" in package_name  or package_name=="" or package_name==None or " " in package_name:
        pip_progress_bar.stop()
        pip_progress_bar.grid_forget()
        package_status_label.config(text=f"Invalid package name: {package_name}")
        uninstall_button.config(state="normal")
        upgrade_button.config(state="normal")
        pip_upgrade_button.config(state="normal")
        package_entry.config(state="normal")
        install_button.config(state="normal")
        root.after(5000, clear)
        return
    def uninstall_package_thread():
        try:
            find_packages=subprocess.run(["python", "-m", "pip", "show",package_name], text=True,capture_output=True,
                                                        creationflags=subprocess.CREATE_NO_WINDOW)
            if f"WARNING: Package(s) not found: {package_name}"in find_packages.stderr:
                pip_progress_bar.stop()
                pip_progress_bar.grid_forget()
                package_status_label.config(text=f"Package '{package_name}' is not installed.")
                upgrade_button.config(state="normal")
                uninstall_button.config(state="normal")
                pip_upgrade_button.config(state="normal")
                package_entry.config(state="normal")
                install_button.config(state="normal")
                root.after(5000, clear)
                
            else:
                result = subprocess.run(["python", "-m", "pip", "uninstall", "-y", package_name], capture_output=True,
                                        text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                
                if "Successfully uninstalled" in result.stdout:
                    pip_progress_bar.stop()
                    pip_progress_bar.grid_forget()
                    package_status_label.config(text=f"Package '{package_name}' has been uninstalled successfully!")
                    uninstall_button.config(state="normal")
                    upgrade_button.config(state="normal")
                    pip_upgrade_button.config(state="normal")
                    package_entry.config(state="normal")
                    install_button.config(state="normal")
                    root.after(5000, clear) 
                elif "Invalid requirement" in result.stderr:
                    pip_progress_bar.stop()
                    pip_progress_bar.grid_forget()
                    package_status_label.config(text=f"Invalid package name: {package_name}")
                    uninstall_button.config(state="normal")
                    upgrade_button.config(state="normal")
                    pip_upgrade_button.config(state="normal")
                    package_entry.config(state="normal")
                    install_button.config(state="normal")
                    root.after(5000, clear)
                else:
                    pip_progress_bar.stop()
                    pip_progress_bar.grid_forget()
                    package_status_label.config(text=f"Error uninstalling package '{package_name}': {result.stderr}")
                    uninstall_button.config(state="normal")
                    upgrade_button.config(state="normal")
                    pip_upgrade_button.config(state="normal")
                    package_entry.config(state="normal")
                    install_button.config(state="normal")
                    root.after(5000, clear)
                
        except Exception as e:
            pip_progress_bar.stop()
            pip_progress_bar.grid_forget()
            package_status_label.config(text=f"Error uninstalling package '{package_name}': {str(e)}")
            uninstall_button.config(state="normal")
            upgrade_button.config(state="normal")
            pip_upgrade_button.config(state="normal")
            package_entry.config(state="normal")
            install_button.config(state="normal")           
            root.after(5000, clear)
    threading.Thread(target=uninstall_package_thread,daemon=True).start()
def uprade_package():
    """升级指定的Python包"""
    clear()
    
    package_name = package_entry.get()
    upgrade_button.config(state="disabled")
    pip_upgrade_button.config(state="disabled")
    package_entry.config(state="disabled")
    install_button.config(state="disabled")

    uninstall_button.config(state="disabled")
    pip_progress_bar.grid(row=5, column=0, columnspan=3, pady=10, padx=10)
    pip_progress_bar.start(10)
    
    def upgrade_package_thread():
        try:
            find_packages=subprocess.run(["python", "-m", "pip", "show",package_name], text=True,capture_output=True,
                                                        creationflags=subprocess.CREATE_NO_WINDOW)
            if f"WARNING: Package(s) not found: {package_name}"in find_packages.stderr:
                pip_progress_bar.stop()
                pip_progress_bar.grid_forget()
                package_status_label.config(text=f"Package '{package_name}' is not installed.")
                upgrade_button.grid_forget()
                pip_upgrade_button.config(state="normal")
                package_entry.config(state="normal")
                install_button.config(state="normal")
                uninstall_button.config(state="normal")
                root.after(5000, clear)
                return 0
            else:
                result = subprocess.run(["python", "-m", "pip", "install", "--upgrade", package_name], capture_output=True,
                                        text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                
                if "Successfully installed" in result.stdout:
                    
                    pip_progress_bar.stop()
                    pip_progress_bar.grid_forget()
                    package_status_label.config(text=f"Package '{package_name}' has been upgraded successfully!")
                    upgrade_button.grid_forget()
                    pip_upgrade_button.config(state="normal")
                    package_entry.config(state="normal")
                    install_button.config(state="normal")
                    uninstall_button.config(state="normal")
                    root.after(5000, clear) 
                elif f"Requirement already satisfied: {package_name}" in result.stdout:
                    
                    pip_progress_bar.stop()
                    pip_progress_bar.grid_forget()
                    package_status_label.config(text=f"Package '{package_name}' is already up to date.")
                    upgrade_button.grid_forget()
                    pip_upgrade_button.config(state="normal")
                    package_entry.config(state="normal")
                    install_button.config(state="normal")
                    uninstall_button.config(state="normal")
                    root.after(5000, clear) 
                else:
                    
                    pip_progress_bar.stop()
                    pip_progress_bar.grid_forget()
                    package_status_label.config(text=f"Error upgrading package '{package_name}': {result.stderr}")
                    upgrade_button.grid_forget()
                    pip_upgrade_button.config(state="normal")
                    package_entry.config(state="normal")
                    install_button.config(state="normal")
                    uninstall_button.config(state="normal")
                    root.after(5000, clear)
                
        except Exception as e:
            
            pip_progress_bar.stop()
            pip_progress_bar.grid_forget()
            package_status_label.config(text=f"Error upgrading package '{package_name}': {str(e)}")
            upgrade_button.grid_forget()
            pip_upgrade_button.config(state="normal")
            package_entry.config(state="normal")
            install_button.config(state="normal") 
            uninstall_button.config(state="normal")  
            
            root.after(5000, clear)
    threading.Thread(target=upgrade_package_thread,daemon=True).start()


def check_python_installation():
    """检查Python是否已安装"""
    try:
        subprocess.check_output(["python", "--version"], creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        status_label.config(text="Python is not installed.")
        pip_upgrade_button.config(state="disabled")
        install_button.config(state="disabled")
        uninstall_button.config(state="disabled")
        root.after(5000, clear)





def save_theme(theme):
    """保存主题设置"""
    if build>22000:
        with open(os.path.join(config_path, "theme.txt"), "w") as a:
            a.write(theme)
    else:
        if os.path.exists(os.path.join(config_path, "theme.txt")):
            os.remove(os.path.join(config_path, "theme.txt"))

def load_theme():
    """加载主题设置"""
    if build>22000:
        try:
            with open(os.path.join(config_path, "theme.txt"), "r") as r:
                theme = r.read()
            if theme == "dark":
                
                sv_ttk.set_theme("dark")
            elif theme == "light":
                
                sv_ttk.set_theme("light")
        except:
            sv_ttk.set_theme("light")


def check_package_upgradeable():
    
    def check_package_upgradeable_thread():
        package_name = package_entry.get()
        package_name1=package_name
        if package_name==None or package_name=="":
            upgrade_button.grid_forget()
            return 
        try:
            find_packages=subprocess.run(["python", "-m", "pip", "show",package_name], text=True,capture_output=True,
                                                    creationflags=subprocess.CREATE_NO_WINDOW)
            check_upgradeable=subprocess.run(["python", "-m", "pip", "install", "--upgrade", "--dry-run", package_name], text=True,capture_output=True, 
                                                    creationflags=subprocess.CREATE_NO_WINDOW)
            current_version=find_packages.stdout.split("\n")[1].split(": ")[1]
            if f"WARNING: Package(s) not found: {package_name}"in find_packages.stderr:
                upgrade_button.grid_forget()
                return
            else:
                latest_version=check_upgradeable.stdout.split("\n")[-2].split("-")[1]
                
                if f"Would install" in check_upgradeable.stdout:
                    if current_version==latest_version:
                        upgrade_button.grid_forget()
                        return
                    else:
                        package_true_name=check_upgradeable.stdout.split("\n")[-2].split("-")[0].split(" ")[-1]
                        upgrade_button.grid(row=4, column=0, columnspan=3, pady=10, padx=10)
                        upgrade_button.config(state="normal")
                        upgrade_button.config(text=f"Upgrade Package: {package_true_name} ({current_version} -> {latest_version})", command=uprade_package)
                        while True:
                            package_name2=package_entry.get()
                            if package_name1!=package_name2:
                                upgrade_button.grid_forget()
                                break
                        return
                else:
                    upgrade_button.grid_forget()
                    return

        except:
            upgrade_button.grid_forget()
            return
    while True:
        a=threading.Thread(target=check_package_upgradeable_thread,daemon=True)
        a.start()
        a.join()
        time.sleep(0.3)




        
        


if __name__ == "__main__":
    if datetime.datetime.now() >= datetime.datetime(2025, 4, 13):
        messagebox.showerror("Error", "This program cannot be opened after Apr. 13, 2025.")
        exit(1)
    if build<9600:
        messagebox.showerror("Error", "Please upgrade to Windows 8.1, or you can not use this program.")
        exit(1)
    elif build>=9600 and build<=18363:
        messagebox.showwarning("Warning", "These Windows' versions will end their support soon.")
    elif build<22000 and build>18363:
        messagebox.showinfo("Advice","Upgrade to Windows 11 for a better experience.(Windows 11 supports sv_ttk FULLY!)")
    root = tk.Tk()
    root.title("PyQuick")
    root.resizable(False, False)
    icon_path = os.path.join(MY_PATH, 'pyquick.ico')
    
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    # 添加 Help 菜单项
    help_menu = tk.Menu(menubar, tearoff=0)
    settings_menu = tk.Menu(menubar, tearoff=0)
    
    menubar.add_cascade(label="Settings", menu=settings_menu)
    menubar.add_cascade(label="Help", menu=help_menu)

    help_menu.add_command(label="About", command=show_about)
    settings_menu.add_command(label="Settings",command=settings)
    

    note = ttk.Notebook(root)
    download_frame = ttk.Frame(note, padding="10")
    pip_frame = ttk.Frame(note, padding="10")
    note.add(download_frame, text="Python Download")
    note.add(pip_frame, text="Pip Management")
    note.grid(padx=10, pady=10, row=0, column=0)

    # Python Download Frame
    version_label = ttk.Label(download_frame, text="Select Python Version:")
    version_label.grid(row=0, column=0, pady=10,padx=10, sticky="e")


    version_combobox = ttk.Combobox(download_frame, values=[''], state="readonly")
    version_combobox.grid(row=0, column=1, pady=10, padx=10, sticky="w")
    version_combobox.current(0)

    version_reload_button = ttk.Button(download_frame, text="Reload", command=python_version_reload)
    version_reload_button.grid(row=0, column=2, pady=10, padx=10, sticky="w")


    destination_label = ttk.Label(download_frame, text="Select Destination:")
    destination_label.grid(row=1, column=0, pady=10,padx=10, sticky="e")


    destination_entry = ttk.Entry(download_frame, width=60)
    destination_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")


    select_button = ttk.Button(download_frame, text="Select Path", command=select_destination)
    select_button.grid(row=1, column=2, pady=10, padx=10, sticky="w")

    thread_label = ttk.Label(download_frame, text="Select Number of Threads:")
    thread_label.grid(row=2, column=0, pady=10,padx=10, sticky="e")

    thread_combobox = ttk.Combobox(download_frame, values=[str(i) for i in range(1, 129)], state="readonly")
    thread_combobox.grid(row=2, column=1, pady=10, padx=10, sticky="w")
    thread_combobox.current(9)  # Default to 32 threads

    download_label= ttk.Label(download_frame, text="Choose download file:")
    download_label.grid(row=3, column=0, pady=10,padx=10, sticky="e")

    
    download_file_combobox = ttk.Combobox(download_frame, values=[''], state="readonly",width=40)
    download_file_combobox.grid(row=3, column=1, pady=10, padx=10, sticky="w")
    

    download_button = ttk.Button(download_frame, text="Download", command=download_selected_version)
    download_button.grid(row=4, column=0, columnspan=3, pady=10, padx=10)

    
    # 取消下载按钮
    cancel_button = ttk.Button(download_frame, text="Cancel Download", command=confirm_cancel_download)
    cancel_button.grid_forget()
    

    # 下载进度
    progress_bar = ttk.Progressbar(download_frame, orient='horizontal', length=300, mode='determinate')
    progress_bar.grid(row=6, column=0, columnspan=3, pady=10, padx=10)


    # 下载状态
    status_label = ttk.Label(download_frame, text="", padding="5")
    status_label.grid(row=7, column=0, columnspan=3, pady=10, padx=10)







    # pip Management Frame
    pip_upgrade_button = ttk.Button(pip_frame, text="Pip Version:", command=upgrade_pip)
    pip_upgrade_button.grid(row=0, column=0, columnspan=3, pady=10, padx=10)


    package_label = ttk.Label(pip_frame, text="Enter Package Name:")
    package_label.grid(row=1, column=0, pady=10, padx=10, sticky="e")


    package_entry = ttk.Entry(pip_frame, width=80)
    package_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")


    install_button = ttk.Button(pip_frame, text="Install Package", command=install_package)
    install_button.grid(row=2, column=0, columnspan=3, pady=10, padx=10)


    uninstall_button = ttk.Button(pip_frame, text="Uninstall Package", command=uninstall_package)
    uninstall_button.grid(row=3, column=0, columnspan=3, pady=10, padx=10)

    upgrade_button=ttk.Button(pip_frame,text="Upgrade Package",command=uprade_package)
    upgrade_button.grid_forget()

    pip_progress_bar=ttk.Progressbar(pip_frame, orient='horizontal', length=300, mode='indeterminate')
    pip_progress_bar.grid_forget()
    pip_progress_bar['value']=0


    package_status_label = ttk.Label(pip_frame, text="", padding="5")
    package_status_label.grid(row=6, column=0, columnspan=3, pady=10, padx=10)
    
    

    
    if build>22000:
        load_theme()
    threading.Thread(target=show_name, daemon=True).start()
    threading.Thread(target=read_python_version, daemon=True).start()
    threading.Thread(target=check_python_installation, daemon=True).start()
    threading.Thread(target=check_package_upgradeable, daemon=True).start()
    threading.Thread(target=allow_thread, daemon=True).start()
    root.mainloop()
