import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

def readWaveSplit(soundFile):
	spf = wave.open(soundFile,'r')

	#Extract Raw Audio from Wav File
	#Becuase this particular file is too big. 
	#For smaller files, use -1
	print "reading frames"

	lenSignal = spf.getnframes()
	framesinSection = 500

	sectionFrames = []
	fs = spf.getframerate()

	for section in range(lenSignal/framesinSection):
		#print section
		tempSignal = spf.readframes(framesinSection)
		tempSignal = np.fromstring(tempSignal, 'Int16')
		sectionFrames.append(tempSignal)
		#print (tempSignal)
	return (sectionFrames, fs)

def takeTransform(sig, fs):
	#Transforms yay!
	print "transforming"
	#omega=np.linspace(-20000, 20000, num=len(sig))
	tran = abs(np.fft.fft(sig))
	omega = np.fft.fftfreq(len(tran), 1./fs)
	
	plt.figure(2)
	plt.title('Fourier Transform of Signal')
	plt.plot(omega, tran)
	plt.show()
	#plt.axis([420, 460, 0 , 5*10^7])
	return (tran, omega)


[signal, fs] = readWaveSplit('SoundFiles/52_piano_notes.wav')
print len(signal)


#numFrames = 44100

#lenSignal = len(signal)

#numSlices = int(len(signal)/numFrames)

#splitSignal = np.array_split(signal,numSlices)


#print(len(splitSignal))

#for section in splitSignal:
	#takeTransform(section, fs)



