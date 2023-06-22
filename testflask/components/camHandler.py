from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(31,GPIO.OUT)
GPIO.setup(29,GPIO.OUT)
serH = GPIO.PWM(31,50)
serV = GPIO.PWM(29,50)

serH.start(0)
serV.start(0)

def setHorizontal(angle):
    if angle > 45 and angle < 135:
        duty = 2+((angle+3)/18)
        serH.ChangeDutyCycle(duty)
        sleep(0.5)
        serH.ChangeDutyCycle(0)
        sleep(1)

def setVertical(direction):
    if direction =='up':
        serV.ChangeDutyCycle(6.5)
        sleep(0.05)
        serV.ChangeDutyCycle(0)
        sleep(0.4)
    elif direction == 'down':
        serV.ChangeDutyCycle(7.6)
        sleep(0.05)
        serV.ChangeDutyCycle(0)
        sleep(0.4)

