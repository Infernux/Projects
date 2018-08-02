#!/usr/bin/python3

import numpy as np

def softmax(x):
    if x.ndim == 2:
        x = x.T
        x = x - np.max(x, axis=0)
        y = np.exp(x) / np.sum(np.exp(x), axis=0)
        return y.T 

    x = x - np.max(x) # オーバーフロー対策
    return np.exp(x) / np.sum(np.exp(x))

def cross_entropy_error(y, t):
    #t = t.argmax(axis=1)

    batch_size = y.shape[0]
    a = np.log(y[np.arange(batch_size), t] + 1e-7) #whyyy
    return -np.sum(a) / batch_size

class add():
    def __init__(self):
        pass

    def forward(self, x, y):
        return x+y

    def backward(self, dout):
        return dout

class mult():
    def __init__(self):
        pass

    def forward(self, x, y):
        self.x = x
        self.y = y
        return x*y

    def backward(self, dout):
        dx = dout * self.y
        dy = dout * self.x
        return dx, dy

class div():
    def __init__(self):
        pass

    def forward(self, x):
        self.x = x
        return 1/x 

    def backward(self, dout):
        return -1/pow(self.x,2)

class sigmoid2():
    def __init__(self):
        pass

    def forward(self, x):
        self.out = 1 / (1+np.exp(-x))
        return self.out

    def backward(self, dout):
        self.dw = dout * self.out * (1.0 - self.out)
        return self.dw

class relu():
    def __init__(self):
        pass

    def forward(self, x):
        self.mask = (x <= 0)
        out = x.copy()
        out[self.mask] = 0
        return out

    def backward(self, dout):
        dout[self.mask] = 0
        dx = dout

        return dx

class dot():
    def __init__(self, weight, bias):
        self.weight = weight
        self.bias = bias 

    def forward(self, x):
        self.x = x
        return np.dot(x, self.weight) + self.bias

    def backward(self, dout):
        dx = np.dot(dout, self.weight.transpose())

        self.dW = np.dot(self.x.transpose(), dout)
        self.db = np.sum(dout, axis=0)

        return dx

class softmax_with_loss():
    def __init__(self):
        pass

    def forward(self, x, t):

        self.t = t
        self.sm = softmax(x)
        self.loss = cross_entropy_error(self.sm, t)
        return self.loss

    def backward(self, dout=1):
        #sm - t

        batch_size = self.t.shape[0] #どうして？？？
        #print(self.sm.size, self.t.size)
        #dw = (self.sm - self.t)/batch_size
        dx = self.sm.copy()
        dx[np.arange(batch_size), self.t] -= 1
        dx = dx / batch_size

        return dx

if __name__ == "__main__":
    print("henlow")
    a = add()
    print(a.forward(1,2))
    print(a.backward(5))

    m = mult()
    print(m.forward(1,2))
    print(m.backward(5))

    d = div()
    print(d.forward(2))
    print(d.backward(5))

    s = sigmoid()
    print(s.forward(2))
    print(s.backward(5))

    m2 = mult()
    print(m2.forward(m.forward(100, 2), 1.1))
    print(m2.backward(1))

    weights = np.arange(1, 9, 1)
    bias = np.arange(0, 12, 1)
    weights = weights.reshape(2, 4)
    bias = bias.reshape(4, 3)
    dot = dot(weights, bias)
    init = np.arange(1, 7, 1)
    init = init.reshape(3, 2)

    print("dot")
    dotfor = dot.forward(init)
    print(dot.backward(dotfor))

    val = np.arange(0, 3, 1)
    t = [0, 0.2, 0.6]
    soft = softmax(val)
    print(soft)
    print(cross_entropy_error(soft, t))

    sml = softmax_with_loss()
    print(sml.forward(val, t))
    print(sml.backward(1))
