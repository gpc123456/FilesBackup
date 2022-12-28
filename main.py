import Core
import GUI
import time
from watchdog.observers import Observer
import json
import sys
import vglobal
from plyer import notification


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
vglobal.set_value("file_lock", "0")  # 配置文件锁,防止线程间文件读写冲突;0:不锁定文件,1:锁定文件
vglobal.set_value("change_need_restart", "0")  # 修改同步目录后是否需要重新启动软件;0:不需要,1:需要

src = ""
des = ""

GUI.StartGUI()
notification.notify(title="自动备份小工具", message="自动备份小工具已启动", timeout=1)

while True:
    try:
        while vglobal.get_value("file_lock") == "1":
            pass
        vglobal.set_value("file_lock", "1")
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
        vglobal.set_value("file_lock", "0")
    except FileNotFoundError:
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
        print("没有找到配置文件,新建配置文件...")
        with open("config", "w", encoding='utf-8') as f:
            f.writelines('{"src":"","des":""}')
        vglobal.set_value("file_lock", "0")
    if (vglobal.get_value("exit") == "1"):
        sys.exit(0)
    time.sleep(1)

vglobal.set_value("change_need_restart", "1")
vglobal.set_value("file_lock", "0")  # 配置文件完整,跳出循环后为文件解锁,防止是否需要重启软件的信息提示发生错误

while True:
    while True:
        if Core.SrcFileExists(src) == 1:
            if Core.DesFileExists(des) == 1:
                notification.notify(
                    title="自动备份小工具", message="发现备份源目录及目标目录", timeout=1)
                vglobal.set_value("status", "发现备份源目录及目标目录")
                print(
                    "["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
                print("发现备份源目录及目标目录")
                break
        if (vglobal.get_value("exit") == "1"):
            sys.exit(0)
        if Core.SrcFileExists(src) != 1 and Core.DesFileExists(des) != 1:
            vglobal.set_value("status", "未找到备份源目录和目标目录,同步服务未启动")
        elif Core.SrcFileExists(src) != 1:
            vglobal.set_value("status", "未找到备份源目录,同步服务未启动")
        else:
            vglobal.set_value("status", "未找到备份目标目录,同步服务未启动")
        time.sleep(1)
    observer = Observer()
    vglobal.set_value("exit_lock", "1")
    Core.Sync(src, des)
    vglobal.set_value("exit_lock", "0")
    vglobal.set_value("status", "同步完成")
    Core.Listening_File(src, des, observer)
    exit_flag = ""
    while True:
        if Core.SrcFileExists(src) == 0 or Core.DesFileExists(des) == 0:
            if Core.SrcFileExists(src) == 0 and Core.DesFileExists(des) == 0:
                print(
                    "["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
                print("同步设备异常拔出,同步终止")
                vglobal.set_value("status", "同步设备异常拔出,同步终止")
                notification.notify(
                    title="自动备份小工具", message="同步设备异常拔出,同步终止", timeout=5)
            elif Core.SrcFileExists(src) == 0:
                print(
                    "["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
                print("同步源目录设备异常拔出,同步终止")
                vglobal.set_value("status", "同步源目录设备异常拔出,同步终止")
                notification.notify(
                    title="自动备份小工具", message="同步源目录设备异常拔出,同步终止", timeout=5)
            else:
                print(
                    "["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]", end="")
                print("同步目标目录设备异常拔出,同步终止")
                vglobal.set_value("status", "同步目标目录设备异常拔出,同步终止")
                notification.notify(
                    title="自动备份小工具", message="同步目标目录设备异常拔出,同步终止", timeout=5)
            Core.EjectDisk(observer)
            exit_flag = "1"  # 设备被拔出,异常退出
            break
        Eject_flag = vglobal.get_value("EjectDiskFlag")
        if Eject_flag == "1":
            Core.EjectDisk(observer)
            notification.notify(
                title="自动备份小工具", message="文件同步已停止,可以弹出磁盘", timeout=5)
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
            if (vglobal.get_value("exit") == "1"):
                sys.exit(0)
            time.sleep(1)
        vglobal.set_value("EjectDiskFlag", "0")
    if exit_flag == "1":
        time.sleep(0.1)
