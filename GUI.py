import threading
import pystray
from PIL import Image
from pystray import MenuItem
import tkinter as tk
from tkinter import filedialog
import json
import vglobal

def click_status(icon: pystray.Icon):
    icon.notify("同步工具状态", vglobal.get_value("status"))


def click_src(icon: pystray.Icon):
    root = tk.Tk()
    root.withdraw()
    Folderpath = filedialog.askdirectory()
    Folderpath=Folderpath.replace("/","\\\\")
    print(Folderpath)
    with open("config", "r", encoding='utf-8') as f:
        json_data = f.read()
        src_and_des = json.loads(json_data)
        src_and_des['src']=Folderpath
        with open("config", "w", encoding='utf-8') as f:
            f.writelines(json.dumps(src_and_des,ensure_ascii=False))
    icon.notify("同步源目录设置成功,如已开始同步,需要重新启动软件后生效")


def click_des(icon, item):
    root = tk.Tk()
    root.withdraw()
    Folderpath = filedialog.askdirectory()
    Folderpath=Folderpath.replace("/","\\\\")
    print(Folderpath)
    with open("config", "r", encoding='utf-8') as f:
        json_data = f.read()
        src_and_des = json.loads(json_data)
        src_and_des['des']=Folderpath
        with open("config", "w", encoding='utf-8') as f:
            f.writelines(json.dumps(src_and_des,ensure_ascii=False))
    icon.notify("同步目标目录设置成功,如已开始同步,需要重新启动软件后生效")


def on_exit(icon: pystray.Icon):
    if vglobal.get_value("exit_lock")=="1":
        print("正在同步文件,无法退出")
        icon.notify("正在同步文件,无法退出")
    else:
        icon.stop()
        vglobal.set_value("exit", "1")


def click_EjectDisk(icon: pystray.Icon):
    if vglobal.get_value("exit_lock")=="1":
        print("正在同步文件,无法弹出磁盘")
        icon.notify("正在同步文件,无法弹出磁盘")
    else:
        vglobal.set_value("EjectDiskFlag","1")

def StartGUI():
    menu = (
        MenuItem(text='状态信息', action=click_status, default=True, visible=True),
        MenuItem(text='设置备份源目录', action=click_src),
        MenuItem(text='设置备份目标目录', action=click_des),
        MenuItem(text='停止同步,解除磁盘占用', action=click_EjectDisk),
        MenuItem(text='退出工具', action=on_exit),
    )
    image = Image.open("img.png")
    icon = pystray.Icon("name", image, "自动备份小工具", menu)
    threading.Thread(target=icon.run).start()