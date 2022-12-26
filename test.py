import time
import os
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


device_status = psutil.disk_partitions()
print(device_status[3][0])

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(event.event_type, event.src_path)

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='F:\\', recursive=True)
observer.start()
print("开始监听文件变化")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
