import numpy as np

class base_learner():
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate

    def learn(self, net, grads):
        for key in net.keys():
            net[key] -= grads[key] * self.learning_rate

class Momentum():
    def __init__(self, lr=0.1, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.v = None

    def learn(self, net, grads):
        if self.v is None:
            self.v = {}
            for key, val in net.items():
                self.v[key] = np.zeros_like(val)

        for key in net.keys():
            self.v[key] = self.momentum * self.v[key] - self.lr*grads[key]
            net[key] += self.v[key]
