import random

from chord_progression import generate_full_chord_sequence
from modes_and_keys import apply_key
from rhythm import generate_rhythm, replace_some_quarters_with_eights
from rhythm import merge_pitches_with_rhythm, rhythm_pdf_presets 

def choose_leading_tone(origin, goal):
	sign = (goal-origin>0) - (goal-origin<0)

	r = random.randint(0,2)
	if r == 0:
		return goal - 7*sign
	elif r == 1:
		return goal - 2*sign
	else:
		return goal - 1*sign

def generate_walking_bass(chords, meter):
	bass = []
	for i in range(len(chords)):
		measure = []
		measure.append(chords[i][0])
		measure.append(random.choice(chords[i][1:]))
		if meter[0] % 4 == 0:
			measure.append(random.choice([i for i in chords[i] if i not in measure]))
		if i < len(chords)-1:
			measure.append(choose_leading_tone(measure[-1], chords[i+1][0]))
		else:
			measure.append(chords[i][0])
		bass.append(measure)
	return bass

