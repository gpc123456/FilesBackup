import threading
import pystray
from PIL import Image
from pystray import MenuItem
import time
import vglobal


def click_status(icon: pystray.Icon):
    icon.notify("备份工具状态", vglobal.get_value("status"))


def click_src():
    vglobal.set_value("set_src", "1")


def click_des():
    vglobal.set_value("set_des", "1")


def on_exit(icon: pystray.Icon):
    if vglobal.get_value("exit_lock") == "1":
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
        print("正在同步文件,无法退出")
        icon.notify("正在同步文件,无法退出")
    else:
        icon.stop()
        vglobal.set_value("exit", "1")


def click_EjectDisk(icon: pystray.Icon):
    if vglobal.get_value("exit_lock") == "1":
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
        print("正在同步文件,无法弹出磁盘")
        icon.notify("正在同步文件,无法弹出磁盘")
    else:
        vglobal.set_value("EjectDiskFlag", "1")


def reset_src_and_des():
    vglobal.set_value("reset_src_des", "1")


def StartGUI():
    menu = (
        MenuItem(text='状态信息', action=click_status, default=True, visible=True),
        MenuItem(text='重置备份源目录和目标目录', action=reset_src_and_des),
        MenuItem(text='设置备份源目录', action=click_src),
        MenuItem(text='设置备份目标目录', action=click_des),
        MenuItem(text='停止同步,解除磁盘占用', action=click_EjectDisk),
        MenuItem(text='退出工具', action=on_exit),
    )
    image = Image.open("img.png")
    icon = pystray.Icon("name", image, "自动备份小工具", menu)
    vglobal.set_value("gui_icon",icon)
    threading.Thread(target=icon.run).start()
