from forms import Forms
from generate_music import generate_song_and_chords, write_to_midi
from jazz_improvisation import generate_jazz_chords_and_improv
from rhythm_track import Beat_Intensity_Presets

# generate_jazz_chords_and_improv(key_note, meter, measures_per_chord,
                                    # pitch_range, swinging, is_coltrane)
                # example args: 'Bb', (4,4), 2, 20, True, True

# p = generate_song_and_chords(Presets, True)
# p = generate_n_hands(Presets, 2)
# p = generate_song_from_chords(Presets, chords, True)


def generate_chord_progression(form, key, scale, *repetitions_of_sequence, **args):
    pass


def convert_presets_to_full_definitions(new_presets):
    result = {
        "meter"      : new_presets["meter"],
        "key"        : new_presets["key"],
        "base"       : new_presets["base"],
        "rhythm_pdf" : Beat_Intensity_Presets[new_presets["rhythm_pdf"]],
        "form"       : Forms[new_presets["form"]],
        "rhythm_repetition_in_mel" : new_presets["rhythm_repetition_in_mel"],
        "repetitions_in_part" : new_presets["repetitions_in_part"],
        "repeat_chord_progression_in_part" : new_presets["repeat_chord_progression_in_part"],
        "max_step_size" : new_presets["max_step_size"],
        "pitch_range": new_presets["pitch_range"],
        "jazzyness": new_presets["jazzyness"],
        "num_hands": new_presets["num_hands"],
    }
    return result


def generate_song(presets, instrument, tempo):
    new_presets = convert_presets_to_full_definitions(presets)
    p = generate_song_and_chords(new_presets)
    write_to_midi(p, "song", instrument, tempo)

