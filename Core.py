import os
import shutil
import time
from datetime import date, timedelta
from watchdog.events import FileSystemEventHandler
import vglobal
import subprocess

def GetGuiIcon(gui_icon):
    global icon
    icon = gui_icon

def Sync(src, des):
    # 检测备份文件夹
    if not os.path.exists(des+"\\Backup"):
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print("初次使用同步功能,初始化同步文件夹")
        vglobal.set_value("status", "初次使用同步功能,初始化同步文件夹中...")
        icon.notify("初次使用同步功能,初始化同步文件夹")
        os.mkdir(des+"\\Backup")
        yesterday = (date.today() + timedelta(days=-1)).strftime("%Y_%m_%d")
        if not os.path.exists(des+"\\DayBackup_"+yesterday):
            os.mkdir(des+"\\DayBackup_"+yesterday)
        cmd = "xcopy /s /y /d /e /I "+src+" "+des+"\\Backup"
        p = subprocess.Popen(cmd, shell=True, encoding='gb2312')
        p.wait()
        # os.system(cmd)
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print("同步文件夹初始化完成,开始监听文件修改")
        icon.notify("同步文件夹初始化完成,实时同步开启")
    else:
        # 检测每日快照备份文件夹,如今日未备份先进行备份
        # 每日备份文件夹格式:DayBackup_yyyy_mm_dd
        yesterday = (date.today() + timedelta(days=-1)).strftime("%Y_%m_%d")
        if not os.path.exists(des+"\\DayBackup_"+yesterday):
            print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
            print("进行每日快照备份中...")
            vglobal.set_value("status", "进行每日快照备份中...")
            icon.notify("进行每日快照备份中...")
            os.mkdir(des+"\\DayBackup_"+yesterday)
            cmd = "xcopy /s /y /d /e /I "+des+"\\Backup "+des+"\\DayBackup_"+yesterday
            p = subprocess.Popen(cmd, shell=True, encoding='gb2312')
            p.wait()
            # os.system(cmd)
            print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
            print("每日快照备份完成")
            icon.notify("每日快照备份完成,更新备份文件夹")
            print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
            print("更新备份文件夹")
            vglobal.set_value("status", "更新备份文件夹中...")
            shutil.rmtree(des+"\\Backup")
            os.mkdir(des+"\\Backup")
            cmd = "xcopy /s /y /d /e /I "+src+" "+des+"\\Backup"
            p = subprocess.Popen(cmd, shell=True, encoding='gb2312')
            p.wait()
            # os.system(cmd)
            print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
            print("更新备份文件夹完成,实时同步开启")
            icon.notify("更新备份文件夹完成,实时同步开启")
        else:
            print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
            print("今日快照已创建,增量同步文件")
            vglobal.set_value("status", "进行初始同步中...")
            icon.notify("进行初始同步中...")
            cmd = "xcopy /s /y /d /e /I "+src+" "+des+"\\Backup"
            p = subprocess.Popen(cmd, shell=True, encoding='gb2312')
            p.wait()
            print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
            print("增量同步完成")
            icon.notify("初始同步完成,实时同步开启")


class MyHandler(FileSystemEventHandler):

    def __init__(self, src, des):
        self.src = src
        self.des = des

    def on_created(self, event):
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print("发现文件更新")
        vglobal.set_value("status", "发现文件更新,正在同步")
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print(event.event_type, event.src_path)
        vglobal.set_value("exit_lock", "1")
        cmd = "xcopy /s /y /d /e /I "+self.src+" "+self.des+"\\Backup"
        p = subprocess.Popen(cmd, shell=True, encoding='gb2312')
        p.wait()
        # os.system(cmd)
        vglobal.set_value("exit_lock", "0")
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print("同步完成")
        vglobal.set_value("status", "同步完成")

    def on_moved(self, event):
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print("发现文件更新")
        vglobal.set_value("status", "发现文件更新,正在同步")
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print(event.event_type, event.src_path)
        vglobal.set_value("exit_lock", "1")
        replace_len = len(self.src)
        relative_path = event.src_path[replace_len+1:]
        delete_path = self.des+"\\Backup\\"+relative_path
        try:
            if os.path.exists(delete_path)==False:
                raise FileNotFoundError
            delete_is_dir = os.path.isdir(delete_path)
            if delete_is_dir == True:
                print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
                print("删除文件夹:"+delete_path)
                shutil.rmtree(delete_path)
            else:
                print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
                print("删除文件:"+delete_path)
                os.remove(delete_path)
        except FileNotFoundError:
            print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
            print("要删除的文件不存在,无需进行删除操作")
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print("移动操作前文件已删除,重新同步目标文件")
        cmd = "xcopy /s /y /d /e /I "+self.src+" "+self.des+"\\Backup"
        p = subprocess.Popen(cmd, shell=True, encoding='gb2312')
        p.wait()
        # os.system(cmd)
        vglobal.set_value("exit_lock", "0")
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print("同步完成")
        vglobal.set_value("status", "同步完成")

    def on_modified(self, event):
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print("发现文件更新")
        vglobal.set_value("status", "发现文件更新,正在同步")
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print(event.event_type, event.src_path)
        vglobal.set_value("exit_lock", "1")
        cmd = "xcopy /s /y /d /e /I "+self.src+" "+self.des+"\\Backup"
        p = subprocess.Popen(cmd, shell=True, encoding='gb2312')
        p.wait()
        # os.system(cmd)
        vglobal.set_value("exit_lock", "0")
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print("同步完成")
        vglobal.set_value("status", "同步完成")

    def on_deleted(self, event):
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print("发现文件删除")
        vglobal.set_value("status", "发现文件删除,正在同步")
        print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
        print(event.event_type, event.src_path)
        vglobal.set_value("exit_lock", "1")
        replace_len = len(self.src)
        relative_path = event.src_path[replace_len+1:]
        delete_path = self.des+"\\Backup\\"+relative_path
        try:
            if os.path.exists(delete_path)==False:
                raise FileNotFoundError
            delete_is_dir = os.path.isdir(delete_path)
            if delete_is_dir == True:
                print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
                print("删除文件夹:"+delete_path)
                shutil.rmtree(delete_path)
                vglobal.set_value("exit_lock", "0")
                print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
                print("同步完成")
                vglobal.set_value("status", "同步完成")
            else:
                print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
                print("删除文件:"+delete_path)
                os.remove(delete_path)
                vglobal.set_value("exit_lock", "0")
                print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
                print("同步完成")
                vglobal.set_value("status", "同步完成")
        except FileNotFoundError:
            print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
            print("要删除的文件不存在,无需进行删除操作")
            vglobal.set_value("exit_lock", "0")
            print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
            print("同步完成")
            vglobal.set_value("status", "同步完成")


def Listening_File(src, des, observer):
    event_handler = MyHandler(src, des)
    observer.schedule(event_handler, path=src, recursive=True)
    observer.start()


def SrcFileExists(src):
    if os.path.exists(src):
        #print("源文件夹存在,可以进行备份")
        return 1
    else:
        #print("源文件夹不存在,不进行备份")
        return 0


def DesFileExists(des):
    if os.path.exists(des):
        #print("目标文件夹存在,可以进行备份")
        return 1
    else:
        #print("目标文件夹不存在,不进行备份")
        return 0


def EjectDisk(observer):
    observer.stop()
    print("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]",end="")
    print("文件监听已停止,可以弹出磁盘")
