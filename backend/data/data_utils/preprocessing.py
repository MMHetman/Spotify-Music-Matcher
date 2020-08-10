from multiprocessing import Pool, Process
from pathlib import Path
from random import randrange, shuffle
import numpy as np

import backend.data.data_utils.spectrograms as sp

DATA_BATCH_SIZE = 12000


def get_flat_rand_seq(args):
    file, data_dir, num_secs = args
    mp3 = Path(data_dir, file)
    mp3_array, rate = sp.mp3_to_array(mp3)
    seg_size = rate * num_secs
    rand_start = randrange(mp3_array.size - 1 - seg_size)
    freqs, times, spec = sp.get_spectrogram(mp3_array[rand_start:(rand_start + seg_size)], rate)
    return spec


def get_rand_specs_from(files, data_dir, num_secs):
    arg_tups = zip(*[files, [data_dir] * len(files), [num_secs] * len(files)])
    with Pool() as pool:
        specs = pool.map(get_flat_rand_seq, arg_tups)
    stacked = np.array(specs)
    return stacked


def create_data_batch(previews_to_process, data_dir, filename):
    specs = get_rand_specs_from(previews_to_process, data_dir, 5)
    np.save('{}.npy'.format(filename), specs)
    del specs


def generate_dataset(track_ids, data_dir, num_samples_per_song):
    preview_dataset = track_ids * num_samples_per_song
    shuffle(preview_dataset)

    with open('training_tracks.csv', 'w') as datafile:
        for tid in track_ids:
            datafile.write(tid + '\n')

    num_batches = int(len(preview_dataset) / DATA_BATCH_SIZE) + 1
    print(len(preview_dataset))
    print(num_batches)
    for start, end in [(i * DATA_BATCH_SIZE, min((i + 1) * DATA_BATCH_SIZE, len(preview_dataset))) for i in
                       range(num_batches)]:
        p = Process(target=create_data_batch, args=(
            preview_dataset[start:end], data_dir, '{}_{}'.format(start, end)))
        p.start()
        p.join()
