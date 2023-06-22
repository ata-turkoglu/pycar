import socketio
import RPi.GPIO as GPIO
import time
from threading import Thread, Event, Timer
import camHandler
import os

GPIO.setmode(GPIO.BOARD)

ena = 22
in2 = 11
in1 = 13
in4 = 15
in3 = 16
enb = 18

buzzer = 37
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, False)

back_sensor_trigger = 3
back_sensor_echo = 5

GPIO.setup(back_sensor_trigger, GPIO.OUT)
GPIO.setup(back_sensor_echo, GPIO.IN)


# right
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
# left
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)

rightMotors = GPIO.PWM(22, 100)
rightMotors.start(50)

leftMotors = GPIO.PWM(18, 100)
leftMotors.start(50)

moveStart = 40
moveDenominator = 100 - moveStart
camState = False

sio = socketio.Client()
sio.connect('http://192.168.1.18:3000')
print('sid', sio.sid)


@sio.on('move')
def move_car(payload):

    x = payload['x']
    y = payload['y']

    if y > 0:
        level = int((y * (moveStart/moveDenominator)) + moveStart)
        # print(level,y,moveStart,moveDenominator)

        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)

        if x > 0:
            rightMotors.ChangeDutyCycle(int((100-x)/100*level))
            leftMotors.ChangeDutyCycle(level)
        elif x < 0:
            rightMotors.ChangeDutyCycle(level)
            leftMotors.ChangeDutyCycle(int((100-abs(x))/100*level))
        else:
            rightMotors.ChangeDutyCycle(level)
            leftMotors.ChangeDutyCycle(level)

    elif y < 0:
        if distance() > 10:
            level = int((abs(y) * (moveStart/moveDenominator)) + moveStart)

            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)

            # right
            if x > 0:
                rightMotors.ChangeDutyCycle(int((100-x)/100*level))
                leftMotors.ChangeDutyCycle(level)
            # left
            elif x < 0:
                rightMotors.ChangeDutyCycle(level)
                leftMotors.ChangeDutyCycle(int((100-abs(x))/100*level))
            else:
                rightMotors.ChangeDutyCycle(level)
                leftMotors.ChangeDutyCycle(level)

    print("move", payload)


@sio.on('left')
def move_left():
    print("left")
    rightMotors.ChangeDutyCycle(95)
    leftMotors.ChangeDutyCycle(95)

    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)


@sio.on('right')
def move_right():
    print("right")
    rightMotors.ChangeDutyCycle(95)
    leftMotors.ChangeDutyCycle(95)

    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)


@sio.on('moveStop')
def move_stop():
    global checkBack
    checkBack = False
    print("move stop")
    rightMotors.ChangeDutyCycle(moveStart)
    leftMotors.ChangeDutyCycle(moveStart)

    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

@sio.on('buzzerOn')
def buzzer_on():
    GPIO.output(buzzer, True)

@sio.on('buzzerOff')
def buzzer_off():
    GPIO.output(buzzer, False)

@sio.on('camOpen')
def camOpen():
    global camState
    print('openCam')
    if camState==False:
        os.system('python flaskapp/main.py')
        camState=True

@sio.on('camHorizontalMove')
def camHorizontalMove(payload):
    print(payload)
    camHandler.setHorizontal(angle=payload['angle'])

@sio.on('camVerticalMove')
def camVerticalMove(direction):
    print('verticalMove')
    camHandler.setVertical(direction)

@sio.on('camVerticalMoveStop')
def camVerticalMoveStop():
    pass


def distance():
    # set Trigger to HIGH
    GPIO.output(back_sensor_trigger, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(back_sensor_trigger, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(back_sensor_echo) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(back_sensor_echo) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


def checkDistance():
    print('checkDistance')
    while True:
        dis = distance()
        print('distance', dis)
        if dis < 25:
            move_stop()
        time.sleep(0.5)


if __name__ == '__main__':
   """  checkBackDistance = Thread(
        target=checkDistance, name='us_sensor', args=())
    checkBackDistance.deamon = True
    checkBackDistance.start() """
