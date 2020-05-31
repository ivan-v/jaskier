import math

from chord_progression import generate_full_chord_sequence, Special_Chords
from forms import Forms, pick_random_form, match_parts_to_form
from modes_and_keys import apply_key, Starting_Pitch
from motif_generator import generate_pitches
from rhythm import generate_rhythm, merge_pitches_with_rhythm, rhythm_pdf_presets, replace_some_quarters_with_eights
from stems import full_walking_bass_over_form, shift_octave, generate_arpeggios, full_bass_chords_over_form


Presets = {
    "meter"      : (4,4),
    "key"        : "Pentatonic",
    "base"       : "G",
    "rhythm_pdf" : rhythm_pdf_presets["default"],
    "chords"     : "major",
    "form"       : Forms["Ballad"],
    "rhythm_length" : 2,
    "rhythm_repetition_in_mel" : 3,
}


def repeat_section(section, times):
    return sum([section for i in range(times)], [])
 

def generate_parts_and_chords(presets, applied_key):
    parts = {}
    for part in presets["form"]:
        if part not in parts:
            option = generate_full_chord_sequence(presets["chords"], applied_key)
            # if chord sequence already exists, make a new one
            while option in list(parts.values()):
                option = generate_full_chord_sequence(presets["chords"], 
                                                             applied_key)
                                      # Special_Chords["8-bar blues"])
            parts[part] = option
    return parts


def generate_melody_pieces(presets, parts, applied_key):
    pieces = {}
    for part in parts:
        chords = parts[part]
        rhythmic_backbone = generate_rhythm(presets["meter"], 
                                            presets["rhythm_length"],
                                            True, presets["rhythm_pdf"])
        # rhythmic_backbone = [replace_some_quarters_with_eights(rhythmic_backbone[i], 3)\
                             # for i in range(len(rhythmic_backbone))]
        rhythmic_backbone = replace_some_quarters_with_eights(rhythmic_backbone, 3)
        rhythm = repeat_section(rhythmic_backbone,
                                math.ceil(len(chords)/len(rhythmic_backbone)))
        while(len(rhythm) != len(parts[part])):
            rhythm = rhythm[:-1]
                                # presets["rhythm_repetition_in_mel"])
        # TODO: Better selection of # of repetitions for rhythm per melody
        # TODO: FIX problem \/
        #  Warning!: does 1 chord per measure
        melody_length = len(sum(rhythm, []))
        melody = generate_pitches(melody_length, applied_key, 18, chords, rhythm)

        while len(melody) > len(sum(rhythm,[])):
            melody.pop()
        pieces[part] = merge_pitches_with_rhythm(melody, sum(rhythm,[]))

    return pieces

def generate_song(presets):
    
    applied_key = apply_key(presets["key"], presets["base"])
    parts = generate_parts_and_chords(presets, applied_key)

    arpeggios = generate_arpeggios(presets, parts, "double upwards")
    # print("Arpeggios:", arpeggios)

    
    walking_bass = full_walking_bass_over_form(presets["form"], parts, presets["meter"])
    print("> wa :: Music AbsPitch")
    print("> wa =", shift_octave(walking_bass, -1))
    print("\n")

    full_bass = full_bass_chords_over_form(presets["form"], parts, presets["meter"])
    print("> bass :: Music AbsPitch")
    print("> bass =", shift_octave(full_bass, -2))
    print("\n")

    pieces = generate_melody_pieces(presets, parts, applied_key)
    # print(pieces["A"])

    song = match_parts_to_form(presets["form"], pieces)        
    song += " :+: note wn " + str(Starting_Pitch[presets["base"]]) 

    print("> song :: Music AbsPitch")
    print("> song =", song)
    print("\n")

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