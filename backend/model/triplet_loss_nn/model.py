from backend.model.triplet_loss_nn.model_config import *

import tensorflow as tf


class SiameseNetworkModel:

    def __init__(self, weights_file):
        self.embedding_model = self.__get_embedding_model()
        self.siamese_model = self.__get_model()
        self.siamese_model.load_weights(weights_file)
        self.siamese_model.compile(loss=self.triplet_loss, optimizer='adam')

    def embed(self, data_input):
        return self.embedding_model.predict(data_input)

    @classmethod
    def __get_embedding_model(cls):
        from kapre.composed import get_melspectrogram_layer
        from keras.layers import Conv2D, BatchNormalization, \
            AveragePooling2D, Dense, Dropout, Flatten
        from keras import initializers

        embedding_model = tf.keras.models.Sequential()
        embedding_model.add(get_melspectrogram_layer(input_shape=shape,
                                                     return_decibel=True))
        embedding_model.add(Conv2D(filters=64, kernel_size=[7, 7],
                                   kernel_initializer=initializers.he_normal(seed=1),
                                   activation="relu"))
        embedding_model.add(BatchNormalization())
        embedding_model.add(AveragePooling2D(pool_size=[2, 2], strides=2))
        embedding_model.add(Conv2D(filters=128, kernel_size=[7, 7], strides=2,
                                   kernel_initializer=initializers.he_normal(seed=1),
                                   activation="relu"))
        embedding_model.add(BatchNormalization())
        embedding_model.add(AveragePooling2D(pool_size=[2, 2], strides=2))
        embedding_model.add(Conv2D(filters=256, kernel_size=[3, 3],
                                   kernel_initializer=initializers.he_normal(seed=1),
                                   activation="relu"))
        embedding_model.add(BatchNormalization())
        embedding_model.add(AveragePooling2D(pool_size=[2, 2], strides=2))
        embedding_model.add(Conv2D(filters=512, kernel_size=[3, 3],
                                   kernel_initializer=initializers.he_normal(seed=1),
                                   activation="relu"))
        embedding_model.add(BatchNormalization())
        embedding_model.add(AveragePooling2D(pool_size=[2, 2], strides=2))
        embedding_model.add(Conv2D(filters=1024, kernel_size=[1, 1],
                                   kernel_initializer=initializers.he_normal(seed=1),
                                   activation="relu"))
        embedding_model.add(BatchNormalization())
        embedding_model.add(AveragePooling2D(pool_size=[2, 2], strides=2))
        embedding_model.add(BatchNormalization())
        embedding_model.add(Flatten())
        embedding_model.add(BatchNormalization())
        embedding_model.add(Dropout(0.6))
        embedding_model.add(Dense(1024, activation="relu",
                                  kernel_initializer=initializers.he_normal(seed=1)))
        embedding_model.add(Dropout(0.5))
        embedding_model.add(Dense(256, activation="relu",
                                  kernel_initializer=initializers.he_normal(seed=1)))
        embedding_model.add(Dropout(0.25))
        embedding_model.add(Dense(64, activation="relu",
                                  kernel_initializer=initializers.he_normal(seed=1)))
        embedding_model.add(Dense(32, activation="relu",
                                  kernel_initializer=initializers.he_normal(seed=1)))
        return embedding_model

    @classmethod
    def __get_model(cls):
        embedding_model = cls.__get_embedding_model()

        input_anchor = tf.keras.layers.Input(shape)
        input_duplicate = tf.keras.layers.Input(shape)

        embedding_anchor = embedding_model(input_anchor)
        embedding_duplicate = embedding_model(input_duplicate)

        output = tf.keras.layers.concatenate(
            [embedding_anchor, embedding_duplicate],
            axis=1
        )

        model = tf.keras.models.Model(
            [input_anchor, input_duplicate],
            output
        )
        return model

    @classmethod
    def triplet_loss(cls, y_true, y_pred):
        anchor, duplicate = y_pred[:, :emb_size], y_pred[:, emb_size:]

        sim_matrix = tf.matmul(tf.nn.l2_normalize(anchor, axis=-1),
                               tf.transpose(tf.nn.l2_normalize(duplicate, axis=-1)))
        sim_ap = tf.linalg.diag_part(sim_matrix)
        sim_an = tf.math.subtract(sim_matrix, tf.linalg.diag(sim_ap))

        mean_neg = tf.math.reduce_sum(sim_an, axis=1, keepdims=True) / (batch_size - 1)

        mask_1 = tf.math.equal(tf.eye(batch_size), tf.constant(1.))
        mask_2 = tf.math.greater(sim_an, tf.reshape(sim_ap, [batch_size, 1]))
        mask = tf.math.logical_or(mask_1, mask_2)
        sim_an_masked = tf.where(mask, tf.constant(-2.0), tf.identity(sim_an))
        closest_neg = tf.math.reduce_max(sim_an_masked, axis=1, keepdims=True)

        l_1 = tf.math.maximum(mean_neg - tf.reshape(sim_ap, [batch_size, 1]) + alpha, 0.0)
        l_2 = tf.math.maximum(closest_neg - tf.reshape(sim_ap, [batch_size, 1]) + alpha, 0.0)
        l_full = l_1 + l_2
        return tf.math.reduce_sum(l_full)
