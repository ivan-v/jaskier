import random
from chord_progression import convert_chord_names_to_over_measures,  invert_chords_in_progression
from generate_music import write_to_midi
from hand_motions import full_chord
from rhythm import generate_rhythm
from rhythm_track import Beat_Intensity_Presets

C  = {"ii6": "Dm6",  "vii_halfdim": "Bm7b5",  "I": "C",  "V7": "G7",  "i": "Cm",  "vii_dim": "Bdim7"}
Eb = {"ii6": "Fm6",  "vii_halfdim": "Dm7b5",  "I": "Eb", "V7": "Bb7", "i": "Ebm", "vii_dim": "Ddim7"}
Gb = {"ii6": "Abm6", "vii_halfdim": "Fm7b5",  "I": "Gb", "V7": "Db7", "i": "Gbm", "vii_dim": "Fdim7"}
A  = {"ii6": "Bm6",  "vii_halfdim": "Gsm7b5", "I": "A",  "V7": "E7",  "i": "Am",  "vii_dim": "Gsdim7"}
# Remember that the last element is also adjacent to the first element!
Set_One = [C, Eb, Gb, A]

B  = {"ii6": "Csm6", "vii_halfdim": "Asm7b5", "I": "B",  "V7": "Fs7", "i": "Bm",  "vii_dim": "Asdim7"}
D  = {"ii6": "Em6",  "vii_halfdim": "Csm7b5", "I": "D",  "V7": "A7",  "i": "Dm",  "vii_dim": "Csdim7"}
F  = {"ii6": "Gm6",  "vii_halfdim": "Em7b5",  "I": "F",  "V7": "C7",  "i": "Fm",  "vii_dim": "Edim7"}
Ab = {"ii6": "Bbm6", "vii_halfdim": "Gm7b5",  "I": "Ab", "V7": "Eb7", "i": "Abm", "vii_dim": "Gdim7"}

Set_Two = [B, D, F, Ab]

Bb  = {"ii6": "Cm6",  "vii_halfdim": "Am7b5",  "I": "Bb", "V7": "F7",  "i": "Bbm", "vii_dim": "Adim7"}
Db  = {"ii6": "Ebm6", "vii_halfdim": "Cm7b5",  "I": "Db", "V7": "Ab7", "i": "Dbm", "vii_dim": "Cdim7"}
E   = {"ii6": "Fsm6", "vii_halfdim": "Dsm7b5", "I": "E",  "V7": "B7",  "i": "Em",  "vii_dim": "Dsdim7"}
G   = {"ii6": "Am6",  "vii_halfdim": "Fsm7b5", "I": "G",  "V7": "D7",  "i": "Gm",  "vii_dim": "Fsdim7"}

Set_Three = [Bb, Db, E, G]

All_Sets = [Set_One, Set_Two, Set_Three]


def generate_jazz_progression():
	return ["I"] + random.sample(["ii6", "vii_halfdim", "V7", "vii_dim"], 4) + ["i"]

def apply_jazz_progression(progression, *keys):
	if not keys:
		# TODO: make generate_keys()
		# keys = generate_keys()
		pass
	else:
		keys = keys[0]
	# TODO: Clean this to be list comprehension, and not nested loops
	result = []
	for key in keys:
		for Set in All_Sets:
			for subset in Set:
				if key == subset["I"]:
					result += [subset[roman] for roman in progression]
	return result


def find_key_from_fifth_chord(chord):
	for Set in All_Sets:
		for key in Set:
			if chord in key.values():
				return key["I"] 


def find_key_from_fifths(chords):
	return [find_key_from_fifth_chord(chord) for chord in chords]


def populate_blues_tabs_with_jazz_chords(meter, tab, *rhythm):
	if not rhythm:
		rhythm = generate_rhythm(meter, 1, False, Beat_Intensity_Presets["4"])
	else:
		rhythm = rhythm[0]
	keys = find_key_from_fifths(tab)
	chord_names = apply_jazz_progression(generate_jazz_progression(), keys)
	chords = convert_chord_names_to_over_measures(chord_names, meter)
	better_chords = invert_chords_in_progression(chords)
	notes = full_chord(better_chords, meter, rhythm)
	return notes

# Returns the note/pitch 4 semitones ahead
Coltrane_Step = {
	"C": "E",
	"G": "B",
	"D": "Fs",
	"A": "Db",
	"E": "Ab",
	"B": "Eb",
	"Gb": "Bb",
	"Fs": "Bb",
	"Db": "F",
	"Ab": "C",
	"Eb": "G",
	"Bb": "D",
	"F":  "A"
}


def pick_coltrane_steps(*first_note):
	if first_note:
		first_note = first_note[0]
	else:
		first_note = random.choice(list(Coltrane_Step.keys()))
	return [first_note, Coltrane_Step[first_note], 
		    Coltrane_Step[Coltrane_Step[first_note]]]


def coltrane_progression(length, *first_note):
	if first_note:
		steps = pick_coltrane_steps(first_note[0])
	else:
		steps = pick_coltrane_steps()
	Steps = {}
	for key in steps:
		for Set in All_Sets:
			for subset in Set:
				if key == subset["I"]:
					Steps[key] = [subset["ii6"][:-1]+"7", subset["V7"], subset["I"]+"maj7"]
					break
	result = [[Steps[steps[0]][2]]]
	current_index = 0
	next_index = 0
	while len(result) < length:
		turn = random.choice([-1, 1])
		current_index = next_index
		next_index += turn
		r = random.randint(0,1)
		if next_index % 3 == 0:
			if current_index % 3 == 1:
				result.append(Steps[steps[next_index % 3]][1:])
			else:
				result.append(Steps[steps[next_index % 3]])
		elif next_index % 3 == 1:
			if current_index % 3 == 0:
				result.append(Steps[steps[next_index % 3]])
			else:
				result.append(Steps[steps[next_index % 3]][r:])
		elif next_index % 3 == 2:
			if current_index % 3 == 0:
				result.append(Steps[steps[next_index % 3]][1:])
			else:
				result.append(Steps[steps[next_index % 3]][r:])
		result.append(Steps[steps[current_index % 3]])

	return sum(result, [])


def make_coltrane_progression(meter, length, *first_note):
	if first_note:
		progression = coltrane_progression(length, first_note[0])
	else:
		progression = coltrane_progression(length)
	chords = convert_chord_names_to_over_measures(progression, meter)
	better_chords = invert_chords_in_progression(chords)
	rhythm = generate_rhythm(meter, 1, False, Beat_Intensity_Presets["4"])
	notes = full_chord(better_chords, meter, rhythm)
	return notes


notes = make_coltrane_progression((3,4), 20, "B")

# TODO: make generate_blues_keys


given_fifths = ["Ab7", "Db7", "Ab7", "Ab7", "Db7", "Db7", "Ab7", "Ab7", "Eb7", "Db7", "Ab7", "Eb7"]
# notes = populate_blues_tabs_with_jazz_chords((2,4), given_fifths)
write_to_midi(notes, "jazz_chords")


