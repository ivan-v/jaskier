import random

# should add up to 1
rhythm_pdf_presets = {
    "default": {"hn": .33, "qn": .66, "en": .01},
}

# meter is a tuple (top, bottom)
# measure_count is an integer

def check_space(meter, measure_count):
    space_for_repeating = False
    if measure_count > 2:
        space_for_repeating = True
    return space_for_repeating


def generate_rhythm_measure(space_left, rhythm_pdf):
    measure = []
    space_values = {"hn": 2, "qn": 1, "en": .5}
    pdf = list(rhythm_pdf.values())
    pmf = [(pdf[i] + sum(pdf[0:i])) for i in range(len(pdf))]
    while space_left > 0:
        r = random.randint(0, 99)/100
        p = next(x for x in pmf if x > r)
        note = list(rhythm_pdf.keys())[list(rhythm_pdf.values()).index(pdf[pmf.index(p)])]
        if space_left >= space_values[note]:
            space_left -= space_values[note]
            measure.append(note)
    return measure


def replace_some_quarters_with_eights(rhythm, frequency):
    new_rhythm = rhythm
    for i in range(len(new_rhythm)):
        r = random.randint(0, frequency)
        if r == 0 and new_rhythm[i] == "qn":
            new_rhythm[i] = "en"
            new_rhythm.insert(i, 'en')
    return new_rhythm



# Doesn't work with whacky meters (anything other than a base-4 in the denominator)
def generate_rhythm(meter, measure_count, show_seperate_measures, rhythm_pdf):
    breathing_space = check_space(meter, measure_count)
    rhythm = []
    first_measure = generate_rhythm_measure(meter[0]/(meter[1]/4), rhythm_pdf)
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
            new_measure = generate_rhythm_measure(meter[0]/(meter[1]/4), rhythm_pdf)
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