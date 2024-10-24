import tkinter as tk 
from tkinter import ttk 
from PIL import ImageTk, Image
from dtmf import DTMF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.fft import fft
import numpy as np


class DTMFApp(tk.Tk):    
    dtmf = DTMF()
    
    def __init__(self):
        super().__init__()
        
        self.title('DTMF Signal Processing by Kurt Timajo  | CPE4A')
        self.geometry('960x500')
        
        self.imageBg = Image.open('assets/bg.png')
        self.bckEnd = ImageTk.PhotoImage(self.imageBg)
        self.bg = tk.Label(self.master, image=self.bckEnd)
        self.bg.place(x=0,y=0)
        
        self.outputDigit = ""
        
        # 1 2 3 
        self.btn1 = Image.open('assets/btn-1.png')
        self.btnEnd1 = ImageTk.PhotoImage(self.btn1)        
        self.numBtn1 = tk.Button(self, image=self.btnEnd1, relief="flat", command=lambda: self.numClicked(1))
        self.numBtn1.place(x=76,y=190)
        
        self.btn2 = Image.open('assets/btn-2.png')
        self.btnEnd2 = ImageTk.PhotoImage(self.btn2)        
        self.numBtn2 = tk.Button(self, image=self.btnEnd2, relief="flat", command=lambda: self.numClicked(2))
        self.numBtn2.place(x=143,y=190)
        
        self.btn3 = Image.open('assets/btn-3.png')
        self.btnEnd3 = ImageTk.PhotoImage(self.btn3)        
        self.numBtn3 = tk.Button(self, image=self.btnEnd3, relief="flat", command=lambda: self.numClicked(3))
        self.numBtn3.place(x=208,y=190)
        
        # 4 5 6
        self.btn4 = Image.open('assets/btn-4.png')
        self.btnEnd4 = ImageTk.PhotoImage(self.btn4)        
        self.numBtn4 = tk.Button(self, image=self.btnEnd4, relief="flat", command=lambda: self.numClicked(4))
        self.numBtn4.place(x=76,y=255)
        
        self.btn5 = Image.open('assets/btn-5.png')
        self.btnEnd5 = ImageTk.PhotoImage(self.btn5)        
        self.numBtn5 = tk.Button(self, image=self.btnEnd5, relief="flat", command=lambda: self.numClicked(5))
        self.numBtn5.place(x=143,y=255)
        
        self.btn6 = Image.open('assets/btn-6.png')
        self.btnEnd6 = ImageTk.PhotoImage(self.btn6)        
        self.numBtn6 = tk.Button(self, image=self.btnEnd6, relief="flat", command=lambda: self.numClicked(6))
        self.numBtn6.place(x=208,y=255)
        
        # 7 8 9
        self.btn7 = Image.open('assets/btn-7.png')
        self.btnEnd7 = ImageTk.PhotoImage(self.btn7)        
        self.numBtn7 = tk.Button(self, image=self.btnEnd7, relief="flat", command=lambda: self.numClicked(7))
        self.numBtn7.place(x=76,y=320)
        
        self.btn8 = Image.open('assets/btn-8.png')
        self.btnEnd8 = ImageTk.PhotoImage(self.btn8)        
        self.numBtn8 = tk.Button(self, image=self.btnEnd8, relief="flat", command=lambda: self.numClicked(8))
        self.numBtn8.place(x=143,y=320)
        
        self.btn9 = Image.open('assets/btn-9.png')
        self.btnEnd9 = ImageTk.PhotoImage(self.btn9)        
        self.numBtn9 = tk.Button(self, image=self.btnEnd9, relief="flat", command=lambda: self.numClicked(9))
        self.numBtn9.place(x=208,y=320)
        
        self.btn0 = Image.open('assets/btn-0.png')
        self.btnEnd0 = ImageTk.PhotoImage(self.btn0)        
        self.numBtn0 = tk.Button(self, image=self.btnEnd0, relief="flat", command=lambda: self.numClicked(0))
        self.numBtn0.place(x=143,y=385)        
   
        self.outputDigitLabel  = tk.Label(self, font=('Arial bold', 30))
        self.outputDigitLabel.config(bg='#1D0669', fg= "white", justify="center")
        self.outputDigitLabel.place(x=160,y=122)
        
        
        self.fig1, self.ax1 = plt.subplots(figsize=(6, 2), dpi=100)
        self.freqCanvas = FigureCanvasTkAgg(self.fig1, master=self)
        self.freqCanvas.get_tk_widget().place(x=330, y=285)
        
        self.fig2, self.ax2 = plt.subplots(figsize=(6, 2), dpi=100)
        self.timeCanvas = FigureCanvasTkAgg(self.fig2, master=self)
        self.timeCanvas.get_tk_widget().place(x=330, y=80)
        
    def numClicked(self, num):       
        # encode
        tone = self.dtmf.encode(str(num))
        self.dtmf.play(tone)        
        # decode
        decoded = self.dtmf.decode(tone)
        self.outputDigit = decoded[0] 
        self.outputDigitLabel.config(text=decoded[0])
        
        self.showFreqDomain(signal=tone)
        self.showTimeDomain(signal=tone)
        
        
    def showFreqDomain(self, signal, sampling_rate=8000):
        N = 2400 
        fft_result = np.abs(fft(signal[0:N]))

        self.ax1.clear()

        self.ax1.plot(fft_result[0:1000])  
        self.ax1.set_title(f"Frequency-Domain Representation of Digit {self.outputDigit}")
        self.ax1.set_xlabel("Frequency (Hz)")
        self.ax1.set_ylabel("Magnitude")
        self.ax1.grid(True)

        self.freqCanvas.draw()
    
    def showTimeDomain(self, signal):
        self.ax2.clear()

        self.ax2.plot(signal[:100])  
        self.ax2.set_title(f"Time-Domain Representation of Digit {self.outputDigit}")
        self.ax2.set_xlabel("Sample")
        self.ax2.set_ylabel("Amplitude")
        self.ax2.grid(True)

        self.timeCanvas.draw()

app = DTMFApp()
app.mainloop()