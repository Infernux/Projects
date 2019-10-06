#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
from tensorflow import keras

import os
import numpy as np
import matplotlib.pyplot as plt

def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
        ])

    model.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

    return model

checkpoint_path = "model.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

dataset = tf.keras.datasets.fashion_mnist

(x_train, y_train), (x_test, y_test) = dataset.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = create_model()

cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
        save_weights_only=True,
        verbose=1)

try:
    model.load_weights(checkpoint_path)
except:
    print("No weights found, starting from scratch")

model.fit(x_train, y_train, epochs=10, callbacks = [cp_callback])
model.evaluate(x_test, y_test, verbose=2)
