import RPi.GPIO as GPIO
from settings import State, PIN_RED, PIN_GREEN, PIN_BLUE, PIN_BUTTON, PIN_RELAIS
import settings



def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_RED, GPIO.OUT)
    GPIO.setup(PIN_GREEN, GPIO.OUT)
    GPIO.setup(PIN_BLUE, GPIO.OUT)
    GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_RELAIS, GPIO.OUT)
    GPIO.output(PIN_RELAIS, GPIO.HIGH)

def change_color(state):
    if settings.current_state not in {State.STOP, State.ISSUE}:
        settings.current_state = state
    GPIO.output(PIN_RED, GPIO.LOW)
    GPIO.output(PIN_GREEN, GPIO.LOW)
    GPIO.output(PIN_BLUE, GPIO.LOW)
    if state == State.ERROR:
        GPIO.output(PIN_RED, GPIO.HIGH)
    elif state in {State.CORRECT, State.WARMUP}:
        GPIO.output(PIN_GREEN, GPIO.HIGH)
    elif state == State.IDLE:
        GPIO.output(PIN_BLUE, GPIO.HIGH)
    elif state == State.ISSUE:
        GPIO.output(PIN_RED, GPIO.HIGH)
        GPIO.output(PIN_GREEN, GPIO.HIGH)
