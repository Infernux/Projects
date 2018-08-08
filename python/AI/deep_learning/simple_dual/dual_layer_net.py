#!/usr/bin/python3

import numpy as np
import argparse

import sys
sys.path.append("../libs")

from dataset.mnist import load_mnist

from network import dual_layer
from mpl import *
from learners import base_learner

def get_minst_data():
    (x_train, t_train), (x_test, t_test) = load_mnist(normalize=True)
    return x_train, t_train, x_test, t_test

def training():
#load_minst
    x_train, t_train, x_test, t_test = get_minst_data()

#create_network
    dl = dual_layer(784, 30, 10)
    np.seterr(all='raise')

#hyper_params
    learning_rate = 0.1
    batch_size = 100
    iter_count = 100000

    learner = base_learner(learning_rate)

    total_acc = []

    for i in range(iter_count):
        #create_batch
        batch_mask = np.random.choice(len(x_train), batch_size)
        x_batch = x_train[batch_mask]
        t_batch = t_train[batch_mask]
        #gradient
        grads = dl.gradient(x_batch, t_batch)

        #learn
        learner.learn(dl.net, grads)

        #accuracy
        if i % 1000 == 0:
            acc = dl.accuracy(x_test, t_test)
            print(acc)
            total_acc.append(acc)

    dl.save_net()
    graphme(np.arange(len(total_acc)), total_acc)

def guess(img):
#convert image
    dl = dual_layer(784, 30, 10)
    dl.predict(img)

parser = argparse.ArgumentParser(description="My great NN")
parser.add_argument('--guess', nargs=1)

args = parser.parse_args(sys.argv[1:])
if args.guess:
    guess(args.guess[0])
else:
    training()
