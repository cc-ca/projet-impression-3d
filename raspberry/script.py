import RPi.GPIO as GPIO
import time
import tools

from PIL import Image 
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import load_model

import numpy as np
import matplotlib.pyplot as plt

import os
import cv2
import random
import time
import datetime

# Définir les broches GPIO pour chaque couleur de la LED et le bouton
pin_red = 13
pin_green = 19
pin_blue = 26
pin_button = 6
color_sequence = ["green", "red", "blue", "off"]
model = load_model('model.h5')


# Initialiser la bibliothèque GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_red, GPIO.OUT)
GPIO.setup(pin_green, GPIO.OUT)
GPIO.setup(pin_blue, GPIO.OUT)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def change_color(color):
    if color == "red":
        GPIO.output(pin_red, GPIO.HIGH)
        GPIO.output(pin_green, GPIO.LOW)
        GPIO.output(pin_blue, GPIO.LOW)
    elif color == "green":
        GPIO.output(pin_red, GPIO.LOW)
        GPIO.output(pin_green, GPIO.HIGH)
        GPIO.output(pin_blue, GPIO.LOW)
    elif color == "blue":
        GPIO.output(pin_red, GPIO.LOW)
        GPIO.output(pin_green, GPIO.LOW)
        GPIO.output(pin_blue, GPIO.HIGH)
    elif color == "off":
        GPIO.output(pin_red, GPIO.LOW)
        GPIO.output(pin_green, GPIO.LOW)
        GPIO.output(pin_blue, GPIO.LOW)




def change_color(x):
    pass

try:
    state = "blue"
    change_color(state)
    consecutive_failures = 0
    
    while True:
        button_state = GPIO.input(pin_button)
        if button_state == GPIO.LOW:
            if state == "blue": # On passe à l'état en marche
                state = "green"
                change_color(state)
                result = tools.predict(model)  # Appel du modele d'IA
                
                while result == "ok":
                    time.sleep(5)
                    result = tools.predict(model)
                    if result in ["spaghetti", "bed not stick"]:
                        consecutive_failures += 1
                        if consecutive_failures == 10:
                            state = "red"
                            change_color(state)
                            break
                    else:
                        consecutive_failures = 0

except KeyboardInterrupt:
    pass
finally:
    change_color("off")
    GPIO.cleanup()