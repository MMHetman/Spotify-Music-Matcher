import numpy as np
import librosa
import tempfile
import json
import requests
import shutil
import h5py
import pandas

from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

from backend.model.triplet_loss_nn.model import BaseModel


def __audio_to_array(file):
    track, sampling_rate = librosa.load(file, sr=None, mono=True)
    return track, sampling_rate


def __get_samples_start(audio_array, sampling_rate, output_sample_size):
    i = 0
    time_len = int(len(audio_array) / sampling_rate)
    variances = []
    while i <= time_len - output_sample_size:
        variances.append(np.var(audio_array[i * sampling_rate: (i + output_sample_size) * sampling_rate]))
        i += 1
    return variances.index(max(variances))


class AudioProcessor:
    def __init__(self, embedding_model: BaseModel, sql_engine):
        self.embedding_model = embedding_model
        self.sql_engine = sql_engine

    def find_similar_tracks(self, file_stream):
        embedding = self.__get_embedding(file_stream)
        labels = self.__find_nearest_neighbours(embedding)
        return self.__scrape_matched_tracks(labels)

    def __process_audio_input(self, file):
        track, sampling_rate = librosa.load(file, sr=None, mono=True)
        start = self.__get_samples_start(track, sampling_rate, 30)
        samples_starts = np.random.choice(np.arange(start * sampling_rate, (start + 25) * sampling_rate), 10, False)
        track = np.expand_dims(track, axis=1)
        samples = np.zeros((10, 5 * sampling_rate, 1))
        for i in range(10):
            samples[i] = track[samples_starts[i]: samples_starts[i] + 5 * sampling_rate]
        return samples

    def __get_samples_start(self, audio_array, sampling_rate, length):
        variance = 0
        highest_variance_start = 0
        for second in range(int((len(audio_array)/sampling_rate) - 31)):
            index = second * sampling_rate
            local_variance = np.var(audio_array[index:(index+(31*sampling_rate))])
            if variance < local_variance:
                variance = local_variance
                highest_variance_start = second
        return highest_variance_start

    def __get_embedding(self, file_stream):
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir, 'track')
        file_stream.save(temp_path)
        embedding = self.embedding_model.embed(self.__process_audio_input(str(temp_path)))
        shutil.rmtree(temp_dir)
        return embedding

    @staticmethod
    def __find_nearest_neighbours(embedding):
        with h5py.File('backend/model/triplet_loss_nn/embeddings.hdf5', 'r') as file:
            cs = cosine_similarity(file['embeddings'], embedding.reshape(1, -1))
            indices = cs.flatten().argsort()[::-1][:50]
            labels = set()
            for i in indices:
                if len(labels) == 5:
                    break
                label = file['labels'][i]
                labels.add("'" + label + "'")
        return labels

    def __scrape_matched_tracks(self, labels):
        query = 'select distinct tracks.track_id, artist_name, track_name, cover ' \
                'from tracks join track_n_artist tna on tracks.track_id = tna.track_id ' \
                'join artists a on a.artist_id = tna.artist_id ' \
                'join cover_n_sample cns on tracks.sample = cns.sample ' \
                'where tracks.track_id in (' + ','.join(labels) + ')'
        return pandas.read_sql(query, self.sql_engine).to_json(orient='records')
