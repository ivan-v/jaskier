import random

from functools import reduce

from modes_and_keys import apply_key
from motif_generator import generate_rhythm, merge_pitches_with_rhythm


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

Special_Chord_Progressions = {
  "8-bar blues": [0, 3, 0, 5, 1, 4, 0, 4, 0],
  }

def make_full_chord_progression(key):
  result = []
  tonics = generate_chord_progression()
  if key == "minor" or key == "Minor":
    chords = [[0,3,7],[0,3,6],[0,3,7],[0,3,7],[0,4,7],[0,4,7],[0,3,6]]
  elif key == "blues" or key == "Blues":
    chords = [[0,4,7],[0,3,7],[0,3,7],[0,4,7],[0,4,7],[0,4,7],[0,3,7]]
  else:
    chords = [[0,4,7],[0,3,7],[0,3,7],[0,4,7],[0,4,7],[0,3,7],[0,3,6]]
  selected_chords = [chords[tonic] for tonic in tonics]
  return [[x + y for x in xs] for xs, y in zip(selected_chords, tonics)]


def generate_pitches_from_chords(chord_progression, mode, base):
  fuller_mode = []
  for i in range(-2, 2):
    for j in range(len(mode)):
      fuller_mode.append(mode[j] + i*12)  

  pitches = []

  for tonic in chord_progression:
    if type(tonic) is list:
      chord = [(fuller_mode[int(len(fuller_mode)/2)+tonic[0]] + base)]
      for note in tonic[1:]:
        chord.append(note + chord[0])  
      pitches.append(chord)
    else:
      pitches.append(fuller_mode[int(len(fuller_mode)/2)+tonic] + base)

  return pitches


def generate_full_chord_sequence(key, mode, base):
  chords = make_full_chord_progression(key)
  return generate_pitches_from_chords(chords, mode, base)



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
def generate_melody_from_tonics(tonics, mode, span, step_tendency, base, meter, rhythm_pdf):
  fuller_mode = []
  for i in range(-3, 4):
    for j in range(len(mode)):
      fuller_mode.append(mode[j] + i*12 + base)
  
  # tonics = sway_tonics(tonics, 2)
  rhythm = generate_rhythm(meter, len(tonics), True, rhythm_pdf)
  pitches = []

  for i in range(len(rhythm)):
    space_left = len(rhythm[i])
    pitches.append(tonics[i])
    if i != len(tonics)-1:
      pitches += find_bridge(tonics[i], tonics[i+1], len(rhythm[i])-1, fuller_mode)
    else:
      for j in range(len(rhythm[i])-1):
        pitches.append(fuller_mode[fuller_mode.index(tonics[i])])

  rhythm = reduce(lambda x,y :x+y,rhythm)
  return merge_pitches_with_rhythm(pitches, rhythm)
  

# print(seq)
# print(convert_full_chords_to_euterpea(seq))


# p = generate_chord_progression()
# pitches = generate_pitches_from_chords(p, key, 60)
# mel = generate_melody_from_tonics(pitches, key, 18, 5, 60, (3,4), rhythm_pdf_presets["default"])

# key = apply_key("Dorian", "Bb")[1]
# seq = generate_full_chord_sequence("major", key, 60)


# print(mel)