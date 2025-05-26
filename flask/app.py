from flask import Flask, request, render_template, redirect, url_for,jsonify,current_app
from werkzeug.utils import secure_filename
import os
import json
import threading
from folder_watch import start_watch,stop

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
is_watching = False


def load_watch_path():
    try:
        with open('settings.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('watch_path')
    except FileNotFoundError:
        return None


watch_path = load_watch_path()
watch_path_index = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/', methods=['GET'])
def index():
    global watch_path
    global watch_path_index
    pathname_index=watch_path_index if watch_path_index else "未設定"
    return render_template('index.html', watch_path=watch_path,is_watching=is_watching,watch_path_index=pathname_index)

@app.route('/set_folder', methods=['POST'])
def set_folder():
    global watch_path
    global is_watching
    global watch_path_index

    files = request.files.getlist('files')

    if not files:
        return "ファイルが送信されていません", 400

    first_file = files[0]
    watch_path_index = os.path.dirname(first_file.filename)

   # 正しい例（Flaskサーバー上に存在するパス）
    watch_path = os.path.abspath(app.config['UPLOAD_FOLDER'])  # uploads フォルダの絶対パス
    

    for file in files:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)

    

    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump({'watch_path': watch_path}, f, ensure_ascii=False, indent=2)

    if not is_watching:
        is_watching = True
        threading.Thread(target=start_watch,args=(watch_path,),daemon=True).start()

    return redirect(url_for('index'))

@app.route('/stop',methods=['POST'])
def stop_watch_route():
    stop()
    global is_watching
    is_watching = False
    return redirect(url_for('index'))

@app.route('/start_watch_route', methods=['POST'])
def start_watch_route():
    global is_watching, watch_path
    if watch_path and not is_watching:
        is_watching = True
        threading.Thread(target=start_watch, args=(watch_path,), daemon=True).start()
    return redirect(url_for('index'))

@app.route('/api/image_list')
def image_list():
    upload_file = os.path.join(current_app.root_path,'uploads')
    if not os.path.exists(upload_file):
        return jsonify([])
    files = os.listdir(upload_file)
    return jsonify(files)


@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('files')
    upload_folder = os.path.join(app.root_path, 'uploads')

    os.makedirs(upload_folder, exist_ok=True)

    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))

    return '', 204  # 成功だけ返す


if __name__ == '__main__':
    app.run(debug=True)
