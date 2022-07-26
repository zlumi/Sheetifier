from analyzer import getProperty, vid2dict, compress_binary_string, key2midi
from midiutil import MIDIFile

vid_path    = "clips/trimmed.mov"
low_key     = "F1"
total_keys  = 65

track       = 0
channel     = 0
bpm         = 82
volume      = 100   # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track, 0, bpm)
vid_data = vid2dict(vid_path, low_key, total_keys, closeness_tolerance=30)
fps = getProperty(vid_path, "fps")

for key in vid_data.keys():
    for note in compress_binary_string(vid_data[key]):
        time = note[0]/fps / (60/bpm)
        duration = (note[1] - note[0])/fps / (60/bpm)

        MyMIDI.addNote(track, channel, key2midi(key), time, duration, volume)

with open("output.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)