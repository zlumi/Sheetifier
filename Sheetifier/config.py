track       = 0
channel     = 0
bpm         = 113
volume      = 100   # 0-127, as per the MIDI standard

vid_path    = "clips/Untitled1.mp4"
low_key     = "A0"
total_keys  = 88
whtOffset   = 100
leftOffset  = 1
widthIncrease = 0

import cv2
from analyzer import getKeyPositions, getProperty, vid2dict

vCap = cv2.VideoCapture(vid_path)
keys = getKeyPositions(
    low_key, total_keys, 
    int(vCap.get(cv2.CAP_PROP_FRAME_WIDTH)) + widthIncrease,
    int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)/5), 
    whtOffset, leftOffset
)
vid_data = vid2dict(vid_path, keys, closeness_tolerance=50)
fps = getProperty(vid_path, "fps")