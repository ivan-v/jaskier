import random

from better_chords import Chord_Type_to_Pitches
from modes_and_keys import apply_key
from generate_music import write_to_midi
from hand_motions import generate_rhythm_from_meter, full_chord

def grow_minor_chord_progression(*progression):
  if progression:
    root = progression[0][0]
  else:
    return [['i', random.choice(['suss', 'm'])]]
  if root[0] == 'i' and root[1] in ['suss', 'm']:
    options = [['bVII', ['9']],
               ['V',    ['7', 'b9', 'b13', 'suss']],
               ['iv',   ['m', 'm6', 'm7', 'm9']],
               ['bIII', ['aug']], 
               ['ii',   ['dim']],
               ['vii',  ['dim/2']],
               ['i',    ['m/b3']],
               ['bII',  ['/4']]]
  elif root[0] == 'ii':
    options = [['bVI',  ['6', 'M7']],
               ['iv',   ['m/b6', 'm6/b6', 'm7/b6', 'm6', 'm7', 'm9']],
               ['i',    ['m/b3']],
               ['bII',  ['/4']]]
  elif root[0] == 'vii' and root[1] in ['dim/2']:
    options = [['bVI',  ['6', 'M7']],
               ['iv',   ['m/b6', 'm6/b6', 'm7/b6', 'm6', 'm7', 'm9']],
               ['i',    ['m/b3']],
               ['bII',  ['/4']]]
  elif root[0] == 'i' and root[1] in ['m/b3']:
    options = [['bII',  ['/4']],
               ['iv',   ['m', 'm6', 'm7', 'm9']]]
  # elif root[0] == 'iv' and root[1] in ['m7']


def grow_major_chord_progression(*progression):
  if progression:
    root = progression[0][0]
  else:
    return [['I', random.choice(['6', 'M7', 'M9', 'suss'])]]

  # function_weights = {
  #   "I": 4,
  #   "ii": 10,
  #   "iii":  
  # }

  if root[0] == 'I' and root[1] in ['6', 'M7', 'M9', 'suss']:
    options = [['V',   ['7', '9', '11', '13', 'suss']], 
               ['IV',  ['6', 'M7', 'm6', 'm']], 
               ['iii', ['m7']], 
               ['ii',  ['m7', 'm9']], 
               ['bII', ['7']], 
               ['IV',  ['m7']], 
               ['bVII',['9']]]
  elif root[0] == 'V' and root[1] in ['7', '9', '11', '13', 'suss']:
    options = [['IV',  ['6', 'M7', 'm6', 'm']], 
               ['ii',  ['m7', 'm9']], 
               ['II',  ['7', '9', 'b9']],
               ['#IV', ['m7b5']],
               ['I',   ['M/5']]]
  elif root[0] == 'ii':
    options = [['IV',  ['6', 'M7', 'm6', 'm']],
               ['vi',  ['m7', 'm9']],
               ['VI',  ['7', '9', 'b9']],
               ['#I',  ['dim7']],
               ['I',   ['dim/b3']],
               ['I',   ['M/3']]]
  elif root[0] == 'iii':
    options = [['ii',  ['m7', 'm9']],
               ['V',   ['7', '9', '11', '13', 'suss']],
               ['VII', ['7', '9', 'b9']],
               ['#II', ['dim7']]]
  elif root[0] == 'IV' and root[1] in ['6', 'M7', 'm6', 'm']:
    options = [['iii', ['m7']], 
               ['vi',  ['m7', 'm9']],
               ['I',   ['7', '9', 'b9']],
               ['III', ['m7b5']]]
  elif root[0] == 'vi':
    options = [['V',   ['7', '9', '11', '13', 'suss']], 
               ['iii', ['m7']], 
               ['III', ['7', '9', 'b9']],
               ['#V',  ['dim7']]]
  elif root[0] == 'bII' or (root[0] == 'IV' and root[1] == 'm7'):
    options = [['ii',  ['m7', 'm9']]]
  elif root[0] == 'bVII':
    options = [['bVI', ['M']]]
  elif root[0] == 'I' and root[1] == 'M/3':
    options = [['IV',  ['6', 'M7', 'm6', 'm']]]
  elif root[0] == 'II':
    options = [['I',   ['m6']],
               ['V',   ['M/2']],
               ['VI',  ['m7b5/b3']]] # the hardest one to process
  elif root[0] == 'V' and root[1] == 'M/2':
    options = [['I',   ['m6']]]
  elif root[0] == 'I' and root[1] == '/5':
    options = [['bVI', ['7']],
               ['bVII',['9']],
               ['#IV', ['m7b5']]]
  elif root[0] == 'VI' and root[1] in ['7', '9', 'b9']:
    options = [['III', ['m7b5']]]
  elif root[0] == 'I' and root[1] in ['7', '9', 'b9']:
    options = [['V',   ['m7']]]
  elif root[0] == 'VII':
    options = [['#IV', ['m7b5']]]
  elif root[0] == 'III' and root[1] in ['7', '9', 'b9']:
    options = [['VII', ['m7b5']]]
  else:
    return False

  selected = random.choice(options)
  return [[selected[0], random.choice(selected[1])]] + progression[0]

def grow_minor_chord_progression(progression):
  return

def generate_chord_progression():
  growth = grow_major_chord_progression()
  while growth:
    progression = growth
    growth = grow_major_chord_progression(progression)
  return progression

def roman_numeral_to_pitch(applied_key, roman_numeral):
  if roman_numeral[0] == 'b':
    modifier = 1
    roman_numeral = roman_numeral[1:]
  elif roman_numeral[0] == '#':
    modifier = -1
    roman_numeral = roman_numeral[1:]
  else:
    modifier = 0
  r_n = roman_numeral.lower()
  if r_n == "i":
    return applied_key[1][0][0] + modifier
  elif r_n == "ii":
    return applied_key[1][0][1] + modifier
  elif r_n == "iii":
    return applied_key[1][0][2] + modifier
  elif r_n == "iv":
    return applied_key[1][0][3] + modifier
  elif r_n == "v":
    return applied_key[1][0][4] + modifier
  elif r_n == "vi":
    return applied_key[1][0][5] + modifier
  elif r_n == "vii":
    return applied_key[1][0][6] + modifier
  else:
    print("error: numeral not found in applied_key", roman_numeral)

def insert_undernotes_in_chords(applied_key, progression, chords_in_pitches):
  fuller_applied_key = [i + applied_key[1][1] for i in applied_key[1][0]]
  fuller_applied_key += [i + 12 + applied_key[1][1] for i in applied_key[1][0]]
  for i in range(len(progression)):
    if len(progression[i][1].split('/')) > 1:
      operating_bit = progression[i][1].split('/')[1]
      if operating_bit[0] == 'b':
        modifier = -1
        operating_bit = operating_bit[1:]
      elif operating_bit == '#':
        modifier = 1
        operating_bit = operating_bit[1:]
      else:
        modifier = 0
      chords_in_pitches[i].append(
        fuller_applied_key[fuller_applied_key.index(chords_in_pitches[i][0]) + int(operating_bit) - 1] + modifier - 12
      )
      # print("inserted the", progression[i][1].split('/')[1], "of", chords_in_pitches[i], "as", chords_in_pitches[i][-1])
  return chords_in_pitches

def invert_chord(chord):
    chord_pitches = chord[0]
    chord_pitches[0] += 12
    chord_pitches.sort()
    return (chord_pitches, chord[1])


def invert_chords_in_progression(chords):
    result = []
    result.append(chords[0])
    for i in range(len(chords) - 1):
        min_chord_size = min([len(i[0]) for i in [chords[i], chords[i + 1]]])
        pitch_differences = [
            chords[i + 1][0][k] - chords[i][0][k] % 12
            for k in range(
                min([len(j[0]) for j in [chords[i], chords[i + 1]]]))
        ]
        new_chord = chords[i + 1]
        attempts = 0
        options = []
        while len(set(pitch_differences)) < min_chord_size - 1:
            new_chord = invert_chord(new_chord)
            pitch_differences = [
                (new_chord[0][k] - chords[i][0][k]) % 12
                for k in range(
                    min([len(j[0]) for j in [chords[i], new_chord]]))
            ]
            options.append((new_chord, len(set(pitch_differences))))
            attempts += 1
            if attempts > 3:
                lowest_diff = min([options[i][1] for i in range(len(options))])
                for chord in options:
                    if chord[1] == lowest_diff:
                        new_chord = chord[0]
                        break
                break
        result.append(new_chord)
        if i == len(chords) - 2:
            return result
    return result


def chord_to_pitch(applied_key, chord):
  return [pitch + roman_numeral_to_pitch(applied_key, chord[0]) + applied_key[1][1]
    for pitch in Chord_Type_to_Pitches[chord[1].split('/')[0]]
  ]

def chord_progression_to_pitches(applied_key, progression):
  chords_in_pitches = [chord_to_pitch(applied_key, chord) for chord in progression]
  return insert_undernotes_in_chords(applied_key, progression, chords_in_pitches)

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




applied_key = apply_key('Ionian', 'B')
a = generate_chord_progression()
# print(a)
for i in range(10):
  a += generate_chord_progression()
b = chord_progression_to_pitches(applied_key, a)

meter = (3, 4)
c = chords_over_measures([[chord, 2] for chord in b], meter)
# print(c) 
d = invert_chords_in_progression(c)


rhythm = generate_rhythm_from_meter(meter)

song = full_chord(d, (3,4), rhythm)

write_to_midi(song, 'testyy', 0)


# def grow_chord_progression(progression, scale_quality):#, function_preferences):
#   x = progression
#   root = x[0]
#   if root == 0:
#     options = [3, 4, 6]
#   elif root == 4 or root == 6:
#     options = [1, 3]
#   elif root == 1:
#     options = [3, 5]
#   elif root == 3 and len(x) > 2:
#     options = [0, 5]
#   elif root == 3:
#     options = [5]
#   elif root == 5:
#     options = [0, 2]
#   else:
#     options = [0]
#   return [random.choice(options + [tonic for tonic in function_preference]*2)] + progression

# def generate_chord_progression(function_preferences):
#   progression = []
#   progression.append(0)
#   progression = grow_chord_progression(progression, function_preferences)
#   while progression[0] != 0:
#     progression = grow_chord_progression(progression, function_preferences)
#   return progression


# print(grow_chord_progression())