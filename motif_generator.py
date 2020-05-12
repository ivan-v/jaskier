import random

from modes_and_keys import apply_key

# meter is a tuple (top, bottom)
# measure_count is an integer

def check_space(meter, measure_count):
    space_for_repeating = False
    if measure_count > 2:
        space_for_repeating = True
    return space_for_repeating

def generate_rhythm_measure(space_left):
    measure = []
    while space_left > 0:
        r = random.randint(0, 3)
        if r == 0 and space_left > 2:
            measure.append("hn")
            space_left -= 2
        elif (r == 1 or r == 2) and space_left > 1:
            measure.append("qn")
            space_left -= 1
        elif r == 3 and space_left > 1:
            measure.append("en")
            measure.append("en")
            space_left -= 1
        else:
            measure.append("en")
            space_left -= .5
    return measure

# Doesn't work with whacky meters (anything other than a base-4 in the denominator)
def generate_rhythm(meter, measure_count):
    breathing_space = check_space(meter, measure_count)
    rhythm = []
    first_measure = generate_rhythm_measure(meter[0]/(meter[1]/4))
    rhythm += first_measure
    measures_left = measure_count - 1
    while measures_left > 0:
        if breathing_space and random.randint(0,3) == 0:
            rhythm += first_measure
        else:
            rhythm += generate_rhythm_measure(meter[0]/(meter[1]/4))
        measures_left -= 1
    return rhythm


# def generate_pitches(size, mode, span, step_size):
    


# def motif_generator(meter, measure_count, span, step_size, modes_key):

#     rhythm = generate_rhythm(meter, measure_count)

#     pitches = generate_pitches(len(rhythm), modes_key, span, step_size)

#     while is_improvable(pitches):
#         pitches = fix(pitches)

#     return map(rhythm, pitches)




# fix(pitches)

# is_improvable(pitches)

# print(generate_rhythm((3,4), 3))