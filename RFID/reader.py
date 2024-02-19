
#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

def read_data():
    try:
        last_id = None
        print("Esperando a leer tag...")

        while True:

            id, data = reader.read()

            # Si es un nuevo tag o el primer tag leído
            if id != last_id or last_id is None:
                #print("Tag detectado:")
                #print(f"ID: {id}")
                print(f"Data: {data}")
                print("Data es de tipo",type(data))
                last_id = id
                time.sleep(1)
                print("Esperando a leer tag...")

                # Aquí puedes realizar acciones adicionales con el ID y la data leídos
    finally:
        GPIO.cleanup()

# Llamar a la función para iniciar la lectura de tags
read_data()



"""
#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def read_data():
        try:
                id, data = reader.read()
                print(id)
                print(data)
        finally:
                GPIO.cleanup()
                return data

"""