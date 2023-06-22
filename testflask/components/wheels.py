import RPi.GPIO as GPIO
from components import backSensor

GPIO.setmode(GPIO.BOARD)

ena = 22
in2 = 11
in1 = 13
in4 = 15
in3 = 16
enb = 18

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

def move_car(x, y):

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
        #if backSensor.distance() > 10:
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

    print("move - wheels", x, y)

def move_stop():
    print("move stop - wheels")
    rightMotors.ChangeDutyCycle(moveStart)
    leftMotors.ChangeDutyCycle(moveStart)

    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def move_right():
    print("right - wheels")
    rightMotors.ChangeDutyCycle(95)
    leftMotors.ChangeDutyCycle(95)

    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def move_left():
    print("left - wheels")
    rightMotors.ChangeDutyCycle(95)
    leftMotors.ChangeDutyCycle(95)

    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)