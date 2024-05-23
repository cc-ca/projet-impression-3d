import time
import threading
import RPi.GPIO as GPIO
from gpio_setup import change_color, setup_gpio
from api import API
from button_listener import button_listener
from tools import capture_image
import settings

if __name__ == "__main__":
    try:
        print("Program running")
        settings.init()
        setup_gpio()
        change_color(settings.State.IDLE)
        threading.Thread(target=button_listener).start()
        threading.Thread(target=capture_image).start()
        api = API()
        api.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        change_color(settings.State.OFF)
        GPIO.cleanup()
        print("Program ended")
