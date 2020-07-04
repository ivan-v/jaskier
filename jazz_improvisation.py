import random

from chord_progression import convert_chord_names_to_over_measures, invert_chords_in_progression
from generate_music import write_to_midi
from hand_motions import arpeggios, full_chord, running_scales
from jazz_chords import apply_jazz_progression, generate_jazz_progression, coltrane_progression
from melodic_alteration import infer_key_from_chords
from rhythm import generate_rhythm, Space_Values, two_durations_that_equal_another
from rhythm_track import Beat_Intensity_Presets
from stems import shift_octave

# TODO: add varied beats
def generate_melodic_continuity_rhythm(chords, meter, varied_beats, swinging):
    length = chords[-1][1][1]
    num_measures = length/(meter[0]/(meter[1]/4))
    result = []
    if not swinging:
        options = [['qn'], ['en', 'en'], [ '(1 % 3)', '(1 % 3)', '(1 % 3)']]
    else:
        options = [["(1 % 3)", "(2 % 3)"]]
    if not varied_beats:
        single_beat = random.choice(options)
    if meter[1] == 4:
        result = single_beat*int(meter[0]*num_measures)
    elif meter[1] == 8:
        result = single_beat*int(meter[0]*.5*num_measures)
    random.shuffle(result)
    
    return result

# TODO: move to a better place, maybe?
def rhythm_for_full_chords(meter):
    if (meter[0] == 4 and meter[1] == 4) or (meter[0] == 8 and meter[1] == 8):
        return ['wn']
    elif (meter[0] == 3 and meter[1] == 4) or (meter[0] == 6 and meter[1] == 8):
        return ['dhn']
    elif (meter[0] == 2 and meter[1] == 4) or (meter[0] == 4 and meter[1] == 8):
        return ['hn']


def make_wrong_notes(to_replace, goal):
    wrong_notes = random.choice(
        ['chromatic approach', 'enclosure', 'chromatic runs'])
    r = random.choice([-1, 1])
    durations = two_durations_that_equal_another(to_replace[1])
    if wrong_notes == 'enclosure' and Space_Values[to_replace[1]] > .65:
        return [[to_replace[0] + r, durations[0], to_replace[2]], [
            to_replace[0] - r, durations[1],
            to_replace[2] + Space_Values[durations[0]]
        ]]
    elif wrong_notes == 'chromatic runs' and Space_Values[to_replace[1]] > .65:
        return [[to_replace[0] + r, durations[0], to_replace[2]], [
            to_replace[0] + 2*r, durations[1],
            to_replace[2] + Space_Values[durations[0]]
        ]]
    else:
        return [to_replace[0] + r, to_replace[1], to_replace[2]]


def add_tension(chords, notes):
    for i in range(len(chords)-1):
        # find the last note for every chord
        last_note = next(
            filter(lambda x: x[2] + Space_Values[x[1]] >= chords[i][1][1] - .005,
                   iter(notes)))
        to_insert = make_wrong_notes(last_note, chords[i+1][0][0])
        if type(to_insert[0]) == int:
            notes[notes.index(last_note)] = to_insert
        else:
            notes[notes.index(last_note)] = to_insert[0]
            for i in range(len(to_insert[1:])):
                notes.insert(notes.index(to_insert[0])+i, to_insert[1+i])
        # assumes root of the chord is the first element
    return notes


def improvise_over_chord_progression(chords, keys, meter, pitch_range,
                                     swinging, *right_notes):
    # phrasing should be param for rhythm
    # phrasing = random.choice(["melodic_continuity", "phrases"])
    rhythm = generate_melodic_continuity_rhythm(chords, meter, False, swinging)

    # right_notes = random.choice(['arpeggios', 'major_scale', 'blues scale'])
    # right_notes = 'major_scale'  #'arpeggios'
    if right_notes:
        right_notes = right_notes[0]
    else:
        right_notes = ['Blues', 'Ionian']

    if right_notes == 'arpeggios':
        notes = arpeggios(chords, meter, rhythm, True, False)
    elif right_notes == 'major_scale':
        notes = running_scales(chords, meZter, rhythm, pitch_range,
                               infer_key_from_chords(chords), False,
                               ['Ionian'], keys)
    elif right_notes == 'blues_scale':
        notes = running_scales(chords, meter, rhythm, pitch_range,
                               infer_key_from_chords(chords), False,
                               ['Blues'], keys)
    else:
        notes = running_scales(chords, meter, rhythm, pitch_range,
                               infer_key_from_chords(chords), False,
                               ['Blues', 'Ionian'], keys)

    rhy = rhythm_for_full_chords(meter)
    full_chords = shift_octave(
        full_chord(invert_chords_in_progression(chords), meter, rhy), -2)
    better_notes = add_tension(chords, notes)
    
    return notes + full_chords

def generate_jazz_chords_and_improv(key_note, meter, measures_per_chord,
                                    pitch_range, swinging, is_coltrane):
    if is_coltrane:
        chords_and_keys = coltrane_progression(20, key_note)
    else:
        progression = generate_jazz_progression()
        chords_and_keys = apply_jazz_progression(progression, key_note)
    
    keys = [i[0] for i in chords_and_keys]
    chord_names = [i[1] for i in chords_and_keys]
    chords_names = [[name, measures_per_chord] for name in chord_names]
    chords = convert_chord_names_to_over_measures(chords_names, meter)
    
    return improvise_over_chord_progression(chords, keys, meter, pitch_range,
                                            swinging)

# progression = ['I', 'vii_dim', 'ii6', 'V7', 'vii_halfdim', 'i']
# test_chords = [([71, 75, 78], (0, 4.0)), ([70, 73, 76, 78], (4.0, 8.0)), ([61, 64, 68, 70], (8.0, 12.0)), ([78, 82, 85, 88], (12.0, 16.0)), ([70, 73, 76, 80], (16.0, 20.0)), ([71, 74, 78], (20.0, 24.0))]
# t = improvise_over_chord_progression(test_chords, progression, (4,4))
def test():
    t = generate_jazz_chords_and_improv('Bb', (4,4), 2, 20, True, True)
    write_to_midi(t, "jazz_improv", 140)


