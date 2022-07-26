import cv2
from analyzer import getKeyPositions, areColorsClose

path = "clips/trimmed.mov"
low_key = "F1"
total_keys = 65
closeness_tolerance = 30
fps = 25

vCap = cv2.VideoCapture(path)
while vCap.isOpened():
    ret, frame = vCap.read()
    if not ret:
        break

    for key in getKeyPositions(low_key, total_keys, int(vCap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)/5), 48):
        color_value = tuple(frame[key[1][1], key[1][0]])

        if "#" in key[0]:
            if not areColorsClose(color_value, (20, 20, 20), closeness_tolerance):
                cv2.circle(frame, key[1], 3, (0, 0, 255), 2)
        elif not areColorsClose(color_value, (239, 252, 254), closeness_tolerance):
            cv2.circle(frame, key[1], 3, (0, 0, 255), 2)
    
    cv2.imshow("frame", frame)

    if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
        break

# SINGLE FRAME VERIFICATION

# frame_n = 24*5

# cap = cv2.VideoCapture(path)
# cap.set(cv2.CAP_PROP_POS_FRAMES, frame_n)
# ret, frame = cap.read()

# for key in getKeyPositions(low_key, total_keys, int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/5), 50):
#     frame[key[1][1], key[1][0]] = (0, 0, 255)

# cv2.imshow("frame", frame)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cap.release()