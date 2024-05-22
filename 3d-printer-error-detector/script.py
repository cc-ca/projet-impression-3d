import RPi.GPIO as GPIO
import time
from tensorflow.keras.models import load_model
import tools
from enum import Enum
from collections import deque
import threading
from flask import Flask, jsonify

class State(Enum):
    OFF = 0
    IDLE = 1
    ERROR = 2
    CORRECT = 3
    STOP = 4 
    ISSUE = 5
    WARMUP = 6

# Flask API class in a separate thread
class API(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.app = Flask(__name__)
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/status', methods=['GET'])
        def get_status():
            global capture_is_running, current_state, error_rate
            return jsonify({
                'is_running': capture_is_running,
                'states': {state.name: (current_state == state) for state in State},
                'error_rate': error_rate
            })

        @self.app.route('/stop', methods=['POST'])
        def stop_printer():
            global stop
            stop()
            return jsonify({'message': 'Printer stopped'}), 200

    def run(self):
        self.app.run(host='0.0.0.0')

# GPIO pin configuration
pin_red, pin_green, pin_blue = 19, 13, 26
pin_button, pin_relais = 6, 4

# Initialize GPIO
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_red, GPIO.OUT)
    GPIO.setup(pin_green, GPIO.OUT)
    GPIO.setup(pin_blue, GPIO.OUT)
    GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(pin_relais, GPIO.OUT)
    GPIO.output(pin_relais, GPIO.HIGH)

# Constants and globals
RUN_DURATION, PRINT_WARM_UP = 60, 300
SLEEP_INTERVAL, SLEEP_LED = 5, 0.1
CONFIDENCE_THRESHOLD, RESTART_INTERVAL = 0.9, 3
MODEL = load_model('model.h5')

# Global variables
history = deque(maxlen=(RUN_DURATION // SLEEP_INTERVAL))
current_state = State.IDLE
capture_is_running = False
error_rate = 0.0
model_thread = None
model_thread_running = True

# Change the LED color based on the current state
def change_color(state):
    global current_state
    if current_state not in {State.STOP, State.ISSUE}:
        current_state = state
    GPIO.output(pin_red, GPIO.LOW)
    GPIO.output(pin_green, GPIO.LOW)
    GPIO.output(pin_blue, GPIO.LOW)
    if state == State.ERROR:
        GPIO.output(pin_red, GPIO.HIGH)
    elif state in {State.CORRECT, State.WARMUP}:
        GPIO.output(pin_green, GPIO.HIGH)
    elif state == State.IDLE:
        GPIO.output(pin_blue, GPIO.HIGH)
    elif state == State.ISSUE:
        GPIO.output(pin_red, GPIO.HIGH)
        GPIO.output(pin_green, GPIO.HIGH)

# Evaluate the model and return the state
def evaluate_model():
    global history, model_thread_running
    try:
        result = tools.capture(MODEL)
        print(result)
        history.append(result)
        return State.CORRECT if result == "0" else State.ERROR
    except Exception:
        while model_thread_running:
            change_color(State.OFF)
            time.sleep(0.3)
            change_color(State.ISSUE)
            time.sleep(1)

# Run the model evaluation loop
def run():
    global history, current_state, error_rate, model_thread_running, capture_is_running
    change_color(State.WARMUP)
    try:
        while model_thread_running:
            if capture_is_running:
                color = evaluate_model()
                change_color(State.OFF)
                time.sleep(SLEEP_LED)
                change_color(color)
                if len(history) >= (RUN_DURATION // SLEEP_INTERVAL - 1):
                    success_count = history.count("0")
                    failure_count = history.count("1")
                    error_rate = failure_count / (success_count + failure_count)
                    if error_rate >= CONFIDENCE_THRESHOLD:
                        print(f"Threshold exceeded - Error rate: {error_rate:.2%}")
                        stop()
                    print(f"No threshold exceeded - Error rate: {error_rate:.2%}")
                else:
                    print("Not enough elements in history for calculation.")
                time.sleep(SLEEP_INTERVAL)
            if not capture_is_running and current_state != State.IDLE:
                change_color(State.IDLE)
    finally:
        change_color(State.IDLE)

# Stop the printer
def stop():
    global current_state, model_thread_running, capture_is_running
    current_state, model_thread_running, capture_is_running = State.STOP, False, False
    change_color(State.ERROR)
    time.sleep(SLEEP_INTERVAL)
    GPIO.output(pin_relais, GPIO.LOW)
    
# Restart the model thread
def restart():
    global history, model_thread, capture_is_running, model_thread_running, current_state
    print("Restarting script...")
    change_color(State.OFF)
    capture_is_running = False
    if model_thread and model_thread.is_alive():
        model_thread_running = False
        model_thread.join()
    model_thread = None
    history.clear()
    current_state = State.IDLE

# Button listener for starting, stopping, and restarting the model thread
def button_listener():
    global capture_is_running, current_state, model_thread, model_thread_running
    button_press_start_time = None
    while True:
        if GPIO.input(pin_button) == GPIO.HIGH:
            if button_press_start_time is None:
                button_press_start_time = time.time()
            elif time.time() - button_press_start_time >= RESTART_INTERVAL:
                restart()
                continue
            time.sleep(0.1)
            if not capture_is_running and model_thread is None and current_state not in {State.STOP, State.ISSUE}: 
                print("Starting model thread...")
                capture_is_running, model_thread_running = True, True
                model_thread = threading.Thread(target=run)
                model_thread.start()
            elif not capture_is_running and model_thread is not None and current_state not in {State.STOP, State.ISSUE}:
                print("Unpausing model thread...")
                capture_is_running = True
            elif capture_is_running and model_thread is not None and current_state not in {State.STOP, State.ISSUE}:
                print("Pausing model thread...")
                capture_is_running = False
            elif current_state in {State.STOP, State.ISSUE}:
                restart()
            time.sleep(0.5)
        else:
            button_press_start_time = None


# Main program execution
if __name__ == "__main__":
    try:
        print("Program running")
        change_color(State.IDLE)
        setup_gpio()
        threading.Thread(target=button_listener).start()
        api = API()
        api.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        change_color(State.OFF)
        GPIO.cleanup()
        print("Program ended")
