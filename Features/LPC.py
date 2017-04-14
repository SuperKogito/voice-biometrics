import audiolazy
from scipy.io import wavfile
import numpy as np
from scipy.fftpack import fft
from math import cos, pi


def hamming(n):
    """Создаем окно Хэмминга из n точек """
    return 0.54 - 0.46 * cos(2 * pi / n * (np.arange(n) + 0.5))


class LPCExtractor(object):

    def __init__(self, fs, win_length_ms, win_shift_ms, n_lpc, pre_emphasis_coef):
        self.PRE_EMPH = pre_emphasis_coef
        self.n_lpc = n_lpc
        #self.n_lpcc = n_lpcc + 1

        self.FRAME_LEN = int(float(win_length_ms) / 1000 * fs)
        self.FRAME_SHIFT = int(float(win_shift_ms) / 1000 * fs)
        self.window = hamming(self.FRAME_LEN)


    def get_lpc(self, signal):
        lpc = audiolazy.lpc(signal, self.n_lpc).numerator
        return lpc[1:]
        #lpcc = lpc_to_lpcc(lpc_, 23, 23)
        #return lpcc


    def lpc_to_lpcc(self, lpc):
        lpcc = zeros(self.n_lpcc)
        lpcc[0] = lpc[0]
        for n in range(1, self.n_lpc):
            lpcc[n] = lpc[n]
            for l in range(0, n):
                lpcc[n] += lpc[l] * lpcc[n - l - 1] * (n - l) / (n + 1)
        for n in range(self.n_lpc, self.n_lpcc):
            lpcc[n] = 0
            for l in range(0, self.n_lpc):
                lpcc[n] += lpc[l] * lpcc[n - l - 1] * (n - l) / (n + 1)
        return -lpcc[1:]


    def extract(self, fs, signal):
        frames = (len(signal) - self.FRAME_LEN) / self.FRAME_SHIFT + 1
        frames = int(frames)
        feature = []
        for f in range(frames):
            frame = signal[f * self.FRAME_SHIFT : f * self.FRAME_SHIFT + self.FRAME_LEN] * window
            frame[1:] -= frame[:-1] * self.PRE_EMPH
            if self.get_lpc(frame):
                feature.append(self.get_lpc(frame))

        feature = np.array(feature)
        #feature[np.isnan(feature)] = 0

        return feature
    
    


def extract(fs, signal):
    ret = LPCExtractor(fs, win_length_ms, win_shift_ms, n_lpc, pre_emphasis_coef).extract(signal)
    return ret


#def extract(fs, signal, win_length_ms, win_shift_ms, n_lpc, pre_emphasis_coef):
    #ret = LPCExtractor(fs, win_length_ms, win_shift_ms, n_lpc, pre_emphasis_coef)
    #return ret


if __name__ == "__main__":
    extractor = LPCCExtractor(8000)


