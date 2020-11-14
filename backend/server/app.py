import sqlite3

from flask import Flask, g, jsonify
from flask_cors import CORS
from flask_restful import Api

from backend.server.genre_voting import GenreElector
from backend.server.model import TensorFlowModelAbstraction
from backend.server.resources import SongAnalysisResource, PopularTracksByGenres
from backend.server.similar_songs_finding import SongsHyperspaceAnalyser
from backend.server.exceptions import InvalidSongData

DEBUG = True


def get_app(database, songs_finder):
    app = Flask(__name__)
    app.config.from_object(__name__)
    api = Api(app)

    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(database)
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @app.errorhandler(InvalidSongData)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    CORS(app, resources={r'/*': {'origins': '*'}})

    api.add_resource(
        SongAnalysisResource, '/', resource_class_kwargs={'sql_engine': get_db, 'songs_finder': songs_finder}
    )
    api.add_resource(
        PopularTracksByGenres, '/top_tracks', resource_class_kwargs={'sql_engine': get_db}
    )
    return app


if __name__ == '__main__':
    embedding_model = TensorFlowModelAbstraction('http://localhost:9000/v1/models/SongEmbedding',
                                                 'backend/model/triplet_loss_nn/embeddings.hdf5')
    database = 'thesis_db'
    genre_chooser = GenreElector(database)
    songs_finder = SongsHyperspaceAnalyser(embedding_model, genre_chooser)
    flask_app = get_app(database, songs_finder)
    flask_app.run()
