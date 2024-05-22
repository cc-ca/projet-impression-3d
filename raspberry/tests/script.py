import time
from tensorflow.keras.models import load_model
import tools
from enum import Enum
from collections import deque
import threading
from flask import Flask, jsonify
import keyboard

class State(Enum):
    OFF = 0
    IDLE = 1
    ERROR = 2
    CORRECT = 3
    STOP = 4 
    ISSUE = 5
    WARMUP = 6

class API(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.app = Flask(__name__)

        @self.app.route('/status', methods=['GET'])
        def get_status():
            global capture_is_running, current_state, error_rate
            state_dict = {state.name: (current_state == state) for state in State}
            status = {
                'is_running': capture_is_running,
                'states': state_dict,
                'error_rate': error_rate
            }
            return jsonify(status)
        
        @self.app.route('/stop', methods=['POST'])
        def stop_printer():
            stop()
            return jsonify({'message': 'Printer stopped'}), 200

    def run(self):
        self.app.run(host='0.0.0.0')

# Constants
RUN_DURATION = 60
PRINT_WARM_UP = 300
SLEEP_INTERVAL = 5
SLEEP_LED = 0.1
CONFIDENCE_THRESHOLD = 0.9
RESTART_INTERVAL = 3
MODEL = load_model('model.h5')

# Global variables
history = deque(maxlen=(RUN_DURATION // SLEEP_INTERVAL))
current_state = State.IDLE
capture_is_running = False
error_rate = 0.0
model_thread = None
model_thread_running = True

def change_color(state):
    global current_state
    if current_state != State.STOP and current_state != State.ISSUE:
        current_state = state

    if state == State.ERROR:
        print("Color : RED")
    elif state == State.CORRECT or state == State.WARMUP:
        print("Color : GREEN")
    elif state == State.IDLE:
        print("Color : BLUE")
    elif state == State.ISSUE:
        print("Color : YELLOW")

def evaluate_model():
    global history, model_thread_running
    try:
        result = tools.capture(MODEL)
        print(result)
        history.append(result)
        if result == "0":
            return State.CORRECT
        else:
            return State.ERROR
    except Exception:
        while model_thread_running:
            change_color(State.OFF)
            time.sleep(0.5)
            change_color(State.ISSUE)
            time.sleep(1)

def run():
    global history, current_state, error_rate, model_thread_running, capture_is_running
    try:
        change_color(State.WARMUP)
        while model_thread_running:
            if capture_is_running:
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
            if not capture_is_running and current_state != State.IDLE:
                change_color(State.IDLE)
    finally:
        change_color(State.IDLE)

def stop():
    global current_state, model_thread_running, capture_is_running
    current_state = State.STOP
    model_thread_running = False
    capture_is_running = False
    change_color(State.ERROR)
    time.sleep(SLEEP_INTERVAL)
    #GPIO.output(pin_relais, GPIO.LOW)
    while model_thread_running:
        change_color(State.OFF)
        time.sleep(0.5)
        change_color(State.ERROR)
        time.sleep(1)
    
def restart():
    global model_thread, capture_is_running, model_thread, model_thread_running, current_state
    print("Restarting script...")
    change_color(State.OFF)
    capture_is_running = False
    # Stop the model thread
    if model_thread and model_thread.is_alive():
        model_thread_running = False
        model_thread.join()
    model_thread = None
    current_state = State.IDLE

def button_listener():
    global capture_is_running, current_state, model_thread, model_thread_running
    button_press_start_time = None
    while True:
        if keyboard.is_pressed('space'):
            if button_press_start_time is None:
                button_press_start_time = time.time()
            else:
                if time.time() - button_press_start_time >= RESTART_INTERVAL:
                    restart()
                    continue
            time.sleep(0.1)  # Debounce delay
            if not capture_is_running and model_thread is None and current_state != State.STOP and current_state != State.ISSUE: 
                print("Starting model thread...")
                capture_is_running = True
                model_thread_running = True
                model_thread = threading.Thread(target=run)
                model_thread.start()
            elif not capture_is_running and model_thread is not None and current_state != State.STOP and current_state != State.ISSUE:
                print("Unpausing model thread...")
                capture_is_running = True
            elif capture_is_running and model_thread is not None and current_state != State.STOP and current_state != State.ISSUE:
                print("Pausing model thread...")
                capture_is_running = False
            elif current_state == State.STOP or current_state == State.ISSUE:
                restart()
            time.sleep(0.5)
        else:
            button_press_start_time = None


if __name__ == "__main__":
    try:
        print("Program running")
        change_color(State.IDLE)
        # Start button listener in a separate thread
        threading.Thread(target=button_listener).start()
        api = API()
        api.start()
        while True:
            time.sleep(1)  # Keep the main thread running
    except KeyboardInterrupt:
        change_color(State.OFF)
        print("Program ended")
        exit(0)
