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
    "form"       : Forms["Ballad"]
}

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
    
    rhythmic_backbone = generate_rhythm(presets["meter"], 2, False,
                                        presets["rhythm_pdf"])
    rhythmic_backbone = replace_some_quarters_with_eights(rhythmic_backbone, 3)

    melodic_backbone = generate_pitches(len(rhythmic_backbone)*3,
                                        applied_key, 18, 2, presets["base"])

    rhythmic_backbone += rhythmic_backbone + rhythmic_backbone
    print(merge_pitches_with_rhythm(melodic_backbone, rhythmic_backbone))

    song = parts
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
        else: 
            Presets[command[1]] = command[2]
    except:
        print("Failed:", command[1], "is not in Presets.")


def handle_input(command):
    if command.split()[0] == "set":
        handle_set(command.split())

generate_song(Presets)
# generate_rhythm(meter, measure_count, show_seperate_measures, rhythm_pdf)