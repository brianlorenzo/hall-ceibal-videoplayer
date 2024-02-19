#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import vlc
import keyboard
import logging

def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def play_video(player, media):
    player.set_media(media)
    player.play()

def switch_video(current_video_index, videos, player):
    current_video_index = (current_video_index + 1) % len(videos)
    play_video(player, videos[current_video_index]['media'])
    return current_video_index

def load_videos_from_file(file_path):
    videos = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                video_info = line.strip().split(',')
                if len(video_info) == 2:
                    videos.append({'id': video_info[0], 'path': video_info[1], 'media': None})
    except Exception as e:
        print(f"Error leyendo videos de archivo: {e}")
    return videos

def main():
    setup_logger()
    logger = logging.getLogger(__name__)

    instance = vlc.Instance()
    player = instance.media_player_new()
    #player.toggle_fullscreen()

    # Cambiar la ruta del archivo según sea necesario
    videos_file_path = 'videos.txt'

    videos = load_videos_from_file(videos_file_path)

    current_video_index = 0
    current_data = videos[current_video_index]['id']
    videos[current_video_index]['media'] = vlc.Media(videos[current_video_index]['path'])
    play_video(player, videos[current_video_index]['media'])

    reader = SimpleMFRC522()

    try:
        # Espera a que el usuario cierre la ventana de VLC
        while True:
            print("Esperando a leer tag...")

            id, data = reader.read()

            # Convertir los datos a cadena y limpiar espacios en blanco
            data_str = str(data).strip()

            # Si es un nuevo tag o el primer tag leído
            if data_str != current_data or current_data is None:
                print(f"Nuevo Tag detectado: {data_str}")
                current_data = data_str

                # Asociar el tag al video correspondiente
                if any(video['id'].strip() == current_data for video in videos):
                    index = next(i for i, video in enumerate(videos) if video['id'].strip() == current_data)
                    if current_video_index != index:
                        current_video_index = index
                        if videos[current_video_index]['media'] is None:
                            videos[current_video_index]['media'] = vlc.Media(videos[current_video_index]['path'])
                        play_video(player, videos[current_video_index]['media'])

                print("Esperando a leer tag...")

            if keyboard.is_pressed('q'):
                player.stop()
                break

            if player.get_state() == vlc.State.Ended:
                current_video_index = switch_video(current_video_index, videos, player)
                current_data = videos[current_video_index]['id']

            # Actualizar la variable con la última ID
            print(f"Última ID actualizada: {current_data}")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        GPIO.cleanup()
            
if __name__ == "__main__":
    main()
