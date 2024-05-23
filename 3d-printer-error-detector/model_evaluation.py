import time
import RPi.GPIO as GPIO
from gpio_setup import change_color
import tools
from settings import State, RUN_DURATION, SLEEP_INTERVAL, SLEEP_LED, MODEL, PIN_RELAIS
import settings

def evaluate_model():
    if settings.current_state != State.ISSUE:
        result = tools.predict_defect(MODEL, settings.image_name)
        print(result)
        settings.history.append(result)
        return State.CORRECT if result == "0" else State.ERROR
    else:
        while settings.model_thread_running:
            change_color(State.OFF)
            time.sleep(settings.SLEEP_LED)
            change_color(State.ISSUE)
            time.sleep(settings.SLEEP_LED)

def run():
    change_color(State.WARMUP)
    while settings.model_thread_running:
        if settings.capture_is_running:
            color = evaluate_model()
            change_color(State.OFF)
            time.sleep(SLEEP_LED)
            change_color(color)
            if len(settings.history) >= (RUN_DURATION // SLEEP_INTERVAL - 1):
                success_count = settings.history.count("0")
                failure_count = settings.history.count("1")
                settings.error_rate = failure_count / (success_count + failure_count)
                print("error rate: ", settings.error_rate, " confidence threshold: ", settings.confidence_threshold)
                if settings.error_rate >= settings.confidence_threshold:
                    print(f"Threshold exceeded - Error rate: {settings.error_rate:.2%}")
                    stop()
                else:
                    print(f"No threshold exceeded - Error rate: {settings.error_rate:.2%}")
            else:
                print("Not enough elements in history for calculation.")
            time.sleep(SLEEP_INTERVAL)
        if not settings.capture_is_running and settings.current_state != State.IDLE:
            change_color(State.IDLE)

def stop():
    settings.current_state, settings.model_thread_running, settings.capture_is_running = State.STOP, False, False
    change_color(State.ERROR)
    time.sleep(SLEEP_LED)
    GPIO.output(PIN_RELAIS, GPIO.LOW)
    while settings.current_state == State.STOP:
        change_color(State.OFF)
        time.sleep(settings.SLEEP_LED)
        change_color(State.ERROR)
        time.sleep(settings.SLEEP_LED)
    
def restart():
    print("Restarting script...")
    change_color(State.OFF)
    settings.capture_is_running = False
    settings.current_state = State.IDLE
    if settings.model_thread and settings.model_thread.is_alive():
        settings.model_thread_running = False
        settings.model_thread.join()
    settings.model_thread = None
    settings.history.clear()
    change_color(State.IDLE)
