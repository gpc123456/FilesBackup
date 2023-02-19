import Core
import GUI
import time
from watchdog.observers import Observer
import json
import sys
import tkinter as tk
from tkinter import filedialog
import vglobal


class Logger(object):
    logfile = ""

    def __init__(self, filename=""):
        self.logfile = filename
        self.terminal = sys.stdout
        return

    def write(self, message):
        self.terminal.write(message)
        if self.logfile != "":
            try:
                self.log = open(self.logfile, "a")
                self.log.write(message)
                self.log.close()
            except:
                pass

    def flush(self):
        pass


sys.stdout = Logger("stdout")
sys.stderr = Logger("stderr")

print("--------------------------------------------")
print("ProcessStart["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]")

vglobal._init()
vglobal.set_value("EjectDiskFlag", "0")  # 0无拔出信号,1有拔出信号
vglobal.set_value("exit", "0")  # 0无退出信号,1有退出信号
vglobal.set_value("exit_lock", "0")  # 0:解锁允许退出,1:锁定不允许退出
vglobal.set_value("status", "系统启动...")  # 状态信息
vglobal.set_value("set_src", "0")  # 0:无src设置请求,1:有src设置请求
vglobal.set_value("set_des", "0")  # 0:无des设置请求,1:有des设置请求
vglobal.set_value("reset_src_des", "0")  # 0:无reset设置请求,1:有reset设置请求
vglobal.set_value("occupy_disk","0") #0:磁盘未被占用,1:磁盘已被占用

src = ""
des = ""

GUI.StartGUI()
icon=vglobal.get_value("gui_icon") #使用icon对象显示通知
time.sleep(0.5)
Core.GetGuiIcon(icon)
icon.notify("自动备份小工具已启动")

def SetSrcAndDes(restart_flag):
    if vglobal.get_value("set_src")=="1":
            root = tk.Tk()
            root.withdraw()
            Folderpath = filedialog.askdirectory()
            Folderpath = Folderpath.replace("/", "\\")
            print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
            print("设置src:"+Folderpath)
            if Folderpath != "":
                with open("config", "r", encoding='utf-8') as f:
                    json_data = f.read()
                    src_and_des = json.loads(json_data)
                    src_and_des['src'] = Folderpath
                with open("config", "w", encoding='utf-8') as f:
                    f.writelines(json.dumps(src_and_des, ensure_ascii=False))
                vglobal.set_value("set_src", "0")
                if restart_flag==0:
                    icon.notify("备份源目录设置成功")
                else:
                    icon.notify("备份源目录设置成功,重新启动软件后生效")
            else:
                vglobal.set_value("set_src", "0")
                icon.notify("未选择备份源目录,同步配置将不会被修改")
    if vglobal.get_value("set_des")=="1":
        root = tk.Tk()
        root.withdraw()
        Folderpath = filedialog.askdirectory()
        Folderpath = Folderpath.replace("/", "\\")
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
        print("设置des:"+Folderpath)
        if Folderpath != "":
            with open("config", "r", encoding='utf-8') as f:
                json_data = f.read()
                src_and_des = json.loads(json_data)
                src_and_des['des'] = Folderpath
            with open("config", "w", encoding='utf-8') as f:
                f.writelines(json.dumps(src_and_des, ensure_ascii=False))
            vglobal.set_value("set_des", "0")
            if restart_flag==0:
                icon.notify("备份目标目录设置成功")
            else:
                icon.notify("备份目标目录设置成功,重新启动软件后生效")
        else:
            vglobal.set_value("set_des", "0")
            icon.notify("未选择备份目标目录,同步配置将不会被修改")
    if vglobal.get_value("reset_src_des")=="1":
        with open("config", "w", encoding='utf-8') as f:
            f.writelines('{"src":"","des":""}')
        vglobal.set_value("reset_src_des", "0")
        if restart_flag==0:
            icon.notify("重置备份源目录和目标目录成功")
        else:
            icon.notify("重置备份源目录和目标目录成功,重新启动软件后生效")

while True:
    try:
        SetSrcAndDes(0)
        with open("config", "r", encoding='utf-8') as f:
            json_data = f.read()
            src_and_des = json.loads(json_data)
            src = src_and_des['src']
            des = src_and_des['des']
            if src == "" and des == "":
                # print("未设置备份源目录和目标目录")
                vglobal.set_value("status", "未设置备份源目录和目标目录,同步服务未启动")
            elif src == "":
                # print("未设置备份源目录")
                vglobal.set_value("status", "未设置备份源目录,同步服务未启动")
            elif des == "":
                # print("未设置备份目标目录")
                vglobal.set_value("status", "未设置备份目标目录,同步服务未启动")
            else:
                break
    except FileNotFoundError:
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
        print("没有找到配置文件,新建配置文件...")
        with open("config", "w", encoding='utf-8') as f:
            f.writelines('{"src":"","des":""}')
    if (vglobal.get_value("exit") == "1"):
        sys.exit(0)
    time.sleep(1)

while True:
    while True:
        SetSrcAndDes(1)
        if Core.SrcFileExists(src) == 1:
            if Core.DesFileExists(des) == 1:
                icon.notify("发现备份源目录及目标目录")
                vglobal.set_value("status", "发现备份源目录及目标目录")
                print(
                    "["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
                print("发现备份源目录及目标目录")
                break
        if Core.SrcFileExists(src) != 1 and Core.DesFileExists(des) != 1:
            vglobal.set_value("status", "未找到备份源目录和目标目录,同步服务未启动")
        elif Core.SrcFileExists(src) != 1:
            vglobal.set_value("status", "未找到备份源目录,同步服务未启动")
        else:
            vglobal.set_value("status", "未找到备份目标目录,同步服务未启动")
        if (vglobal.get_value("exit") == "1"):
            sys.exit(0)
        time.sleep(1)
    observer = Observer()
    vglobal.set_value("occupy_disk","1")
    vglobal.set_value("exit_lock", "1")
    Core.Sync(src, des)
    vglobal.set_value("exit_lock", "0")
    vglobal.set_value("status", "同步完成")
    Core.Listening_File(src, des, observer)
    exit_flag = ""
    while True:
        SetSrcAndDes(1)
        if Core.SrcFileExists(src) == 0 or Core.DesFileExists(des) == 0:
            if Core.SrcFileExists(src) == 0 and Core.DesFileExists(des) == 0:
                print(
                    "["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
                print("无法找到备份源目录和目标目录,同步终止")
                vglobal.set_value("status", "无法找到备份源目录和目标目录,同步终止")
                icon.notify("无法找到备份源目录和目标目录,同步终止")
            elif Core.SrcFileExists(src) == 0:
                print(
                    "["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
                print("无法找到备份源目录,同步终止")
                vglobal.set_value("status", "无法找到备份源目录,同步终止")
                icon.notify("无法找到备份源目录,同步终止")
            else:
                print(
                    "["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
                print("无法找到备份目标目录,同步终止")
                vglobal.set_value("status", "无法找到备份目标目录,同步终止")
                icon.notify("无法找到备份目标目录,同步终止")
            Core.EjectDisk(observer)
            vglobal.set_value("occupy_disk","0")
            exit_flag = "1"  # 备份源目录或目标目录失去跟踪,异常退出
            break
        Eject_flag = vglobal.get_value("EjectDiskFlag")
        if Eject_flag == "1":
            Core.EjectDisk(observer)
            vglobal.set_value("occupy_disk","0")
            icon.notify("文件同步已停止,可以弹出磁盘")
            exit_flag = "0"  # 正常退出
            break
        if (vglobal.get_value("exit") == "1"):
            sys.exit(0)
        time.sleep(1)
    if exit_flag == "0":
        vglobal.set_value("status", "为确保您可以正常拔出设备,同步服务暂时停止1分钟")
        begin_count = 0
        while begin_count < 60:
            begin_count = begin_count+1
            SetSrcAndDes(1)
            if (vglobal.get_value("exit") == "1"):
                sys.exit(0)
            time.sleep(1)
        vglobal.set_value("EjectDiskFlag", "0")
    if exit_flag == "1":
        time.sleep(0.1)
