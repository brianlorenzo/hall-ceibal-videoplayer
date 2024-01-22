#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import vlc
import time

reader = SimpleMFRC522()

def read_data():
        try:
                id, data = reader.read()
                print(id)
                print(data)
        finally:
                GPIO.cleanup()
                return data



def play_video(player, media):
    player.set_media(media)
    player.play()

def load_videos_from_file(file_path):
    videos = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                video_info = line.strip().split(',')
                if len(video_info) == 2:
                    videos.append({'id': video_info[0], 'path': video_info[1], 'media': None})
    except Exception as e:
        print(f"Error loading videos from file: {e}")
    return videos

# Cambiar la ruta del archivo según sea necesario
videos_file_path = 'videos.txt'

instance = vlc.Instance()

# Crear el reproductor principal
main_player = instance.media_player_new()

# Cargar la lista de videos
videos = load_videos_from_file(videos_file_path)

ultima_lectura = None

# Cargar los medios para cada video
for video in videos:
    video['media'] = instance.media_new(video['path'])
    video['media'].get_mrl()

# Loop principal
while True:
    try:
        # Simular la lectura del sensor
        nueva_lectura = input("Ingrese un valor de ID ('q' para salir): ")

        # Salir si se ingresa 'q'
        if nueva_lectura.lower() == 'q':
            main_player.stop()
            break

        # Verificar si la última lectura ha cambiado
        if nueva_lectura != ultima_lectura:
            ultima_lectura = nueva_lectura

            # Buscar el video asociado a la nueva lectura
            video_encontrado = next((video for video in videos if video['id'] == ultima_lectura), None)

            if video_encontrado:
                print(f"Cambiando al video asociado a '{ultima_lectura}'")
                play_video(main_player, video_encontrado['media'])
            else:
                print(f"No se encontró un video asociado a '{ultima_lectura}'")

    except Exception as e:
        print(f"Error: {e}")

# Esperar a que se cierre el reproductor antes de salir
main_player.stop()
