#!/usr/bin/python3

import random
from math import sqrt, exp, sin, cos, log2
import matplotlib.pyplot as plt
import numpy as np

gaussian_variance = 0.4
gaussian_target = 2
max_gaussian = 0
delta = 1e-6

omega_matrix_size = 8
omega_matrix = list()
inverse_omega_matrix = list()

def generate_inverse_omega_matrix(size):
    w = 2*np.pi/size
    for j in range(0, size):
        for k in range(0, size):
            val = [0, 0]
            val[0] = cos(w * j * k)
            val[1] = sin(w * j * k)
            inverse_omega_matrix.append(val)

def generate_omega_matrix(size):
    w = -2*np.pi/size
    for j in range(0, size):
        for k in range(0, size):
            val = [0, 0]
            val[0] = cos(w * j * k)
            val[1] = sin(w * j * k)
            omega_matrix.append(val)

def multiply_invert_omega_matrix_with_vector(vector):
    res = list()

    for j in range(0, len(vector)):
        acc = [0,0]
        for i in range(0, len(vector)):
            acc[0] += vector[i][0] * inverse_omega_matrix[j*len(vector) + i][0] - vector[i][1] * inverse_omega_matrix[j*len(vector) + i][1]
            acc[1] += vector[i][0] * inverse_omega_matrix[j*len(vector) + i][1] + vector[i][1] * inverse_omega_matrix[j*len(vector) + i][0]

        acc[0] /= len(vector)
        acc[1] /= len(vector)
        res.append(acc)

    return res

# real input
def multiply_add_omega_matrix_with_vector(vector):
    res = list()

    for j in range(0, len(vector)):
        acc = [0,0]
        for i in range(0, len(vector)):
            acc[0] += vector[i] * omega_matrix[j*len(vector) + i][0]
            acc[1] += vector[i] * omega_matrix[j*len(vector) + i][1]
        res.append(acc)

    return res

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

def naive_idft(samples):
    fhat = list()
    w = 2*np.pi/len(samples)
    for k in range(0, len(samples)):
        acc = [0, 0]
        j = 0
        for sample in samples:
            acc[0] += sample[0] * cos(w*j*k) - sample[1] * sin(w*j*k)
            acc[1] += sample[0] * sin(w*j*k) + sample[1] * cos(w*j*k)
            j+=1

        acc[0] /= len(samples)
        acc[1] /= len(samples)

        fhat.append(acc)

    return fhat

def swap(arr, i1, i2):
    tmp = arr[i1]
    arr[i1] = arr[i2]
    arr[i2] = tmp


def rearrange_data_for_fft(samples):
    N = len(samples)

    omega_size_log2 = int(log2(omega_matrix_size))
    data_size_log2 = int(log2(N))

    elements_to_order = N
    count = 1
    for _ in range(data_size_log2 - omega_size_log2):
        for i in range(count):
            rearrange_data_for_fft_sub(samples, elements_to_order, elements_to_order*i)

        elements_to_order //= 2
        count *= 2

def rearrange_data_for_fft_sub(samples, N, offset):
    N2 = N//2
    for i in range(1, N2, 2):
        swap(samples, offset+N2+i-1, offset+i)

    count = 1
    for i in range(2, N2, 2):
        for j in range(count):
            swap(samples, offset+i-j, offset+i-j-1)
        count += 1

    count = 1
    for i in range(N2 + 2, N, 2):
        for j in range(count):
            swap(samples, offset+i-j, offset+i-j-1)
        count += 1

    return samples

def invert_bits(i, bitcount):
    a = 0
    mask = 2 ** (bitcount-1)
    shift = (bitcount - 1)

    for _ in range(bitcount//2):
        a |= ((i & mask) >> shift)
        mask //= 2
        shift -= 2

    if bitcount & 1:
        a |= (i&mask)
        mask //= 2

    for _ in range(bitcount//2):
        shift += 2
        a |= ((i & mask) << shift)
        mask //= 2

    return a

def rearrange_data_for_fft_mem(samples):
    s = samples.copy()

    N = len(samples)

    omega_size_log2 = int(log2(omega_matrix_size))
    data_size_log2 = int(log2(N))

    count = data_size_log2 - omega_size_log2
    inc = (2 ** count)

    #for i in range(N):
    i = 0
    while i < N:
        in_index = invert_bits(i, data_size_log2)
        s[i] = samples[in_index]
        for _ in range(omega_matrix_size-1):
            in_index += inc
            i += 1
            s[i] = samples[in_index]
        i += 1

    return s

def naive_iterative_fft(samples):
    N = len(samples)

    omega_size_log2 = int(log2(omega_matrix_size))
    data_size_log2 = int(log2(N))

    count = data_size_log2 - omega_size_log2

    #前処理
    samples = rearrange_data_for_fft_mem(samples)
    #rearrange_data_for_fft(samples)

    for i in range(N // omega_matrix_size):
        #in C -> write in place at the end of the function
        offset = omega_matrix_size * i
        res = multiply_add_omega_matrix_with_vector(samples[offset:offset+omega_matrix_size])
        for res_idx in range(omega_matrix_size):
            samples[offset+res_idx] = res[res_idx]

    half_N = omega_matrix_size

    for _ in range(data_size_log2 - omega_size_log2):
        w = -2*np.pi/(half_N*2)
        for y in range(N // half_N // 2): #//2 is because you always need your odds and evens as pairs
            fhat_even = samples[(y*2)*half_N:((y*2)+1)*half_N] #in C -> use a pointer
            fhat_odd = samples[((y*2)+1)*half_N:((y*2)+2)*half_N] #in C -> use a pointer
            for i in range(half_N):
                samples[(y*half_N*2)+i] = [fhat_even[i][0] + fhat_odd[i][0] * cos(w*i) - fhat_odd[i][1] * sin(w*i), fhat_even[i][1] + fhat_odd[i][1] * cos(w*i) + fhat_odd[i][0] * sin(w*i)]
                samples[(y*half_N*2)+half_N+i] = [fhat_even[i][0] + fhat_odd[i][0] * -cos(w*i) - fhat_odd[i][1] * -sin(w*i), fhat_even[i][1] + fhat_odd[i][1] * -cos(w*i) + fhat_odd[i][0] * -sin(w*i)]
        half_N *= 2

def naive_fft(samples):
    if len(samples) <= omega_matrix_size:
        return multiply_add_omega_matrix_with_vector(samples)
    #return naive_dft(samples)
    f_even = list()
    f_odd = list()
    N = len(samples)
    half_N = int(N / 2)
    w = -2*np.pi/N
    i = 0
    for _ in range(0, half_N):
        f_even.append(samples[i])
        i+=1
        f_odd.append(samples[i])
        i+=1

    fhat_even = naive_fft(f_even)
    fhat_odd = naive_fft(f_odd)
    res = list()
    for i in range(0, half_N):
        v = [fhat_even[i][0] + fhat_odd[i][0] * cos(w*i) - fhat_odd[i][1] * sin(w*i), fhat_even[i][1] + fhat_odd[i][1] * cos(w*i) + fhat_odd[i][0] * sin(w*i)]
        res.append(v)
    for i in range(0, half_N):
        v = [fhat_even[i][0] + fhat_odd[i][0] * cos(w*(i+half_N)) - fhat_odd[i][1] * sin(w*(i+half_N)), fhat_even[i][1] + fhat_odd[i][1] * cos(w*(i+half_N)) + fhat_odd[i][0] * sin(w*(i+half_N))]
        res.append(v)

    return res

def matrix_ifft(samples):
    if len(samples) <= omega_matrix_size:
        return multiply_invert_omega_matrix_with_vector(samples)

    f_even = list()
    f_odd = list()
    N = len(samples)
    half_N = int(N / 2)
    w = 2*np.pi/N
    i = 0
    for _ in range(0, half_N):
        f_even.append(samples[i])
        i+=1
        f_odd.append(samples[i])
        i+=1

    fhat_even = matrix_ifft(f_even)
    fhat_odd = matrix_ifft(f_odd)

    res = list()
    for i in range(0, half_N):
        v = [fhat_even[i][0] + fhat_odd[i][0] * cos(w*i) - fhat_odd[i][1] * sin(w*i), fhat_even[i][1] + fhat_odd[i][1] * cos(w*i) + fhat_odd[i][0] * sin(w*i)]
        v[0] /= 2
        v[1] /= 2
        res.append(v)
    for i in range(0, half_N):
        v = [fhat_even[i][0] + fhat_odd[i][0] * cos(w*(i+half_N)) - fhat_odd[i][1] * sin(w*(i+half_N)), fhat_even[i][1] + fhat_odd[i][1] * cos(w*(i+half_N)) + fhat_odd[i][0] * sin(w*(i+half_N))]
        v[0] /= 2
        v[1] /= 2
        res.append(v)

    return res

def naive_ifft(samples):
    if len(samples) < 16:
        return naive_idft(samples)

    f_even = list()
    f_odd = list()
    N = len(samples)
    half_N = int(N / 2)
    w = 2*np.pi/N
    i = 0
    for _ in range(0, half_N):
        f_even.append(samples[i])
        i+=1
        f_odd.append(samples[i])
        i+=1

    fhat_even = naive_ifft(f_even)
    fhat_odd = naive_ifft(f_odd)

    res = list()
    for i in range(0, half_N):
        v = [fhat_even[i][0] + fhat_odd[i][0] * cos(w*i) - fhat_odd[i][1] * sin(w*i), fhat_even[i][1] + fhat_odd[i][1] * cos(w*i) + fhat_odd[i][0] * sin(w*i)]
        v[0] /= 2
        v[1] /= 2
        res.append(v)
    for i in range(0, half_N):
        v = [fhat_even[i][0] + fhat_odd[i][0] * cos(w*(i+half_N)) - fhat_odd[i][1] * sin(w*(i+half_N)), fhat_even[i][1] + fhat_odd[i][1] * cos(w*(i+half_N)) + fhat_odd[i][0] * sin(w*(i+half_N))]
        v[0] /= 2
        v[1] /= 2
        res.append(v)

    return res

def improved_dft(samples):
    f_even = list()
    f_odd = list()
    N = len(samples)
    half_N = int(N / 2)
    w = -2*np.pi/N
    i = 0
    for _ in range(0, half_N):
        f_even.append(samples[i])
        i+=1
        f_odd.append(samples[i])
        i+=1

    fhat_even = naive_dft(f_even)
    fhat_odd = naive_dft(f_odd)
    res = list()
    for i in range(0, half_N):
        v = [fhat_even[i][0] + fhat_odd[i][0] * cos(w*i) - fhat_odd[i][1] * sin(w*i), fhat_even[i][1] + fhat_odd[i][1] * cos(w*i) + fhat_odd[i][0] * sin(w*i)]
        res.append(v)
    for i in range(0, half_N):
        v = [fhat_even[i][0] + fhat_odd[i][0] * cos(w*(i+half_N)) - fhat_odd[i][1] * sin(w*(i+half_N)), fhat_even[i][1] + fhat_odd[i][1] * cos(w*(i+half_N)) + fhat_odd[i][0] * sin(w*(i+half_N))]
        res.append(v)

    return res

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

def compute_PSD(samples, dt):
    freq_list = list()
    power_list = list()
    i = 0
    for sample in samples:
        power_list.append([multiply_complex_by_conjugate(sample) / len(samples), 0])
        freq_list.append(1/(dt*len(samples)) * i)
        i+=1

    return power_list, freq_list

def add_padding(indices, samples, delta):
    last = indices[len(samples)-1]
    for i in range(len(samples), 2**(int(log2(len(samples)))+1)):
        last += delta
        indices.append(last)
        samples.append(0)

if __name__ == '__main__':
    generate_omega_matrix(omega_matrix_size)
    generate_inverse_omega_matrix(omega_matrix_size)

    vec = list()
    for i in range(2**19):
        vec.append(i)
    fhat = np.fft.fft(vec, len(vec))
    #vec = naive_fft(vec)

    vec = naive_iterative_fft(vec)
    for i in range(len(fhat)):
        if abs(vec[i][0] - fhat[i].real) > 1e-3:
            print("Fucked at index {}".format(i), vec[i], fhat[i])
            break
    import sys
    sys.exit(0)

    random.seed(42)
    max_gaussian = gaussian(gaussian_target, gaussian_target, gaussian_variance)

    #gaussian_test()

    indices_list, sample_list = generate_signal_from_list_of_freq([120, 50, 192, 1200, 4000], 0, 1, delta)
    noisy_sample_list = add_noise_to_graph(sample_list, 10)
    add_padding(indices_list, sample_list, delta)

    #fhat_ref = np.fft.fft(sample_list, len(sample_list))
    #fhat = naive_dft(sample_list)
    #fhat = improved_dft(sample_list)

    fhat = naive_fft(sample_list)

    power_list, freq_list = compute_PSD(fhat, delta)
    max_indice = int(np.floor(len(freq_list)/2))
    freq = (1/(delta*len(fhat))) * np.arange(len(fhat))
    plt.plot(freq_list, [power[0] for power in power_list])
    plt.xlim(freq_list[1], freq_list[max_indice])
    plt.ylim(0, max([power[0] for power in power_list][1:]))
    plt.show()
    #for a in range(0, len(power_list)):
    #    power_list[a][0] = 0 if power_list[a][0] < 120 else power_list[a][0]
    #for a in range(100, len(power_list)):
    #    power_list[a] = 0
    #plt.plot(freq_list, [power[0] for power in power_list])
    plt.plot(freq_list, [power[0] for power in power_list])
    plt.xlim(freq_list[1], freq_list[max_indice])
    plt.ylim(0, max([power[0] for power in power_list][1:]))
    plt.show()

    ifft = matrix_ifft(power_list)

    # actually only half the sampling rate is usable
    plt.plot(indices_list, [item[0] for item in idft], color='r')
    plt.plot(indices_list, [item[0] for item in ifft], color='b')
    #plt.plot(indices_list, sample_list, color='r')
    plt.xlim(indices_list[0], indices_list[-1])
    plt.show()
