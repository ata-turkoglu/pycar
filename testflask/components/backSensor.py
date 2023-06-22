import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

back_sensor_trigger = 3
back_sensor_echo = 5

GPIO.setup(back_sensor_trigger, GPIO.OUT)
GPIO.setup(back_sensor_echo, GPIO.IN)

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

