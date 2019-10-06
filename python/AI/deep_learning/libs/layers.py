#!/usr/bin/python3

import numpy as np

def cross_entropy_loss(x, t):
    if x.ndim == 1:
        print("henlo")
        pass

    batch_size = x.shape[0]
    x = x[np.arange(batch_size),t]
    try:
        log = np.log(x+1e-7)
    except:
        print(x)
        print("except")
    return -np.sum(log) / batch_size

class Identity():
    def __init__(self):
        pass

    def forward(self, x):
        return x

    def backward(self, dout):
        return dout

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

class Step():
    def __init__(self):
        pass

    def forward(self, x):
        self.out = x > 0
        return self.out

    def backprop(self, dout):
        return res

class RELU():
    def __init__(self):
        pass

    def forward(self, x):
        self.out = np.maximum(0, x)
        return self.out

    def backprop(self, dout):
        dout[self.out <= 0] = 0
        return dout

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
        batch_size = self.t.shape[0]
        if self.t.size == self.soft.size:
            dx = (self.soft - self.t) / batch_size
        else:
            dx = self.soft.copy()
            dx[np.arange(batch_size), self.t] -= 1
            dx = dx / batch_size
        return dx

def softmax(array):
    array = array - np.max(array)
    array = np.exp(array)

    ss = np.sum(array)
    return array / ss

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    functions = 0

    if functions:
        x=np.arange(-5, 5, 0.1)
        s=RELU()
        y=s.forward(x)

        plt.plot(x, y)
        plt.show()
    else:
        x = np.arange(0, 3, 1)
        y = np.array([0, 0.4, 2])
        y = softmax(y)
        plt.bar(x, y)
        plt.show()
