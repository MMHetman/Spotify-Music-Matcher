#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
from scipy import signal

millis_per_sec = 1000

M = 512
window_shift = 512

def mp3_to_array(file):
    audio = AudioSegment.from_file(file, format='mp3').set_channels(1)[:(millis_per_sec * 30)]
    return np.array(audio.get_array_of_samples()), audio.frame_rate

def get_spectrogram(audio, sampling_rate):
    return signal.spectrogram(audio, fs=sampling_rate, window='hanning',
                              nperseg=M, noverlap=M-window_shift,
                              detrend=False, scaling='spectrum')

def plot_spectrogram(freqs, times, Sx):
   print(Sx.shape)
   f, ax = plt.subplots()
   ax.pcolormesh(times, freqs / 1000, 10 * np.log10(Sx), cmap='viridis')
   ax.set_ylabel('Frequency [kHz]')
   ax.set_xlabel('Time [s]')
   plt.show()


mp3_array, rate = mp3_to_array('/samples/0aeZzfSoZAcETjba8MCvco')
freqs, times, spec = get_spectrogram(mp3_array, rate)
print(mp3_array.size)
plot_spectrogram(freqs, times, spec)
