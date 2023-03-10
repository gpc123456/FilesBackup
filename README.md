## FileBackup是一个简单的实时文件同步备份程序  

--- 
### 简介 
FileBackup可以对文件夹或者磁盘内文件进行实时同步与备份，通过对文件夹或磁盘内文件的修改进行监听，当文件夹或磁盘中的文件发生修改时，备份文件将同步被修改，确保备份文件始终与源文件保持一致。  
FileBackup还会每日为备份文件创建快照，当备份文件和源文件均发生损坏时，可以通过快照恢复文件，最大程度避免文件丢失。
FileBackup备了简易的GUI，方便各类用户进行操作。

---
### 使用方法  
#### 软件运行或打包  
您可以使用Python解释器直接执行本项目中的 `main.py` 来使用本程序，在使用本程序之前请确保您已安装以下Python包：  
> Nuitka == 1.3.3
Pillow == 9.3.0
pystray == 0.19.4
six == 1.16.0
watchdog == 2.2.0
  
或者您也可以使用nuitka将本项目编译打包后使用，具体打包步骤请参照本项目中的 `build.txt` 。请注意，在打包项目前请确认您已安装上述的Python包，如果您打包后的程序执行环境为Windows7，请您不要使用Python 3.9及以上版本进行打包。  
#### 软件使用
1. 软件运行后，将会在任务栏托盘显示一个程序图标 <img src="img.png" alt="图片替换文本" width="20"/>，鼠标左键单击该图标可以查看程序当前运行状态，鼠标右键单击该图标弹出程序操作菜单，可以对程序进行操作。  
2. 首次使用本程序需要对备份的源目录（你要备份的目录）和备份的目标目录（要将该目录备份到哪里）进行设置，通过鼠标右键单击程序图标进行设置。设置完成后自动开始初始化备份文件夹，初始化完成后开启实时备份。使用菜单选项中的 `重置备份源目录和目标目录` 可以清除当前设置。   
3. 实时同步需要监听备份源目录，当您的备份源目录为可移动存储设备时，对该设备的监听会导致您无法弹出该设备。因此当您的备份源目录为可移动存储设备时，请先右键程序图标，在菜单中选择 `停止同步,解除磁盘占用` 随后再弹出该设备。
4. 本程序会在您指定的备份目标目录下生成两种文件夹：  
- `Backup` 为热备份文件夹，与源目录内容保持一致
- `DayBackup_(日期)` 为对应日期的快照