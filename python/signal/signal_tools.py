#!/usr/bin/python3

import random
from math import sqrt, exp, sin, cos
import matplotlib.pyplot as plt
import numpy as np

gaussian_variance = 0.4
gaussian_target = 2
max_gaussian = 0
delta = 1e-4

def naive_dft(samples):
    fhat = list()
    w = -2*np.pi/len(samples)
    for k in range(0, len(samples)):
        acc = [0, 0]
        j = 0
        for sample in samples:
            real = sample * cos(w * j * k)
            complex_part = sample * sin(w * j * k)
            acc[0] += real
            acc[1] += complex_part
            j+=1

        fhat.append(acc)

    return fhat

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

def add_noise_to_graph(values, max_noise):
    noisy_samples = list()
    for sample in values:
        noise = (gaussian(random.randrange(0, 40)/10, gaussian_target, gaussian_variance) / max_gaussian) * max_noise
        noisy_samples.append(sample + noise)
        #noisy_samples.append(sample + random.gauss(gaussian_target, gaussian_variance) - (max_gaussian/2))

    return noisy_samples

def conjugate(val):
    new_v = val.copy()
    new_v[1] = -new_v[1]

    return new_v

def multiply_complex_by_conjugate(sample):
    conj = conjugate(sample)
    # multiplying both complex parts gives i^2 which is -1
    return sample[0] * (conj[0] + conj[1]) + sample[1] * conj[0] - sample[1] * conj[1]

def multiply_complex_by_conjugate_2(sample):
    # multiplying both complex parts gives i^2 which is -1
    return sample * sample.conjugate()

def compute_PSD(samples, dt):
    freq_list = list()
    power_list = list()
    i = 0
    for sample in samples:
        power_list.append(multiply_complex_by_conjugate(sample) / len(samples))
        freq_list.append(1/(dt*len(samples)) * i)
        i+=1

    return power_list, freq_list

if __name__ == '__main__':
    random.seed(42)
    max_gaussian = gaussian(gaussian_target, gaussian_target, gaussian_variance)

    #gaussian_test()

    print('main')
    indices_list, sample_list = generate_signal_from_list_of_freq([120, 50], 0, 1, delta)
    noisy_sample_list = add_noise_to_graph(sample_list, 10)

    #fhat = np.fft.fft(sample_list, len(sample_list))
    #fhat = np.fft.fft(noisy_sample_list, len(sample_list))
    #fhat = naive_dft(sample_list)
    fhat = naive_dft(noisy_sample_list)

    power_list, freq_list = compute_PSD(fhat, delta)
    max_indice = int(np.floor(len(freq_list)/2))
    freq = (1/(delta*len(fhat))) * np.arange(len(fhat))
    plt.plot(freq_list, power_list)
    plt.xlim(freq_list[1], freq_list[max_indice])
    plt.ylim(0, max(power_list[1:]))
    plt.show()
    for a in range(0, len(power_list)):
        power_list[a] = 0 if power_list[a] < 120 else power_list[a]
    #for a in range(100, len(power_list)):
    #    power_list[a] = 0
    plt.plot(freq_list, power_list)
    plt.xlim(freq_list[1], freq_list[max_indice])
    plt.ylim(0, max(power_list[1:]))
    plt.show()

    ifft = np.fft.ifft(power_list)

    # actually only half the sampling rate is usable
    plt.plot(indices_list, sample_list, color='r')
    plt.plot(indices_list, ifft, color='b')
    plt.xlim(indices_list[1], indices_list[-1])
    plt.show()
