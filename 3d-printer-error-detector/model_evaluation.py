import time
import RPi.GPIO as GPIO
import tools
from settings import State, RUN_DURATION, SLEEP_INTERVAL, SLEEP_LED, MODEL, PIN_RELAIS
import settings
import color

def evaluate_model():
    if settings.current_state != State.ISSUE:
        result = tools.predict_defect(MODEL, settings.image_path)
        print(result)
        settings.history.append(result)
        return State.CORRECT if result == "0" else State.ERROR

def run():
    color.change_color(State.WARMUP)
    while settings.model_thread_running:
        if settings.capture_is_running:
            light = evaluate_model()
            color.change_color(State.OFF)
            time.sleep(SLEEP_LED)
            color.change_color(light)
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
            color.change_color(State.IDLE)

def stop():
    settings.current_state, settings.model_thread_running, settings.capture_is_running = State.STOP, False, False
    color.change_color(State.ERROR)
    time.sleep(SLEEP_LED)
    GPIO.output(PIN_RELAIS, GPIO.LOW)
    color.pulsing_light(State.ERROR)

def restart():
    print("Restarting script...")
    color.change_color(State.OFF)
    settings.capture_is_running = False
    settings.current_state = State.IDLE
    if settings.model_thread and settings.model_thread.is_alive():
        settings.model_thread_running = False
        settings.model_thread.join()
    settings.model_thread = None
    settings.history.clear()
    settings.error_rate = None
    color.change_color(State.IDLE)
