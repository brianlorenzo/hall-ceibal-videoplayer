# Bibliotecas
# SISTEMA

import sys
import os.path
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# GOOGLE DRIVE
sys.path.append(os.path.join(directorio_actual, "DRIVE"))

from google_drive_api import *

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

# RFID
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
#from rfid_utils import *

# VIDEO PLAYER
import vlc
#from videoplayer import *

import time #Se queda aca

import keyboard #Se queda aca
import logging #Se queda aca
import threading #Se queda aca
import io



# Bandera global para indicar si se presionó la tecla 'q' para cerrar aplicación
cerrar_aplicacion = False  

# Configuracion de Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
id_carpeta = "17hpy0N-HCGaTHFvdjn5dcKNqSb1MRxIF"
download_path = '../videos/'
# GUARDAR EL ARCHIVO 'credentials.json' EN ESTA CARPETA


def obtener_credenciales():
    """Obtiene las credenciales del usuario para acceder a la API de Google Drive.
    Si no existen o no son válidas, inicia el flujo de autenticación.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def listar_archivos_en_carpeta(service, id_carpeta):
    """Lista todos los archivos en una carpeta específica de Google Drive.

    Args:
        service: El servicio de la API de Drive.
        id_carpeta: El ID de la carpeta en Google Drive.

    Returns:
        Una lista de diccionarios con los archivos encontrados, cada uno con su id y nombre.
    """
    results = service.files().list(
        q=f"'{id_carpeta}' in parents",
        fields='nextPageToken, files(id, name)'
    ).execute()
    return results.get('files', [])


def descargar_archivo(service, file_id, filename):
    """Descarga un archivo de Google Drive.

    Args:
        service: El servicio de la API de Drive.
        file_id: El ID del archivo que se va a descargar.
        filename: El nombre del archivo para guardar.
    """
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f'Descarga {int(status.progress() * 100)}% completada.')

    with open(filename, 'wb') as f:
        f.write(fh.getvalue())


def actualizar_archivos(id_carpeta):
    """Actualiza todos los archivos de una carpeta específica de Google Drive."""
    # Definir el path de descarga
    global download_path
    
    # Verifica si la carpeta de destino existe, si no, la crea
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Obtener las credenciales
    creds = obtener_credenciales()
    # Construir el servicio de la API de Drive
    service = build('drive', 'v3', credentials=creds)

    # Listar los archivos en la carpeta
    items = listar_archivos_en_carpeta(service, id_carpeta)

    if not items:
        print('No se encontraron archivos en la carpeta.')
    else:
        print('Archivos:')
        for item in items:
            file_path = os.path.join(download_path, item['name'])
            print(f'Descargando {item["name"]} ({item["id"]}) a {file_path}')
            try:
                descargar_archivo(service, item['id'], file_path)
            except Exception as e:
                print(f'Error descargando {item["name"]}: {e}')


def cargar_videos_de_archivo(file_path):
    """
    Carga información de videos (nombres, path, tag asociado) desde un archivo de texto y devuelve una lista de diccionarios.

    Args:
        file_path (str): Ruta del archivo de texto que contiene la información de los videos.

    Returns:
        list: Lista de diccionarios con la información (nombres, path, tag asociado) de los videos.
    """
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


def inicializar_player(velocidad=1):
    """
    Inicializa una instancia de VLC con un nuevo reproductor para los videos del programa.

    Args:
        velocidad (int, optional): Velocidad de reproducción del video. Por defecto es 1.

    Returns:
        vlc.MediaPlayer: Instancia del reproductor VLC.
    """

    # Se crea una instancia VLC y un mediaplayer para reproducir videos
    instance = vlc.Instance()
    player = instance.media_player_new()
    
    # Se configuran las características del reproductor
    player.toggle_fullscreen()  # -Pantalla completa
    player.set_rate(velocidad)  # -Velocidad de reproducción

    return player


def play_video(player, media):
    """
    Reproduce un video en un objeto 'player' dado con el contenido en 'media'.

    Args:
        player (vlc.MediaPlayer): Instancia del reproductor VLC.
        media (vlc.Media): Objeto de media a reproducir.
    """

    player.set_media(media)
    player.play()


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
    videos_file_path = './videos/videos.txt'
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
