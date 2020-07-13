# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
# [START gae_python37_app]
from flask import Flask, request, send_from_directory
from jazz_improvisation import test
from handle_input import generate_song
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

app.config["CLIENT_DOWNLOADS"] = "/tmp/"


@app.route('/')
def hello():
    test()
    res = send_from_directory(app.config["CLIENT_DOWNLOADS"], filename="jazz_improv.mid")
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/song')
def song():
    res = send_from_directory(app.config["CLIENT_DOWNLOADS"], filename="song.mid")
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/song_gen')
def song_gen():
    
    key = request.args.get('key')
    meter = request.args.get('meter')
    scale = request.args.get('scale')
    rhythm_intensity = request.args.get('rhythm_pdf')
    form = request.args.get('form')
    rhythm_repetition_in_mel = request.args.get('rhythm_repetition_in_mel') 
    repetitions_in_part = request.args.get('repetitions_in_part')
    repeat_chord_progression_in_part = request.args.get('repeat_chord_progression_in_part')
    max_step_size = request.args.get('max_step_size')
    pitch_range_mel = request.args.get('pitch_range')
    jazziness = request.args.get('jazziness')
    number_of_hand_motions = request.args.get('num_hands')

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
        "repeat_chord_progression_in_part" : int(repeat_chord_progression_in_part),
        "max_step_size" : int(max_step_size),
        "pitch_range": int(pitch_range_mel),
        "jazzyness": int(jazziness),
        "num_hands": int(number_of_hand_motions)
    }

    generate_song(new_presets, tempo)

    res = send_from_directory(app.config["CLIENT_DOWNLOADS"], filename="song.mid")
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8013, debug=True)
# [END gae_python37_app]
