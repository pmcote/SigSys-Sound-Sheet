import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import csv
import collections
import pylab
from operator import itemgetter


#The name of the sound file that we are analyzing
FILE = 'SoundFiles/scale_and_chord.wav'

#Make a dictionary that maps the strings of note frequency (Hz) to note names
def makeNoteDictionary(fileName):
	#Create a blank dictionary
	noteDictionary = {}
	noteDictionaryNoteIndex = {}
	#Open the csv file
	with open(fileName, 'rb') as  csvfile:
		noteReader = csv.reader(csvfile,delimiter = ',',)
		for row in noteReader:
			#Add frequency, note name pairs to the dictionary
			noteDictionary[row[1]] = row[0]
			noteDictionaryNoteIndex[row[0]] = row[1]
	#Return the frequency note paris
	return (noteDictionary,noteDictionaryNoteIndex)

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

def readWaveSplit(soundFile, framesinSection):
	#Open the wave sound file
	spf = wave.open(soundFile,'r')

	#Extract Raw Audio from Wav File
	print "reading frames"
	#get the number of frames
	lenSignal = spf.getnframes()
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
	threshold = 160*noiseAmp
	#print threshold
	#Filter for each note, and if the max value is above the threshold, add the note to the list of notes
	for noteFreq in noteDictionary.keys():
		noteTransform = filterNote(float(noteFreq),omeg,tran)
		if noteTransform > threshold:
			noteString.append(noteDictionary[noteFreq])
	return noteString

def sameNotes(noteList1, noteList2):
	commonNotes = list(set(noteList1).intersection(noteList2))
	return commonNotes

def rounding(toRound):
	diff = 1000
	length = None
	for noteLength in rhythmDict.keys():
		if (abs(toRound - noteLength) < diff):
			diff = abs(toRound - noteLength)
	return  noteLength

# def rhythm(counter):
# 	noteRhythm = []
# 	sign = 1;
# 	[length, difference, sign] = rounding(counter, sign)
# 	noteRhythm.append(length)
# 	while noteRhythm[-1] != 0:
# 		[length, difference, sign] = rounding(difference, sign)
# 		noteRhythm.append(length)
# 	print sum(noteRhythm)
# 	try:
# 		return rhythmDict[sum(noteRhythm)]
# 	except KeyError:
# 		return "testing"



                

"""Main"""
print "Creating data structure for notes"
#Create note dictionary
[noteDictionary, noteDictionaryNoteIndex] = makeNoteDictionary('Notes.csv')
print "reading file"
#read the file
framesinSection = 1000
[signal, fs] = readWaveSplit(FILE, framesinSection) #returns signal and sampling frequency

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
	if (signalIndex % 10 == 0):
		print '%d out of %d' %(signalIndex, len(signal))
	#take the transform of each section
	[transform,omega] = takeTransform(signalSection, fs)
	#find all the notes in each section
	noteSection = categorize(transform, omega, noiseAmplitude)
	#if there are notes
	if noteSection:
		#add the notes to the detected notes list
		detectedNotes.append(noteSection)
	else:
		detectedNotes.append([])
		if first:
			#plt.figure(1)
			#plt.plot(omega,transform)
			#pylab.show()
			first = False
		#print "not empty!"
	#print noteSection
	#print(max(transform))
	#print omega[np.where(transform == max(transform))]
noteFramesToCheck = 3
realNotes = []
maybeRealNotes = []
noteTimeDictionary = {}
for index, noteSection in enumerate(detectedNotes[noteFramesToCheck:]):
	maybeRealNotes = []
	maybeRealNotes = sameNotes(noteSection,detectedNotes[index - 1])
	for numFramesBefore in range(2,noteFramesToCheck):
		maybeRealNotes = sameNotes(maybeRealNotes, detectedNotes[index - numFramesBefore])
	if maybeRealNotes:
		realNotes.append(maybeRealNotes)
	else:
		realNotes.append([''])
print realNotes


for frame,noteCluster in enumerate(realNotes):
	time = frame * (float(framesinSection)/fs)
	for note in noteCluster:
		if note:
			if noteTimeDictionary.has_key(note):
				noteTimeDictionary[note].append(time)
			else:
				noteTimeDictionary[note] = [time]
print noteTimeDictionary

notesPresent = noteTimeDictionary.keys()
noteFreqPairs = []
for notePresent in notesPresent:
	noteFreq = noteDictionaryNoteIndex[notePresent]
	noteFreqPairs.append([noteFreq, notePresent])

sortedNotes = sorted(noteFreqPairs, key=itemgetter(0))
notesPresentSorted = []
for noteFreqPair in sortedNotes:
	notesPresentSorted.append(noteFreqPair[1])

yvals=range(1,len(notesPresentSorted) + 1)
plt.figure(1)
plt.yticks(yvals,notesPresentSorted)


for index,eachNote in enumerate(notesPresentSorted):
	timesPresent = noteTimeDictionary[eachNote]
	yvalForNote = [index + 1] * len(timesPresent)
	plt.plot(timesPresent,yvalForNote, 'bs')

plt.show()






