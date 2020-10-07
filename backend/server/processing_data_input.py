import numpy as np
import librosa


class InputProcessor:
    @classmethod
    def process_audio_input(cls, file):
        track, sampling_rate = librosa.load(file, sr=None, mono=True)
        start = cls.__get_samples_start(track, sampling_rate, 30)
        samples_starts = np.random.choice(np.arange(start*sampling_rate, (start+25)*sampling_rate), 10, False)
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
    def __get_samples_start(cls, audio_array, sampling_rate, output_sample_size):
        i = 0
        time_len = int(len(audio_array)/sampling_rate)
        variances = []
        while i <= time_len-output_sample_size:
            variances.append(np.var(audio_array[i * sampling_rate: (i + output_sample_size) * sampling_rate]))
            i += 1
        return variances.index(max(variances))

