from flask import Flask, request, render_template, redirect, url_for, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import time
import json
import shutil
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

is_watching = False

# 設定ファイルから監視パスを読み込む（なければNone）
def load_watch_path():
    try:
        with open('settings.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('watch_path')
    except FileNotFoundError:
        return None

watch_path = load_watch_path()
# ファイルを . で分け、拡張子が{}のものを返すぜ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
# uploadsに保存
def save_files(files):
    upload_folder = os.path.join(app.root_path, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))

# デフォルト処理
@app.route('/', methods=['GET'])
def index():
    pathname_index = watch_path if watch_path else "未設定"
    return render_template('index.html', watch_path=watch_path, is_watching=is_watching, watch_path_index=pathname_index)

#　uploadsの中身をリストにして返す
@app.route('/api/image_list')
def image_list():
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    if not os.path.exists(upload_folder):
        return jsonify([])
    files = os.listdir(upload_folder)
    return jsonify(files)

# htmlからfilesをもってくる
@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('files')
    save_files(files)
    return '', 204

# uploadsの初期化
@app.route('/clear_uploads',methods=['POST'])
def clear_uploads():
    upload_folder = os.path.join(app.root_path,'uploads')
    if os.path.exists(upload_folder):
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder,filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    return '',204

# ファイルシステムのイベントハンドラ
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            print("新しいファイルが追加されました:", event.src_path)
            # ここにファイル追加時の処理を書くことも可能
            filename = os.path.basename(event.src_path)
            destination_path = os.path.join(UPLOAD_FOLDER,filename)
            shutil.copy2(event.src_path,destination_path)

observer = None

def start_observer(path):
    global observer
    observer = Observer()
    observer.schedule(MyHandler(), path=path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def start_observer_in_thread(path):
    t = threading.Thread(target=start_observer, args=(path,), daemon=True)
    t.start()

def stop_observer():
    global observer
    if observer is not None:
        observer.stop()
        observer.join()
        observer = None

if __name__ == '__main__':
    # もし起動時に監視開始したいならここで呼ぶ
    start_observer_in_thread(watch_path)

    app.run(debug=True)
