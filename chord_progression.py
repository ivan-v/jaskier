import random

from modes_and_keys import apply_key, Starting_Pitch 
from rhythm import generate_rhythm, merge_pitches_with_rhythm

def grow_chord_progression(progression):
  x = progression
  root = x[0]
  if root == 0:
    options = [3, 4, 6]
  elif root == 4 or root == 6:
    options = [1, 3]
  elif root == 1:
    options = [3, 5]
  elif root == 3 and len(x) > 2:
    options = [0, 5]
  elif root == 3:
    options = [5]
  elif root == 5:
    options = [0, 2]
  else:
    options = [0]
  return [random.choice(options)] + progression


def generate_chord_progression():
  progression = []
  progression.append(0)
  progression = grow_chord_progression(progression)
  while progression[0] != 0:
    progression = grow_chord_progression(progression)
  return progression

Special_Chords = {
  "8-bar blues": [0, 3, 0, 5, 1, 4, 0, 4, 0],
}

# TODO: Needs a fair bit of work 
def make_full_chord_progression(applied_key, *input_tonics):
  result = []
  m = applied_key[1][0]
  m += [i+12 for i in m]
  m += [i+36 for i in m]
  m.sort()
  m = list(set(m))
  if input_tonics:
    tonics = input_tonics[0]
  else:
    tonics = generate_chord_progression()
  chords = [[0,4,7],[0,3,7],[0,3,7],[0,4,7],[0,4,7],[0,3,7],[0,3,6]]
  selected_chords = [[0, m[tonic+2]-m[tonic], m[tonic+4]-m[tonic]] for tonic in tonics]
  return [[note + applied_key[1][0][i] + applied_key[1][1]
           for note in selected_chords[i]] for i in range(len(selected_chords))]

a= make_full_chord_progression(apply_key("Ionian", "C"), [0,1,2,3,4,5,6])


def make_chord_progression(chord_names):
  for name in chord_names:
    pass
  return


def generate_pitches_from_chords(chord_progression, applied_key):
  
  fuller_mode = sum(list(map(lambda x: [i + 12*x for i in applied_key[1][0]],
                             range(-2,2))), [])
  pitches = []

  for tonic in chord_progression:
    if type(tonic) is list:
      chord = [(fuller_mode[int(len(fuller_mode)/2)+tonic[0]] + applied_key[1][1])]
      for note in tonic[1:]:
        chord.append(note + chord[0])  
      pitches.append(chord)
    else:
      pitches.append(fuller_mode[int(len(fuller_mode)/2)+tonic] + applied_key[1][1])

  return pitches


def generate_full_chord_sequence(applied_key, *input_chords):
  if input_chords:
    chords = make_full_chord_progression(applied_key, input_chords[0])
  else:
    chords = make_full_chord_progression(applied_key)
  return chords# generate_pitches_from_chords(chords, applied_key)


def available_pitches_in_full_chord(chord):
  return list(map(lambda x: [i + 12*x for i in chord], range(-2,3)))


def available_pitches_in_chords(chords):
  return [available_pitches_in_full_chord(chord) for chord in chords]


def convert_roman_to_arabic(roman_numeral):
  switcher = {
    "i":   0,
    "ii":  1,
    "iii": 2,
    "iv":  3,
    "v":   4,
    "vi":  5,
    "vii": 6,
  }
  return switcher[roman_numeral]


def construct_chord(offset, chord_name, is_minor):
  num_string = ''.join([i if i.isdigit() else '' for i in chord_name])
  if num_string:
    num = int(num_string)
  else:
    num = 0

  if is_minor:
    chord = [0, 3, 7]
  else:
    chord = [0, 4, 7]

  if "dim" in chord_name:
    chord = [0, 3, 6]
  elif "aug" in chord_name:
    chord = [0, 4, 8]

  if num == 7:
    if is_minor:
      chord.append(chord[-1] + 3)
    elif "dim" in chord_name:
      chord.append(chord[-1] + 2)
    elif "maj" in chord_name:
      chord.append(chord[-1] + 4)
    else:
      chord.append(chord[-1] + 3)
  elif num == 6:
    chord.append(chord[-1] + 2)
  elif num == 9:
    if is_minor:
      chord.append(chord[-1] + 3)
    elif "dim" in chord_name:
      chord.append(chord[-1] + 2)
    elif "maj" in chord_name:
      chord.append(chord[-1] + 4)
    else:
      chord.append(chord[-1] + 3)
    if "maj" in chord_name:
      chord.append(chord[-1] + 3)
    else:
      chord.append(chord[-1] + 4)
  elif num == 11:
    if is_minor:
      chord.append(chord[-1] + 3)
    elif "dim" in chord_name:
      chord.append(chord[-1] + 2)
    elif "maj" in chord_name:
      chord.append(chord[-1] + 4)
    else:
      chord.append(chord[-1] + 3)
    if "maj" in chord_name:
      chord.append(chord[-1] + 3)
    else:
      chord.append(chord[-1] + 4)
    chord.append(chord[-1] + 3)

  return [i + offset for i in chord]


# applied_key needed for this way/style.
# expected style of chord_name input: iiidim7, IV, or VI7, etc.
def construct_chord_from_roman(applied_key, chord_name):
  if len(chord_name) == 1:
    degree = chord_name
    d = 1
  elif len(chord_name) > 2 and chord_name[2].lower() == "i":
    degree = chord_name[:3]
    d = 3
  elif chord_name[1].lower() == "i" or chord_name[1].lower() == "v":
    degree = chord_name[:2]
    d = 2
  else:
    degree = chord_name[:1]
    d = 1
  is_minor = degree.islower()
  tone = convert_roman_to_arabic(degree.lower())
  offset = applied_key[1][0][tone] + applied_key[1][0]
 
  return construct_chord(offset, chord_name, is_minor)

# accepts style Amin7, Ddim7, Cb9, Cbmaj11
def construct_chord_from_name(chord_name):
  if chord_name[:2] in Starting_Pitch:
    name = chord_name[:2]
  elif chord_name[:1] in Starting_Pitch:
    name = chord_name[:1]
  else:
    print("Error: chord (starting pitch) name not found")

  offset = Starting_Pitch[name]
  is_minor = 'm' in chord_name and (chord_name.index('m') >= len(chord_name)-3\
             or chord_name[chord_name.index('m') + 2] != 'j')

  return construct_chord(offset, chord_name, is_minor)

def convert_roman_chord_names_to_sequence(mode, given_chords):
  return [construct_chord_from_roman(mode, chord) for chord in given_chords]

def convert_chord_names_to_sequence(given_chords):
  return [construct_chord_from_name(chord) for chord in given_chords]


# assumes chords format of [[pitches], num_measures]
def chords_over_measures(chords, meter, *starting_time):
  result = []
  measure_length = meter[0]/(meter[1]/4)
  if starting_time:
    t1 = starting_time
  else:
    t1 = 0
  for chord in chords:
    t2 = t1 + chord[1]*measure_length
    result.append((chord[0], (t1, t2)))
    t1 = t2
  return result

def convert_chord_names_to_over_measures(given_chords, meter,
                                         *measures_per_chord_default):
  if measures_per_chord_default:
    default = measures_per_chord_default
  else:
    # default length of 1 measure per chord
    default = 1
  chords_with_lengths = []
  for entry in given_chords:
    if type(entry) == list:
      chords_with_lengths.append(entry)
    else:
      chords_with_lengths.append([entry, default])
  just_chords = [chord[0] for chord in chords_with_lengths]
  chords_with_pitches = convert_chord_names_to_sequence(just_chords)
  fuller_chords = [[chords_with_pitches[i], chords_with_lengths[i][1]]
                                     for i in range(len(given_chords))]
  return chords_over_measures(fuller_chords, meter)

# not currently used
def sway_tonics(tonics, step_tendency):
  for i in range(len(tonics)):
    r = random.randint(0, step_tendency)
    if i < len(tonics)-1 and tonics[i+1] > tonics[i]:
      if r == 0:
        tonics[i] += 12
    elif i < len(tonics)-1 and tonics[i+1] < tonics[i]:
      if r == 0:
        tonics[i] -= 12
    elif r == 0:
      tonics[i] -= 12
    elif r == 0:
      tonics[i] += 12
    else:
      pass
  return tonics

