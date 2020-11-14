import json
from abc import ABC, abstractmethod
import io

import h5py
import librosa
import requests
import numpy as np
import matplotlib.pyplot as plt
import cv2

from librosa.display import specshow

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


class TensorFlowModelAbstraction(BaseModel):
    def __init__(self, model_address, embedding_file):
        self.embedding_file = embedding_file
        self.model_address = model_address

    def get_known_ids(self):
        with h5py.File(self.embedding_file) as file:
            ids = np.unique(file['labels']).astype(str)
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
        return samples, start

    def embed(self, input_file):
        input_tensor, start = self.__get_samples(*librosa.load(input_file, sr=None))
        data = json.dumps({
            'instances': input_tensor.tolist()
        })

        response = requests.post(self.model_address + ':predict', data=data.encode('utf-8'))
        return np.mean(response.json()['predictions'], axis=0), start

    '''def embed(self, input_file):
        y, sr = librosa.load(input_file)
        start = self.__get_samples_start(y, sr, 30)
        y = y[start:start+25*sr]
        mels = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        mels = librosa.power_to_db(mels)

        fig_size = plt.rcParams["figure.figsize"]
        fig_size[0] = float(mels.shape[1]) / float(100)
        fig_size[1] = float(mels.shape[0]) / float(100)
        plt.rcParams["figure.figsize"] = fig_size
        plt.axis('off')
        plt.axes([0., 0., 1., 1.0], frameon=False, xticks=[], yticks=[])
        specshow(mels, cmap='gray_r')
        plt.savefig('x',
                    bbox_inches=None, pad_inches=0)
        plt.close()
        print(cv2.imread('x'))
        img = cv2.cvtColor(cv2.imread('x.png'), cv2.COLOR_BGR2GRAY)
        emb_set = np.zeros((10, 128, 128, 1))
        for j in range(10):
            for start in range(0, img.shape[1] - 128, 128):
                emb_set[j] = np.expand_dims(img[:, start:start + 128], 2) / 255

        input_tensor, start = emb_set, start
        data = json.dumps({
            'instances': input_tensor.tolist()
        })

        response = requests.post(self.model_address + ':predict', data=data)
        return np.mean(response.json()['predictions'], axis=0), start'''

    def read_embedding_file(self):
        return h5py.File(self.embedding_file, 'r')
