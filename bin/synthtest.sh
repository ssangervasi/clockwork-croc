#!/bin/bash

sound_font='./data/GeneralUser/GeneralUser GS v1.471.sf2'
midi='./data/MIDI_sample.mid'

# fluidsynth "${sound_font}" "${midi}"
echo "synth"
fluidsynth "${sound_font}"

sleep 2 

echo "mido"
pipenv run mido-play "$midi" &

echo "waiting"
wait %2

echo "done"
