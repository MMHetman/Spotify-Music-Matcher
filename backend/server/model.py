import json
from abc import ABC, abstractmethod

import h5py
import librosa
import requests
import numpy as np


class BaseModel(ABC):
    @abstractmethod
    def embed(self, input_file):
        pass

    @abstractmethod
    def read_embedding_file(self):
        pass

    @abstractmethod
    def get_known_ids(self):
        pass


class TensorFlowModelReflection(BaseModel):
    def __init__(self, model_address, embedding_file):
        self.embedding_file = embedding_file
        self.model_address = model_address

    def get_known_ids(self):
        with h5py.File(self.embedding_file) as file:
            ids = np.unique(file['labels'])
        return ids

    @staticmethod
    def __get_samples_start(audio_array, sampling_rate, length):
        variance = 0
        highest_variance_start = 0
        for second in range(int((len(audio_array) / sampling_rate) - (length + 1))):
            index = second * sampling_rate
            local_variance = np.var(audio_array[index:(index + ((length + 1) * sampling_rate))])
            if variance < local_variance:
                variance = local_variance
                highest_variance_start = second
        return highest_variance_start

    def __get_samples(self, audio_array, sampling_rate):
        start = self.__get_samples_start(audio_array, sampling_rate, 30)
        samples_starts = np.random.choice(np.arange(start * sampling_rate, (start + 25) * sampling_rate), 10, False)
        track = np.expand_dims(audio_array, axis=1)
        samples = np.zeros((10, 5 * sampling_rate, 1))
        for i in range(10):
            samples[i] = track[samples_starts[i]: samples_starts[i] + 5 * sampling_rate]
        return samples

    def embed(self, input_file):
        input_tensor = self.__get_samples(*librosa.load(input_file))
        data = json.dumps({
            'instances': input_tensor.tolist()
        })

        response = requests.post(self.model_address + ':predict', data=data.encode('utf-8'))
        return np.mean(response.json()['predictions'], axis=0)

    def read_embedding_file(self):
        return h5py.File(self.embedding_file, 'r')
