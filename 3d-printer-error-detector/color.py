import RPi.GPIO as GPIO
from settings import State, PIN_RED, PIN_GREEN, PIN_BLUE
import settings
import time

def change_color(state):
    if settings.current_state not in {State.STOP, State.ISSUE, State.OFF}:
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

def pulsing_light(color):
    while settings.current_state in {State.STOP, State.ISSUE}:
        change_color(color)
        time.sleep(settings.SLEEP_LED)
        change_color(State.OFF)
        time.sleep(settings.SLEEP_LED)