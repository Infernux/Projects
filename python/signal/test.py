#!/usr/bin/python3

import unittest

import numpy as np
from signal_tools import generate_signal_from_list_of_freq, compute_PSD, naive_dft, naive_idft

delta = 1e-3
error = 1e-8

def convertNumpyComplexToMyComplex(array):
    val_list = list()
    for v in array:
        val_list.append([v.real, v.imag])

    return val_list

class TestDFT(unittest.TestCase):
    def test_dft(self):
        # generate data
        indices_list, sample_list = generate_signal_from_list_of_freq([120, 50], 0, 1, delta)

        ref_fhat  = np.fft.fft(sample_list, len(sample_list)) #compute fft using numpy
        test_fhat = naive_dft(sample_list) #compute dft using my own function

        for idx in range(0, len(sample_list)):
            self.assertTrue(abs(ref_fhat[idx].real - test_fhat[idx][0]) < error)
            self.assertTrue(abs(ref_fhat[idx].imag - test_fhat[idx][1]) < error)

    def test_idft(self):
        # generate data
        indices_list, sample_list = generate_signal_from_list_of_freq([120, 50], 0, 1, delta)
        ref_fhat  = np.fft.fft(sample_list, len(sample_list)) #compute fft using numpy
        test_fhat = naive_dft(sample_list) #compute dft using my own function
        ref_f = np.fft.ifft(ref_fhat)
        test_f = naive_idft(test_fhat) #compute dft using my own function

        for idx in range(0, len(sample_list)):
            self.assertTrue(abs(ref_f[idx].real - test_f[idx][0]) < error)
            self.assertTrue(abs(ref_f[idx].imag - test_f[idx][1]) < error)

class TestPSD(unittest.TestCase):
    def test_PSD(self):
        #generate data
        indices_list, sample_list = generate_signal_from_list_of_freq([120, 50], 0, 1, delta)
        #compute the fft
        fhat = np.fft.fft(sample_list, len(sample_list))
        myfhat = convertNumpyComplexToMyComplex(fhat)

        power_list, freq_list = compute_PSD(myfhat, delta)
        PSD = fhat * np.conj(fhat) / len(fhat)
        for idx in range(0, len(power_list)):
            self.assertTrue(abs(power_list[idx][0] - PSD[idx].real) < error)
            self.assertTrue(abs(power_list[idx][1] - PSD[idx].imag) < error)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPSD)
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
