from scipy.io import wavfile as wav
import numpy as np

def unite(file_names, root=None):
    '''Соединяет несколько записей в одну'''
    united_version = list()
    for file in file_names:
        if root:
            rate, f = wav.read(root + file)
        rate, f = wav.read(file)
        united_version = united_version + f.tolist()  #соединяем файлы   
    return united_version


def get_parts(start, end, signal=None, rate=None, filepath=None, root=None):
    '''Выделяет нужный сегмант записи
        start - секунда начала сегмента
        end - секунда конца сегмента '''
    if filepath:
        if root:
            rate, signal = wav.read(root + filepath)
        rate, signal = wav.read(filepath)
        
    part = signal[start*rate : end*rate] #выделяем сегмент записи
    return np.asarray(part)