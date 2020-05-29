import random

from chord_progression import available_pitches_in_full_chord
from rhythm import generate_rhythm, replace_some_quarters_with_eights, merge_pitches_with_rhythm, rhythm_pdf_presets
# from modes_and_keys import apply_key


def select_motion():
#     r = random.randint(0, 15)
#     if r == 0:
#         return [0, 0]
#     elif r == 15:
#         return [-1, 0, -1]
#     elif r % 5 == 1:
#         return [1, 2]
#     elif r % 5 == 2:
#         return [2, 4]
#     elif r % 5 == 3:
#         return [-1, -2]
#     elif r % 5 == 4:
#         return [-2, -4]
#     else:
#         return [3, 5]

    return random.choice([[0,0], [1,0,-1], [1,2], [2,4], [-1,-2], [-2,-4],
                         [3,5], [-1,0,1], [0,2], [2,0], [-2,-1], [-3,-1],
                         [5,3], [-2,0,1], [2,1], [4,2], [-4,-2], [-1,-3]])

        # maybe the other way (0,-1,0), too?

def verify_motion_with_chords(pp, chords, rhythm):
    while len(pp) > len(rhythm):
        pp.pop()
    av = [sum(available_pitches_in_full_chord(chord), []) for chord in chords]
    c = [0]+[len(rhythm[i]) for i in range(len(rhythm[0:len(rhythm)+1]))]
    cc = [(c[i] + sum(c[0:i])) for i in range(len(c))]
    q = [zip(rhythm[i], pp[cc[i]:cc[i+1]]) for i in range(len(rhythm))]
    z = ([list(qq) for qq in q])

    nums = [[z[i][j][1] for j in range(len(z[i]))] for i in range(len(z))]

    g = sum([[num in av[i] for num in nums[i]] for i in range(len(nums))], [])
    
    # TODO: this should be a more complete filter
    for v in g[len(pp)-3:]:
        i = 0
        if v:
            i += 1
    return(v > .33*3)
    # return all(sum(g, []))


def select_and_verify_motion(chords, rhythm, pitches, span,
                               previous_motion, applied_key):
    base = applied_key[1][1]
    mode = applied_key[1][0]
    motion = select_motion()
    potential_pitches = []
    fuller_mode = sum(list(map(lambda x: [i + 12*x for i in mode],
                               range(-2,2))),[])

    # prevent the same motion repeating too much
    # and from pitches going out of range
    current_place_in_mode = fuller_mode.index((pitches[-1]-base))
    new_tones = list(map(lambda x: fuller_mode[current_place_in_mode+x], motion))
    potential_pitches = list(map(lambda x: x + base, new_tones))
    out_of_range = span/2 < abs(potential_pitches[-1] - base)


    while not verify_motion_with_chords(pitches+potential_pitches,
                                        chords, rhythm) \
          or  motion == previous_motion or out_of_range:
        motion = select_motion()
        current_place_in_mode = fuller_mode.index(pitches[-1] - base)
        new_tones = list(map(lambda x: fuller_mode[current_place_in_mode+x], motion))
        potential_pitches = list(map(lambda x: x + base, new_tones))
        out_of_range = span/2 < abs(potential_pitches[-1] - base)

    motion = previous_motion
    # Problem: we may cut our chords_and_rhythm unneccessarily when our motion
    # gets rejected later. 
    
    pitches += potential_pitches

    return pitches

def generate_pitches(length, applied_key, span, chords, rhythm):
    pitches = [applied_key[1][1]]
    previous_motion = []
    penultimate_motion = []
    while len(pitches) < length:
        pitches = select_and_verify_motion(chords, rhythm, pitches, span,
                                           [], applied_key)
    return pitches


# TODO: make a better generate_motif

