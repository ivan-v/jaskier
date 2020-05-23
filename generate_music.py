import math

from chord_progression import generate_full_chord_sequence, Special_Chords
from forms import Forms, pick_random_form
from modes_and_keys import apply_key
from motif_generator import generate_pitches
from rhythm import generate_rhythm, merge_pitches_with_rhythm, rhythm_pdf_presets, replace_some_quarters_with_eights


Presets = {
    "meter"      : (3,4),
    "key"        : "Aeolian",
    "mode"       : "C",
    "base"       : 61,
    "rhythm_pdf" : rhythm_pdf_presets["default"],
    "chords"     : "minor",
    "form"       : Forms["Ballad"],
    "rhythm_length" : 2,
    "rhythm_repetition_in_mel" : 3,
}

def repeat_section(section, times):
    return sum([section for i in range(times)], [])

def generate_song(presets):
    
    parts = {}
    applied_key = apply_key(presets["key"], presets["mode"])[1]

    for part in presets["form"]:
        if part not in parts:
            option = generate_full_chord_sequence(presets["chords"], applied_key,
                                                  presets["base"])
            while option in list(parts.values()):
                option = generate_full_chord_sequence(presets["chords"],
                                                      applied_key,
                                                      presets["base"])
            parts[part] = option
    
    pieces = {}
    for part in parts:
        chords = parts[part]
        rhythmic_backbone = generate_rhythm(presets["meter"], 
                                            presets["rhythm_length"],
                                            True, presets["rhythm_pdf"])
        rhythmic_backbone = [replace_some_quarters_with_eights(rhythmic_backbone[i], 3)\
                             for i in range(len(rhythmic_backbone))]
        rhythmic_backbone = replace_some_quarters_with_eights(rhythmic_backbone, 3)
        rhythm = repeat_section(rhythmic_backbone,
                                math.ceil(len(chords)/len(rhythmic_backbone)))
                                # presets["rhythm_repetition_in_mel"])
    # TODO: Better selection of # of repetitions for rhythm per melody
    # TODO: FIX problem \/
    #  Warning!: does 1 chord per measure
 
       melody_length = len(sum(rhythm, []))
        melody = generate_pitches(melody_length, applied_key, 18,
                                    presets["base"], chords, rhythm)
    
        while len(melody) > len(sum(rhythm,[])):
            melody.pop()
    
        pieces[part] = merge_pitches_with_rhythm(melody, sum(rhythm,[]))
    
    song = ""
    for i in range(len(presets["form"])):
        song += pieces[presets["form"][i]]
        if i < len(presets["form"])-1:
            song += " :+: "

    song += ":+: note wn " + presets["base"] 
    # rhythmic_backbone = generate_rhythm(presets["meter"],
    #                                     presets["rhythmic_length"], False,
    #                                     presets["rhythm_pdf"])
    # rhythmic_backbone = replace_some_quarters_with_eights(rhythmic_backbone, 3)
    # melodic_backbone = generate_pitches(len(rhythmic_backbone)*3,
    #                                     applied_key, 18, 2, presets["base"])
    # rhythmic_backbone = repeat_section(rhythmic_backbone,3)
    # print(merge_pitches_with_rhythm(melodic_backbone, rhythmic_backbone))
    # print(generate_pitches(len(chords)*3, applied_key, 18, 2, presets["base"]))
    print(song)
    return song




# TODO: Proper type-checking
def handle_set(command):
    try:
        Presets[command[1]]
        if command[1] == "meter":
            Presets[command[1]] = tuple([int(command[2]), int(command[3])])
        elif command[1] == "base":
            Presets[command[1]] = int(command[2])
        elif command[1] == "rhythm_length":
            Presets[command[1]] = int(command[2])
        elif command[1] == "rhythm_repetition_in_mel":
            Presets[command[1]] = int(command[2])
        else: 
            Presets[command[1]] = command[2]
    except:
        print("Failed:", command[1], "is not in Presets.")


def handle_input(command):
    if command.split()[0] == "set":
        handle_set(command.split())

generate_song(Presets)
# generate_rhythm(meter, measure_count, show_seperate_measures, rhythm_pdf)