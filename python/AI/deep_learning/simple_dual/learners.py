class base_learner():
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate

    def learn(self, net, grads):
        for key in net.keys():
            net[key] -= grads[key] * self.learning_rate
