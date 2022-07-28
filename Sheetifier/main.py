from midiutil import MIDIFile
from analyzer import compress_binary_string, key2midi
from config import *

MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track, 0, bpm)

for key in vid_data.keys():
    for note in compress_binary_string(vid_data[key]):
        time = note[0]/fps / (60/bpm)
        duration = (note[1] - note[0])/fps / (60/bpm)

        MyMIDI.addNote(track, channel, key2midi(key), time, duration, volume)

with open("output.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)