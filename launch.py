import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import sv_ttk
import os
import getpass
import sys

user_name = getpass.getuser()
path=f"/Users/{user_name}/pt_saved/launch"
def refresh_path():
    try:
        os.mkdir(path)
    except:
        pass
    try:
        with open(f"{path}/launch.txt","r") as f:
            u=f.read()
    except FileNotFoundError:
        with open(f"{path}/launch.txt","w") as f:
            f.write("")
        with open(f"{path}/launch.txt","r") as f:
            u=f.read()
    return str(u);

patha=f"/User/{user_name}/pt_saved/"
def all_enabled():
    u=refresh_path()
    if(u==""):
        label.config(text="Please select a version")
        entry.grid(row=1,column=5,columnspan=2,sticky="nsew",padx=10,pady=10)
        button.grid(row=2,column=5,columnspan=2,sticky="nsew",padx=10,pady=10)
        button2.grid(row=3,column=5,columnspan=2,sticky="nsew",padx=10,pady=10)
    else:
        start()

def start():
    label.config(text="Starting...")
    u=refresh_path()
    entry.grid_forget()
    button.grid_forget()
    button2.grid_forget()
    if(("python_tool.app" in u) or ("Pyquick.app" in u) or ("Python_tool.app" in u) or ("Pt.app" in u) or ("Python_Tool.app" in u) or ("python_tool.py" in u)):
        if "python_tool.py" in u:
            os.system(f"python3 {u}")
        else:
            os.system(f"open {u}")
        def en():

            sys.exit(1)
        en()
    else:
        with open(f"{path}/launch.txt","w") as f:
            f.write("")
        all_enabled()

def askfile():
    destination_path = filedialog.askopenfilename()
    if destination_path:
        entry.delete(0, tk.END)
        entry.insert(0, destination_path)
        with open(f"{path}/launch.txt", "w") as f:
            f.write(destination_path)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Python Tool")
    label=ttk.Label(root,text="",font=("Arial",20))
    label.grid(row=0,column=5,columnspan=2,sticky="nsew",padx=10,pady=10)
    entry=ttk.Entry(root,width=30)
    entry.grid_forget()
    button=ttk.Button(root,text="select",command=askfile)
    button.grid_forget()
    button2=ttk.Button(root,text="start",command=start)
    button2.grid_forget()
    sv_ttk.set_theme("dark")
    root.resizable(False,False)
    all_enabled()
    root.mainloop()