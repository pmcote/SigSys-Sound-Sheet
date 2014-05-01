import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import csv
import collections
import pylab

#The name of the sound file that we are analyzing
FILE = 'SoundFiles/Piano.wav'

#Make a dictionary that maps the strings of note frequency (Hz) to note names
def makeNoteDictionary(fileName):
	#Create a blank dictionary
	noteDictionary = {}
	#Open the csv file
	with open(fileName, 'rb') as  csvfile:
		noteReader = csv.reader(csvfile,delimiter = ',',)
		for row in noteReader:
			#Add frequency, note name pairs to the dictionary
			noteDictionary[row[1]] = row[0]
	#Return the frequency note paris
	return noteDictionary

#return maximum value of the transform for frequencies in range min to max
def filterNote(noteFreq, omega, tran):
#This filter exists in the frequency domain. The input is the FFT of the signal
	#The witdth of the pass band of the band pass filter
	filterRange = .03*noteFreq
	#Initializing the maximum value
	maxVal = 0;
	#The low end of the pass band
	minFreq = noteFreq - filterRange
	#The high end of the pass band
	maxFreq = noteFreq + filterRange
	#Initialize the filtered signal list
	filteredSignal = [0]
	#Go through the frequencies and add the values of the transfom if they're in the right range
	for index, frequency in enumerate(omega):
		if (frequency > minFreq and frequency < maxFreq):
			filteredSignal.append(tran[index])
	maxVal = max(filteredSignal)

	#Return the maximum value of the transform within the filtered range
	return maxVal

#Open the wave file

def readWaveSplit(soundFile):
	#Open the wave sound file
	spf = wave.open(soundFile,'r')

	#Extract Raw Audio from Wav File
	print "reading frames"
	#get the number of frames
	lenSignal = spf.getnframes()
	#number of frames in each "section" that we're analyzing
	framesinSection = 1000
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
		 
	return (sectionFrames, fs)

def takeTransform(sig, fs):
	#Transforms yay!
	#print "transforming"
	#Transform is the magnitude of the FFT of the signal
	tran = abs(np.fft.fft(sig))
	#The frequencies corresponding to the transform
	omega = np.fft.fftfreq(len(tran), 1./fs)
	
	#Return the transform and frequency
	return (tran, omega)

#Decide if a signal contains a certain note
def categorize(tran, omeg, noiseAmp):
	#Intialize variables
	noteString = []
	threshold = 9000*noiseAmp
	#Filter for each note, and if the max value is above the threshold, add the note to the list of notes
	for noteFreq in noteDictionary.keys():
		noteTransform = filterNote(float(noteFreq),omeg,tran)
		if noteTransform > threshold:
			noteString.append(noteDictionary[noteFreq])
	return noteString


                

"""Main"""
print "Creating data structure for notes"
#Create note dictionary
noteDictionary = makeNoteDictionary('Notes.csv')
print "reading file"
#read the file
[signal, fs] = readWaveSplit(FILE) #returns signal and sampling frequency

print "Categorizing notes"
#intialize a list of detected notes
detectedNotes = []

first = True
#Take the transform of initial signal
[transform,omega] = takeTransform(signal[0], fs)
#get rid of all the zeros
trimmed = np.trim_zeros(np.absolute(transform))
#calculate the average noise (without all the zeros)
noiseAmplitude = np.average(trimmed)

#Analyze each section for notes
for signalIndex,signalSection in enumerate(signal[1:]):
	print '%d out of %d' %(signalIndex, len(signal))
	#take the transform of each section
	[transform,omega] = takeTransform(signalSection, fs)
	#find all the notes in each section
	noteSection = categorize(transform, omega, noiseAmplitude)
	#if there are notes
	if noteSection:
		#add the notes to the detected notes list
		detectedNotes.append(noteSection)
		if first:
			plt.figure(1)
			plt.plot(omega,transform)
			pylab.show()
			first = False
		print "not empty!"
		print noteSection
		print(max(transform))
		print omega[np.where(transform == max(transform))]
for potentialNotes in detectedNotes(5:):





