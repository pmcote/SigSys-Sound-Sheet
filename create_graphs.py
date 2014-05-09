import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import csv
import collections
import pylab

FILE = 'SoundFiles/scale_and_chord.wav'

def readWave(soundFile):
	#Open the wave sound file
	spf = wave.open(soundFile,'r')

	#Extract Raw Audio from Wav File
	signal = spf.readframes(-1)
	signal = np.fromstring(signal, 'Int16')
	fs = spf.getframerate()


	time=np.linspace(0, len(signal)/fs, num=len(signal))

	return (signal, time, fs)

def takeTransform(sig, fs):
	#Transforms yay!
	#print "transforming"
	#Transform is the magnitude of the FFT of the signal
	tran = abs(np.fft.fft(sig))
	#The frequencies corresponding to the transform
	omega = np.fft.fftfreq(len(tran), 1./fs)
	
	#Return the transform and frequency
	return (tran, omega)

def readWaveSplit(soundFile):
	#Open the wave sound file
	spf = wave.open(soundFile,'r')

	#Extract Raw Audio from Wav File
	print "reading frames"
	#get the number of frames
	lenSignal = spf.getnframes()
	#number of frames in each "section" that we're analyzing
	framesinSection = 22050
	#Initialize the list of frames in each section
	sectionFrames = []
	#Get the sampling frequency
	fs = spf.getframerate()

	#Actually read the sound file 1000 frames at a time
	for section in range(lenSignal/framesinSection):
		#Read the frames
		tempSignal = spf.readframes(framesinSection)
		#Convert the frames into a numpy array
		tempSignal = np.fromstring(tempSignal, 'Int16')
		#add the frames into the list of all the frames
		sectionFrames.append(tempSignal)
		 
	return (sectionFrames,fs)

#[signal,time, fs] = readWave(FILE)
#[transform, frequency] = takeTransform(signal,fs)
i = 0
[signalSections, fs] = readWaveSplit(FILE)
[transformChunk, frequencyChunk] = takeTransform(signalSections[i], fs)
timeChunk = np.linspace(0, len(signalSections[i])/fs, num=len(signalSections[i]))

#ENTIRE SOUND FILE TIME
#plt.figure(1)
#plt.title("Sound File in the Time Domain")
#plt.xlabel("Time (s)")
#plt.ylabel("Volume")
#plt.plot(time,signal)

#ENTIRE SOUND FILE TRANSFORM
#plt.figure(2)
#plt.title("Fourier Transform of Entire Sound File")
#plt.xlabel("Frequency (Hz)")
#plt.ylabel("Magnitude of the Transform")
#plt.plot(frequency,transform)

#SECTION 
#Frequency
plt.figure(3)
plt.title("Fourier Transform of Section  (number of frames = 22050)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude of the Transform")
plt.plot(frequencyChunk,transformChunk)

pylab.show()