import os
# [START gae_python37_app]
from flask import Flask, request, send_from_directory
from jazz_improvisation import test
from handle_input import generate_song
from rhythm_track import Beat_Intensity_Presets

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

app.config["CLIENT_DOWNLOADS"] = "/tmp/"


@app.route('/')
def hello():
    test()
    res = send_from_directory(app.config["CLIENT_DOWNLOADS"], filename="jazz_improv.midi", as_attachment=True)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/song')
def song():
    res = send_from_directory(app.config["CLIENT_DOWNLOADS"], filename="song.midi", as_attachment=True)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/backing_track_gen')
def backing_track_gen():

    new_presets = {
        "style" : request.args.get('style'),
        "key"   : request.args.get('key').split()[0],
        "meter" : eval(request.args.get('meter')),
        "measures_per_chord" : int(request.args.get('measures_per_chord')),
        "rhythm_pdf" : Beat_Intensity_Presets[request.args.get('rhythm_pdf')],
        "rhythm_intensity": request.args.get('rhythm_pdf'),
        "num_repetitions" : int(request.args.get('num_repetitions')),
        "instrument" : int(request.args.get('instrument')),
    }

    tempo = int(request.args.get('tempo'))

    generate_backing_track(new_presets, tempo)

    res = send_from_directory(app.config["CLIENT_DOWNLOADS"], filename="song.midi")
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/song_gen')
def song_gen():

    key = request.args.get('key')
    meter = request.args.get('meter')
    scale = request.args.get('scale')
    rhythm_intensity = Beat_Intensity_Presets[request.args.get('rhythm_pdf')]
    form = request.args.get('form')
    rhythm_repetition_in_mel = request.args.get('rhythm_repetition_in_mel') 
    repetitions_in_part = request.args.get('repetitions_in_part')
    repeat_chord_progression_in_part = request.args.get('repeat_chord_progression_in_part')
    max_step_size = request.args.get('max_step_size')
    pitch_range_mel = request.args.get('pitch_range')
    jazziness = request.args.get('jazziness')
    number_of_hand_motions = request.args.get('num_hands')
    
    instrument = int(request.args.get('instrument'))

    tempo = int(request.args.get('tempo'))

    if scale == "Major (Ionian)":
        scale = "Ionian"
    elif scale == "Minor (Aeolian)":
        scale = "Aeolian"
    if number_of_hand_motions == "Only Melody":
        number_of_hand_motions = 0

    new_presets = {
        "meter"      : eval(meter),
        "key"        : scale.split()[0],
        "base"       : key.split()[0],
        "rhythm_pdf" : rhythm_intensity,
        "form"       : form,
        "rhythm_repetition_in_mel" : int(rhythm_repetition_in_mel),
        "repetitions_in_part" : int(repetitions_in_part),
        "repeat_chord_progression_in_part" : int(repeat_chord_progression_in_part)+1,
        "max_step_size" : int(max_step_size),
        "pitch_range": int(pitch_range_mel),
        "jazzyness": int(jazziness),
        "num_hands": int(number_of_hand_motions),
    }
    
    generate_song(new_presets, instrument, tempo)

    res = send_from_directory(app.config["CLIENT_DOWNLOADS"], filename="song.midi")
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8013, debug=True)
# [END gae_python37_app]
