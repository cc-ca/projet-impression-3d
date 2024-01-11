import RPi.GPIO as GPIO
import time
import cv2
from tensorflow.keras.models import load_model
import tools
from enum import Enum

# Define an enumeration class
class Color(Enum):
    OFF = 0
    IDLE = 1
    ERROR = 2
    CORRECT = 3
    
# Définir les broches GPIO pour chaque couleur de la LED et le bouton
pin_red = 19
pin_green = 13
pin_blue = 26
pin_button = 6


# Initialiser la bibliothèque GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_red, GPIO.OUT)
GPIO.setup(pin_green, GPIO.OUT)
GPIO.setup(pin_blue, GPIO.OUT)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Constants
RUN_DURATION = 60
SLEEP_INTERVAL = 5
SLEEP_LED = 0.001
CONFIDENCE_THRESHOLD = 0.9
model = load_model('model.h5')


def change_color(color):
    GPIO.output(pin_red, GPIO.LOW)
    GPIO.output(pin_green, GPIO.LOW)
    GPIO.output(pin_blue, GPIO.LOW)

    if color == Color.ERROR:
        GPIO.output(pin_red, GPIO.HIGH)
    elif color == Color.CORRECT:
        GPIO.output(pin_green, GPIO.HIGH)
    elif color == Color.IDLE:
        GPIO.output(pin_blue, GPIO.HIGH)

def evaluate_model(cap):
    result = tools.capture(model, cap)
    print(result)

    if result == "OK":
        return Color.CORRECT
    else:
        return Color.ERROR

def run():
    try:
        while True:
            end_time = time.time() + RUN_DURATION
            success_count = 0
            failure_count = 0
            
            while time.time() < end_time:
                color = evaluate_model(cap)
                change_color(Color.OFF)
                time.sleep(0.001)
                change_color(color)
    
                if color == Color.ERROR:
                    failure_count += 1
                elif color == Color.CORRECT:
                    success_count += 1
                    
                time.sleep(SLEEP_INTERVAL)
                
            if failure_count/(success_count+failure_count) >= CONFIDENCE_THRESHOLD:
                print("depassement seuil")
                break
            print("pas depassement seuil")
    finally:
        change_color(Color.IDLE)
        


if __name__ == "__main__":
    try:
        print("Programme en cours")
        change_color(Color.IDLE)
        while True:
            if(GPIO.input(pin_button) == GPIO.LOW):
                run()
    except KeyboardInterrupt:
        change_color(Color.OFF)
        GPIO.cleanup()
        print("Fin programme")
    