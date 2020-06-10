import random

from chord_progression import available_pitches_in_chords
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


def select_and_verify_motion(chords, rhythm, pitches, span,
                               previous_motion, applied_key):
    base = applied_key[1][1]
    mode = applied_key[1][0]
    fuller_mode = [j + base for j in sum(list(map(lambda x: 
                                                  [i + 12*x for i in mode],
                                                           range(-3,2))),[])]
    motion = select_motion(fuller_mode, pitches[-1])
    # prevent the same motion repeating too much
    # and from pitches going out of range
    current_place_in_mode = fuller_mode.index(pitches[-1])
    new_tones = [fuller_mode[current_place_in_mode+x] for x in motion]
    out_of_range = span/2 < abs(new_tones[-1] - base)

    while motion == previous_motion or out_of_range:
        motion = select_motion(fuller_mode, pitches[-1])
        new_tones = [fuller_mode[current_place_in_mode+x] for x in motion]
        out_of_range = span/2 < abs(new_tones[-1] - base)
    motion = previous_motion
    # Problem: we may cut our chords_and_rhythm unneccessarily when our motion
    # gets rejected later. -- ^what?
    
    pitches += new_tones

    return pitches

def generate_pitches(length, base, span, chords, rhythm):
    av = [sum(chord, []) for chord in available_pitches_in_chords(chords)]
    ap = sum([[av[i] for note in rhythm[i]] for i in range(len(rhythm))], [])
    
    pitches = [base]
    previous_motion = []
    previous_motion = []
    out_of_range = True
    while len(pitches) < length:
        while out_of_range or motion == previous_motion:
            new_tones = []
            motion = select_motion()
            while len(motion) > length - len(pitches):
                motion.pop() 

            for m in motion:
                if new_tones == []:
                    prev = pitches[-1]
                    available = ap[len(pitches)-1]
                else:
                    prev = new_tones[-1]
                    available = ap[len(pitches)-1 + len(new_tones)]
                available.append(prev)
                available.sort()
                available = list(dict.fromkeys(available))
                if (m + available.index(prev)) > len(available)-1 or \
                                     (m + available.index(prev)) < 0:
                    out_of_range = True
                else:
                    new_tones.append(available[m + available.index(prev)])

            out_of_range = span/2 < abs(new_tones[-1] - base)

        previous_motion = motion
        pitches += new_tones

    return pitches

# TODO: make a better generate_motif

