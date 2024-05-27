import RPi.GPIO as GPIO
from settings import PIN_RED, PIN_GREEN, PIN_BLUE, PIN_BUTTON, PIN_RELAIS

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_RED, GPIO.OUT)
    GPIO.setup(PIN_GREEN, GPIO.OUT)
    GPIO.setup(PIN_BLUE, GPIO.OUT)
    GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_RELAIS, GPIO.OUT)
    GPIO.output(PIN_RELAIS, GPIO.HIGH)
