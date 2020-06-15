import math

from chord_progression import convert_chord_names_to_sequence, generate_full_chord_sequence, Special_Chords
from forms import Forms, pick_random_form, match_parts_to_form, match_and_alter_parts_to_form
from melodic_alteration import insert_passing_tones, strip_part
from modes_and_keys import apply_key, Starting_Pitch
from motif_generator import generate_pitches
from rhythm import generate_rhythm, merge_pitches_with_rhythm, rhythm_pdf_presets, replace_some_quarters_with_eights, Space_Values
from stems import shift_octave#, generate_arpeggios, full_walking_bass_over_form, full_bass_chords_over_form


from midiutil import MIDIFile

Presets = {
    "meter"      : (4,4),
    "key"        : "Ionian",
    "base"       : "E",
    "rhythm_pdf" : rhythm_pdf_presets["default"],
    "form"       : Forms["Ballade"],
    "rhythm_length" : 2,
    "rhythm_repetition_in_mel" : 3,
    "repetitions_in_part" : 2,
}

def repeat_section(section, times):
    return sum([section for i in range(times)], [])
 

def generate_parts_and_chords(presets, applied_key):
    parts = {}
    for part in presets["form"]:
        if part not in parts:
            option = generate_full_chord_sequence(applied_key)
            # if chord sequence already exists, make a new one
            while option in list(parts.values()):
                option = generate_full_chord_sequence(applied_key)
                                      # Special_Chords["8-bar blues"])
            parts[part] = repeat_section(option, presets["repetitions_in_part"])
    return parts


def generate_melody_pieces(presets, parts):
    pieces = {}
    for part in parts:
        chords = parts[part]
        base = Starting_Pitch[presets["base"]]
        rhythmic_backbone = generate_rhythm(presets["meter"], 
                                            presets["rhythm_length"],
                                            True, presets["rhythm_pdf"])

        rhythmic_backbone = replace_some_quarters_with_eights(rhythmic_backbone, 3)
        rhythm = repeat_section(rhythmic_backbone,
                                math.ceil(len(chords)/len(rhythmic_backbone)))
        
        if len(chords)-len(rhythm) < 0:
            while len(rhythm) != len(chords):
                rhythm.pop()

        # TODO: Better selection of # of repetitions for rhythm per melody
        # TODO: FIX problem \/
        #  Warning!: does 1 chord per measure
        melody_length = len(sum(rhythm, []))
        melody = generate_pitches(melody_length, base, 18, chords, rhythm)
        while len(melody) > len(sum(rhythm,[])):
            melody.pop()

        bit = merge_pitches_with_rhythm(melody, sum(rhythm,[]))
        melody = bit
        for i in range(presets["repetitions_in_part"]):
            if i < presets["repetitions_in_part"]-1:
                melody += melody
                chords += chords
        with_passing_tones = insert_passing_tones(strip_part(melody), 2, .5, chords, presets["meter"])
        pieces[part] = merge_pitches_with_rhythm(with_passing_tones[0], with_passing_tones[1])

    return pieces

# TODO: Major rework and update to new form
# def generate_song_and_chords(presets):
    
#     applied_key = apply_key(presets["key"], presets["base"])
#     parts = generate_parts_and_chords(presets, applied_key)

#     arpeggios = generate_arpeggios(presets, parts, "double upwards")
#     # print("Arpeggios:", arpeggios)

    
#     # bass = full_walking_bass_over_form(presets["form"], parts, presets["meter"])
#     # print("Walking Bass:", shift_octave(bass, -1))
#     full_bass = full_bass_chords_over_form(presets["form"], parts, presets["meter"])
#     print("\n")
#     print('> bass :: Music AbsPitch')
#     print("> bass = ", shift_octave(full_bass, -2))

#     pieces = generate_melody_pieces(presets, parts)
#     # print(pieces)

#     song = match_and_alter_parts_to_form(presets["form"], pieces)        
#     song += ":+: note wn " + str(Starting_Pitch[presets["base"]]) 
#     print('> song :: Music AbsPitch')
#     print("> song = ", shift_octave(song, 0))
#     return song
def sync_note_durations(song):
    time_length = 0
    for i in range(len(song)):
        song[i][2] = time_length
        time_length += Space_Values[song[i][1]]
    return song


def generate_song_from_chords(presets, given_chords):
    chords = convert_chord_names_to_sequence(given_chords)
    parts = {"A": chords}
    pieces = generate_melody_pieces(presets, parts)
    song = match_and_alter_parts_to_form(Forms["One-part"], pieces)        
    # TODO: Add whole note at the end, maybe?
    return song


# For now, "song" format assumes [note1, note2, note3, ...]
def write_to_midi(song):
    track    = 0
    channel  = 0
    time     = 0   # In beats
    tempo    = 130  # In BPM
    volume   = 100 # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                         # automatically created)
    MyMIDI.addTempo(track,time, tempo)

    for i in range(len(song)):
        MyMIDI.addNote(track, channel, song[i][0], song[i][2], Space_Values[song[i][1]], volume)

    with open("song.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)


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

chords = ['Am', 'G', 'Fmaj7', 'Em', 
  'Dm7', 'G7', 'Cmaj7', 'Bbmaj7', 'Bm11', 'E7', 'Am', 'G', 'Fmaj7', 'Em', 
  'Dm7', 'G7', 'Cmaj7']
p = generate_song_from_chords(Presets, chords)
write_to_midi(sync_note_durations(p))

