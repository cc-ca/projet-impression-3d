import RPi.GPIO as GPIO
import os, sys
import time
from tensorflow.keras.models import load_model
import tools
from enum import Enum
from collections import deque
import threading

class Color(Enum):
    OFF = 0
    IDLE = 1
    ERROR = 2
    CORRECT = 3

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
is_running = False
current_color = Color.IDLE

def change_color(color):
    global current_color
    current_color = color
    GPIO.output(pin_red, GPIO.LOW)
    GPIO.output(pin_green, GPIO.LOW)
    GPIO.output(pin_blue, GPIO.LOW)

    if color == Color.ERROR:
        GPIO.output(pin_red, GPIO.HIGH)
    elif color == Color.CORRECT:
        GPIO.output(pin_green, GPIO.HIGH)
    elif color == Color.IDLE:
        GPIO.output(pin_blue, GPIO.HIGH)

def evaluate_model():
    global history
    result = tools.capture(MODEL)
    print(result)
    history.append(result)

    if result == "0":
        return Color.CORRECT
    else:
        return Color.ERROR

def run():
    global is_running
    global history
    global current_color
    try:
        while True:
            while is_running:
                color = evaluate_model()
                change_color(Color.OFF)
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
            if not is_running and current_color != Color.IDLE:
                change_color(Color.IDLE)
                
    finally:
        change_color(Color.IDLE)

def stop():
    change_color(Color.ERROR)
    time.sleep(SLEEP_INTERVAL)
    GPIO.output(pin_relais, GPIO.LOW)
    time.sleep(5)
    restart()
    
def restart():
    print("Restarting script...")
    change_color(Color.OFF)
    time.sleep(1)
    # Cleanup GPIO
    GPIO.cleanup()
    # Restart the script
    python = sys.executable
    os.execl(python, python, *sys.argv)

def button_listener():
    global is_running
    model_thread = None
    button_press_start_time = None
    while True:
        if GPIO.input(pin_button) == GPIO.HIGH:
            if button_press_start_time is None:
                button_press_start_time = time.time()
            else:
                if time.time() - button_press_start_time >= 3:
                    restart()
            time.sleep(0.1)  # Debounce delay
            if not is_running:
                if model_thread is not None and model_thread.is_alive():
                    print("Pausing model thread...")
                    is_running = False
                else:
                    print("Starting model thread...")
                    is_running = True
                    model_thread = threading.Thread(target=run)
                    model_thread.start()
            else:
                print("Pausing model thread...")
                is_running = False
            time.sleep(0.5)  # Delay to handle multiple button presses
        else:
            button_press_start_time = None


if __name__ == "__main__":
    try:
        print("Program running")
        change_color(Color.IDLE)
        # Start button listener in a separate thread
        threading.Thread(target=button_listener).start()
        while True:
            time.sleep(1)  # Keep the main thread running
    except KeyboardInterrupt:
        change_color(Color.OFF)
        GPIO.cleanup()
        print("Program ended")
