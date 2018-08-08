import pickle
import numpy as np

from layers import *

class dual_layer:
    def __init__(self, input_layer, middle_layer, output_layer, default_weight=0.1):
        self.filename = "net.pickle"
        self.net = {}

        try:
            self.load_net()
        except:
            print("No net")
            self.generate_weights(input_layer, middle_layer, output_layer, default_weight)

        self.create_network()

    def generate_weights(self, input_layer, middle_layer, output_layer, default_weight):
        self.net['w1'] = np.random.randn(input_layer, middle_layer)*default_weight
        self.net['b1'] = np.zeros(middle_layer)
        self.net['w2'] = np.random.randn(middle_layer, output_layer)*default_weight
        self.net['b2'] = np.zeros(output_layer)

    def create_network(self):
        self.layers = []

        a1 = Affine(self.net['w1'], self.net['b1'])
        self.layers.append(a1)
        trig1 = Sigmoid()
        self.layers.append(trig1)
        a2 = Affine(self.net['w2'], self.net['b2'])
        self.layers.append(a2)

        self.last = SoftMax_loss()

    def save_net(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.net, f)
        pass

    def load_net(self):
        with open(self.filename, "rb") as f:
            self.net = pickle.load(f) 
        pass

    def predict(self, x):
        for layer in self.layers:
            x = layer.forward(x)

        return x

    def accuracy(self, x, t):
        res = self.predict(x)
        #softmax(res)
        #教師データと比較
        if t.ndim == 2:
            #one hot labelではない場合
            pass

        #axisを0にすると、配列のデータを全部合わせて
        #最大値の位置を戻す
        o = np.argmax(res, axis=1)
        
        return np.sum(o == t) / float(x.shape[0])

    def gradient(self, x, t):
        out = self.predict(x)
        self.last.forward(out, t)

        dout = 1
        dout = self.last.backprop(dout)
        self.layers.reverse()
        for layer in self.layers:
            dout = layer.backprop(dout)
        self.layers.reverse()

        grads = {}
        grads['w1'] = self.layers[0].dw
        grads['b1'] = self.layers[0].db
        grads['w2'] = self.layers[2].dw
        grads['b2'] = self.layers[2].db
        return grads
