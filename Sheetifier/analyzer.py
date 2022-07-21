import cv2

def getKeyPositions(strtKey:str, nKeys:int, totalWidth:int, barYPos:int, blkwhtOffset:int) -> list:
    keys = []
    
    for i in range(7):
        intChar = ord(strtKey)+i
        if intChar <= 71:
            keys.append(chr(intChar))
        else:
            keys.append(chr(intChar-7))

    for key in keys:
        if  key in ["C", "D", "F", "G", "A"]:
            keys.insert(keys.index(key)+1, key+"#")
        keys[keys.index(key)] = key+"0"

    while True:
        for key in keys:
            if len(keys) < nKeys:
                keys.append(key[:-1]+str(int(key[-1])+1))
            else:
                break
        break

    whites = 0
    wCount = 0
    for key in keys:
        if not "#" in key:
            whites += 1
    for key in keys:
        if not "#" in key:
            keys[keys.index(key)] = (key, (
                int(totalWidth/whites*wCount) + int(totalWidth/whites/2),
                barYPos + blkwhtOffset
            ))
            wCount += 1
        else:
            keys[keys.index(key)] = (key, (int(totalWidth/whites*wCount), barYPos))
    
    return keys

def areColorsClose(value1, value2, tolerance:int):
    if type(value1) == str:
        value1 = tuple(map(int, value1[1:-1].split(",")))
    if type(value2) == str:
        value2 = tuple(map(int, value2[1:-1].split(",")))

    if abs(value1[0] - value2[0]) <= tolerance and abs(value1[1] - value2[1]) <= tolerance and abs(value1[2] - value2[2]) <= tolerance:
        return True
    return False

def find_white_and_black_key_colors(vidPath, starting_key:str="F", total_keys:int=65):
    vCap = cv2.VideoCapture(vidPath)
    keys = getKeyPositions(
        starting_key, total_keys, 
        int(vCap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
        int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)/5), 
        50
    )

    detected_colors = {}

    for frame in range(int(vCap.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = vCap.read()

        for key in keys:
            color_value = tuple(frame[
                key[1][1], key[1][0]
            ])

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

    return(white_unpressed, black_unpressed)

def vid2dict(vidPath:str, starting_key:str="F", total_keys:int=65, white_unpressed:tuple=(239, 252, 254), black_unpressed:tuple=(20, 20, 20), closeness_tolerance:int=50) -> dict:
    vCap = cv2.VideoCapture(vidPath)
    keys = getKeyPositions(
        starting_key, total_keys, 
        int(vCap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
        int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)/5), 
        50
    )

    data = {}
    for key in keys:
        data[key[0]] = []
    frame_number = 0

    for frame in range(int(vCap.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = vCap.read()
        frame_number += 1

        for key in keys:
            color_value = tuple(frame[
                key[1][1], key[1][0]
            ])

            if "#" in key[0]:
                if areColorsClose(color_value, black_unpressed, closeness_tolerance):
                    data[key[0]].append("0")
                else:
                    data[key[0]].append("1")
            else:
                if areColorsClose(color_value, white_unpressed, closeness_tolerance):
                    data[key[0]].append("0")
                else:
                    data[key[0]].append("1")

    out = {}
    for keyName in data.keys():
        if "1" in data[keyName]:
            out[keyName] = "".join(data[keyName])
    
    return out