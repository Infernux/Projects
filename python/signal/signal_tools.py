#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np

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

def add_noise_to_graph():
    pass


if __name__ == '__main__':
    print('main')
    indices_list, return_list = generate_signal_from_list_of_freq([100, 50, 1000], 0, 0.1, 1e-4)

    plt.plot(indices_list, return_list)
    plt.show()
