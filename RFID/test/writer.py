#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        text = input('Nuevos datos')
        print("Coloca el tag para escribir")
        reader.write(text)
        print("Escrito exitosamente.")
finally:
        GPIO.cleanup()