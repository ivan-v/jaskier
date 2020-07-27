import random

from chord_progression import convert_chord_names_to_over_measures
from melodic_alteration import strip_part
from rhythm import generate_rhythm_measure, Space_Values
from stems import choose_leading_tone

from midiutil import MIDIFile

# from generate_music import write_to_midi

Beat_Intensity_Presets = {
    "0":  {"hn": .8, "qn": .2},
    "1":  {"hn": .7,  "(3 % 8)": .2,  "qn": .1, "(1 % 3)": .0,  "en": .0},
    "2":  {"hn": .5,  "(3 % 8)": .1,  "qn": .2, "(1 % 3)": .1,  "en": .1},
    "3":  {"hn": .4,  "(3 % 8)": .3,  "qn": .2, "(1 % 3)": .0,  "en": .1},
    "4":  {"hn": .3,  "(3 % 8)": .2,  "qn": .3, "(1 % 3)": .1,  "en": .1},
    "5":  {"hn": .1,  "(3 % 8)": .2,  "qn": .5, "(1 % 3)": .1,  "en": .1},
    "6":  {"hn": .1,  "(3 % 8)": .2,  "qn": .3, "(1 % 3)": .3,  "en": .2},
    "7":  {"hn": .05, "(3 % 8)": .15, "qn": .3, "(1 % 3)": .2,  "en": .3},
    "8":  {"hn": .0,  "(3 % 8)": .1,  "qn": .2, "(1 % 3)": .2,  "en": .15},
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


# returns a list of indexes for a chord
def generate_rhythmic_motion(length, min_chord_size, repeating_pitches):
    result = []
    for i in range(length):
        choice = random.choice(list(range(min_chord_size)))
        if not repeating_pitches:
            while choice in result:
                choice = random.choice(range(0,min_chord_size))
        result.append(choice)
    return result

# TODO: Make more configurable in terms of where chords vs notes
def generate_full_rhythmic_motion(rhythm, leading_tone, rhythmic_motion,
                                  chords, meter):
    result = []
    time_length = 0
    measure_length = meter[0] / (meter[1] / 4)
    for i in range(len(chords)):
        # \/ size of measure for the chord
        measure_size = int(
            len(rhythm) *
            ((chords[i][1][1] - chords[i][1][0]) / measure_length))
        current_rhythm = rhythm
        # potential warning: is funky with small fractions, like .23 of a measure
        while measure_size > len(current_rhythm):
            if len(current_rhythm) + len(rhythm) <= measure_size:
                current_rhythm = rhythm[0:len(rhythm)]
            else:
                current_rhythm += current_rhythm[:int(len(rhythm) / 2) + 1]
        for j in range(measure_size):
            if j == measure_size - 1 and i != len(chords) - 1:
                result.append([
                    choose_leading_tone(chords[i][0][0], chords[i][0], chords[i + 1][0][0]),
                    current_rhythm[j], time_length
                ])
            elif j + len(rhythmic_motion) > measure_size - leading_tone - 1:
                pitch = chords[i][0][rhythmic_motion[measure_size
                                                     - leading_tone - j - 1]]
                result.append([pitch, current_rhythm[j], time_length])
            elif j != measure_size - 1:
                result += [[p, current_rhythm[j], time_length]
                           for p in chords[i][0]]
            time_length += Space_Values[current_rhythm[j]]
    return result


sequence = ['Am', 'G', 'Fmaj7', 'Em', 
  'Dm7', 'G7', 'Cmaj7', 'Bbmaj7', 'Bm11', 'E7', 'Am', 'G', 'Fmaj7', 'Em', 
  'Dm7', 'G7', 'Cmaj7']


def write_to_midi(song, filename, instrument, *tempo):
    track    = 0
    channel  = 0
    time     = 0   # In beats
    if not tempo:
        tempo    = 160 # In BPM
    else:
        tempo = tempo[0]
    volume   = 100 # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                         # automatically created)
    MyMIDI.addTempo(track, time, tempo)

    for i in range(len(song)):
        if song[i][0] < 60:
            volume = 92
        elif song[i][0] < 50:
            volume = 86
        elif song[i][0] < 45:
            volume = 83
        else:
            volume = 100
        MyMIDI.addNote(track, channel, song[i][0], song[i][2],
                       Space_Values[song[i][1]], volume)
    
    MyMIDI.addProgramChange(0, 0, 0, instrument)

    with open(filename + ".mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)


# meter = (4,4)
# chords = convert_chord_names_to_over_measures(sequence, meter)
# rhythm = generate_rhythmic_beat(meter, 5, 2, False)

# g = generate_rhythmic_motion(3, 3, False)
# rm = generate_full_rhythmic_motion(rhythm, True, g, chords, meter)
# write_to_midi(rm, "backing_track", 105)

