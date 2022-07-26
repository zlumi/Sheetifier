import cv2

def getProperty(vidPath:str, property:str):
    vCap = cv2.VideoCapture(vidPath)
    property = property.upper().lower()

    if property == "fps":
        return vCap.get(cv2.CAP_PROP_FPS)
    elif property == ("framecount" or "frame_count"):
        return vCap.get(cv2.CAP_PROP_FRAME_COUNT)
    elif property == "duration":
        return getProperty(vidPath, "framecount")/getProperty(vidPath, "fps")
    else:
        raise Exception("Invalid property argument passed to getProperty()")

def getKeyPositions(start_key:str, total_key_amount:int, total_width:int, barY:int, whiteOffsetFromBlack:int = 48) -> list:
    keys = []
    template = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    for firstOctaveKey in template[template.index(start_key[:-1]):]:
        keys.append(firstOctaveKey + start_key[-1])

    firstOctaveLength = len(keys)

    for i in range(total_key_amount-firstOctaveLength):
        keyName = template[i%12]
        specified_keyName = keyName + str(int(start_key[-1])+int((i+firstOctaveLength)/12)+1)

        keys.append(specified_keyName)

    while True:
        for key in keys:
            if len(keys) < total_key_amount:
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
                int(total_width/whites*wCount) + int(total_width/whites/2),
                barY + whiteOffsetFromBlack
            ))
            wCount += 1
        else:
            keys[keys.index(key)] = (key, (int(total_width/whites*wCount), barY))
    
    return keys

def areColorsClose(value1, value2, tolerance:int):
    if type(value1) == str:
        value1 = tuple(map(int, value1[1:-1].split(",")))
    if type(value2) == str:
        value2 = tuple(map(int, value2[1:-1].split(",")))

    if abs(value1[0] - value2[0]) <= tolerance and abs(value1[1] - value2[1]) <= tolerance and abs(value1[2] - value2[2]) <= tolerance:
        return True
    return False

def find_white_and_black_key_colors(vidPath, starting_key:str, total_keys:int, whiteOffsetFromBlack:int):
    vCap = cv2.VideoCapture(vidPath)
    keys = getKeyPositions(
        starting_key, total_keys, 
        int(vCap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
        int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)/5), 
        whiteOffsetFromBlack
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

def vid2dict(vidPath:str, starting_key:str, total_keys:int, whiteOffsetFromBlack: int, white_unpressed:tuple=(239, 252, 254), black_unpressed:tuple=(20, 20, 20), closeness_tolerance:int=50) -> dict:
    vCap = cv2.VideoCapture(vidPath)
    keys = getKeyPositions(
        starting_key, total_keys, 
        int(vCap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
        int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)/5), 
        whiteOffsetFromBlack
    )

    data = {}
    for key in keys:
        data[key[0]] = []

    for frame in range(int(vCap.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = vCap.read()

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

def compress_binary_string(binary_string:str) -> list:
    compressed = []

    for i in range(len(binary_string)):
        if binary_string[i] == "1":
            if i > 0:
                if binary_string[i-1] == "0":
                    compressed.append([i])
            else:
                compressed.append([i])

            try:
                if binary_string[i+1] == "0":
                    compressed[-1].append(i)
            except IndexError:
                compressed[-1].append(i)

            pass

        else:
            pass

    return compressed

def key2midi(keyName:str):
    if not "#" in keyName:
        if keyName[0] == "C":
            return int(keyName[1])*12 + 12
        elif keyName[0] == "D":
            return int(keyName[1])*12 + 14
        elif keyName[0] == "E":
            return int(keyName[1])*12 + 16
        elif keyName[0] == "F":
            return int(keyName[1])*12 + 17
        elif keyName[0] == "G":
            return int(keyName[1])*12 + 19
        elif keyName[0] == "A":
            return int(keyName[1])*12 + 21
        elif keyName[0] == "B":
            return int(keyName[1])*12 + 23
        else:
            raise Exception("Invalid key name")

    else:
        if keyName[0] == "C":
            return int(keyName[2])*12 + 13
        elif keyName[0] == "D":
            return int(keyName[2])*12 + 15
        elif keyName[0] == "F":
            return int(keyName[2])*12 + 18
        elif keyName[0] == "G":
            return int(keyName[2])*12 + 20
        elif keyName[0] == "A":
            return int(keyName[2])*12 + 22
        else:
            raise Exception("Invalid key name")