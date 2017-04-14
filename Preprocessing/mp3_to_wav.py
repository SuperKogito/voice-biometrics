from pydub import AudioSegment
AudioSegment.converter  = 'C:/ffmpeg/bin/ffmpeg.exe'
from scipy.io import wavfile
import re
import glob
import os

def mp3_to_wav(win, wout):
    '''Convert mp3 to wav'''
    sound = AudioSegment.from_mp3(win)
    sound.export(wout, format='wav')

    
def get_one_channel(wout):
    '''Remove one of two channels'''
    fs, signal =  wavfile.read(wout)
    one_channel_signal = signal[:, 0]
    wavfile.write(wout, fs, one_channel_signal)
    
    
def monophonic(signal):
    if signal.ndim > 1:
        signal = signal[:,0]
    return signal

    
def move_to(file, directory):
    os.rename(file, directory + '/' + file) #перемещаем файл в папку
    
    
datafolder = '/Users/1/Desktop/imposter/'
folders = os.listdir(datafolder)[:1]

for folder in folders:
    wavfolder = datafolder + '/' + folder + '/' + 'wav' #путь до папки wav
    rowfolder = datafolder + '/' + folder + '/' + 'row' #путь до папки row
    
    os.makedirs(rowfolder) #создаем директории
    os.makedirs(wavfolder)

    files_in_folder = glob.glob(datafolder + folder + '/*.mp3') #список mp3 файлов в папке
    
    for file in files_in_folder:
        track_name = re.sub('mp3', 'wav', file.split(folder + '\\')[1])
        wav_file = wavfolder + '/' + track_name + '.wav' #путь до wav 
        mp3_to_wav(file, wav_file) #создаем wav 
        get_one_channel(wav_file) #удаляем канал
        
        os.rename(file, rowfolder + '/' + file.split(folder + '\\')[1]) #перемещаем mp3 в row