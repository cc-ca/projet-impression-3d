import RPi.GPIO as GPIO
import time

pin_test = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_test, GPIO.OUT)

while True:
        GPIO.output(pin_test, GPIO.HIGH)
        print("HIGH = circuit fermé")

        time.sleep(5)

        GPIO.output(pin_test, GPIO.LOW)
        print("LOW = circuit ouvert ")

        time.sleep(5)