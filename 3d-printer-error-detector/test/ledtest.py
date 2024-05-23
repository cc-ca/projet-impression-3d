import RPi.GPIO as GPIO
import time

# Définir les broches GPIO pour chaque couleur de la LED
pin_red = 13
pin_green = 19
pin_blue = 26

# Initialiser la bibliothèque GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_red, GPIO.OUT)
GPIO.setup(pin_green, GPIO.OUT)
GPIO.setup(pin_blue, GPIO.OUT)

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

try:
    while True:
        change_color("blue")
        time.sleep(2)
        change_color("green")
        time.sleep(2)
        change_color("red")
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
