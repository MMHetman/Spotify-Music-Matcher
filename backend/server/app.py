from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from sqlalchemy import create_engine

from backend.server.similar_songs_finding import SongsHyperspaceAnalyser
from backend.server.model import TensorFlowModelAbstraction
from backend.server.resources import SongAnalysisResource

DEBUG = True
embedding_model = TensorFlowModelAbstraction('http://localhost:9000/v1/models/SongEmbedding',
                                            'backend/model/triplet_loss_nn/embeddings.hdf5')
sql_engine = create_engine('mysql+pymysql://root:password@localhost/spotify_music_matcher')
songs_finder = SongsHyperspaceAnalyser(embedding_model)

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)

CORS(app, resources={r'/*': {'origins': '*'}})

api.add_resource(
    SongAnalysisResource, '/', resource_class_kwargs={'sql_engine': sql_engine, 'songs_finder': songs_finder}
)

if __name__ == '__main__':
    app.run()
