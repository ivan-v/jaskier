import random

from rhythm import generate_rhythm, replace_some_quarters_with_eights, merge_pitches_with_rhythm, rhythm_pdf_presets
from modes_and_keys import apply_key

def select_motion():
    r = random.randint(0,15)
    if r == 0:
        return [0,0]
    elif r == 15:
        return [-1,0,-1]
    elif r % 5 == 1:
        return [1,2]
    elif r % 5 == 2:
        return [2,4]
    elif r % 5 == 3:
        return [-1,-2]
    elif r % 5 == 4:
        return [-2,-4]
    else:
        return [3, 5]
        # maybe the other way (0,-1,0), too?

def generate_pitches(length, mode, span, step_size, base):
    pitches = [base]
    previous_motion = []
    penultimate_motion = []

    fuller_mode = []
    for i in range(-2, 2):
        for j in range(len(mode)):
            fuller_mode.append(mode[j] + i*12)

    while len(pitches) < length:
        motion = select_motion()
        # prevent the same motion repeating too much
        # and from pitches going out of range
        is_repeating = motion == previous_motion #and motion == penultimate_motion

        current_place_in_mode = fuller_mode.index((pitches[-1]-base))
        new_tones = list(map(lambda x: fuller_mode[current_place_in_mode+x], motion))
        potential_pitches = list(map(lambda x: x + base, new_tones))
        out_of_range = span/2 < abs(potential_pitches[-1] - base)

        while is_repeating or out_of_range:
            motion = select_motion()
            is_repeating = motion == previous_motion #and motion == penultimate_motion
            current_place_in_mode = fuller_mode.index(pitches[-1] - base)
            new_tones = list(map(lambda x: fuller_mode[current_place_in_mode+x], motion))
            potential_pitches = list(map(lambda x: x + base, new_tones))
            out_of_range = span/2 < abs(potential_pitches[-1] - base)

        penultimate_motion = previous_motion    
        previous_motion = motion

        pitches += potential_pitches

    # trim down if too long
    while len(pitches) > length:
        pitches.pop()

    return pitches


def motif_generator(meter, measure_count, span, step_size, modes_key, base, rhythm_pdf):

    rhythm = generate_rhythm(meter, measure_count, False, rhythm_pdf)
    pitches = generate_pitches(len(rhythm), modes_key, span, step_size, base)

#     while is_improvable(pitches):
#         pitches = fix(pitches)

    return merge_pitches_with_rhythm(pitches, rhythm)

# TOOD: "step_size" doesn't do anything atm

# mode = apply_key("Aeolian", "D")
# rhythm = generate_rhythm((3,4), 3, False, {"hn": .33, "qn": .66, "en": .01})
# rhythm = replace_some_quarters_with_eights(rhythm, 3)
# print(rhythm)
# print(generate_pitches(len(rhythm), mode[1], 18, 2, 64))
# print(motif_generator((3,4), 7, 18, 3, mode[1], 60, rhythm_pdf_presets["default"]))


# fix(pitches)

# is_improvable(pitches)
