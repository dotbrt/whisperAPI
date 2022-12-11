import os
from flask import Flask, jsonify, request, render_template
from transcriber import transcribe
# initialize our Flask application
app = Flask(__name__)


ALLOWED_EXTENSIONS = set(['m4a'])
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.m4a', '.txt']
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
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(
                path, uploaded_file.filename))
        file = os.path.join(path, uploaded_file.filename)
        content = transcribe(file)
        return jsonify(content)


# @app.route("/message", methods=["GET"])
# def message():
#     posted_data = request.get_json()
#     name = posted_data['name']
#     return jsonify(" Hope you are having a good time " + name + "!!!")


#  main thread of execution to start the server
if __name__ == '__main__':
    app.run()
