import RPi.GPIO as GPIO
import time
from tensorflow.keras.models import load_model
import tools
from enum import Enum

# le switch off est connecté à la broche 5 le circuit est femé par defaut (low) lorsque la pin est High le circuit est ouvert



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
pin_switch_off = 5


# Initialiser la bibliothèque GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_red, GPIO.OUT)
GPIO.setup(pin_green, GPIO.OUT)
GPIO.setup(pin_blue, GPIO.OUT)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_switch_off, GPIO.OUT)

# Constantes
RUN_DURATION = 60
SLEEP_INTERVAL = 5
SLEEP_LED = 0.1
CONFIDENCE_THRESHOLD = 0.9
model = load_model('model.h5')

def switch_off():
    GPIO.ouptut(pin_switch_off, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(pin_switch_off, GPIO.LOW)

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

def evaluate_model():
    result = tools.capture(model)
    print(result)

    if result == "0":
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
                color = evaluate_model()
                change_color(Color.OFF)
                time.sleep(SLEEP_LED)
                change_color(color)
    
                if color == Color.ERROR:
                    failure_count += 1
                elif color == Color.CORRECT:
                    success_count += 1
                    
                time.sleep(SLEEP_INTERVAL)
                
            if failure_count/(success_count+failure_count) >= CONFIDENCE_THRESHOLD:
                print("depassement seuil")
                switch_off()
                break
            print("pas depassement seuil")
    finally:
        change_color(Color.IDLE)
        


if __name__ == "__main__":
    try:
        print("Programme en cours")
        change_color(Color.IDLE)
        while True:
            if(GPIO.input(pin_button) == GPIO.HIGH):
                run()
            time.sleep(0.1)
    except KeyboardInterrupt:
        change_color(Color.OFF)
        GPIO.cleanup()
        print("Fin programme")
    
