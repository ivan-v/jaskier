# Algorithmic Music Composition

Grammar-based midi music-file generation using Python 3, with some additional libraries.

## Python Version used

3.7.7

### Prerequisites

What you need to install and how to install them

```
pip install midiutil
pip install statistics
```

The standard Python libraries of `math` and `sys` are also used. 

## Running the program

Eventually there will be a web interface for the program.
For now, this is how you run it:

```
python generate_music.py
```
Doing so will generate a midi file in the current directory, by default named `song.mid`.
To tinker around with the song-generation settings, the best way to do so is to modify `hand_motions.py` and `Presets` in `generate_music.py`.

## Author

**Ivan Viro**
