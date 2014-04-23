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
def filterNote(noteFreq, omega, transform):
	filterRange = 10
	minFreq = noteFreq - filterRange
	maxFreq = noteFreq + filterRange
	filteredSignal = []
	for index, frequency in enumerate(omega):
		if (frequency > minFreq and frequency < maxFreq):
			filteredSignal.append(transform[index])
	avgVal = sum(filteredSignal)/len(filteredSignal)
	return avgVal
def filterNoteForPlots(noteFreq, omega, transform):
	filterRange = 10
	minFreq = noteFreq - filterRange
	maxFreq = noteFreq + filterRange
	filteredSignal = []
	for index, frequency in enumerate(omega):
		if (frequency > minFreq and frequency < maxFreq):
			filteredSignal.append(transform[index])
		else:
			filteredSignal.append(0)
	return filteredSignal
#checks if average value from filterNote is within range
def threshhold(avgVal):
        minVal = 1000
        if avgVal > minVal:
                return True
        else:
                return False

#Open the wave file
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


#Transforms yay!
print "transforming"
transform = np.fft.fft(signal)
omega=np.linspace(-20000, 20000, num=len(transform))
plt.figure(2)
plt.title('Fourier Transform of Signal')
plt.plot(omega, transform)

#create a dictionary of frequency to note names
noteDictionary = makeNoteDictionary('Notes.csv')

print "filtering"
for noteFiltered in noteDictionary.keys():
	noteTransform = filterNote(float(noteFiltered),omega,transform)
	includeNote = threshhold(noteTransform)
	if includeNote:
		print noteDictionary[noteFiltered]
                
#plt.figure(3)
#plt.title('Filtered Note')
#plt.plot(omega,noteTransform)

plt.show()


