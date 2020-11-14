import json
import unittest

import h5py
import numpy as np
import werkzeug

from backend.server.app import get_app
from backend.server.genre_voting import GenreElector
from backend.server.model import BaseModel
from backend.server.similar_songs_finding import SongsHyperspaceAnalyser


class ModelMockup(BaseModel):
    embedding_file = 'backend/server/unit_tests/test_hyperspace.hdf5'

    def embed(self, input_file):
        return np.random.random(32), 0

    def read_embedding_file(self):
        return h5py.File(self.embedding_file, 'r')

    def get_known_ids(self):
        with h5py.File(self.embedding_file, 'r') as file:
            ids = np.array(np.unique(file['labels']).astype(str))
        return ids


class ServerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.embedding_model = ModelMockup()
        self.database = 'backend/server/unit_tests/test_db'
        self.genre_chooser = GenreElector(self.database)
        self.songs_finder = SongsHyperspaceAnalyser(self.embedding_model, self.genre_chooser)
        app = get_app(self.database, self.songs_finder)
        app.config['TESTING'] = True
        app.config['DEBUG'] = False

        self.test_client = app.test_client()

    def test_root(self):
        with open('test.mp3', 'rb') as audio_file:
            response = self.test_client.post(
                "/",
                data={
                    "file": (audio_file, 'test.mp3'),
                },
                content_type="multipart/form-data"
            )
        result = json.loads(response.data)
        track_ids = set()
        for track in json.loads(result['results']):
            track_ids.add(track['track_id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(track_ids), 5)

    def test_root_w_parameters(self):
        with open('test.mp3', 'rb') as audio_file:
            response = self.test_client.post(
                "/",
                data={
                    "file": (audio_file, 'test.mp3'),
                    "acousticness": ('Low'),
                    "energy": ('High'),
                    "danceability": ('Medium'),
                    "valence": ('Medium'),
                    "genres": ("rock,metal")
                },
                content_type="multipart/form-data"
            )
        result = json.loads(response.data)
        track_ids = set()
        for track in json.loads(result['results']):
            track_ids.add(track['track_id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(track_ids), 5)

    def test_root_empty_file(self):
        response = self.test_client.post(
            "/",
            data={
                "acousticness": ('Low'),
                "energy": ('High'),
                "danceability": ('Medium'),
                "valence": ('Medium'),
                "genres": ("rock,metal")
            },
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)

    def test_root_invalid_file(self):
        response = self.test_client.post(
            "/",
            data={
                "file": (None, 'test.txt'),
                "acousticness": ('Low'),
                "energy": ('High'),
                "danceability": ('Medium'),
                "valence": ('Medium'),
                "genres": ("rock,metal")
            },
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)

    def test_root_invalid_attrs_name(self):
        response = self.test_client.post(
            "/",
            data={
                "file": (None, 'test.txt'),
                "NOT EXISTING ATTR": ('Low'),
                "energy": ('High'),
                "danceability": ('Medium'),
                "valence": ('Medium'),
                "genres": ("rock,metal")
            },
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)

    def test_root_invalid_attrs_val(self):
        response = self.test_client.post(
            "/",
            data={
                "file": (None, 'test.txt'),
                "acousticness": ('NOT EXISTING VAL'),
                "energy": ('High'),
                "danceability": ('Medium'),
                "valence": ('Medium'),
                "genres": ("rock,metal")
            },
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)

    def test_top_tracks_query(self):
        response = self.test_client.get(
            "/top_tracks",
            data={
                "genres": 'rock,pop',
                "amount": 5
            },
            content_type="multipart/form-data"
        )
        result = json.loads(json.loads(response.data))
        max_pop = result[0]['popularity']
        for track in result:
            self.assertGreaterEqual(max_pop, track['popularity'])
        self.assertEqual(len(result), 5)
        self.assertEqual(response.status_code, 200)

    def test_top_tracks_query_wrong_amount(self):
        response = self.test_client.get(
            "/top_tracks",
            data={
                "genres": 'rock,pop',
                "amount": 123456
            },
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)

    def test_top_tracks_query_wrong_genre(self):
        response = self.test_client.get(
            "/top_tracks",
            data={
                "genres": 'NOT EXISTING GENRE',
                "amount": 10
            },
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)

    def test_songs_finding(self):
        known_ids = np.array(self.songs_finder.get_known_ids())
        self.assertTrue(known_ids.size > 1)
        with open('test.mp3', 'rb') as audio_file:
            fileS = werkzeug.datastructures.FileStorage(audio_file, 'test.mp3')
            res = self.songs_finder.find_similar_songs(fileS, known_ids[:10])
        self.assertEqual(np.array(res).size, 3)
        self.assertGreater(np.array(res[0]).size, 0)

    def test_genre_candidates(self):
        known_ids = np.array(self.songs_finder.get_known_ids())
        res = self.genre_chooser.query_candidates(['funk'], known_ids)
        self.assertGreater(len(list(res)), 0)

unittest.main()
