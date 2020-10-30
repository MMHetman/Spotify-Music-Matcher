import pandas as pd
import werkzeug
from flask_restful import Resource, reqparse

from backend.server.similar_songs_finding import SongsFinder


class SongAnalysisResource(Resource):
    ATTRIBUTES_MARGIN = 0.1
    TEMPO_MARGIN = 10
    RESULTS_BASE_QUERY = \
        "select distinct " \
        "tracks.track_id, track_name, popularity, acousticness," \
        "danceability, duration_ms, energy, instrumentalness, `key`," \
        "liveness, mode, tempo, valence, sample, artist_name, album_name, " \
        "cover, a.artist_id, genre_name " \
        "from tracks " \
        "join track_n_artist tna on tracks.track_id = tna.track_id " \
        "join artists a on a.artist_id = tna.artist_id " \
        "join albums a2 on a2.album_id = tracks.album_id " \
        "join song_n_cover snc on tracks.track_id = snc.id " \
        "join artist_n_genre ang on a.artist_id = ang.artist_id " \
        "join genres g on g.genre_id = ang.genre_id"

    ATTRIBUTES_LIMITS = {
        'acousticness': (0.35, 0.7),
        'energy': (0.45, 0.66),
        'danceability': (0.4, 0.6),
        'valence': (0.4, 0.7)
    }

    def __init__(self, sql_engine, songs_finder: SongsFinder):
        self.songs_finder = songs_finder
        self.sql_engine = sql_engine

    def post(self):
        args = self.__parse_request()
        file = args['file']
        attributes = self.__get_attributes(args)
        genres = args['genres'].split(',') if args['genres'] != 'undefined' else None
        candidates_ids = None
        if any([value is not None for value in attributes.values()]):
            candidates_query = self.__get_candidates_query(self.songs_finder.get_known_ids(), attributes, genres)
            candidates_ids = pd.read_sql(candidates_query, self.sql_engine)
        matched_ids = self.songs_finder.find_similar_songs(file, candidates_ids['track_id'])
        results_query = self.RESULTS_BASE_QUERY + " where tracks.track_id in (" + ",".join(matched_ids) + ')'
        return pd.read_sql_query(results_query, self.sql_engine).to_json(orient='records')

    def __parse_request(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True)
        parse.add_argument('acousticness')
        parse.add_argument('energy')
        parse.add_argument('danceability')
        parse.add_argument('valence')
        parse.add_argument('genres')
        args = parse.parse_args()
        return args

    def __get_attributes(self, args):
        return {
            'acousticness': self.__parse_users_constrain(args['acousticness'], 'acousticness'),
            'energy': self.__parse_users_constrain(args['energy'], 'energy'),
            'danceability': self.__parse_users_constrain(args['danceability'], 'danceability'),
            'valence': self.__parse_users_constrain(args['valence'], 'valence')
        }

    def __parse_users_constrain(self, attribute_value, attribute_name):
        limits = self.ATTRIBUTES_LIMITS[attribute_name]
        if attribute_value == 'High':
            return str(limits[1] - self.attributes_margin), '1'
        if attribute_value == 'Medium':
            return str(limits[0] - self.attributes_margin), str(limits[1] + self.attributes_margin)
        if attribute_value == 'Low':
            return '0', str(limits[0] + self.attributes_margin)
        return '0', '1'

    def __get_candidates_query(self, known_ids, attributes, genres):
        query = "select distinct tracks.track_id " \
                "from tracks " \
                "join track_n_artist tna on tracks.track_id = tna.track_id " \
                "join artist_n_genre ang on tna.artist_id = ang.artist_id " \
                "join genres g on g.genre_id = ang.genre_id " \
                "where tracks.track_id in ('" + "','".join(known_ids) + "') and " \
                "acousticness between " + " and ".join(attributes['acousticness']) + " and " \
                "valence between " + " and ".join(attributes['valence']) + " and " \
                "energy between " + " and ".join(attributes['energy']) + " and " \
                "danceability between " + " and ".join(attributes['danceability'])
        if genres is not None:
            query += " and genre_name in ('" + "','".join(genres) + "')"
        return query

    def __constrain_to_str(self, attribute_value, attribute_name):
        limits = self.parse_users_constrain(attribute_value, attribute_name)
        return attribute_name + ' between ' + str(limits[0]) + ' and ' + str(limits[1]) + ' '

    @staticmethod
    def __process_results(tracks, artists):
        return '{ "tracks": ' + tracks.to_json(orient='records') + ', "artists": ' + artists.to_json(
            orient='records') + '}'
