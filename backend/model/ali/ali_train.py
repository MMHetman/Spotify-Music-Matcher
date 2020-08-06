from backend.model.ali.ali_model import ALIModel
from keras_adversarial import gan_targets
import numpy as np


def get_batch_range(batch_num, batch_size, data_size):
    return (batch_num * batch_size, min((batch_num + 1) * batch_size, data_size))


def rescale_batch(batch):
    batch += -(np.min(batch))
    batch /= np.max(batch) / (1 - (-1))
    batch += (-1)
    return batch


def train_on_data_batch(model, data_file, print_interval):
    data = np.load(data_file)
    num_batches = int(data.shape[0] / batch_size + 1)
    batch_losses = []
    batch_indices = [
        get_batch_range(i, batch_size, data.shape[0]) for i in range(num_batches)
    ]
    for i in range(len(batch_indices)):
        start, end = batch_indices[i]
        # batch = rescale_batch(data[start:end, :, :, None])
        batch = data[start:end, :, :, None]
        targets = gan_targets(end - start)
        targets[0] *= np.random.uniform(0.7, 0.9, end - start)[:, None]
        targets[3] *= np.random.uniform(0.7, 0.9, end - start)[:, None]
        losses = model.train_on_batch(batch, targets)
        batch_losses.append(losses)
        if i % print_interval == 0:
            print(losses)
            print(np.mean(np.reshape(model.predict(data[start:end, :, :, None]), (4, -1)), axis=1))

    return batch_losses


def train_one_epoch(model, data_files, print_interval):
    epoch_losses = []
    for f in data_files:
        print('training on {}'.format(f))
        epoch_losses += train_on_data_batch(model, f, print_interval)

    return epoch_losses


def save_weights(model, weight_file):
    model.save_weights(weight_file)


def get_model_memory_usage(batch_size, model):
    try:
        from keras import backend as K
    except:
        from tensorflow.keras import backend as K

    shapes_mem_count = 0
    internal_model_mem_count = 0
    for l in model.layers:
        layer_type = l.__class__.__name__
        if layer_type == 'Model':
            internal_model_mem_count += get_model_memory_usage(batch_size, l)
        single_layer_mem = 1
        out_shape = l.output_shape
        if type(out_shape) is list:
            out_shape = out_shape[0]
        for s in out_shape:
            if s is None:
                continue
            single_layer_mem *= s
        shapes_mem_count += single_layer_mem

    trainable_count = np.sum([K.count_params(p) for p in model.trainable_weights])
    non_trainable_count = np.sum([K.count_params(p) for p in model.non_trainable_weights])

    number_size = 4.0
    if K.floatx() == 'float16':
        number_size = 2.0
    if K.floatx() == 'float64':
        number_size = 8.0

    total_memory = number_size * (batch_size * shapes_mem_count + trainable_count + non_trainable_count)
    gbytes = np.round(total_memory / (1024.0 ** 3), 3) + internal_model_mem_count
    return gbytes


model = ALIModel().model
batch_size = 101
epochs = 5
print_interval = 10


print(model.metrics_names)
losses = []
for e in range(epochs):
    print('epoch {}'.format(e))
    losses += train_one_epoch(model, ['0_12000.npy'], print_interval)
    save_weights(model, 'model_weights_8_epoch_{}'.format(e))

print(len(losses))
with open('model_losses_8.csv') as losses_file:
    for loss in losses:
        losses_file.write(','.join([str(l) for l in loss]) + '\n')
