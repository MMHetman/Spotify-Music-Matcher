import time

import librosa
import numpy as np
import tempfile
import shutil
import os
from pathlib2 import Path
from flask import Flask, flash, request, redirect
from flask_cors import CORS

from backend.model.triplet_loss_nn.model import SiameseNetworkModel

DEBUG = True
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

model = SiameseNetworkModel('backend/model/train_hard_mining/cp.ckpt')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def audio_to_array(file):
    track, sampling_rate = librosa.load(file, sr=None, mono=True)
    track = np.expand_dims(track, axis=1)
    return track[: sampling_rate * 5]


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
            temp_dir = tempfile.mkdtemp()
            temp_path = Path(temp_dir, 'track')
            file.save(temp_path)
            audio_array = np.expand_dims(audio_to_array(str(temp_path)), axis=0)
            shutil.rmtree(temp_dir)

            return {'embedding': model.embed(audio_array).tolist()}


if __name__ == '__main__':
    app.run()
