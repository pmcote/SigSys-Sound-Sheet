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
	filterRange = 10
	minFreq = noteFreq - filterRange
	maxFreq = noteFreq + filterRange
	filteredSignal = []
	for index, frequency in enumerate(omega):
		if (frequency > minFreq and frequency < maxFreq):
			filteredSignal.append(tran[index])
	avgVal = sum(filteredSignal)/len(filteredSignal)
	return avgVal
def filterNoteForPlots(noteFreq, omega, tran):
	filterRange = 10
	minFreq = noteFreq - filterRange
	maxFreq = noteFreq + filterRange
	filteredSignal = []
	for index, frequency in enumerate(omega):
		if (frequency > minFreq and frequency < maxFreq):
			filteredSignal.append(tran[index])
		else:
			filteredSignal.append(0)
	return filteredSignal
#checks if average value from filterNote is within range
def threshhold(avgVal):
        minVal = 10000
        if avgVal > minVal:
                return True
        else:
                return False

#Open the wave file
def readWave():
	spf = wave.open('SoundFiles/beep-01a.wav','r')

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
	return signal

def takeTransform(sig):
	#Transforms yay!
	print "transforming"
	tran = np.fft.fft(sig)
	omega=np.linspace(-20000, 20000, num=len(tran))
	plt.figure(2)
	plt.title('Fourier Transform of Signal')
	plt.plot(omega, tran)
	return tran

def categorize(tran):
#create a dictionary of frequency to note names
	print "Creating data structure for notes"
	noteDictionary = makeNoteDictionary('Notes.csv')
	omega=np.linspace(-20000, 20000, num=len(tran))
	freqCont = []
	print "filtering"
	for noteFiltered in noteDictionary.keys():
		noteTransform = filterNote(float(noteFiltered),omega,tran)
		includeNote = threshhold(noteTransform)
		if includeNote:
			freqCont.append(noteDictionary[noteFiltered])
	return freqCont
                
#plt.figure(3)
#plt.title('Filtered Note')
#plt.plot(omega,noteTransform)

"""Main"""
signal = readWave()
transform = takeTransform(signal)
frequencyContent = categorize(transform)
print frequencyContent

plt.show()


