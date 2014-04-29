import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import csv
import collections
import pylab

#here it works better for me if I import pylab and then use pylab.show()
#instead of plt.show()
FILE = 'SoundFiles/Piano.wav'

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
	maxVal = max(filteredSignal)
	return maxVal

#Open the wave file

def readWaveSplit(soundFile):
	spf = wave.open(soundFile,'r')

	#Extract Raw Audio from Wav File
	print "reading frames"

	lenSignal = spf.getnframes()
	framesinSection = 1000

	sectionFrames = []
	fs = spf.getframerate()


	for section in range(lenSignal/framesinSection):
		#print section
		tempSignal = spf.readframes(framesinSection)
		tempSignal = np.fromstring(tempSignal, 'Int16')
		sectionFrames.append(tempSignal)
		#print (tempSignal)
	#noise = np.average(sectionFrames[0])
	return (sectionFrames, fs)

def takeTransform(sig, fs):
	#Transforms yay!
	#print "transforming"
	tran = abs(np.fft.fft(sig))
	omega = np.fft.fftfreq(len(tran), 1./fs)
	
	plt.figure(2)
	plt.clf()
	plt.title('Fourier Transform of Signal')
	plt.plot(omega, tran)
	return (tran, omega)

def categorize(tran, omeg, noiseAmp):
#create a dictionary of frequency to note names
	noteString = []
	#print "filtering"
	threshold = 10000*noiseAmp
	for noteFreq in noteDictionary.keys():
		noteTransform = filterNote(float(noteFreq),omeg,tran)
		#includeNote = threshold(noteTransform)
		if noteTransform > threshold:
			#print noteDictionary[noteFiltered]
			noteString.append(noteDictionary[noteFreq])
	return noteString
                

"""Main"""
print "Creating data structure for notes"
noteDictionary = makeNoteDictionary('Notes.csv')
print "reading file"
[signal, fs] = readWaveSplit(FILE) #returns signal and sampling frequency

print "Categorizing notes"
notes = [['-1']]
first = True
[transform,omega] = takeTransform(signal[0], fs)
trimmed = np.trim_zeros(np.absolute(transform))
noiseAmplitude = np.average(trimmed)


for signalSection in signal[1:]:
	[transform,omega] = takeTransform(signalSection, fs)
	noteSection = categorize(transform, omega, noiseAmplitude)
	if noteSection:
		if first:
			pylab.show()
			first = False
		print "not empty!"
		print noteSection
		print(max(transform))
		print omega[np.where(transform == max(transform))]
		if (noteSection.sort() != notes[-1].sort()):
			plt.show()
			notes.append(noteSection)
			print "new note!"
			print noteSection

print notes

