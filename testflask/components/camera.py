import cv2
from objectDetection import od

camera = cv2.VideoCapture(0)


def change_brightness(img, value=50):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def gen_frames():
    while True:
        success, frame = camera.read()
        count = 0
        if not success:
            break
        else:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            frame = change_brightness(frame, value=30)
            if count % 60 == 0:
                frame = od.detect(img=frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            if count == 60:
                conut = 0
            else:
                count = count+1
            # concat frame one by one and show result
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
