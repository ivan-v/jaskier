import random

from melodic_alteration import alter_part
from rhythm import Space_Values

Forms = {
    "One-part": ["A"],
    "Binary":   ["A", "B"],
    "Ternary":  ["A", "B", "A"],
    "Arch":     ["A", "B", "C", "B", "A"],
    "Sonata":   ["A", "B", "A"],
    "Ballad":   ["A", "A", "B", "A"],
    "Ballade":  ["A", "A", "B", "A", "B", "A"],
    "Ballade1": ["A", "B", "C", "D", "C", "D", "E", "F", "A", "B"],
    "Ballade2": ["A", "B", "C", "D", "C", "D", "E", "A", "B", "A", "B"],
    "Ballade3": ["A", "B", "A", "B", "C", "D", "E"],
    "Rondo":    ["A", "B", "A", "C", "A", "D", "A", "E", "A", "F"],
    "Verse-chorus": ["Intro", "A", "B", "A", "C", "B", "C", "B"],
}

def pick_random_form():
    name = random.choice(list(Forms))
    return (name, Forms[name])

# Assumes no overlap
def sync_note_durations(notes, *starting_time):
    result = []
    if starting_time:
        time_length = starting_time[0]
    else:
        time_length = 0
    for i in range(len(notes)):
        result.append([notes[i][0], notes[i][1], time_length])
        time_length += Space_Values[notes[i][1]]
    return result

# Matching parts also syncs the notes correctly

def match_parts_to_form(form, parts):
    result = []
    time_length = 0
    for i in range(len(form)):
        times = list(set([note[2] for note in parts[form[i]]]))
        times.sort()
        for j in times:
            notes = [note for note in parts[form[i]] if note[2] == j]
            if notes != []:
                [result.append([note[0], note[1], time_length]) for note in notes]
                time_length += Space_Values[notes[0][1]]
    return result


def match_and_alter_parts_to_form(form, parts):
    result = []
    introduced = []
    alterated = []
    time_length = 0
    for i in range(len(form)):
        subresult = []
        times = list(set([note[2] for note in parts[form[i]]]))
        times.sort()
        for j in times:
            notes = [note for note in parts[form[i]] if note[2] == j]
            if notes != []:
                [subresult.append([note[0], note[1], time_length])
                                                 for note in notes]
                time_length += Space_Values[notes[0][1]]
        if parts[form[i]] not in introduced:
            introduced += [parts[form[i]]]
            result += subresult
        elif i == len(form)-1:
            result += subresult
        else:
            option = sync_note_durations(alter_part(subresult),
                                                subresult[0][2])
            while [[[note[0], note[1]] for note in option]] \
                                                in alterated:
                option = alter_part(subresult)
            alterated += [option]
            result += option
    return result

