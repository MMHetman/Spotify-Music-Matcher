from flask import Flask, flash, request, redirect
from flask_cors import CORS
from sqlalchemy import create_engine

from backend.server.processing_data_input import AudioProcessor
from backend.model.triplet_loss_nn.model import TensorFlowModelReflection

DEBUG = True
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config.from_object(__name__)

sql_engine = create_engine('mysql+pymysql://root:password@localhost/spotify_music_matcher')

CORS(app, resources={r'/*': {'origins': '*'}})

embedding_model = TensorFlowModelReflection('http://localhost:9000/v1/models/SongEmbedding',
                                            'backend/model/triplet_loss_nn/embeddings.hdf5')
data_processor = AudioProcessor(embedding_model, sql_engine)


def check_if_file_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        attributes_values = request.form['attributes']
        attributes_names = request.form['attributesNames']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            return data_processor.find_similar_tracks(file)


if __name__ == '__main__':
    app.run()
