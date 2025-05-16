from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

watch_path = None  

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/', methods=['GET'])
def index():
    global watch_path
    return render_template('index.html', watch_path=watch_path)

@app.route('/set_folder', methods=['POST'])
def set_folder():
    global watch_path
    files = request.files.getlist('files')

    if not files:
        return "ファイルが送信されていません", 400

    
    first_file = files[0]
    folder_name = os.path.dirname(first_file.filename)
    # フォルダ名の抜き出し


    for file in files:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)

    watch_path = folder_name  
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
