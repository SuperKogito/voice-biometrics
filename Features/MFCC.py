import scipy
import numpy as np
import python_speech_features

def delta(feat, N):

    if N < 1:
        raise ValueError('N must be an integer >= 1')
    NUMFRAMES = len(feat)
    denominator = 2 * sum([i**2 for i in range(1, N+1)])
    delta_feat = np.empty_like(feat)
    padded = np.pad(feat, ((N, N), (0, 0)), mode='edge')   # padded version of feat
    for t in range(NUMFRAMES):
        delta_feat[t] = np.dot(np.arange(-N, N+1), padded[t : t+2*N+1]) / denominator   # [t : t+2*N+1] == [(N+t)-N : (N+t)+N+1]
    return delta_feat


def get_mfcc(path, signalpath=None, signal = None, rate=None):
    if path == True:
        rate, signal = scipy.io.wavfile.read(signalpath)
        signal = np.cast['float'](signal)

    mfcc_ = python_speech_features.mfcc(signal, rate, winlen=0.02, winstep=0.01, numcep=13, nfilt=24, nfft=512, 
             lowfreq=0, highfreq=4000, preemph=0.97, ceplifter=0, appendEnergy=True)

    delta_ = delta(mfcc_, 1)
    deltadelta_ = delta(delta_, 1)
    mfcc = np.concatenate((mfcc_, delta_, deltadelta_), axis = 1)
    return mfcc


def get_bob_mfcc(signal):
    signal = np.cast['float'](signal)
    import bob.ap
    c = bob.ap.Ceps(sampling_frequency = 16000, win_length_ms = 20, win_shift_ms = 10, n_filters = 24, 
                    n_ceps = 13, f_min = 0., f_max = 4000., delta_win = 2, 
                    pre_emphasis_coeff = 0.97, dct_norm = True, mel_scale = True)
    c.with_delta = True
    c.with_delta_delta = True
    c.with_energy = True
    mfcc = c(signal)
    return mfcc