import random

from rhythm import Space_Values
from rhythm_track import generate_rhythmic_beat, generate_rhythmic_motion
from stems import shift_octave

# TODO: add/complete hand motions

def octave_doubling(chords, meter, rhythm):
    degree = generate_rhythmic_motion(1, 3, True)[0]
    measure_length = meter[0]/(meter[1]/4)
    notes = []
    time_length = 0
    for i in range(len(chords)):
        # \/ size of measure for the chord
        measure_size = int(len(rhythm)*((chords[i][1][1]-chords[i][1][0])/measure_length))
        for j in range(measure_size):
            notes.append([chords[i][0][degree], rhythm[j], time_length])
            notes.append([chords[i][0][degree]-12, rhythm[j], time_length])
            time_length += Space_Values[rhythm[j]]
    return notes

def arpeggios(chords):
    return

def full_chord(chords, rhythm):
    return

def running_scale(pitches):
    return

def pick_hand_motion(chords, meter, rhythm):
    return octave_doubling(chords, meter, rhythm)

def generate_rhythm_from_meter(meter, **kargs):
    if "intensity" in kargs:
        intensity = kargs["intensity"]
    else:
        intensity = random.choice(list(range(0, 4)))
    # TODO: make different rhythm-measure lengths work fine with chord-measure-durations
    if "rhythm_len" in kargs:
        rhythm_length = kargs["rhythm_len"]
    else:
        rhythm_length = 1 # random.choice(1,2)
    return generate_rhythmic_beat(meter, intensity, rhythm_length, False)

def generate_hand_motion(chords, meter, **args):
    if "rhythm" in args:
        beats = args["rhythm"]
    else:
        if "rhythm_len" in args:
            l = args["rhythm_len"]
        else:
            l = False
        if "intensity" in args:
            inten = args["intensity"]
        else:
            inten = False
        if inten and l:
            beats = generate_rhythm_from_meter(meter, rhythm_len=l, intensity=inten)
        elif inten:
            beats = generate_rhythm_from_meter(meter, intensity=inten)
        elif l:
            beats = generate_rhythm_from_meter(meter, rhythm_len=l)
        else:
            beats = generate_rhythm_from_meter(meter)

    # determine how much shift_octave to do
    if "hand" in args:
        hand = args["hand"]
    else:
        hand = "left"

    if hand.lower() == "left":
        return shift_octave(pick_hand_motion(chords, meter, beats), -2)
    else:
        return shift_octave(pick_hand_motion(chords, meter, beats), 1)

def generate_hand_motions(parts, meter, **args):
    motions = {}
    if "rhythm" in args:
        beats = args["rhythm"]
        for part in parts:
            motions[part] = generate_hand_motion(parts[part], meter, rhythm=beats)
    else:
        if "rhythm_len" in args:
            l = args["rhythm_len"]
        else:
            l = False
        if "intensity" in args:
            inten = args["intensity"]
        else:
            inten = False
        if inten and l:
            for part in parts:
                motions[part] = generate_hand_motion(parts[part], meter, 
                                                     rhythm_len=l,
                                                     intensity=inten)
        elif inten:
            for part in parts:
                motions[part] = generate_hand_motion(parts[part], meter, 
                                                         intensity=inten)
        elif l:
            for part in parts:
                motions[part] = generate_hand_motion(parts[part], meter,
                                                            rhythm_len=l)
        else:
            for part in parts:
                motions[part] = generate_hand_motion(parts[part], meter)
    return motions

