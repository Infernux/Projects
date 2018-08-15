import numpy as np

from functions import *

class Sigmoid():
    def __init__(self):
        pass

    def forward(self, x):
        #1/1+e(-x)
        x = 1+np.exp(-x)
        self.out = 1/x
        return self.out

    def backprop(self, dout):
        res = self.out * (1 - self.out) * dout
        return res 

class Affine():
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def forward(self, x):
        self.x = x
        res = np.dot(x, self.weights)
        return res + self.bias

    def backprop(self, dout):
        self.dw = np.dot(self.x.T, dout)
        self.db = np.sum(dout, axis=0) #?
        return np.dot(dout, self.weights.T)

class SoftMax_loss():
    def __init__(self):
        pass

    def forward(self, x, t):
        self.t = t
        self.soft = softmax(x)
        return cross_entropy_loss(self.soft, t)

    def backprop(self, dout):
        a = np.zeros_like(self.soft)
        a[np.arange(self.soft.shape[0]), self.t] = 1
        out = self.soft - a
        return out