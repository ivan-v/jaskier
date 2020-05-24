import random

from chord_progression import available_pitches_in_full_chord
from rhythm import generate_rhythm, replace_some_quarters_with_eights, merge_pitches_with_rhythm, rhythm_pdf_presets
from modes_and_keys import apply_key


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
    
    # print('retrying')
    for v in g[len(pp)-3:]:
        i = 0
        if v:
            i += 1
    return(v > .33*3)
    # return all(sum(g, []))


def select_and_verify_motion(chords, rhythm, pitches, span,
                             previous_motion, mode, base):
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

def generate_pitches(length, mode, span, base, chords, rhythm):
    pitches = [base]
    previous_motion = []
    penultimate_motion = []
    while len(pitches) < length:
        pitches = select_and_verify_motion(chords, rhythm, pitches, span,
                                           [], mode, base)
    return pitches


def motif_generator(meter, measure_count, span, modes_key, base, rhythm_pdf):

    rhythm = generate_rhythm(meter, measure_count, False, rhythm_pdf)
    pitches = generate_pitches(len(rhythm), modes_key, span, base)

#     while is_improvable(pitches):
#         pitches = fix(pitches)

    return merge_pitches_with_rhythm(pitches, rhythm)

# TOOD: "step_size" doesn't do anything atm

# mode = apply_key("Aeolian", "D")
# rhythm = generate_rhythm((3,4), 3, False, {"hn": .33, "qn": .66, "en": .01})
# rhythm = replace_some_quarters_with_eights(rhythm, 3)
# print(rhythm)
# print(generate_pitches(len(rhythm), mode[1], 18, 2, 64))
# print(motif_generator((3,4), 7, 18, 3, mode[1], 60, rhythm_pdf_presets["default"]))


# fix(pitches)

# is_improvable(pitches)
