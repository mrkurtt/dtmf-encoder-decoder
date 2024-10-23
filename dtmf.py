import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
import sounddevice as sd

class DTMF:
    Fs = 8000
    dtmf_mapping = {
        '1' : (697, 1209),
        '2' : (697, 1336),
        '3' : (697, 1477),
        '4' : (770, 1209),
        '5' : (770, 1336),
        '6' : (770, 1477),
        '7' : (852, 1209),
        '8' : (852, 1336),
        '9' : (852, 1477),
        '*' : (941, 1209),
        '0' : (941, 1336),
        '#' : (941, 1477)
    }
    
    def __init__(self):
        pass
    
    def encode(self, number):
        m = 0.5 #length of each tone
        s = 0.2 #space between tones
        x = np.array([])
        n = np.arange(0, int(m*self.Fs))
        for num in number:
            p = np.sin(2*np.pi*(self.dtmf_mapping[num][0]/self.Fs)*n) + np.sin(2*np.pi*(self.dtmf_mapping[num][1]/self.Fs)*n)
            space = np.zeros(int(s*self.Fs))
            x = np.concatenate((x, p, space))
        return x
    
    def decode(self, tone, edges=None):
        L_Freqs = np.array([697.0, 770.0, 852.0, 941.0])
        H_Freqs = np.array([1209.0, 1336.0, 1477.0])
        KEYS = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['*', '0', '#']]

        L_RANGE = (680.0, 960.0)
        H_RANGE = (1180.0, 1500.0)

        number = []
        if edges is None:
            edges = self.split_dtmf(tone)
        for edge in edges:
            #compute dft of tone segment
            X = np.abs(fft(tone[edge[0]:edge[1]]))
            N = len(X)
            res = float(self.Fs)/N

            #look for peak in low frequency range
            a = int(L_RANGE[0]/res)
            b = int(L_RANGE[1]/res)
            lo = a + np.argmax(X[a:b])

            #look for peak in high frequency range
            a = int(H_RANGE[0]/res)
            b = int(H_RANGE[1]/res)
            hi = a + np.argmax(X[a:b])

            row = np.argmin(abs(L_Freqs - lo*res))
            col = np.argmin(abs(H_Freqs - hi*res))

            number.append(KEYS[row][col])
            return number
        
    def split_dtmf(self, x, win = 240, th= 200):
        edges = []
        w = np.reshape(x[:int(len(x)/win)*win], (-1, win))
        w_e = np.sum(w*w, axis = 1)
        L = len(w_e)

        idx = 0
        while idx<L:
            while idx < L and w_e[idx] < th:
                idx = idx + 1            
            if idx >= L:
                break
            i = idx
            while i < L and w_e[i] > th:
                i = i + 1
            edges.append((idx*win, i*win))
            idx = i

        return edges

    def play(self, tone):
        sd.play(tone, self.Fs)
    
    def showTimeDomain(self, tone):
        plt.figure(figsize=(15, 4))
        plt.plot(tone[:100])
        plt.title(f"Time-Domain Representation of the DTMF Signal (First 100 Samples)")
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()
        
    def showFrequencyDomain(self, tone):
        N=2400
        fft_result = np.abs(fft(tone[0:N]))

        plt.figure(figsize=(10, 4))
        plt.plot(fft_result[0:1000])  
        plt.title("Frequency-Domain Representation of the DTMF Signal (FFT)")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.grid(True)
        plt.show()