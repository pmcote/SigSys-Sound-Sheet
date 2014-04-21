import csv


noteDictionary = {}

def whichNote (noteDict, tolerance, frequency):
	noteFreqs = noteDict.keys()
	for note in noteFreqs:
		if (abs(float(note)-frequency) <= tolerance):
			return noteDict[note]
	return 'did not match'	

#Open the csv file
with open('Notes.csv', 'rb') as  csvfile:
	noteReader = csv.reader(csvfile,delimiter = ',',)
	for row in noteReader:
		#Add frequency, note name pairs to the dictionary
		noteDictionary[row[1]] = row[0]

print noteDictionary

# Test Bench

#Should be C8
print whichNote(noteDictionary, 1, 4186)

#Should be A6
print whichNote(noteDictionary, 0.5, 1760.5)

#should be did not match
print whichNote(noteDictionary, 10, 0)
