import cv2
import piano

piano_size = 65
starting_key = "F"
vCap = cv2.VideoCapture("./clips/low.mp4")

if __name__ == "__main__":
    keys = piano.getKeyPositions(
        starting_key, piano_size, 
        int(vCap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
        int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - int(vCap.get(cv2.CAP_PROP_FRAME_HEIGHT)/5), 
        50
    )

    count = 0
    for frame in range(int(vCap.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = vCap.read()

        for key in keys:
            cv2.circle(frame, (key[1][0], key[1][1]), 3, (0, 0, 255), -1)

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break