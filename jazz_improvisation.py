import random

from chord_progression import convert_chord_names_to_over_measures, invert_chords_in_progression
from generate_music import write_to_midi
from hand_motions import arpeggios, full_chord
from jazz_chords import apply_jazz_progression, generate_jazz_progression
from rhythm import generate_rhythm, Space_Values
from rhythm_track import Beat_Intensity_Presets
from stems import shift_octave

# TODO: add varied beats
def generate_melodic_continuity_rhythm(chords, meter, varied_beats):
    length = chords[-1][1][1]
    num_measures = length/(meter[0]/(meter[1]/4))
    result = []
    options = [['qn'], ['en', 'en'], [ '(1 % 3)', '(1 % 3)', '(1 % 3)']]
    if not varied_beats:
        single_beat = random.choice(options)
    if meter[1] == 4:
        return single_beat*int(meter[0])
    elif meter[1] == 8:
        return single_beat*int(meter[0]*.5)

# TODO: move to a better place
def rhythm_for_full_chords(meter):
    # result = []
    # for i in range(len(chords)):
    #     duration = list(Space_Values.keys())[list(Space_Values.values()).index(chords[i][1][1] - chords[i][1][0])]
    #     result += [duration]
    # return result
    if meter[0] == 4 and meter[1] == 4:
        return ['wn']
    elif meter[0] == 2 and meter[1] == 4:
        return ['hn']


def improvise_over_chord_progression(chords, chord_progression, meter):
    # phrasing should be param for rhythm
    # phrasing = random.choice(["melodic_continuity", "phrases"])
    rhythm = generate_melodic_continuity_rhythm(chords, meter, False)

    # right_notes = random.choice(['arpeggios', 'major_scale', 'blues scale'])
    right_notes = 'arpeggios'
    wrong_notes = random.choice(['chromatic approach', 'enclosure', 'chromatic runs'])
    
    if right_notes == 'arpeggios':
        notes = arpeggios(chords, meter, rhythm, True)
    rhy = rhythm_for_full_chords(meter)
    full_chords = shift_octave(full_chord(invert_chords_in_progression(chords), meter, rhy), -2)

    return notes + full_chords

# x = generate_jazz_progression()
# a = apply_jazz_progression(x, 'B')
# b = convert_chord_names_to_over_measures(a, (4,4))
# print(x)
# print(invert_chords_in_progression(b))

def generate_jazz_chords_and_improv(key_note, meter):
    progression = generate_jazz_progression()
    chord_names = apply_jazz_progression(progression, key_note)
    chords = convert_chord_names_to_over_measures(chord_names, meter)
    return improvise_over_chord_progression(chords, progression, meter)

# progression = ['I', 'vii_dim', 'ii6', 'V7', 'vii_halfdim', 'i']
# test_chords = [([71, 75, 78], (0, 4.0)), ([70, 73, 76, 78], (4.0, 8.0)), ([61, 64, 68, 70], (8.0, 12.0)), ([78, 82, 85, 88], (12.0, 16.0)), ([70, 73, 76, 80], (16.0, 20.0)), ([71, 74, 78], (20.0, 24.0))]
# t = improvise_over_chord_progression(test_chords, progression, (4,4))
t = generate_jazz_chords_and_improv('G', (4,4))
write_to_midi(t, "jazz_improv", 100)


