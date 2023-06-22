import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

buzzer = 37
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, False)

def on():
    GPIO.output(buzzer, True)

def off():
    GPIO.output(buzzer, False)