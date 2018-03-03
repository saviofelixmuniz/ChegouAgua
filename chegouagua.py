# Libraries
import RPi.GPIO as GPIO
import time
import requests

TOTAL_HEIGHT = 32.8
MAX_WATER_HEIGHT = 28.8




# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


def postMeasurement(volumePercentage):
    payload = {'measurement': volumePercentage}
    requests.post('http://localhost:3000/api/measurement', data=payload)


if __name__ == '__main__':
    try:
        while True:
            dist = distance()

            currentHeight = TOTAL_HEIGHT - dist
            volumePercentage = currentHeight / MAX_WATER_HEIGHT

            print("Measured Percentage = %.1f cm" % volumePercentage)
            postMeasurement(volumePercentage)
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()