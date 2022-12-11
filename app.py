import os
from flask import Flask, jsonify, request, render_template, abort
from transcriber import transcribe
from werkzeug.utils import secure_filename
# initialize our Flask application
app = Flask(__name__)


ALLOWED_EXTENSIONS = set(['m4a'])
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.m4a']
app.config['UPLOAD_PATH'] = 'tmp'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/", methods=["POST"])
def upload_file():
    path = app.config['UPLOAD_PATH']
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        elif filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return abort(400)
            else:
                uploaded_file.save(os.path.join(
                    path, filename))
                file = os.path.join(path, filename)
                content = transcribe(file)
                return jsonify(content)


#  main thread of execution to start the server
if __name__ == '__main__':
    app.run()
