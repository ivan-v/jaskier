import random

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
def generate_rhythm(meter, measure_count, show_seperate_measures):
    breathing_space = check_space(meter, measure_count)
    rhythm = []
    first_measure = generate_rhythm_measure(meter[0]/(meter[1]/4))
    unique_measures = {tuple(first_measure)}
    if show_seperate_measures:
        first_measure = [first_measure]
    rhythm += first_measure
    measures_left = measure_count - 1
    while measures_left > 0:
        if breathing_space and random.randint(0,2) == 0:
            if show_seperate_measures:
                rhythm += [random.choice([list(i) for i in unique_measures])]
            else:
                rhythm += random.choice([list(i) for i in unique_measures])
        else:
            new_measure = generate_rhythm_measure(meter[0]/(meter[1]/4))
            unique_measures.add(tuple(new_measure))
            if show_seperate_measures:
                rhythm += [new_measure]
            else:
                rhythm += new_measure
        measures_left -= 1
    return rhythm

def merge_pitches_with_rhythm(pitches, rhythm):
    result = ""
    for i in range(len(pitches)):
        result += "note " + rhythm[i] + " " + str(pitches[i]) 
        if i < len(pitches)-1:
            result += " :+: "
    return result