from flask import Flask, render_template, request, Response
from components import camera, buzzer, camHandler, wheels

app = Flask(__name__)

@app.route('/move', methods=["POST"])
def move_car():
    x = request.form.get('x')
    y = request.form.get('y')
    print('move--main',x,y)
    wheels.move_car(x=int(x), y=int(y))
    return ''

@app.route('/left')
def move_left():
    print('left--main')
    wheels.move_left()
    return ''

@app.route('/right')
def move_right():
    print('right--main')
    wheels.move_right()
    return ''

@app.route('/moveStop')
def move_stop():
    print('moveStop--main')
    wheels.move_stop()
    return ''

@app.route('/buzzerOn')
def buzzer_on():
    buzzer.on()
    return ''

@app.route('/buzzerOff')
def buzzer_off():
    buzzer.off()
    return ''

@app.route('/camHorizontalMove', methods=['POST'])
def camHorizontalMove():
    angle = request.form.get('angle')
    print('camHorizontalMove',angle)
    camHandler.setHorizontal(angle=int(angle))
    return ''

@app.route('/camVerticalMove', methods=['POST'])
def camVerticalMove():
    direction = request.form.get('direction')
    print('verticalMove',direction)
    camHandler.setVertical(direction)
    return ''

@app.route('/video_feed')
def video_feed():
    return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='192.168.1.100',port=4000)