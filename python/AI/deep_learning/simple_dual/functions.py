#!/usr/bin/python3

import numpy as np

def softmax(x):
    x = x - np.max(x)
    x = np.exp(x)

    if x.ndim != 1:
        ss = np.sum(x, axis=1)
        ss = ss.reshape(x.shape[0],1)
    else:
        ss = np.sum(x)

    return x/ss

def cross_entropy_loss(x, t):
    if x.ndim == 1:
        print("henlo")
        pass

    batch_size = x.shape[0]
#本物の数式は: log(x)*t ですが0ではないTは一つだけです
    x = x[np.arange(batch_size),t]
    try:
        log = np.log(x+1e-7)
    except:
        print(x)
        print("except")
    return -np.sum(log) / batch_size

if __name__ == '__main__':
    print("softmax test")
    a = np.arange(1, 7, 1)
    a = a.reshape(3, 2)
    print(softmax(a))

    a = np.arange(1, 3, 1)
    print(softmax(a))

    print("cross_entropy test")
    a = np.arange(1, 10, 1)
    a = a.reshape(3, 3)

    t = np.arange(0, 3, 1)

    print(cross_entropy_loss(a, t))
