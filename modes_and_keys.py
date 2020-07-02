# Modes are recorded in relative pitches to the tonic/root note, 0.
Modes = {
  "Ionian":     [0, 2, 4, 5, 7, 9, 11],
  "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
  "Lydian":     [0, 2, 4, 6, 7, 9, 11],
  "Dorian":     [0, 2, 3, 5, 7, 9, 10],
  "Phrygian":   [0, 1, 3, 5, 7, 8, 10],
  "Aeolian":    [0, 2, 3, 5, 7, 8, 10],

  # from David Cope's "Techniques of the Contemporary Composer"
  "Alaska":           [0, 3, 5, 7, 8, 10, 11],
  "Jewish":           [0, 1, 4, 5, 7, 8, 10],
  "India":            [0, 2, 3, 6, 7, 9, 11],
  "Spain":            [0, 1, 3, 5, 7, 8, 11],
  "Asian-Bartok":     [0, 2, 3, 6, 7, 9, 10],
  "Hungarian-Bartok": [0, 2, 4, 6, 7, 9, 10],
  "Bulgarian-Bartok": [0, 1, 3, 5, 7, 9, 10],

  "Pentatonic": [0, 2, 4, 6, 9],
  "Blues":      [0, 3, 5, 6, 7, 10],
  "Japan":      [0, 2, 4, 5, 6, 7, 9, 10, 11],
  "Peru":       [0, 3, 5, 7, 10],
  "Slavic":     [0, 5, 7, 8],

}

Starting_Pitch = {
  "C":  60,
  "Cs": 61,
  "Db": 61,
  "D":  62,
  "Ds": 63,
  "Eb": 63,
  "E":  64,
  "Fb": 64,
  "Es": 65,
  "F":  65,
  "Fs": 66,
  "Gb": 66,
  "G":  67,
  "Gs": 68,
  "Ab": 68,
  "A":  69,
  "As": 70,
  "Bb": 70,
  "B":  71,
  "Cb": 71,
  "Bs": 60,
}


def dominant_key_of_tonic(tonic_key):
  new_root = tonic_key[1][1] + tonic_key[1][0][4]
  if new_root > 71:
    new_root -= 12
  new_pitch = list(Starting_Pitch.keys())[list(Starting_Pitch.values()).index(new_root)]
  return apply_key(tonic_key[0].split()[1], new_pitch)


def apply_key(mode, pitch):
  modulo = Modes[mode] # + Keys[key][i]
  return (str(pitch + " " + mode), (modulo, Starting_Pitch[pitch]))


def make_key(name):
  return apply_key(name.split()[1], name.split()[0])


