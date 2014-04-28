import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import csv
import collections
import pylab

#here it works better for me if I import pylab and then use pylab.show()
#instead of plt.show()


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
	filteredSignal = [0]
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
def readWave(soundFile):
	spf = wave.open(soundFile,'r')

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
	#plt.figure(1)
	#plt.title('Signal Wave...')
	#plt.plot(Time,signal)
	return (signal, fs)

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
	#print "transforming"
	#omega=np.linspace(-20000, 20000, num=len(sig))
	tran = abs(np.fft.fft(sig))
	omega = np.fft.fftfreq(len(tran), 1./fs)
	
	plt.figure(2)
	plt.clf()
	plt.title('Fourier Transform of Signal')
	plt.plot(omega, tran)
	#plt.axis([420, 460, 0 , 5*10^7])
	return (tran, omega)

def categorize(tran, omeg, maxVal):
#create a dictionary of frequency to note names
	freqCont = []
	#print "filtering"
	threshold = 1000000
	for noteFreq in noteDictionary.keys():
		noteTransform = filterNote(float(noteFreq),omeg,tran)
		#includeNote = threshold(noteTransform)
		if noteTransform > threshold:
			#print noteDictionary[noteFiltered]
			freqCont.append(noteDictionary[noteFreq])
	return freqCont
                

"""Main"""
print "Creating data structure for notes"
noteDictionary = makeNoteDictionary('Notes.csv')
print "reading file"
[wholesignal, fs] =  readWave('SoundFiles/52_piano_notes.wav')
maxSignalVal = np.max(wholesignal)
print (maxSignalVal)
[signal, fs] = readWaveSplit('SoundFiles/52_piano_notes.wav') #returns signal and sampling frequency

print "Categorizing notes"
notes = [['-1']]
for signalSection in signal:
	[transform,omega] = takeTransform(signalSection, fs)
	#plt.show()
	noteSection = categorize(transform, omega, maxSignalVal)
	print(max(transform))
	print omega[np.where(transform == max(transform))]
	if noteSection:
		pylab.show()
		print "not empty!"
		plt.show()
		print noteSection
		if (noteSection.sort() != notes[-1].sort()):
			notes.append(noteSection)
			print "new note!"
			print noteSection

print notes

	
#[transform, omega] = takeTransform(signal, fs) #returns transform and frequency
#frequencyContent = categorize(transform, omega) #returns frequency content of note
#plt.show()


