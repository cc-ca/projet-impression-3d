import RPi.GPIO as GPIO
import os, sys
import time
from tensorflow.keras.models import load_model
import tools
from enum import Enum
from collections import deque
import threading

class State(Enum):
    OFF = 0
    IDLE = 1
    ERROR = 2
    CORRECT = 3
    STOP = 4 

# GPIO pin numbers
pin_red = 19
pin_green = 13
pin_blue = 26
pin_button = 6
pin_relais = 5

# Initialize GPIO library
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_red, GPIO.OUT)
GPIO.setup(pin_green, GPIO.OUT)
GPIO.setup(pin_blue, GPIO.OUT)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_relais, GPIO.OUT)
GPIO.output(pin_relais, GPIO.HIGH)

# Constants
RUN_DURATION = 60
SLEEP_INTERVAL = 5
SLEEP_LED = 0.1
CONFIDENCE_THRESHOLD = 0.9
MODEL = load_model('model.h5')

# Global variables
history = deque(maxlen=(RUN_DURATION // SLEEP_INTERVAL))
current_state = State.IDLE
is_running = False

def change_color(state):
    global current_state
    if state != State.STOP:
        current_state = state
    GPIO.output(pin_red, GPIO.LOW)
    GPIO.output(pin_green, GPIO.LOW)
    GPIO.output(pin_blue, GPIO.LOW)

    if state == State.ERROR:
        GPIO.output(pin_red, GPIO.HIGH)
    elif state == State.CORRECT:
        GPIO.output(pin_green, GPIO.HIGH)
    elif state == State.IDLE:
        GPIO.output(pin_blue, GPIO.HIGH)

def evaluate_model():
    global history
    result = tools.capture(MODEL)
    print(result)
    history.append(result)

    if result == "0":
        return State.CORRECT
    else:
        return State.ERROR

def run():
    global history
    global current_state
    try:
        while True:
            while is_running:
                color = evaluate_model()
                change_color(State.OFF)
                time.sleep(SLEEP_LED)
                change_color(color)

                # Check if there are enough elements in history for calculation
                if len(history) >= (RUN_DURATION // SLEEP_INTERVAL - 1):
                    success_count = history.count("0")
                    failure_count = history.count("1")
                    error_rate = failure_count / (success_count + failure_count)
                    if error_rate >= CONFIDENCE_THRESHOLD:
                        print("Threshold exceeded - Error rate: {:.2%}".format(error_rate))
                        stop()
                    print("No threshold exceeded - Error rate: {:.2%}".format(error_rate))
                else:
                    print("Not enough elements in history for calculation.")
                time.sleep(SLEEP_INTERVAL)
            if not is_running and current_state != State.IDLE:
                change_color(State.IDLE)
                
    finally:
        change_color(State.IDLE)

def stop():
    global current_state
    current_state = State.STOP
    change_color(State.ERROR)
    time.sleep(SLEEP_INTERVAL)
    GPIO.output(pin_relais, GPIO.LOW)
    while True:
        change_color(State.OFF)
        time.sleep(0.5)
        change_color(State.ERROR)
        time.sleep(1)
        if GPIO.input(pin_button) == GPIO.HIGH:
            restart()
    
def restart():
    print("Restarting script...")
    change_color(State.OFF)
    time.sleep(1)
    # Cleanup GPIO
    GPIO.cleanup()
    # Restart the script
    python = sys.executable
    os.execl(python, python, *sys.argv)

def button_listener():
    global is_running
    global current_state
    model_thread = None
    while True:
        if GPIO.input(pin_button) == GPIO.HIGH:
            time.sleep(0.1)  # Debounce delay
            if not is_running and model_thread is None and current_state != State.STOP:
                print("Starting model thread...")
                is_running = True
                model_thread = threading.Thread(target=run)
                model_thread.start()
            elif not is_running and model_thread is not None and current_state != State.STOP:
                print("Restarting model thread...")
                is_running = True
            elif is_running and model_thread is not None and current_state != State.STOP:
                print("Pausing model thread...")
                is_running = False


if __name__ == "__main__":
    try:
        print("Program running")
        change_color(State.IDLE)
        # Start button listener in a separate thread
        threading.Thread(target=button_listener).start()
        while True:
            time.sleep(1)  # Keep the main thread running
    except KeyboardInterrupt:
        change_color(State.OFF)
        GPIO.cleanup()
        print("Program ended")
