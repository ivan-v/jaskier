import random

from chord_progression import available_pitches_in_full_chord
from forms import match_parts_to_form
from rhythm import generate_rhythm, replace_some_quarters_with_eights
from rhythm import merge_pitches_with_rhythm, rhythm_pdf_presets

def shift_octave(part, shift):
    result = part
    for i in range(len(result)):
        result[i][0] += 12*int(shift)
    return result


def choose_leading_tone(origin_pitch, origin_chord, goal):
    sign = (goal-origin>0) - (goal-origin<0)

    r = random.randint(0,2)
    available_pitches = available_pitches_in_full_chord(origin_chord)
    options = [goal - 7*sign, goal - 2*sign, goal - 1*sign]

    random.shuffle(options)

    for option in options:
        if option in available_pitches:
            return option
    return goal

