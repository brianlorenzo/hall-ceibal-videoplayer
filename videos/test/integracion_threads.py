import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import vlc
import keyboard
import logging
import threading

exit_flag = False  # Bandera para indicar si se presionó la tecla 'q'

def setup_logger():
    # Inciializar un logger para revisar en caso de error y debug
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cargar_videos_de_archivo(file_path):
    # Carga información de videos desde un archivo de texto proporcionado en 'file_path'
    # y la devuelve como una lista de diccionarios (videos[])
    videos = []
    try:
        # Abre el archivo en modo de lectura ('r' de read)
        with open(file_path, 'r') as file:
            # Itera sobre cada línea del archivo
            for line in file:
                # Elimina espacios en blanco alrededor de la línea y divide los elementos por coma
                video_info = line.strip().split(',')
                # Verifica si la línea contiene exactamente dos elementos
                if len(video_info) == 2:
                    # Agrega un nuevo diccionario a la lista de videos con el ID y la ruta del video
                    videos.append({'id': video_info[0], 'path': video_info[1]})
    except Exception as e:
        # Si se produce un error durante la lectura del archivo, imprime un mensaje de error
        print(f"Error leyendo videos de archivo: {e}")
    return videos

def inicializar_player():
    # Inicializa una instancia de VLC con un nuevo reproductor para los videos del programa.
    # Devuelve el objeto 'vlc player' instanciado. 

    instance = vlc.Instance()
    player = instance.media_player_new()
    #player.toggle_fullscreen()
    return player

def play_video(player, media):
    # Reproduce un video en un objeto 'player' dado con el contenido en 'media'

    player.set_media(media)
    player.play()

"""
def switch_video(current_video_index, videos, player):
    # Pasa al siguiente video de la lista y devuelve el index del mismo

    # Calcula el índice del siguiente video utilizando aritmética modular
    current_video_index = (current_video_index + 1) % len(videos)

    # Reproduce el siguiente video utilizando el reproductor multimedia VLC
    play_video(player, vlc.Media(videos[current_video_index]['path']))

    return current_video_index
"""

def handle_keyboard(player):
    # Handler del teclado

    # Hace polling sobre el teclado y si la tecla 'q' está apretada 
    # cierra las ventanas y recursos de VLC. Como se usa en threads
    # agrega un 'time.sleep' para ceder el procesador
    
    global exit_flag
    while True:
        if keyboard.is_pressed('q'):
            player.stop()
            player.set_fullscreen(False)    # Desactiva el modo de pantalla completa
            player.release()                # Libera los recursos del reproductor VLC
            exit_flag = True                # Establece la bandera de salida en True
            break
        
        # Para ceder procesador
        time.sleep(0.1)

def handle_tag_reading(videos, player):
    # Handler de la lectura RFID
    
    # Crea una instancia de lectura simple
    reader = SimpleMFRC522()

    # Inicializa el index de video actual en 0 y los datos en None
    current_video_index = 0
    current_data = None
    
    # ------------- Lugar para inicializar con video de standby ----------- #
 
    # Si no se indica salir, espera a la lectura de un nuevo tag
    while not exit_flag:
        print("Esperando a leer tag...")
        id, data = reader.read()
        # Convertir los datos a cadena y limpiar espacios en blanco
        data_str = str(data).strip()
        print(f"Nuevo Tag detectado: {data_str}")
        
        # Si es un nuevo tag o el primer tag leído
        if data_str != current_data or current_data is None:
            current_data = data_str

            # Asocia el tag al video correspondiente
            for video in videos:
                if video['id'].strip() == current_data:
                    # Cuando el video asociado, lo reproduce
                    play_video(player, vlc.Media(video['path']))
                    break

        # Para ceder procesador
        time.sleep(0.1)

def main():
    # Programa principal: inicializa todo y crea un hilo para el teclado y otro para la lectura de tags
    
    setup_logger()
    logger = logging.getLogger(__name__)

    # Carga los videos según los paths relativos configurados en 'videos.txt'
    videos_file_path = 'videos.txt'

    videos = cargar_videos_de_archivo(videos_file_path)
    player = inicializar_player()

    try:
        # Crear e iniciar el hilo de manejo del teclado (para debug)
        keyboard_thread_instance = threading.Thread(target=handle_keyboard, args=(player,))
        keyboard_thread_instance.start()

        # Crear e iniciar el hilo de lectura de tags y reproductor de videos
        tag_reading_thread_instance = threading.Thread(target=handle_tag_reading, args=(videos, player))
        tag_reading_thread_instance.start()

        # Esperar a que el usuario cierre la ventana de VLC o presione 'q'
        while not exit_flag:
            time.sleep(0.1)

    except Exception as e:
        logger.error(f"Error: {e}")
    
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
