from rhythm import generate_rhythm_measure

Beat_Intensity_Presets = {
    "0":  {"hn": .8, "qn": .2},
    "1":  {"hn": .6,  "(3 % 8)": .2,  "qn": .1, "(1 % 3)": .0,  "en": .1},
    "2":  {"hn": .5,  "(3 % 8)": .1,  "qn": .1, "(1 % 3)": .2,  "en": .1},
    "3":  {"hn": .4,  "(3 % 8)": .3,  "qn": .1, "(1 % 3)": .1,  "en": .1},
    "4":  {"hn": .3,  "(3 % 8)": .2,  "qn": .3, "(1 % 3)": .1,  "en": .1},
    "5":  {"hn": .2,  "(3 % 8)": .2,  "qn": .2, "(1 % 3)": .2,  "en": .2},
    "6":  {"hn": .1,  "(3 % 8)": .2,  "qn": .3, "(1 % 3)": .3,  "en": .2},
    "7":  {"hn": .05, "(3 % 8)": .15, "qn": .3, "(1 % 3)": .2,  "en": .3},
    "8":  {"hn": .0,  "(3 % 8)": .1,  "qn": .3, "(1 % 3)": .2,  "en": .5},
    "9":  {"hn": .0,  "(3 % 8)": .05, "qn": .2, "(1 % 3)": .25, "en": .5},
    "10": {"hn": .0,  "(3 % 8)": .05, "qn": .1, "(1 % 3)": .25, "en": .6},
}

# levels of intensity: 0-10
def generate_rhythmic_beat(meter, intensity, length, show_seperate_measures):
    beat = []
    beats = 0
    rhythm_pdf = Beat_Intensity_Presets[str(intensity)]
    while beats < length:
        measure = generate_rhythm_measure(meter[0]/(meter[1]/4), rhythm_pdf)
        if show_seperate_measures:
            beat += [measure]
        else:
            beat += measure
        beats += 1
    return beat

