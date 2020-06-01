import random
from rhythm import merge_pitches_with_rhythm

# test_pieces = {
#     'A': 'note qn 71 :+: note qn 70 :+: note hn 66 :+: note qn 71 :+: note en 75 :+: note en 76 :+: note en 75 :+: note en 73 :+: note en 68 :+: note en 71 :+: note en 73 :+: note en 71 :+: note en 70 :+: note en 73 :+: note en 70 :+: note en 76 :+: note en 73 :+: note en 70 :+: note en 66 :+: note en 68 :+: note en 66 :+: note en 64 :+: note en 64 :+: note en 64', 
#     'B': 'note en 71 :+: note en 71 :+: note en 75 :+: note en 71 :+: note en 73 :+: note en 75 :+: note en 76 :+: note en 76 :+: note en 80 :+: note en 83 :+: note en 80 :+: note en 73 :+: note en 76 :+: note en 80 :+: note en 78 :+: note en 82 :+: note en 78 :+: note en 76 :+: note en 73 :+: note en 76 :+: note en 80 :+: note en 76 :+: note en 73 :+: note en 76'
# }

def strip_part(part):
    rhythm = []
    pitches = []
    for bit in part.split(' '):
        if bit.isdigit():
            pitches.append(int(bit))
        elif bit != ":+:" and bit != "note":
            rhythm.append(bit)
    return (pitches, rhythm)


def is_rhythm_constant(sequence):
    return sequence[1][1:] == sequence[1][:-1]

def is_trillable(sequence):
    for i in range(len(sequence[0])-1):
        if sequence[0][i] - sequence[0][i+1] < 6:
            return True
    return False


def alterate_part(part):
    sequence = strip_part(part)
    alteration = random.choice(['retrograde', 'trills'])#, 'invert'])
    if is_trillable(sequence) and alteration == 'trills':
        r = random.choice([1, 2, 3])
        if r == 1:
            sequence = add_quarter_trills(sequence)
        elif r == 2:
            sequence = add_eighth_trills(sequence)
        else:
            sequence = add_quarter_trills(sequence)
            sequence = add_eighth_trills(sequence)
    else: #if alteration == 'retrograde':
        r = random.choice([1, 2, 3])
        if r == 1 and not is_rhythm_constant(sequence):
            sequence = retrograde_only_rhythm(sequence)
        elif r == 2:
            sequence = retrograde_with_rhythm(sequence)
        else:
            sequence = retrograde_without_rhythm(sequence)
    # else:
        # sequence = invert(sequence)
    return merge_pitches_with_rhythm(sequence[0], sequence[1])

# ---------Alterations--------- #

# Returns the reverse of the sequence
def retrograde_with_rhythm(sequence):
    return (sequence[0][::-1], sequence[1][::-1])

def retrograde_without_rhythm(sequence):
    return (sequence[0][::-1], sequence[1])

def retrograde_only_rhythm(sequence):
    return (sequence[0], sequence[1][::-1])

# TODO: Make this sound good
# Returns the inverse (centered around the tonic, assumed to be the first)
# of the sequence
def invert(sequence):
    result = []
    tonic = sequence[0][0]
    return ([tonic - sequence[0][i] + tonic for i in range(len(sequence[0]))],
                                                                   sequence[1])

def insert_n_trills(sequence, i, n, note):
    first_pitch  = sequence[0].pop(i)
    second_pitch = sequence[0].pop(i)
    sequence[1].pop(i)
    sequence[1].pop(i)
    [sequence[0].insert(i, second_pitch)  for j in range(0, n)]
    [sequence[0].insert(i+j, first_pitch) for j in range(0, n*2, 2)]
    [sequence[1].insert(i+j, 'en') for j in range(0, n*2)]
    return sequence


# Replaces longer notes with connecting trills
def add_quarter_trills(sequence):
    for i in range(len(sequence[0])-1):
        if sequence[0][i] - sequence[0][i+1] < 6:
            if sequence[1][i] == 'hn' == sequence[1][i+1]:
                sequence = insert_n_trills(sequence, i, 2, 'qn')
    return sequence


def add_eighth_trills(sequence):
    for i in range(len(sequence[0])-1):
        if sequence[0][i] - sequence[0][i+1] < 6:
            if ((sequence[1][i] == 'hn' and sequence[1][i+1] == 'qn') or \
                (sequence[1][i] == 'qn' and sequence[1][i+1] == 'hn')):
                sequence = insert_n_trills(sequence, i, 3, 'en')
            elif sequence[1][i] == 'qn' == sequence[1][i+1]:
                sequence = insert_n_trills(sequence, i, 2, 'en')
    return sequence
