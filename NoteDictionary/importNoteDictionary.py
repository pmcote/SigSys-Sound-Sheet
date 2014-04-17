import csv
with open('Notes.csv', 'rb') as  csvfile:
	noteReader = csv.reader(csvfile,delimiter = ',',)
	for row in noteReader:
		print','.join(row)