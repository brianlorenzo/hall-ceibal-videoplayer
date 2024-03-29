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

    # Cambiar la ruta del archivo según sea necesario
    videos_file_path = 'videos.txt'

    videos = load_videos_from_file(videos_file_path)

    current_video_index = 0
    current_id = videos[current_video_index]['id']
    videos[current_video_index]['media'] = vlc.Media(videos[current_video_index]['path'])
    play_video(player, videos[current_video_index]['media'])

    # Espera a que el usuario cierre la ventana de VLC
    while True:
        try:
            if keyboard.is_pressed('s'):
                logger.info("Se presionó la tecla S")
                current_video_index = switch_video(current_video_index, videos, player)
                current_id = videos[current_video_index]['id']

            # Verificar si 'current_id' es igual a la 'id' de algún video
            if any(video['id'] == current_id for video in videos):
                index = next(i for i, video in enumerate(videos) if video['id'] == current_id)
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
                current_id = videos[current_video_index]['id']

            # Actualizar la variable con la última ID
            print(f"Última ID actualizada: {current_id}")

        except Exception as e:
            logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
