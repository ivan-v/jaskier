import math

from chord_progression import generate_full_chord_sequence, Special_Chords, convert_chord_names_to_over_measures, invert_chords_in_progression
from forms import Forms, pick_random_form, match_parts_to_form, match_and_alter_parts_to_form, sync_note_durations
from hand_motions import generate_hand_motions
from melodic_alteration import insert_passing_tones, strip_part
from midiutil import MIDIFile
from modes_and_keys import apply_key, Starting_Pitch
from motif_generator import generate_pitches
from rhythm import generate_rhythm, merge_pitches_with_rhythm, rhythm_pdf_presets, replace_some_quarters_with_eights, Space_Values
from stems import shift_octave


Presets = {
    "meter"      : (4,4),
    "key"        : "Aeolian",
    "base"       : "D",
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


def generate_melody_pieces(presets, parts, given_chords):
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
        
        length = 0
        for i in range(len(chords)):
            if type(given_chords[i]) == list and \
               type(given_chords[i][0]) == str:
                length += given_chords[i][1]
            else:
                length += 1

        while length > len(rhythm):
            rhythm += rhythmic_backbone

        # TODO: improve (currently pops .5 of the rhythm-measure at a time)
        rhythm_len = len(rhythm)
        while rhythm_len > length:
            if rhythm[-1] == []:
                rhythm.pop()
            rhythm[-1] = rhythm[-1][0:int(len(rhythm[-1])/2)]
            rhythm_len -= .5

        chords = reset_chord_times(chords, presets["meter"])
        # TODO: Better selection of # of repetitions for rhythm per melody
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
        chords = reset_chord_times(chords, presets["meter"])
        melody = sync_note_durations(melody)
        with_passing_tones = insert_passing_tones(strip_part(melody), 1, .5, chords, presets["meter"])
        pieces[part] = merge_pitches_with_rhythm(with_passing_tones[0], with_passing_tones[1])
    return pieces

def compute_chord_times(parts, form, meter):
    result = []
    time_length = 0
    for part in parts:
        for i in range(len(parts[part])):
            # TODO: fix assumption that each chord is one measure long
            parts[part][i] = (parts[part][i], (time_length, 
                              time_length + meter[0]/(meter[1]/4)))
            result.append((parts[part][i][0], (time_length, 
                           time_length + meter[0]/(meter[1]/4))))
            time_length += meter[0]/(meter[1]/4)
    return result

def reset_chord_times(chords, meter):
    time_length = 0
    result = []
    for chord in chords:
        result.append((chord[0], (time_length,
                       time_length + meter[0]/(meter[1]/4))))
        time_length += meter[0]/(meter[1]/4)
    return result


def generate_song_and_chords(presets, make_hand_motions):
    
    applied_key = apply_key(presets["key"], presets["base"])
    parts = generate_parts_and_chords(presets, applied_key)

    chords = compute_chord_times(parts, presets["form"], presets["meter"])
    chords = invert_chords_in_progression(chords)
    pieces = generate_melody_pieces(presets, parts, chords)
    melody = match_and_alter_parts_to_form(presets["form"], pieces)
    final_note = [[melody[0][0], 'wn', melody[-1][2] + Space_Values[melody[-1][1]]]]
    if make_hand_motions:
        for part in parts:
            for i in range(presets["repetitions_in_part"]):
                if i < presets["repetitions_in_part"]-1:
                    parts[part] += parts[part]
        hand_motions = generate_hand_motions(parts, presets["meter"])
        hands = match_parts_to_form(presets["form"], hand_motions)
        # no hand motion for the first time a melody is played in the piece
        for i in range(len(hands)):
            index = int(len(pieces[presets["form"][0]])/presets["repetitions_in_part"])
            if int(hands[i][2]) >= int(melody[index][2]):
                hands = hands[i:]
                break
        return melody + hands + final_note
    else:
        return melody + final_note



def sort_notes_into_measures(notes, meter):
    measure_count = 0
    beats_count = 0
    measure = []
    measures = []
    for note in notes:
        if beats_count + Space_Values[note[1]] > meter[0]/(meter[1]/4):
            beats_count = Space_Values[note[1]]
            measure_count += 1
            measures.append(measure)
            measure = [note]
        else:
            beats_count += Space_Values[note[1]]
            measure.append(note)
    return measures


def generate_song_from_chords(presets, given_chords, make_hand_motions):
    chords = convert_chord_names_to_over_measures(given_chords, presets["meter"])
    chords = invert_chords_in_progression(chords)
    parts = {"A": chords}
    pieces = generate_melody_pieces(presets, parts, given_chords)
    song = match_and_alter_parts_to_form(Forms["One-part"], pieces)
    melody = sync_note_durations(song)
    final_note = [[melody[0][0], 'wn', melody[-1][2] + Space_Values[melody[-1][1]]]]
    if make_hand_motions:
        hand_motions = generate_hand_motions(parts, presets["meter"])
        hands = match_parts_to_form(Forms["One-part"], hand_motions)
        return melody + hands + final_note
    else:
        return melody + final_note


def generate_n_hands(presets, n, *given_chords):
    applied_key = apply_key(presets["key"], presets["base"])
    if given_chords:
        parts = given_chords
        form = Forms["One-part"]
    else:
        form = presets["form"]
        parts = generate_parts_and_chords(presets, applied_key)
    chords = compute_chord_times(parts, form, presets["meter"])
    chords = invert_chords_in_progression(chords)
    hands = []
    hand_motions = []
    for i in range(n):
        hand_motion = generate_hand_motions(parts, presets["meter"])
        while hand_motion in hand_motions:
            hand_motion = generate_hand_motions(parts, presets["meter"])
        hand_motions.append(hand_motion)
        # assuming max num of simultaneous hands = 6
        if i == 0:
            shift = 2
        elif i == 1:
            shift = 0
        elif i == 2:
            shift = 3
        elif i == 3:
            shift = 1
        elif i == 4:
            shift = 4
        else:
            shift = -1
        for part in hand_motion:
            hand_motion[part] = shift_octave(hand_motion[part], shift)
        hands += match_parts_to_form(form, hand_motion)

    return hands

# For now, "song" format assumes [note1, note2, note3, ...]
def write_to_midi(song, filename):
    track    = 0
    channel  = 0
    time     = 0   # In beats
    tempo    = 160 # In BPM
    volume   = 100 # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                         # automatically created)
    MyMIDI.addTempo(track, time, tempo)

    for i in range(len(song)):
        if song[i][0] < 60:
            volume = 93
        elif song[i][0] < 50:
            volume = 89
        elif song[i][0] < 45:
            volume = 85
        else:
            volume = 100
        MyMIDI.addNote(track, channel, song[i][0], song[i][2], Space_Values[song[i][1]], volume)

    with open(filename + ".mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)


# TODO: Proper type-checking, maybe?
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

# Both of these work \/

p = generate_song_and_chords(Presets, True)
# p = generate_n_hands(Presets, 2)
# p = generate_song_from_chords(Presets, chords, True)
write_to_midi(p, "song")

