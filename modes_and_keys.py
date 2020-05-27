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


def apply_key(mode, key):
  modulo = Modes[mode] # + Keys[key][i]
  return (str(key + " " + mode), modulo)
