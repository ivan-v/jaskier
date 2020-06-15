import random

from chord_progression import convert_chord_names_to_sequence
from melodic_alteration import strip_part
from rhythm import generate_rhythm_measure, Space_Values
from stems import choose_leading_tone

from midiutil import MIDIFile

Beat_Intensity_Presets = {
    "0":  {"hn": .8, "qn": .2},
    "1":  {"hn": .6,  "(3 % 8)": .2,  "qn": .1, "(1 % 3)": .0,  "en": .1},
    "2":  {"hn": .5,  "(3 % 8)": .1,  "qn": .1, "(1 % 3)": .2,  "en": .1},
    "3":  {"hn": .4,  "(3 % 8)": .3,  "qn": .1, "(1 % 3)": .1,  "en": .1},
    "4":  {"hn": .3,  "(3 % 8)": .2,  "qn": .3, "(1 % 3)": .1,  "en": .1},
    "5":  {"hn": .2,  "(3 % 8)": .2,  "qn": .2, "(1 % 3)": .2,  "en": .2},
    "6":  {"hn": .1,  "(3 % 8)": .2,  "qn": .3, "(1 % 3)": .3,  "en": .2},
    "7":  {"hn": .05, "(3 % 8)": .15, "qn": .3, "(1 % 3)": .2,  "en": .3},
    "8":  {"hn": .0,  "(3 % 8)": .1,  "qn": .3, "(1 % 3)": .2,  "en": .5},
    "9":  {"hn": .0,  "(3 % 8)": .05, "qn": .2, "(1 % 3)": .25, "en": .5},
    "10": {"hn": .0,  "(3 % 8)": .05, "qn": .1, "(1 % 3)": .25, "en": .6},
}

# levels of intensity: 0-10
def generate_rhythmic_beat(meter, intensity, length, show_seperate_measures):
    beat = []
    beats = 0
    rhythm_pdf = Beat_Intensity_Presets[str(intensity)]
    while beats < length:
        measure = generate_rhythm_measure(meter[0]/(meter[1]/4), rhythm_pdf)
        if show_seperate_measures:
            beat += [measure]
        else:
            beat += measure
        beats += 1
    return beat


def generate_rhythmic_motion(length, min_chord_size, repeating_pitches):
    result = []
    for i in range(length):
        choice = random.choice(list(range(min_chord_size)))
        if not repeating_pitches:
            while choice in result:
                choice = random.choice(range(0,min_chord_size))
        result.append(choice)
    return result


def full_rhythmic_motion_to_euterpea(sequence, rhythm, leading_tone, rhythmic_motion):
  euterpea_string = ""
  count = 0
  for chord in sequence:
    c = 0
    for j in range(len(rhythm)):
      # by default, rhythmic motion goes after the chords
      if j == len(rhythm)-1 and count != len(sequence)-1:
        chord_string = " note " + rhythm[j] + " " + str(choose_leading_tone(chord[0], sequence[count+1][0]))
      elif j + len(rhythmic_motion) > len(rhythm) - leading_tone - 1:
        pitch = chord[rhythmic_motion[len(rhythm) - leading_tone - j - 1]]
        chord_string = "note " + rhythm[j] + " " + str(pitch) + " "
      elif j != len(rhythm)-1:
        chord_string = "("
        for i in range(len(chord)):
          chord_string += "note " + rhythm[j] + " " + str(chord[i])
          if chord[i] is not chord[-1]:
            chord_string += " :=: "
          else:
            chord_string += ") "
      euterpea_string += chord_string
      c += 1
      if c < len(rhythm):
        euterpea_string += ":+: "
    count += 1
    if count < len(sequence):
        euterpea_string += ":+: "
  return euterpea_string



def convert_full_chords_to_euterpea(sequence, rhythm, leading_tone):
  euterpea_string = ""
  count = 0
  for chord in sequence:
    c = 0
    for j in range(len(rhythm)):
      if j != len(rhythm)-1:
        chord_string = "("
        for i in range(len(chord)):
          chord_string += "note " + rhythm[j] + " " + str(chord[i])
          if chord[i] is not chord[-1]:
            chord_string += " :=: "
          else:
            chord_string += ") "
      elif count != len(sequence)-1:
        chord_string += " :+: note " + rhythm[j] + " " + str(choose_leading_tone(chord[0], sequence[count+1][0]))
      euterpea_string += chord_string
      c += 1
      if c < len(rhythm):
        euterpea_string += ":+: "
    count += 1
    if count < len(sequence):
        euterpea_string += ":+: "
  return euterpea_string


sequence = ['Am', 'G', 'Fmaj7', 'Em', 
  'Dm7', 'G7', 'Cmaj7', 'Bbmaj7', 'Bm11', 'E7', 'Am', 'G', 'Fmaj7', 'Em', 
  'Dm7', 'G7', 'Cmaj7']


chords = convert_chord_names_to_sequence(sequence)

rhythm = generate_rhythmic_beat((3,4), 6, 2, False)

g = generate_rhythmic_motion(3, 3, False)
testy = "note qn 64 :+: note qn 72 :+: note qn 72 :+: note hn 72 :+: note qn 72 :+: note qn 71 :+: note qn 65 :+: note qn 71 :+: note hn 72 :+: note qn 67 :+: note qn 67 :+: note qn 69 :+: note qn 67 :+: note hn 60 :+: note qn 60 :+: note qn 60 :+: note qn 67 :+: note qn 67 :+: note hn 60 :+: note qn 58 :+: note qn 69 :+: note qn 73 :+: note qn 69 :+: note hn 69 :+: note qn 71 :+: note qn 69 :+: note qn 60 :+: note qn 52 :+: note hn 52 :+: note qn 55 :+: note qn 62 :+: note qn 72 :+: note qn 65 :+: note hn 57 :+: note qn 64 :+: note qn 64 :+: note qn 60 :+: note qn 57 :+: note hn 62 :+: note qn 62 :+: note qn 62 :+: note qn 67 :+: note qn 71 :+: note qn 64 :+: note qn 72 :+: note qn 72 :+: note hn 72 :+: note qn 72 :+: note qn 71 :+: note qn 65 :+: note qn 71 :+: note hn 72 :+: note qn 67 :+: note qn 67 :+: note qn 69 :+: note qn 67 :+: note hn 60 :+: note qn 60 :+: note qn 60 :+: note qn 67 :+: note qn 67 :+: note hn 60 :+: note qn 58 :+: note qn 69 :+: note qn 73 :+: note qn 69 :+: note hn 69 :+: note qn 71 :+: note qn 69 :+: note qn 60 :+: note qn 52 :+: note hn 52 :+: note qn 55 :+: note qn 62 :+: note qn 72 :+: note qn 65 :+: note hn 57 :+: note qn 64 :+: note qn 64 :+: note qn 60 :+: note qn 57 :+: note hn 62 :+: note qn 62 :+: note qn 62 :+: note qn 67 :+: note qn 71:+: note wn 64"
rm = full_rhythmic_motion_to_euterpea(chords, rhythm, True, g)
t = strip_part(testy)
# print(convert_full_chords_to_euterpea(chords, rhythm, True))

degrees  = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
track    = 0
channel  = 0
time     = 0   # In beats
duration = .5   # In beats
tempo    = 130  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
MyMIDI.addTempo(track,time, tempo)



for i in range(len(t[0])):
    duration = Space_Values[t[1][i]]
    MyMIDI.addNote(track, channel, t[0][i], time, duration, volume)
    time += duration

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

