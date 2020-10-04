import json
import shutil
import tempfile
import pandas
import h5py
import librosa
import numpy as np
import requests

from flask import Flask, flash, request, redirect
from flask_cors import CORS
from pathlib2 import Path
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine

from backend.server.processing_data_input import InputProcessor

DEBUG = True
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config.from_object(__name__)

sql_engine = create_engine('mysql+pymysql://root:password@localhost/spotify_music_matcher')

CORS(app, resources={r'/*': {'origins': '*'}})

input_processor = InputProcessor


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

            data = json.dumps({
                'instances': InputProcessor().process_audio_input(str(temp_path)).tolist()
            })

            response = requests.post('http://localhost:9000/v1/models/SongEmbedding:predict', data=data.encode('utf-8'))
            shutil.rmtree(temp_dir)
            embedding = np.mean(response.json()['predictions'], axis=0)
            with h5py.File('backend/model/triplet_loss_nn/embeddings.hdf5', 'r') as file:
                cs = cosine_similarity(file['embeddings'], embedding.reshape(1, -1))
                indices = cs.flatten().argsort()[::-1][:50]
                labels = set()
                for i in indices:
                    if len(labels) == 5:
                        break
                    label = file['labels'][i]
                    labels.add("'"+label+"'")

            query = 'select distinct track_id, artist_name, track_name, cover ' \
                    'from tracks join track_n_artist tna on tracks.track_id = tna.track_id ' \
                    'join artists a on a.artist_id = tna.artist_id ' \
                    'join cover_n_sample cns on tracks.sample = cns.sample ' \
                    'where tracks.track_id in (' + ','.join(labels) + ')'
            json_res = pandas.read_sql(query, sql_engine).to_json(orient='records')
            return json_res


if __name__ == '__main__':
    app.run()
