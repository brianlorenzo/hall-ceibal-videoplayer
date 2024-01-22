# Ref:   https://github.com/iadjedj/lgp_rpi_video
#       Tutorial: https://www.youtube.com/watch?v=Y3SJ8qLqQA8
#
# Hay que ejecutar con SUDO PYTHON PLAYVIDEOVLC.PY

import vlc
import keyboard
import time

def play_video(player, media):
    player.set_media(media)
    player.play()

instance = vlc.Instance()
player = instance.media_player_new()

videos = [
    vlc.Media('../enlace360(360p).mp4'),
    vlc.Media('../olimpiada(360p).mp4')
]

current_video_index = 0

play_video(player, videos[current_video_index])

# Espera a que el usuario cierre la ventana de VLC
while True:
    # Si se apreta 's' de switch
    if keyboard.is_pressed('s'):
        time.sleep(1)
        print("Se presionó la tecla S")

        # Cambiar al siguiente video en la lista
        current_video_index = (current_video_index + 1) % len(videos)
        play_video(player, videos[current_video_index])
        time.sleep(1)

    # Si se apreta 'q' de quit
    if keyboard.is_pressed('q'):
        player.stop()
        break

    # Deja todo en loop
    if player.get_state() == vlc.State.Ended:
        # Cambiar al siguiente video en la lista cuando se completa la reproducción
        current_video_index = (current_video_index + 1) % len(videos)
        play_video(player, videos[current_video_index])


"""
import vlc
import keyboard
import time

def play_video(player, media):
    # You need to call "set_media()" to (re)load a video before playing it

    player.set_media(media)
    player.play()

instance = vlc.Instance()
player = instance.media_player_new()

#Poner en pantalla completa
#player.toggle_fullscreen()

# Create libVLC objects representing the video
video1 = vlc.Media('../enlace360(360p).mp4')
video2 = vlc.Media('../olimpiada(360p).mp4')

# setting media to the media player
player.set_media(video1)
 
# Velocidad de reproduccion
#player.set_rate(10)


current_video = video1

play_video(player, current_video)

# Espera a que el usuario cierre la ventana de VLC
while True:
    # Si se apreta 's' de switch
    if keyboard.is_pressed('s'):
        time.sleep(1)
        print("Se presionó la tecla  S")
        
        if current_video == video1:
            current_video = video2

        if current_video == video2:
            current_video = video1 
        
        play_video(player, current_video)
        time.sleep(1)

    # Si se apreta 'q' de quit
    if keyboard.is_pressed('q'):
        player.stop()
        break

    # Deja todo en loop
    if player.get_state() == vlc.State.Ended:
            play_video(player, current_video)
"""