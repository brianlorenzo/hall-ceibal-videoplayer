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
    

    # Si se apreta '1' para el video 1
    if keyboard.is_pressed('1'):
        # Verificar si ya se está reproduciendo el video 1
        if current_video_index != 0:
            current_video_index = 0
            play_video(player, videos[current_video_index])

            print("Se presionó la tecla 1")
        
        

    # Si se apreta '2' para el video 2
    if keyboard.is_pressed('2'):

        # Verificar si ya se está reproduciendo el video 2
        if current_video_index != 1:
            current_video_index = 1
            play_video(player, videos[current_video_index])
            
            print("Se presionó la tecla 2")



    # Si se apreta 'q' de quit
    if keyboard.is_pressed('q'):
        player.stop()
        break

    # Deja todo en loop
    if player.get_state() == vlc.State.Ended:
        # Cambiar al siguiente video en la lista cuando se completa la reproducción
        current_video_index = (current_video_index + 1) % len(videos)
        play_video(player, videos[current_video_index])
