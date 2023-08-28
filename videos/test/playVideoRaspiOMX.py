from omxplayer.player import OMXPlayer
import time

# Ruta del archivo de video que deseas reproducir
ruta_del_video = 'ruta/al/video.mp4'

# Crea una instancia del reproductor OMXPlayer
reproductor = OMXPlayer(ruta_del_video)

# Espera un tiempo para permitir que el reproductor se inicie
time.sleep(5)

# Controla la reproducción (por ejemplo, pausa después de 10 segundos)
time.sleep(10)
reproductor.pause()

# Espera otros 5 segundos antes de detener la reproducción
time.sleep(5)

# Detén la reproducción y libera los recursos
reproductor.stop()
