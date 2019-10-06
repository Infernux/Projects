#!/usr/bin/python3

import pickle
import numpy as np
from dataset.mnist import load_mnist
from PIL import Image

from libs.layers import *

class network:
    #def __init__(self, input_layer_size, middle_layer_size, middle_layer_count, output_layer_size): #could create that
    def __init__(self, input_layer_size, middle_layer_size, output_layer_size):
        self.filename = "net.pickle"

        try:
            self.load_net()
        except:
            print("No network found")
            self.randomize_network_weights(input_layer_size, middle_layer_size, output_layer_size)

        self.create_network()

    def create_network(self):
        self.layers = []

        self.layers.append(Affine(self.weights["w1"], self.weights["b1"]))
        self.layers.append(RELU())
        self.layers.append(Affine(self.weights["w2"], self.weights["b2"]))
        self.lastlayer = SoftMax_loss()

    def save_net(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.weights, f)

    def load_net(self):
        with open(self.filename, "rb") as f:
            self.weights = pickle.load(f)

    def predict(self, x):
        tmp = x
        for l in self.layers:
            tmp = l.forward(tmp)

        return softmax(tmp)

    def loss(self, x, t):
        res = self.predict(x) #入力をそのまま入れる
        return self.lastlayer.forward(x, t)

    def randomize_network_weights(self, in_size, mid_size, out_size):
        self.weights = {}
        self.weights["w1"] = np.random.randn(in_size, mid_size) #need one weight per input/mid combination
        self.weights["b1"] = np.random.randn(mid_size) #need one weight per input/mid combination
        self.weights["w2"] = np.random.randn(mid_size, out_size) #need one weight per mid/output combination
        self.weights["b2"] = np.random.randn(out_size) #need one weight per mid/output combination

    def accuracy(self, x, labels):
        predictions = self.predict(x)
        y = np.argmax(predictions, axis=1)
        t = np.argmax(labels, axis=1)
        accuracy = np.sum(y==t) / float(y.shape[0])

    def gradient(self, x, labels):
        self.loss(x, labels)

        dout = 1
        dout = self.lastlayer.backprop(dout)

        self.layers.reverse()

        for l in self.layers:
            dout = l.backprop(dout)

        self.layers.reverse()

        grads = {}
        grads['w1'], grads['b1'] = self.layers[0].dw, self.layers[0].db
        grads['w2'], grads['b2'] = self.layers[1].dw, self.layers[1].db

        return grads

def img_show(img):
    pilimg = Image.fromarray(np.uint8(img))
    pilimg.show()

(x_train, t_train), (x_test, t_test) = load_mnist(flatten=True, normalize=False)

my_net = network(784, 100, 10)

iteration_number = 1000
train_size = x_train.shape[0]
batch_size = 1
learn_rate = 0.1

iteration_per_epoch = (train_size / batch_size, 1)

for i in range(iteration_number):
    #create a batch
    mask = np.random.choice(train_size, batch_size) #訓練データから、batch_size個を選ぶ
    x_batch = x_train[mask]
    t_batch = t_train[mask]

    #勾配
    grad = my_net.gradient(x_batch, t_batch)

    #更新
    for key in my_net.net.keys():
        my_net.net[key] -= grad[key] * learning_rate

    loss = my_net.loss()
    train_loss_list.append(loss)

    if i%iteration_per_epoch == 0:
        train_acc = network.accuracy(x_train, t_train)
        test_acc = network.accuracy(x_test, y_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)

        print("train acc : ", train_acc, ", test acc : ", test_acc)


#my_net.save_net()
