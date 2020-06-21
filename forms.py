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


# Matching parts also syncs the notes correctly

def match_parts_to_form(form, parts):
    result = []
    time_length = 0
    for i in range(len(form)):
        last_note = max([note[2] for note in parts[form[i]]])
        for j in range(int(last_note)):
            notes = [note for note in parts[form[i]] if note[2] == j]
            if notes != []:
                [result.append([note[0], note[1], time_length]) for note in notes]
                time_length += Space_Values[notes[0][1]]
            if j == int(last_note):
                notes = [note for note in parts[form[i]] if note[2] == last_note]
            if notes != []:
                [result.append([note[0], note[1], time_length]) for note in notes]
                time_length += Space_Values[notes[0][1]]
    return result

# TODO: Needs fix/update
def match_and_alter_parts_to_form(form, parts):
    result = []
    # introduced = []
    # alterated = []
    time_length = 0
    for i in range(len(form)):
        done_notes = set()
        for note in parts[form[i]]:
            for some_note in parts[form[i]]:
                if some_note is note and str(some_note) not in done_notes:
                    result.append([note[0], note[1], time_length])
                    done_notes.add(str(note))
                elif some_note[2] == note[2] \
                    and some_note is not note \
                    and str(some_note) not in done_notes:
                    result.append([note[0], note[1], time_length])
            time_length += Space_Values[note[1]]
    #     if parts[form[i]] not in introduced:
    #         introduced += [parts[form[i]]]
    #         result += parts[form[i]]
    #     elif i == len(form)-1:
    #         result += parts[form[i]]
    #     else:
    #         option = alter_part(parts[form[i]])
    #         while option in alterated:    
    #             option = alter_part(parts[form[i]])
    #         alterated += [option]
    #         result += option
    return result

