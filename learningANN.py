import os
import sounddevice as sd
import numpy as np
import scipy.signal as sg
import scipy.io.wavfile as wav


def name_wav():
    directory  = r'/home/adminmaster/Music/wav'
    files = os.listdir(directory)
    wav_file = filter(lambda x: x.endswith('.wav'), files)
    list_good = []
    list_fail = []
    for el in wav_file:
        wav_name = "/home/adminmaster/Music/wav/" + os.path.basename(el)
        if str(el).find('_good_') > -1 :
            list_good += [parsing_wav(wav_name)]
            print('good')
        elif str(el).find('_fail_') > -1 :
            # parsing_wav(wav_name)
            list_fail += [parsing_wav(wav_name)]
            print('fail')
    print(list_good)
    print(list_fail)


def parsing_wav(wav_name):
    print('input par')
    sample_rate, samples = wav.read(str(wav_name))
    frequencies, times, spectrogram = sg.spectrogram(samples, sample_rate, nfft=4096)

    # more brightness, contrast
    for s1 in spectrogram:
        for i in range(len(s1)):
            s1[i] = np.arctan((s1[i]**0.4)/10)

    # 2d -> 1d
    i1size = spectrogram.shape[0]
    i2size = spectrogram.shape[1]
    spectrogram2 = np.zeros((i1size))
    i1 = 0
    while i1 < i1size:
        i2 = 0
        while i2 < i2size:
            spectrogram2[i1] = spectrogram2[i1] + spectrogram[i1, i2]
            i2 = i2 + 1
        i1 = i1 + 1
    b = [spectrogram2[i] for i in range(len(spectrogram2))]
    freq_step = 22100/2048
    # return str(freq_step * b.index(max(b[0:200]))) + 'Hz, ' + str(freq_step * b.index(max(b[300:500]))) + 'Hz, ' + str(freq_step * b.index(max(b[600:800]))) + 'Hz, ' + str(freq_step * b.index(max(b[1200:1500]))) + 'Hz, ' + str(freq_step * b.index(max(b[1600:1900]))) + 'Hz'
    print('output wav 1')
    return [str(freq_step * b.index(max(b[0:200]))), str(freq_step * b.index(max(b[300:500]))), str(freq_step * b.index(max(b[600:800]))), str(freq_step * b.index(max(b[1200:1500]))), str(freq_step * b.index(max(b[1600:1900])))]
    print('output wav 2')


name_wav()


