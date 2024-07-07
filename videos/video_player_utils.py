import vlc

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
