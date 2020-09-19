#!/usr/bin/python3

import random
from math import sqrt, exp
import matplotlib.pyplot as plt
import numpy as np

gaussian_variance = 0.4
gaussian_target = 2
max_gaussian = 0

def generate_signal_from_list_of_freq(freq_list, range_from, range_to, delta):
    if range_from > range_to:
        print("Invalid range, {} isn't smaller than {}".format(range_from, range_to))
        return
    if len(freq_list) <= 0:
        print('Invalid list, got an empty list'.format(delta))
        return
    if delta < 0:
        print('Invalid delta, expected a positive float, got {}'.format(delta))
        return

    indices_list = list()
    return_list = list()

    for x in np.arange(range_from, range_to, delta):
        indices_list.append(x)
        acc = 0
        for f in freq_list:
            acc += np.sin(2*np.pi*f*x)

        return_list.append(acc)

    return indices_list, return_list

def gaussian_test():
    indices_list = list()
    return_list = list()
    for f in np.arange(0, 4, 1e-2):
        indices_list.append(f)
        return_list.append(gaussian(f, gaussian_target, gaussian_variance))

    plt.plot(indices_list, return_list)
    plt.show()

def gaussian(x, target, variance):
    factor = 1/(variance*sqrt(2*np.pi))
    exp_operand = ((x-target)**2)
    exp_operand = -exp_operand/(2 * variance ** 2)

    return factor * exp(exp_operand)

def add_noise_to_graph(values):
    noisy_samples = list()
    for sample in values:
        noisy_samples.append(sample + gaussian(random.randrange(0, 40)/10, gaussian_target, gaussian_variance) - (max_gaussian/2))
        #noisy_samples.append(sample + random.gauss(gaussian_target, gaussian_variance) - (max_gaussian/2))

    return noisy_samples

if __name__ == '__main__':
    random.seed(42)
    max_gaussian = gaussian(gaussian_target, gaussian_target, gaussian_variance)

    #gaussian_test()

    print('main')
    #indices_list, sample_list = generate_signal_from_list_of_freq([100, 50, 1000], 0, 0.1, 1e-4)
    indices_list, sample_list = generate_signal_from_list_of_freq([100, 50], 0, 0.1, 1e-4)
    noisy_sample_list = add_noise_to_graph(sample_list)

    plt.plot(indices_list, sample_list)
    plt.plot(indices_list, noisy_sample_list)
    plt.show()
