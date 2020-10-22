import shutil
import tempfile
from abc import ABC, abstractmethod
from collections import Iterable
from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity

from backend.server.model import BaseModel


class SongsFinder(ABC):

    @abstractmethod
    def find_similar_songs(self, audio_file, candidates_ids) -> Iterable:
        pass

    @abstractmethod
    def get_known_ids(self) -> Iterable:
        pass


class SongsHyperspaceAnalyser(SongsFinder):

    def __init__(self, embedding_model: BaseModel):
        self.embedding_model = embedding_model

    def get_known_ids(self):
        return self.embedding_model.get_known_ids()

    def find_similar_songs(self, file_stream, candidates_ids=None):
        embedding = self.__get_embedding(file_stream)
        found_ids = self.__find_nearest_neighbours(embedding, candidates_ids)
        return found_ids

    def __get_embedding(self, file_stream):
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir, 'track')
        file_stream.save(temp_path)
        embedding = self.embedding_model.embed(str(temp_path))
        shutil.rmtree(temp_dir)
        return embedding

    def __find_nearest_neighbours(self, embedding, candidates_ids=None):
        with self.embedding_model.read_embedding_file() as file:
            cs = cosine_similarity(file['embeddings'], embedding.reshape(1, -1))
            indices = cs.flatten().argsort()[::-1]
            labels = set()
            for i in indices:
                if len(labels) == 5:
                    break
                if candidates_ids is not None and i in candidates_ids:
                    label = file['labels'][i]
                    labels.add("'" + label + "'")
        return labels
