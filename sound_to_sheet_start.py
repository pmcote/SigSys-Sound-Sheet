#This script will take a imput string and make it into a score
#We can add this to any file to do this
from abjad import *

#This is our file ourput of notes that will become the Lilypond score
string_notes = ["","c", "d'"]
actual_notes = []
for item in string_notes:
	if item == "":
		pass
	else:
		actual_notes.append(item)
print actual_notes

duration = Duration(1,4)
notes = scoretools.make_notes(actual_notes,duration)
staff = Staff(notes)


show(staff)


