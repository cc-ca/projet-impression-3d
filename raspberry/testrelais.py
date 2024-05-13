import RPi.GPIO as GPIO
import time

pin_test = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_test, GPIO.OUT)

GPIO.output(pin_test, GPIO.HIGH)
time.sleep(5)
GPIO.output(pin_test, GPIO.LOW)