## Found code from: http://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

#find max frequencies, return them in order
##The problem is that there are hundreds of indeces needed to be deleted for each value
def maxFreq(transform, Omega):
    freq = [10001]
    while abs(freq[-1]) > 10000:   
        maxInd = np.argmax(abs(transform[0:len(transform)/2]))
        indRange = np.linspace(maxInd -10, maxInd + 10, 21)    
        freq.append(Omega[maxInd])
        transform = np.delete(transform, indRange)
        Omega = np.delete(Omega, indRange)
    return freq[1:]

#Open the wave file
spf = wave.open('beep-01a.wav','r')

#Extract Raw Audio from Wav File
#Becuase this particular file is too big. 
#For smaller files, use -1
signal = spf.readframes(-1)
#Make the frames into an array of integers
signal = np.fromstring(signal, 'Int16')
#Get the frame rate of the file
fs = spf.getframerate()

#Get an array of time values. We know the frame rate
#And the number of frames, so the array is easy
Time=np.linspace(0, len(signal)/fs, num=len(signal))

#Plot the wave
plt.figure(1)
plt.title('Signal Wave...')
plt.plot(Time,signal)
#plt.xlim([3.1,3.105])

#Transforms yay!
transform = np.fft.fft(signal)
Omega=np.linspace(-20000, 20000, num=len(transform))
plt.figure(2)
plt.title('Fourier Transform of Signal')
plt.plot(Omega, transform)
print maxFreq(transform, Omega)

plt.show()






    





