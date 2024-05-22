import time
import threading
import RPi.GPIO as GPIO
from model_evaluation import run, restart
from settings import State, PIN_BUTTON, RESTART_INTERVAL
import settings

def button_listener():
    button_press_start_time = None
    while True:
        if GPIO.input(PIN_BUTTON) == GPIO.HIGH:
            if button_press_start_time is None:
                button_press_start_time = time.time()
            elif time.time() - button_press_start_time >= RESTART_INTERVAL:
                restart()
                continue
            time.sleep(0.1)
            if not settings.capture_is_running and settings.model_thread is None and settings.current_state not in {State.STOP, State.ISSUE}: 
                print("Starting model thread...")
                settings.capture_is_running, settings.model_thread_running = True, True
                settings.model_thread = threading.Thread(target=run)
                settings.model_thread.start()
            elif not settings.capture_is_running and settings.model_thread is not None and settings.current_state not in {State.STOP, State.ISSUE}:
                print("Unpausing model thread...")
                settings.capture_is_running = True
            elif settings.capture_is_running and settings.model_thread is not None and settings.current_state not in {State.STOP, State.ISSUE}:
                print("Pausing model thread...")
                settings.capture_is_running = False
            elif settings.current_state in {State.STOP, State.ISSUE}:
                restart()
            time.sleep(0.5)
        else:
            button_press_start_time = None
