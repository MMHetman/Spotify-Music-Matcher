from flask import Flask, flash, request, redirect
from flask_cors import CORS

from backend.data.spectgrams_coverter import mp3_to_array

DEBUG = True
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            mp3_array, rate = mp3_to_array(file)
            return {'spectrogram': [mp3_array.tolist(), rate]}


if __name__ == '__main__':
    app.run()
