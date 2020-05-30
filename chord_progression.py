import random

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

def make_full_chord_progression(key, applied_key, *input_tonics):
  result = []
  if input_tonics:
    tonics = input_tonics[0]
  else:
    tonics = generate_chord_progression()
  if key == "minor" or key == "Minor":
    chords = [[0,3,7],[0,3,6],[0,4,7],[0,3,7],[0,4,7],[0,4,7],[0,3,6]]
  elif key == "blues" or key == "Blues":
    chords = [[0,4,7],[0,3,7],[0,3,7],[0,4,7],[0,4,7],[0,4,7],[0,3,7]]
  else:
    chords = [[0,4,7],[0,3,7],[0,3,7],[0,4,7],[0,4,7],[0,3,7],[0,3,6]]
  selected_chords = [chords[tonic] for tonic in tonics]
  print(applied_key)
  print(list(zip(selected_chords, tonics)))
  a = [[note + applied_key[1][0][i] + applied_key[1][1] for note in selected_chords[i]] for i in range(len(selected_chords))]
  print(a)
  return a#[[x + y for x in xs] for xs, y in zip(selected_chords, tonics)]


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


def generate_full_chord_sequence(key, applied_key, *input_chords):
  if input_chords:
    chords = make_full_chord_progression(key, applied_key, input_chords[0])
  else:
    chords = make_full_chord_progression(key, applied_key)
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


# expected style of chord_name input: iiidim7, IV, or VI7, etc.
def construct_chord(mode, chord_name):
  if len(chord_name) > 2 and chord_name[2].lower() == "i":
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
  
  num_string = ''.join([i if i.isdigit() else '' for i in chord_name])
  if num_string:
    num = int(num_string)
  else:
    num = 0

  if is_minor:
    chord = [0, 3, 7]
  else:
    chord = [0, 4, 7]

  if 'dim' in chord_name:
    chord = [0, 3, 6]
  elif 'aug' in chord_name:
    chord = [0, 4, 8]

  if num == 7:
    if is_minor:
      chord.append(chord[-1] + 3)
    else:
      chord.append(chord[-1] + 4)
  elif num == 6:
    chord.append(chord[-1] + 3)
  elif num == 9:
    chord.append(chord[-1] + 6)
  chord = [i + applied_key[1][0][tone] for i in chord]
  return chord


def convert_chord_names_to_sequence(mode, given_chords):
  return [construct_chord(mode, chord) for chord in given_chords]


def convert_full_chords_to_euterpea(sequence):
  euterpea_string = ""
  count = 0
  for chord in sequence:
    chord_string = "("
    for note in chord:
      chord_string += "note qn " + str(note)
      if note is not chord[-1]:
        chord_string += " :=: "
      else:
        chord_string += ") "
    euterpea_string += chord_string
    count += 1
    if count < len(sequence):
      euterpea_string += ":+: "
  return euterpea_string


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

def find_bridge(start, goal, length, fuller_mode):
  if fuller_mode.index(goal) > fuller_mode.index(start):
    path = fuller_mode[fuller_mode.index(start):fuller_mode.index(goal)]
  else:
    path = fuller_mode[fuller_mode.index(goal):fuller_mode.index(start)]
    path.reverse()
  if length == len(path):
    return path
  elif length == len(path)-1:
    return path[1:]
  elif length == len(path)-2:
    return path[1:-1]
  elif length == len(path)*2:
    return [val for val in path for _ in (0,1)]
  elif length < len(path):
    path = path[1:-1]
    while len(path) != length:
      path.remove(random.choice(path[1:-1]))
    return path
  else:
    # duplicate an element at random
    while len(path) != length:
      if len(path) > 2:
        element = random.choice(path[1:-1])
      elif len(path) > 1:
        element = random.choice(path[1:])
      else:
        element = random.choice(path)
      path.insert(path.index(element), element)
    return path


# TODO: Should this exist?
def generate_melody_from_tonics(tonics, applied_key, span, mode,
                                step_tendency, meter, rhythm_pdf):
  fuller_mode = sum(list(map(lambda x: [i + 12*x for i in mode],
                             range(-2,2))), [])
  
  # tonics = sway_tonics(tonics, 2)
  rhythm = generate_rhythm(meter, len(tonics), True, rhythm_pdf)
  pitches = []

  for i in range(len(rhythm)):
    space_left = len(rhythm[i])
    pitches.append(tonics[i])
    if i != len(tonics)-1:
      pitches += find_bridge(tonics[i], tonics[i+1], len(rhythm[i])-1,
                                                           fuller_mode)
    else:
      for j in range(len(rhythm[i])-1):
        pitches.append(fuller_mode[fuller_mode.index(tonics[i])])

  rhythm = sum(rhythm,[])
  return merge_pitches_with_rhythm(pitches, rhythm)
  