from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from backend.data.spectgrams_coverter import mp3_to_array, get_spectrogram
import pathlib

# configuration
DEBUG = True
ALLOWED_EXTENSIONS = {'mp3'}

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            mp3_array, rate = mp3_to_array(file)
            spectr = get_spectrogram(mp3_array, rate)[0]

            return {'spectrogram': spectr.tolist()}


if __name__ == '__main__':
    app.run()
