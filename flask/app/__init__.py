import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from .image_reader import ProcessImage

app = Flask(__name__)

UPLOAD_FOLDER = './app/tmp/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 3 * 1024 * 1024

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template('fileform.html')


@app.route('/check-image', methods=['GET', 'POST'])
def check_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify(success=False, message='file param is required'), 400

        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            destination = os.path.join(UPLOAD_FOLDER, filename)
            file.save(destination)

            element = ProcessImage(destination)
            results = element.read_image().execute_detection()
            os.remove(destination)
            # results = dict(objects=objects, explicit_content=[])
            return jsonify(success=True, results=results), 200

        return 'error', 400

    if request.method == 'GET':
        return redirect(url_for('index'))
