import numpy as np
from scipy.io import wavfile
from sklearn import mixture
import bob

#get MFCC
rate = 16000
win_length_ms = 20 # The window length of the cepstral analysis in milliseconds
win_shift_ms = 10 # The window shift of the cepstral analysis in milliseconds
n_filters = 24 # The number of filter bands
n_ceps = 13 # The number of cepstral coefficients
f_min = 0. # The minimal frequency of the filter bank
f_max = 4000. # The maximal frequency of the filter bank
delta_win = 1 # The integer delta value used for computing the first and second order derivatives
pre_emphasis_coef = 0.97 # The coefficient used for the pre-emphasis
dct_norm = True # A factor by which the cepstral coefficients are multiplied
mel_scale = True # Tell whether cepstral features are extracted on a linear (LFCC) or Mel (MFCC) scale

c = bob.ap.Ceps(rate, win_length_ms, win_shift_ms, n_filters, n_ceps, f_min, f_max, delta_win, pre_emphasis_coef, mel_scale, dct_norm)
c.with_delta = True
c.with_delta_delta = True
c.with_energy = True

track = 'example.wav'
rate, signal =  wavfile.read(track)    
signal = signal[:, 1] #for 2 channels
signal = np.cast['float'](signal) #vector should be in **float**

example_mfcc = c(signal) #mfcc + mfcc' + mfcc''
example_gmm = mixture.GaussianMixture(n_components = 10, max_iter=150).fit(example_mfcc)
np.save('example_gmm.npy', example_gmm)
