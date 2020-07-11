from generate_music import write_to_midi
from jazz_improvisation import generate_jazz_chords_and_improv


generate_jazz_chords_and_improv(key_note, meter, measures_per_chord,
                                    pitch_range, swinging, is_coltrane)
                # example args: 'Bb', (4,4), 2, 20, True, True

p = generate_song_and_chords(Presets, True)
p = generate_n_hands(Presets, 2)
p = generate_song_from_chords(Presets, chords, True)


def generate_chord_progression(form, key, scale, *repetitions_of_sequence, **args)


def generate_song(key, scale, meter, **args):
    if "rhythm_intensity" in args:
        rhythm_intensity = args["rhythm_intensity"]
    else:
        rhythm_intensity = "5"
    if "jazziness" in args:
        jazziness = args["jazziness"]
    else:
        jazziness = 0
    if "tempo" in args:
        tempo = args["tempo"]
    else:
        tempo = random.randint(135, 165)
    if "form" in args:
        form = args["form"]
    else:
        form = "Ballad #1"
    if "max_step_size" in args:
        max_step_size = args["max_step_size"]
    else:
        max_step_size = 13
    if "pitch_range_mel" in args:
        pitch_range_mel = args["pitch range mel"]
    else:
        pitch_range_mel = 17
    if "rhythm_repetition_in_mel" in args:
        rhythm_repetition_in_mel = args["rhythm_repetition_in_mel"] + 1
    else:
        rhythm_repetition_in_mel = 3
    if "repetitions_in_part" in args:
        repetitions_in_part = args["repetitions_in_part"] + 1
    else:
        repetitions_in_part = 2
    if "repeat_chord_progression_in_part" in args:
        repeat_chord_progression_in_part = args["repeat_chord_progression_in_part"] + 1
    else:
        repeat_chord_progression_in_part = 1
    if "number_of_hand_motions" in args:
        number_of_hand_motions = args["number_of_hand_motions"]
    else:
        number_of_hand_motions = 1

    new_presets = {
        "meter"      : meter,
        "key"        : scale,
        "base"       : key,
        "rhythm_pdf" : rhythm_intensity,
        "form"       : form,
        "rhythm_repetition_in_mel" : rhythm_repetition_in_mel,
        "repetitions_in_part" : repetitions_in_part,
        "repeat_chord_progression_in_part" : repeat_chord_progression_in_part,
        "max_step_size" : max_step_size,
        "pitch_range": pitch_range_mel,
        "jazzyness": jazziness,
        "num_hands": number_of_hand_motionsz
    }

    
    p = generate_song_and_chords(new_presets)


write_to_midi(p, "song", 0)



