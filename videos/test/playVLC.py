#import RPi.GPIO as GPIO
import vlc
import keyboard

def play_video(player, media):
    # You need to call "set_media()" to (re)load a video before playing it

    player.set_media(media)
    player.play()

instance = vlc.Instance()
player = instance.media_player_new()

# Create libVLC objects representing the video
video1 = vlc.Media('./drones(1080p).mp4')

play_video(player, video1)

# Espera a que el usuario cierre la ventana de VLC
while True:
    # Detecta si se presiona la tecla "q" para cerrar el video
    if keyboard.is_pressed('q'):
        player.stop()
        break