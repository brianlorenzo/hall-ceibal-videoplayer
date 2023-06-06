import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def readTag():
    try:
            id, data = reader.read()
            print(id)
            print(data)
    finally:
            GPIO.cleanup()
            return id
    
def playVideo(id_video):
       #play video
       return 0
    
    
id_video = readTag()

