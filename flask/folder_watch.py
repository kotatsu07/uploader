from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os


class Imagecheck(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            ext = os.path.splitext(event.src_path)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.gif']:
               print("画像が取得されました")

def start_watch(path):
        global stop_flag
        stop_flag = False
        event_handler = Imagecheck()
        observer = Observer()
        observer.schedule(event_handler,path = path,recursive=False)
        observer.start()

        try:
          while not stop_flag:
            time.sleep(1)
        except KeyboardInterrupt:
          observer.stop()
        observer.join()

def stop():
    global stop_flag
    stop_flag = True
