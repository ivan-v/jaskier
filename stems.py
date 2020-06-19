import random

from forms import match_parts_to_form
from rhythm import generate_rhythm, replace_some_quarters_with_eights
from rhythm import merge_pitches_with_rhythm, rhythm_pdf_presets

def shift_octave(part, shift):
    result = part
    for i in range(len(result)):
        result[i][0] += 12*int(shift)
    return result


def choose_leading_tone(origin, goal):
    sign = (goal-origin>0) - (goal-origin<0)

    r = random.randint(0,2)
    if r == 0:
        return goal - 7*sign
    elif r == 1:
        return goal - 2*sign
    else:
        return goal - 1*sign

