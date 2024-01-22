import vlc

# Ruta completa del archivo de video
ruta_video = '../olimpiada(1080).mp4'

# Crear instancia del reproductor VLC
vlc_instance = vlc.Instance()

# Crear reproductor
reproductor = vlc_instance.media_player_new()

# Cargar el archivo de video
media = vlc_instance.media_new(ruta_video)

# Establecer la media en el reproductor
reproductor.set_media(media)

# Reproducir el video
reproductor.play()

# Esperar a que la reproducción termine
while reproductor.is_playing():
    pass

# Liberar recursos
reproductor.stop()
