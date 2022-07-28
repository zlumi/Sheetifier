import cv2
from analyzer import areColorsClose
from config import *

def vidEval(fps=25):
    vCap = cv2.VideoCapture(vid_path)
    while vCap.isOpened():
        ret, frame = vCap.read()
        if not ret:
            break

        for key in keys:
            color_value = tuple(frame[key[1][1], key[1][0]])

            if "#" in key[0]:
                if not areColorsClose(color_value, (20, 20, 20), 50):
                    cv2.circle(frame, key[1], 3, (0, 0, 255), 2)
            elif not areColorsClose(color_value, (239, 252, 254), 50):
                cv2.circle(frame, key[1], 3, (0, 0, 255), 2)

        cv2.imshow("frame", frame)

        if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
            break

def singleFrameEval(frame_n:int = 24*5):
    cap = cv2.VideoCapture(vid_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_n)
    ret, frame = cap.read()

    for key in keys:
        cv2.circle(frame, key[1], 3, (0, 0, 255), 2)

    cv2.imshow("frame", frame)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    singleFrameEval()