import time
import threading
import RPi.GPIO as GPIO
from gpio_setup import setup_gpio
from api import API
from button_listener import button_listener
from tools import capture_image
import settings
import color

if __name__ == "__main__":
    try:
        print("Program running")
        settings.init()
        setup_gpio()
        color.change_color(settings.State.IDLE)
        threading.Thread(target=button_listener).start()
        threading.Thread(target=capture_image).start()
        api = API()
        api.start()
        while True:
            # Keep the main thread alive to keep the other threads running
            time.sleep(1)
    except KeyboardInterrupt:
        color.change_color(settings.State.OFF)
        GPIO.cleanup()
        print("Program ended")
