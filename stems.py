import random

from forms import match_parts_to_form
from rhythm import generate_rhythm, replace_some_quarters_with_eights
from rhythm import merge_pitches_with_rhythm, rhythm_pdf_presets

def shift_octave(part, shift):
    sliced = part.split()
    pitches = [i.isdigit() and int(i) > 20 for i in sliced]
    for i in range(len(pitches)):
      if pitches[i]:
        sliced[i] = str(int(sliced[i])+int(12*shift))
    return ' '.join(sliced)


def generate_arpeggios(presets, parts, pattern):
    arpeggios = ""
    if presets["meter"][1] == 4:
        note = 'qn'
    else:
        note = 'en'
    if pattern == "double upwards":
        pitches = [sum([val for val in parts[part] for _ in (0, 1)], [])
                                                       for part in parts]
    else:
        pitches = [sum(parts[part], []) for part in parts]

    pieces = {}
    c = 0
    for part in parts:
        pieces[part] = merge_pitches_with_rhythm(pitches[c],
                                                 [note]*len(pitches[c]))
        c += 1
    
    return match_parts_to_form(presets["form"], pieces)


def choose_leading_tone(origin, goal):
    sign = (goal-origin>0) - (goal-origin<0)

    r = random.randint(0,2)
    if r == 0:
        return goal - 7*sign
    elif r == 1:
        return goal - 2*sign
    else:
        return goal - 1*sign

def generate_walking_bass(chords, meter):
    bass = []
    for i in range(len(chords)):
        measure = []
        measure.append(chords[i][0])
        if meter[0] > 2:
            measure.append(random.choice(chords[i][1:]))
        if meter[0] % 4 == 0:
            measure.append(random.choice([i for i in chords[i]
                                          if i not in measure]))
        if i < len(chords)-1:
            measure.append(choose_leading_tone(measure[-1], chords[i+1][0]))
        else:
            measure.append(chords[i][0])
        bass.append(measure)
    return bass


# "parts" is a dictionary of parts with their chord progressions as values
def provide_walking_bass(parts, meter):
    sections = {}
    for part in parts:
        sections[part] = sum(generate_walking_bass(parts[part], meter), [])
    return sections

# we assume that different sections have the same meter
def full_walking_bass_over_form(form, parts, meter):
    sections = provide_walking_bass(parts, meter)
    # \/ could use improvement
    beat = 'qn'
    for section in sections:
        sections[section] = " :+: ".join(['note ' + beat + ' ' + str(note)
                                            for note in sections[section]])
    return match_parts_to_form(form, sections)


def basic_full_bass(chords, meter, beat):
    bass = []
    for i in range(len(chords)):
        bass.append("(note " + beat + " " + str(chords[i][0]) + " :=: note " 
                    + beat + " " + str(chords[i][1]) + " :=: note " 
                    + beat + " " + str(chords[i][2]) + " )")
    return bass


def waltz_bass(chords, meter):
    bass = []
    if meter[0] == 3 and meter[1] == 8:
        beat = 'en'
    else:
        beat = 'qn'
    for i in range(len(chords)):
        bass.append("note " + beat + " " + str(chords[i][0]) + (" :+: (note " 
                    + beat + " " + str(chords[i][1]+12) + " :=: note " 
                    + beat + " " + str(chords[i][2]+12) + " )")*2)
    return bass


def generate_full_bass(chords, meter, beat):
    if meter[0] == 3 or meter[0] == 6:
        bass = waltz_bass(chords, meter)
    else:
        bass = basic_full_bass(chords, meter, beat)
    return bass

def provide_full_bass(parts, meter, beat):
    sections = {}
    for part in parts:
        sections[part] = " :+: ".join(generate_full_bass(parts[part], meter, beat))
    return sections


def full_bass_chords_over_form(form, parts, meter):
    beat = "(" + str(meter[0]) + " % " + str(meter[1]) + ")"
    sections = provide_full_bass(parts, meter, beat)
    return match_parts_to_form(form, sections)
    
