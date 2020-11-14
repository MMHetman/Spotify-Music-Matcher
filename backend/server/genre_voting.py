import sqlite3
from abc import ABC, abstractmethod
from collections import Iterable

import pandas as pd


class Elector(ABC):
    def find_candidates(self, predicted_similar_ids: Iterable, known_ids):
        winner_genre = self.elect(predicted_similar_ids)
        candidates = self.query_candidates(winner_genre, known_ids)
        candidates = [cand[0] for cand in candidates]
        return candidates, winner_genre

    @abstractmethod
    def elect(self, predicted_similar_ids: Iterable) -> Iterable:
        pass

    @abstractmethod
    def query_candidates(self, winner_genre, known_ids) -> Iterable:
        pass


class GenreElector(Elector):
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine

    def elect(self, predicted_similar_ids) -> Iterable:
        votes = self.__query_votes(predicted_similar_ids)
        winner = votes[votes['votes_num'] == votes['votes_num'].max()]
        return winner['genre_name']

    def __query_votes(self, track_ids) -> Iterable:
        query = 'select genre_name, count(distinct tna.track_id) as votes_num ' \
                'from tracks ' \
                'join track_n_artist tna on tracks.track_id = tna.track_id ' \
                'join artist_n_genre ang on tna.artist_id = ang.artist_id ' \
                'join genres g on ang.genre_id = g.genre_id where tna.track_id in ' \
                "(" + ",".join(track_ids) + ") " \
                                               'group by g.genre_name'
        with sqlite3.connect(self.sql_engine) as con:
            votes = pd.read_sql(query, con)
        return votes

    def query_candidates(self, winner_genre, known_ids):
        query = "select tracks.track_id " \
                "from tracks " \
                "join track_n_artist tna on tracks.track_id = tna.track_id " \
                "join artist_n_genre ang on tna.artist_id = ang.artist_id " \
                "join genres g on g.genre_id = ang.genre_id " \
                "where tracks.track_id in ('" + "','".join(known_ids) + "') and " \
                "genre_name in ('" + "','".join(winner_genre) +"')"
        with sqlite3.connect(self.sql_engine) as con:
            cur = con.cursor()
            cur.execute(query)
            data = cur.fetchall()
        return data
