import numpy as np
from scipy.io import wavfile
import bob
from sklearn import mixture
from math import e, pi, log



# Base Function
def get_likelihood(X, means, cov, w):
    N, f = X.shape
    P = []
    for vector_index in range(N):
        weighted_prob = []
        for i in range(0,10):
            gaussian = (w[i])*np.exp(-0.5*np.dot(np.dot((X[vector_index]-means[i]), (np.linalg.inv(cov[i]))), 
                (np.transpose(X[vector_index]-means[i]))))/(((2*pi)**(f/2))*((np.linalg.det(cov[i]))**0.5))
            weighted_prob.append(gaussian)
        P.append(sum(weighted_prob))
    S = (1/N)*sum(log(j) for j in filter(lambda a: a!=0, P))
    return S



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
#signal = signal[:, 1] #for 2 channels
signal = np.cast['float'](signal) #vector should be in **float**
example_mfcc = c(signal) #mfcc + mfcc' + mfcc''
example_gmm = mixture.GaussianMixture(n_components = 10, max_iter=150).fit(example_mfcc) #voice model - золотой стандрат 


#example_gmm имеет три атрибита - means_, covariances_, weights_
#сохраняем в дикеркорию в формате npy
np.save('example_gmm.means_', example_gmm.means_)
np.save('example_gmm.covariances_', example_gmm.covariances_)
np.save('example_gmm.weights_', example_gmm.weights_)


#загружаем 
means_ = np.load('example_gmm.means_.npy')
covariances_ = np.load('example_gmm.covariances_.npy')
weights_ = np.load('example_gmm.weights_.npy')
    
new_unknown_mfcc = np.load('new_unknown_gmm_data.npy') #mfcc новой поступившей записи


#считем близость голосов на записях
final_result = get_likelihood(new_unknown_gmm, means_, covariances_, weights_) 

#при данных настройках threshold = -60
if final_result < threshold:
    print('Верификация личности успешно пройдена')
else:
    print('Личность звонящего не соответствуе личности владельца банковского счета')

