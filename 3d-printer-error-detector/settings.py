# settings.py
from collections import deque
from tensorflow.keras.models import load_model
from enum import Enum

class State(Enum):
    OFF = 0
    IDLE = 1
    ERROR = 2
    CORRECT = 3
    STOP = 4
    ISSUE = 5
    WARMUP = 6

RESTART_INTERVAL = 3
PIN_RED, PIN_GREEN, PIN_BLUE = 19, 13, 26
PIN_BUTTON, PIN_RELAIS = 6, 4
RUN_DURATION, PRINT_WARM_UP = 60, 300
SLEEP_INTERVAL, CAPTURE_INTERVAL, SLEEP_LED = 5, 3, 0.1
MODEL = load_model('model.h5')

def init():
    global history, current_state, capture_is_running, error_rate, model_thread, model_thread_running, image_path, confidence_threshold
    history = deque(maxlen=(RUN_DURATION // SLEEP_INTERVAL))
    current_state = State.IDLE
    capture_is_running = False
    error_rate = None
    model_thread = None
    model_thread_running = True
    image_path = None
    confidence_threshold = 0.8