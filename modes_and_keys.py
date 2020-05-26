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

  # TODO: make non-8 note scales work properly
  "Pentatonic": [0, 2, 4, 6, 9],
  "Blues":      [0, 3, 5, 6, 7, 10],
  "Japan":      [0, 2, 4, 5, 6, 7, 9, 10, 11],
  "Peru":       [0, 3, 5, 7, 10],
  "Slavic":     [0, 5, 7, 8],

}

# Keys are recorded how/which tones (selected by the modes) have to be modified
Keys = {
  "C":  [0, 0, 0, 0, 0, 0, 0],
  "G":  [0, 0, 0, 0, 0, 0, 1], # [shift f up]
  "D":  [0, 1, 0, 0, 0, 1, 0], # [shift f, c up]
  "A":  [0, 0, 1, 0, 0, 1, 1], # [shift f, c, g up]
  "E":  [0, 1, 1, 0, 0, 1, 1], # [shift f, c, g, d up]
  "B":  [0, 1, 1, 0, 1, 1, 1], # [shift f, c, g, d, a up]
  "Fs": [1, 1, 1, 0, 1, 1, 1], # [shift f, c, g, d, a, e up]
  "Cs": [1, 1, 1, 1, 1, 1, 1], # [shift f, c, g, d, a, e, b up]
  "F":  [0, 0, 0, -1, 0, 0, 0], # [shift b down]
  "Bb": [-1, 0, 0, -1, 0, 0, 0], # [shift b, e down]
  "Eb": [-1, 0, 0, -1, -1, 0, 0], # [shift b, e, a down]
  "Ab": [-1, -1, 0, -1, -1, 0, 0], # [shift b, e, a, d down]
  "Db": [-1, -1, 0, -1, -1, -1, 0], # [shift b, e, a, d, g down]
  "Gb": [-1, -1, -1, -1, -1, -1, 0], # [shift b, e, a, d, g, c down]
  "Cb": [-1, -1, -1, -1, -1, -1, -1] # [shift b, e, a, d, g, c, f down] 
}

def apply_key(mode, key):
  modulo = [0, 0, 0, 0, 0, 0, 0]
  for i in range(len(Keys[key])):
    modulo[i] = Modes[mode][i] + Keys[key][i]
  return (str(key + " " + mode), modulo)
