import RPi.GPIO as GPIO
import time
import cv2
from tensorflow.keras.models import load_model
import tools

# Définir les broches GPIO pour chaque couleur de la LED et le bouton
pin_red = 19
pin_green = 13
pin_blue = 26
pin_button = 6
model = load_model('model.h5')

# Initialiser la bibliothèque GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_red, GPIO.OUT)
GPIO.setup(pin_green, GPIO.OUT)
GPIO.setup(pin_blue, GPIO.OUT)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def change_color(color):
    GPIO.output(pin_red, GPIO.LOW)
    GPIO.output(pin_green, GPIO.LOW)
    GPIO.output(pin_blue, GPIO.LOW)

    if color == "red":
        GPIO.output(pin_red, GPIO.HIGH)
    elif color == "green":
        GPIO.output(pin_green, GPIO.HIGH)
    elif color == "blue":
        GPIO.output(pin_blue, GPIO.HIGH)

try:
    print("Programme en cours")
    # Ouvrir la webcam (la webcam par défaut a l'ID 0)
    cap = cv2.VideoCapture(0)
    change_color("blue")
    time.sleep(2)
    consecutive_failures = 0
    
    while True:
        result = tools.capture(model, cap)  # Appel du modele d'IA
        print(result)
        if(result == "OK"):
            change_color("green")
        else :
            change_color("red")
        time.sleep(5)

except KeyboardInterrupt:
    pass
finally:
    print("Fin programme")
    cap.release()
    change_color("off")
    GPIO.cleanup()
