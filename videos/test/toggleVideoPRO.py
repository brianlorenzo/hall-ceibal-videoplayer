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

def main():
    setup_logger()
    logger = logging.getLogger(__name__)

    instance = vlc.Instance()
    player = instance.media_player_new()

    videos = [
        {'id': '1', 'path': '../enlace360(360p).mp4', 'media': None},
        {'id': '2', 'path': '../olimpiada(360p).mp4', 'media': None}
    ]

    # Asociar teclas con cada video
    video_keys = {video['id']: i for i, video in enumerate(videos)}

    current_video_index = 0
    videos[current_video_index]['media'] = vlc.Media(videos[current_video_index]['path'])
    play_video(player, videos[current_video_index]['media'])

    # Espera a que el usuario cierre la ventana de VLC
    while True:
        try:
            if keyboard.is_pressed('s'):
                logger.info("Se presionó la tecla S")
                current_video_index = switch_video(current_video_index, videos, player)

            # Verificar si la tecla presionada está asociada a un video
            for key, index in video_keys.items():
                if keyboard.is_pressed(key):
                    logger.info(f"Se presionó la tecla {key}")
                    if current_video_index != index:
                        current_video_index = index
                        if videos[current_video_index]['media'] is None:
                            videos[current_video_index]['media'] = vlc.Media(videos[current_video_index]['path'])
                        play_video(player, videos[current_video_index]['media'])

            if keyboard.is_pressed('q'):
                player.stop()
                break

            if player.get_state() == vlc.State.Ended:
                current_video_index = switch_video(current_video_index, videos, player)

        except Exception as e:
            logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
