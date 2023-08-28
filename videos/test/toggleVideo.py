# Ref:   https://github.com/iadjedj/lgp_rpi_video
#       Tutorial: https://www.youtube.com/watch?v=Y3SJ8qLqQA8
#
# Hay que ejecutar con SUDO PYTHON PLAYVIDEOVLC.PY

import vlc
import keyboard

def play_video(player, media):
    # You need to call "set_media()" to (re)load a video before playing it

    player.set_media(media)
    player.play()

instance = vlc.Instance()
player = instance.media_player_new()

#Poner en pantalla completa
player.toggle_fullscreen()

# Create libVLC objects representing the video
video1 = vlc.Media('../enlace360_360p.mp4')
video2 = vlc.Media('../olimp2022_360p.mp4')

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
        if current_video == video1:
            current_video = video2

        if current_video == video2:
            current_video = video1 
        
        play_video(player, current_video)

    # Si se apreta 'q' de quit
    if keyboard.is_pressed('q'):
        player.stop()
        break

    # Detecta si se presiona la tecla "q" para cerrar el video
    if player.get_state() == vlc.State.Ended:
            play_video(player, current_video)