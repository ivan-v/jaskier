from modes_and_keys import Starting_Pitch

Pitches_to_Chord_Type = {
    (0, 4, 7):'M', 
    (0, 3, 7):'m', 
    (0, 5, 7):'suss', 
    (0, 3, 6):'dim', 
    (0, 4, 8):'aug', 
    (0, 4, 7, 11):'M7', 
    (0, 3, 7, 10):'m7', 
    (0, 4, 7, 10):'7', 
    (0, 4, 6, 10):'7b5',
    (0, 3, 6, 10):'m7b5', 
    (0, 4, 7, 9):'6',
    (0, 3, 7, 9):'m6',
    (0, 4, 8, 10):'7#5',
    (0, 3, 7, 14):'m+9', 
    (0, 3, 6, 9):'dim7', 
    (0, 3, 6, 10):'halfdim7', 
    (0, 3, 7, 10, 14):'m9', 
    (0, 4, 7, 10, 11):'Dom.min9', 
    (0, 4, 7, 10, 14):'9',
    (0, 4, 7, 10, 13):'b9', 
    (0, 4, 7, 11, 14):'M9', 
    (0, 7, 10, 14, 17):'11', 
    (0, 4, 7, 10, 15):'7#9', 
    (0, 4, 7, 10, 18):'7#11', 
    (0, 3, 7, 10, 14, 17):'m11', 
    (0, 4, 7, 11, 14, 18):'M7#11', 
    (0, 4, 7, 10, 14, 21):'13', 
    (0, 4, 7, 11, 14, 21):'M13', 
    (0, 3, 7, 10, 14, 17, 21):'m13',
}


Qualities_to_Pitches = {
    "simple major happy": (0, 4, 7),
    "simple minor sad": (0, 3, 7),
    "major minor regal martial": (0, 5, 7),
    "minor dark strained complex": (0, 3, 6),
    "major anticipation motion": (0, 4, 8),
    "major pretty delicate": (0, 4, 7, 11),
    "major dominant jazzy": (0, 4, 7, 10),
    "minor pensive moody introspective": (0, 3, 7, 10),
    "minor sad tender complex jazzy": (0, 3, 7, 10, 14),
    "major energetic lively jazzy": (0, 4, 7, 11, 14),
    "minor dispairing sorrow difficult": (0, 3, 6, 10),
    "major playful": (0, 4, 7, 9),
    "minor dark sensuous troubled": (0, 3, 7, 9),
}





def determine_scale_quality(qualities):
    quality_evaluation = sum(sum([[(0 if 'major minor'
                             in entry else (1 if 'major'
                             in entry else -1)) for entry in [bit
                             for bit in
                             list(Qualities_to_Pitches.keys())
                             if quality in bit]] for quality in
                             qualities], []))
    if quality_evaluation > 0:
        return 'major'
    else:
        return 'minor'

def get_chords_from_qualities(qualities, scale_):
    return [[Qualities_to_Pitches[entry] for entry in
            list(Qualities_to_Pitches.keys()) if quality in entry]
            for quality in qualities]


# scale_quality_known = False
# qualities = ['dark', 'sad', 'jazzy']
# qualities_in_pitches = [[Qualities_to_Pitches[entry] for entry in list(Qualities_to_Pitches.keys()) if quality in entry] for quality in qualities]


def convert_chord_name_to_chord(base, quality):
    root = Starting_Pitch[base]
    pitches = list(list(pitches_to_chord_type.keys())[list(pitches_to_chord_type.values()).index(quality)])
    return [i + root for i in pitches]


def convert_chord_names_to_chords(chord_names):
    return [convert_chord_name_to_chord(chord_name[0], chord_name[1]) for chord_name in chord_names]


def convert_chord_to_name(chord):
    pitches = [i - chord[0] for i in chord]
    quality = pitches_to_chord_type[tuple(pitches)]
    root = chord[0]
    while root > 71:
        root -= 12

    starting_pitch = list(Starting_Pitch.keys())[list(Starting_Pitch.values()).index(root)]
    if 's' in starting_pitch:
        starting_pitch = starting_pitch.replace('s', '#')
    return starting_pitch + ' ' + quality


def convert_chords_to_names(chords):
    return [convert_chord_to_name(chord) for chord in chords]