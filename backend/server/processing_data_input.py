import numpy as np
import librosa


class InputProcessor:
    @classmethod
    def process_audio_input(cls, file):
        track, sampling_rate = librosa.load(file, sr=None, mono=True)
        samples_starts = cls.__get_samples_starts(track, sampling_rate, 30)
        track = np.expand_dims(track, axis=1)
        samples = np.zeros((10, 5*sampling_rate, 1))
        for i in range(10):
            samples[i] = track[samples_starts[i]: samples_starts[i] + 5 * sampling_rate]
        return samples

    @classmethod
    def __audio_to_array(cls, file):
        track, sampling_rate = librosa.load(file, sr=None, mono=True)
        return track, sampling_rate

    @classmethod
    def __get_samples_starts(cls, audio_array, sampling_rate, output_sample_size):
        i = 0
        variances = np.zeros(26)
        while i < 26:
            variances[i] = np.var(audio_array[i * sampling_rate: (i + output_sample_size) * sampling_rate])
            i += 1
        probabilities = variances/(np.sum(variances))
        return np.random.choice(26, 10, p=probabilities, replace=False)

