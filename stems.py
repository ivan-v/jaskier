import random

from functools import reduce

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

def generate_walking_bass(chords):
	bass = []
	for i in range(len(chords)):
		measure = []
		measure.append(chords[i][0])
		measure.append(random.choice(chords[i][1:]))
		measure.append(random.choice([i for i in chords[i] if i not in measure]))
		if i < len(chords)-1:
			measure.append(choose_leading_tone(measure[-1], chords[i+1][0]))
		else:
			measure.append(chords[i][0])
		bass.append(measure)
	return bass


key = apply_key("Aeolian", "C")[1]
seq = generate_full_chord_sequence("minor", key, 60)
walk = generate_walking_bass(seq)
rhythm = generate_rhythm((3,4), len(seq)+2*len(seq)/3, False, rhythm_pdf_presets["default"])
rhythm = replace_some_quarters_with_eights(rhythm, 3)
# print(len(seq)*4, len(reduce(lambda x,y: x+y, walk)))
# print(len(rhythm), len(reduce(lambda x,y: x+y, walk)))
b = merge_pitches_with_rhythm(reduce(lambda x,y: x+y, walk), rhythm)
print(b)