import random

from chord_progression import available_pitches_in_chords
from rhythm import generate_rhythm, replace_some_quarters_with_eights, merge_pitches_with_rhythm, rhythm_pdf_presets, Space_Values
# from modes_and_keys import apply_key
from modes_and_keys import apply_key, dominant_key_of_tonic
from forms import sync_note_durations


# TODO: make a better generate_motif
# eventual FIX measure assumption; changing backbone_len isn't noticable 
def generate_rhythm_for_melody(chords, rhythm_pdf, backbone_len,
                               rhythm_repetition_in_mel, meter):
    backbones = []
    num_measures = chords[-1][1][1]/(meter[0]/(meter[1]/4))
    num_backbones = (num_measures/rhythm_repetition_in_mel)/backbone_len
    if type(num_backbones) == float:
        num_backbones = int(num_backbones) + 1
    [
    backbones.append(generate_rhythm(meter, backbone_len, True, rhythm_pdf))
    for i in range(num_backbones)
    ]
    backbones = sum(backbones, [])
    result = []
    for i in range(rhythm_repetition_in_mel):
        result += backbones
    # "File down" if rhythm is too long
    # Eventual FIX improve (currently pops .5 of the rhythm-measure at a time)
    rhythm_len = len(result)

    popped_a_half = False
    while rhythm_len > num_measures:
        if result[-1] == []:
            result.pop()
        if (rhythm_len - num_measures) % 1 == 0:
            while rhythm_len > num_measures:
                result.pop()
                rhythm_len -= 1
        elif not popped_a_half:
            result[-1] = result[-1][:int(len(result[-1])/2)]
        else:
            result.pop()
        rhythm_len -= .5
    return result


def motion(pitch_1, pitch_2):
    if abs(pitch_1 - pitch_2) > 2:
        return "disjunct"
    else:
        return "conjunct"

def convert_pitches_to_dominant_key(given_pitches, base, tonic_key):
    pitches = sum(given_pitches, [])
    fuller_key = sum(
        list(
            map(lambda x: [i + 12 * x + base for i in tonic_key[1][0]],
                range(-3, 3))), [])
    degrees = [
        fuller_key.index(pitch) % len(tonic_key[1][0]) for pitch in pitches
    ]
    offsets = [int((pitch - base) / 12) for pitch in pitches]
    new_key = dominant_key_of_tonic(tonic_key)
    result = [
        new_key[1][0][i] + 12 * offsets[i] + new_key[1][1]
        for i in range(len(degrees))
    ]
    new_pitches = [[result[i + j] for j in range(len(given_pitches[i]))]
                   for i in range(len(given_pitches))]
    return new_pitches

def generate_ap(chords, rhythm, fuller_mode, pitch_range, base):
    chords_without_duration = [chord[0] for chord in chords]
    av = [sum(chord, []) for chord
          in available_pitches_in_chords(chords_without_duration)]
    av_with_duration = {}
    for i in range(len(av)):
        av_with_duration[chords[i][1][0]] = av[i]
    durations = list(av_with_duration.keys())
    ap = []
    time_length = 0
    for i in range(len(rhythm)):
        for j in range(len(rhythm[i])):
            closest = max([i for i in durations if i <= time_length])
            ap.append(av_with_duration[closest])
            time_length += Space_Values[rhythm[i][j]] 
    for i in range(len(ap)):
        # Give a weighed preference towards pitches in the chord
        # (as compared to the scale)
        ap[i] = [val for val in ap[i] for _ in (0, 1)]
        ap[i] = [val for val in ap[i] for _ in (0, 1)]
        ap[i] += fuller_mode
    # Make the pitches within the pitch_range
    ap = [[ap[i][j] for j in range(len(ap[i])) if pitch_range/2 > abs(ap[i][j] - base)]
          for i in range(len(ap))] 
    return ap


# eventual FIX we assume base is lowest pitch of the first chord
def generate_pitches_for_melody(chords, chord_progression, pitch_range,
                                meter, max_step_size, rhythm, applied_key, fuller_mode):
    base = applied_key[1][1]
    ap = generate_ap(chords, rhythm, fuller_mode, pitch_range, base)

    result = []
    expected_motion = random.choice(["conjunct", "disjunct"])
    current_motion_count = 0
    motion_limit = 3
    previous_five_notes = []
    for i in range(len(rhythm)):
        if len(result) == 0:
            measure = [base]
        else:
            measure = []
        for j in range(len(rhythm[i])):
            if len(measure) == 0:
                last_pitch = result[-1][-1]
            else:
                last_pitch = measure[-1]

            if last_pitch in ap[i+j]:
                ap[i+j].remove(last_pitch)
            option = random.choice(ap[i+j])
            # Make sure new pitch is in range and that motions alternate
            if current_motion_count > motion_limit:
                if expected_motion == "conjunct":
                    expected_motion = "disjunct"
                    motion_limit = random.randint(2,7)
                else:
                    expected_motion = "conjunct"
                    motion_limit = random.randint(2,5)
                current_motion_count = 0
            # Make sure the same pitch isn't repeated more than 5 times consecutively
            tries = 0
            while len(set(previous_five_notes)) == 5 or \
                  abs(option - last_pitch) > max_step_size or \
                  motion(option, last_pitch) != expected_motion:
                option = random.choice(ap[i+j])
                tries += 1
                if tries > 80:
                    break
            current_motion_count += 1
            measure.append(option)
            if not len(previous_five_notes) < 5:
                previous_five_notes.pop(0)
            previous_five_notes.append(option)
        result.append(measure)
    # Now to force-insert motif(s)
    motif_len = chords[0][1][1]/(meter[0]/(meter[1]/4))
    if motif_len % 1 != 0:
        motif_len = int(motif_len) + 1
    else:
        motif_len = int(motif_len)
    motif = result[:motif_len]
    motif_rhythm = rhythm[:motif_len]
    dominant_motif = convert_pitches_to_dominant_key(motif, base, applied_key)
    # insert a 5-version of the motif where the 5 chords are
    # TODO: FIX so that dominants are not off-thrown by non 1-per-measure
    dominants = [i for i in range(len(chord_progression)) if chord_progression[i] == 4]
    for dominant in dominants:
        for i in range(motif_len):
            result[dominant + i] = dominant_motif[i]
            rhythm[dominant + i] = motif_rhythm[i]
    tonics = [
                i for i in range(len(chord_progression))
                if chord_progression[i] == 0 and i != 0 and random.randint(0, 1) == 1
                and i != len(chord_progression) - 1
             ]
    for tonic in tonics:
        for i in range(motif_len):
            result[tonic + i] = motif[i]
            rhythm[tonic + i] = motif_rhythm[i]
    return [sum(result, []), rhythm]


def generate_melody(applied_key, chords, chord_progression, rhythm_pdf,
                    backbone_len, rhythm_repetition_in_mel, meter, pitch_range,
                    max_step_size, fuller_mode):
    rhythm = generate_rhythm_for_melody(chords, rhythm_pdf, backbone_len,
                                        rhythm_repetition_in_mel, meter)
    rhym_and_pitches = generate_pitches_for_melody(
        chords, chord_progression, pitch_range, meter, max_step_size, rhythm,
        applied_key, fuller_mode)
    pitches = rhym_and_pitches[0]
    rhythm = sum(rhym_and_pitches[1], [])

    notes = merge_pitches_with_rhythm(pitches[:len(rhythm)], rhythm)
    return sync_note_durations(notes)

