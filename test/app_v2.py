# AUXILIARES
import time 
import keyboard 
import logging 
import threading 
import io

# SISTEMA
import sys
import os.path
# Agrego al PATH el directorio del repositorio
directorio_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(directorio_actual, "../DRIVE"))
sys.path.append(os.path.join(directorio_actual, "../videos"))
sys.path.append(os.path.join(directorio_actual, "../RFID"))
sys.path.append(os.path.join(directorio_actual, "../WEB"))

# GOOGLE DRIVE
from google_drive_api import *
"""GUARDAR EL ARCHIVO 'credentials.json' EN ESTA CARPETA"""

# VIDEO PLAYER
from video_player_utils import *

# RFID
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


# Configuracion de API Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
id_carpeta = "17hpy0N-HCGaTHFvdjn5dcKNqSb1MRxIF"
download_path = '../videos/'

# Bandera global para indicar si se presionó la tecla 'q' para cerrar aplicación
cerrar_aplicacion = False  


def handle_keyboard(player):
    """
    Maneja las entradas del teclado para finalizar el programa al presionar 'q'.

    Args:
        player (vlc.MediaPlayer): Instancia del reproductor VLC.
    """

    # Hace polling sobre el teclado y si la tecla 'q' está apretada 
    # cierra las ventanas y recursos de VLC. 
    global cerrar_aplicacion
    while True:
        # Delay no bloqueante para ceder el procesador
        time.sleep(0.1)

        # Polling de la tecla 'q' en teclado
        if keyboard.is_pressed('q'):
        # Cierra el reproductor y libera los recursos de VLC
            player.stop()
            player.set_fullscreen(False)    
            player.release()                
        
        # Establece la bandera de salida en True
            cerrar_aplicacion = True        
            print(" El programa finaliza por teclado")
            break

        if keyboard.is_pressed('d'):
            actualizar_archivos(id_carpeta)


def handle_tag_reading(videos, player):
    """
    Maneja la lectura de etiquetas RFID y reproduce el video asociado.

    Args:
        videos (list): Lista de diccionarios con la información de los videos.
        player (vlc.MediaPlayer): Instancia del reproductor VLC.
    """
    
    # Crea una instancia de lectura simple
    reader = SimpleMFRC522()

    #Inicializa el indexado para tomar el último video cargado (standby) y los datos en None
    current_video_index = -1  #ToDo: que el index sea directo 'standby' y no necesariamente el último
    current_data = None

    # Reproduce el video indexado inicialmente (standby)
    standby_video = videos[current_video_index]['path']
    play_video(player, vlc.Media(standby_video))
 
    # Mientras que no se cierre la aplicación por teclado ('q')
    while not cerrar_aplicacion:
        
    # Lectura de tag
        print("Esperando a leer tag...")
        id, data = reader.read()
        
    # Convierte los datos a cadena de texto y limpia espacios en blanco
        data_str = str(data).strip()
        print(f"Nuevo Tag detectado: {data_str}")
        
    # Si es un nuevo tag (o el primero) reproduce un video nuevo asociado al tag
        if data_str != current_data or current_data is None:
            current_data = data_str

    # Busca video asociado a tag y lo reporudce
            for video in videos:
                if video['id'].strip() == current_data:
                    # Cuando el video asociado, lo reproduce
                    play_video(player, vlc.Media(video['path']))
                    break

    # Delay no bloqueante para ceder el procesador
        time.sleep(0.1)
    

def main():
    """
    Programa principal:
    - Inicializa el logger y el reproductor de video.
    - Carga los videos desde el archivo.
    - Crea hilos para manejar el teclado y la lectura de tags.
    - Hace polling de la bandera global para cerrar la aplicación.
    - Maneja errores globales y libera recursos al finalizar.
    """
    
    # Inicializa logger para el proceso princial
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Inicializa el reproductor de videos
    player = inicializar_player()

    # Carga los videos para posterior reproducción
    videos_file_path = '../videos/videos.txt'
    videos = cargar_videos_de_archivo(videos_file_path)
    standby_video = videos[-1]['path']

    try:
    # Crear e iniciar el hilo de manejo del teclado
        keyboard_thread_instance = threading.Thread(target=handle_keyboard, args=(player,))
        keyboard_thread_instance.start()

    # Crear e iniciar el hilo de lectura de tags y reproductor de videos
        tag_reading_thread_instance = threading.Thread(target=handle_tag_reading, args=(videos, player))
        tag_reading_thread_instance.start()

    # Mientras que no se cierre la aplicación por teclado ('q')
    # al terminar un video, siempre volver al video de 'standby'
        while not cerrar_aplicacion:
            if player.get_state() == vlc.State.Ended:
                play_video(player, vlc.Media(standby_video))

    # Delay no bloqueante para ceder el procesador
            time.sleep(0.1)

    except Exception as e:
        logger.error(f"Error en el transcurso del programa. ERROR: {e}") #ToDo: Mejorar el manejo de errores
    
    # Al terminar el programa
    #   -Se liberan GPIOs
    #   -Se libera la instancia VLC (ToDo: asegurar esto)
    #   -Se cierre el código
    finally:
        GPIO.cleanup()
        sys.exit()


if __name__ == "__main__":
    main()
