import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import csv

def makeNoteDictionary(fileName):
#Open the csv file
	noteDictionary = {}
	with open(fileName, 'rb') as  csvfile:
		noteReader = csv.reader(csvfile,delimiter = ',',)
		for row in noteReader:
			#Add frequency, note name pairs to the dictionary
			noteDictionary[row[1]] = row[0]
	return noteDictionary

#return average value of frequencies in range min to max
def filterNote(noteFreq, omega, tran):
	filterRange = .03*noteFreq
	maxVal = 0;
	minFreq = noteFreq - filterRange
	maxFreq = noteFreq + filterRange
	filteredSignal = []
	for index, frequency in enumerate(omega):
		if (frequency > minFreq and frequency < maxFreq):
			filteredSignal.append(tran[index])
	##print len(filteredSignal)
	# if noteFreq == 391.995:
	# 	plt.figure(3)
	# 	plotOmega = np.linspace(minFreq, maxFreq, len(filteredSignal))
	# 	plt.title('Filtered Note')
	# 	plt.plot(plotOmega, filteredSignal)
	# 	plt.axis([minFreq, maxFreq, 0 , 50000])
	maxVal = max(filteredSignal)
	return maxVal

#Open the wave file
def readWave():
	spf = wave.open('SoundFiles/27_5.wav','r')

	#Extract Raw Audio from Wav File
	#Becuase this particular file is too big. 
	#For smaller files, use -1
	print "reading frames"
	signal = spf.readframes(-1)

	#Make the frames into an array of integers
	print "converting to integer array"
	signal = np.fromstring(signal, 'Int16')

	#Get the frame rate of the file
	print "getting frame rate"
	fs = spf.getframerate()

	#Get an array of time values. We know the frame rate
	#And the number of frames, so the array is easy
	Time=np.linspace(0, len(signal)/fs, num=len(signal))

	#Plot the wave
	plt.figure(1)
	plt.title('Signal Wave...')
	plt.plot(Time,signal)
	return (signal, fs)

def takeTransform(sig, fs):
	#Transforms yay!
	print "transforming"
	#omega=np.linspace(-20000, 20000, num=len(sig))
	tran = np.fft.fft(sig)
	omega = np.fft.fftfreq(len(tran), 1./fs)
	
	plt.figure(2)
	plt.title('Fourier Transform of Signal')
	plt.plot(omega, tran)
	#plt.axis([420, 460, 0 , 5*10^7])
	return (tran, omega)

def categorize(tran, omeg):
#create a dictionary of frequency to note names
	freqCont = []
	print "filtering"
	threshold = 10000000
	for noteFiltered in noteDictionary.keys():
		noteTransform = filterNote(float(noteFiltered),omeg,tran)
		#includeNote = threshold(noteTransform)
		if noteTransform > threshold:
			print noteDictionary[noteFiltered]
			freqCont.append(noteDictionary[noteFiltered])
	return freqCont
                

"""Main"""
print "Creating data structure for notes"
noteDictionary = makeNoteDictionary('Notes.csv')
[signal, fs] = readWave() #returns signal and sampling frequency
[transform, omega] = takeTransform(signal, fs) #returns transform and frequency
frequencyContent = categorize(transform, omega) #returns frequency content of note
plt.show()


