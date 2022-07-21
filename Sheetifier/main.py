import cv2
import json
from analyzer import *

piano_size = 65
starting_key = "F"
vCap = cv2.VideoCapture("./clips/low.mp4")

# Color values
white = (239, 252, 254)
black = (20, 20, 20)

if __name__ == "__main__":
    keys = getKeyPositions(
        starting_key, piano_size, 
        int(vCap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
        int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)/5), 
        50
    )

    count = 0
    data = {}
    for key in keys:
        data[key[0]] = []

    # FIND KEY COLOURS

    detected_colors = {}

    for frame in range(int(vCap.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = vCap.read()

        for key in keys:
            color_value = tuple(frame[
                key[1][1], key[1][0]
            ])
            data[key[0]].append(color_value)

            if str(color_value) not in detected_colors.keys():
                detected_colors[str(color_value)] = 1
            else:
                detected_colors[str(color_value)] += 1

    rankedPixelOccurancy = sorted(detected_colors, key=lambda k: detected_colors[k], reverse=True)
    white_unpressed = rankedPixelOccurancy[0]

    for color in rankedPixelOccurancy:
        if not areColorsClose(white_unpressed, color, 50):
            black_unpressed = color
            break
    print(white_unpressed, black_unpressed)