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

player.toggle_fullscreen()

# Create libVLC objects representing the video
video1 = vlc.Media('../enlace360_360p.mp4')

# setting media to the media player
player.set_media(video1)
 
# setting play rate
# doubles the speed of the video
player.set_rate(5)


current_video = video1

play_video(player, video1)

# Espera a que el usuario cierre la ventana de VLC
while True:
    # Detecta si se presiona la tecla "q" para cerrar el video
    if player.get_state() == vlc.State.Ended:
            play_video(player, current_video)

    if keyboard.is_pressed('q'):
        player.stop()
        break