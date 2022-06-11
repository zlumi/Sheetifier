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