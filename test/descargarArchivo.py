import os
import gdown
import warnings


# Carpeta con todos los videos: https://drive.google.com/drive/folders/17hpy0N-HCGaTHFvdjn5dcKNqSb1MRxIF?usp=sharing

def verificar_y_descargar_archivo(nombre_archivo, url_archivo, carpeta_destino="."):
    path_archivo = os.path.join(carpeta_destino, nombre_archivo)
    
    if os.path.isfile(path_archivo):
        print(f"El archivo '{nombre_archivo}' ya existe en la carpeta '{carpeta_destino}'.")
    else:
        print(
        f"""Descargando el archivo '{nombre_archivo}' 
            en la carpeta '{carpeta_destino}'..."""
        )
        
        # Desactivar temporalmente los warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            gdown.download(url_archivo, path_archivo)
        print("Descarga completada.")

# Especifica el nombre del archivo, el enlace de Google Drive y la carpeta destino
nombre_archivo = "olimpiada(360p).mp4"
enlace_google_drive = "https://drive.google.com/file/d/1jCfk64GIljHza5Ac-VQgf5rNJHSAgp0e/view?usp=drive_link"
carpeta_destino = "../videos/"

# Llama a la función para verificar y descargar el archivo en la carpeta especificada
verificar_y_descargar_archivo(nombre_archivo, enlace_google_drive, carpeta_destino)

# Descarga un segundo archivo
nombre_archivo = "enlace360(360p).mp4"
enlace_google_drive = "https://drive.google.com/file/d/13XiFJdeW3HxTRYWtxhhhdTQUw87jNKtB/view?usp=drive_link"

verificar_y_descargar_archivo(nombre_archivo, enlace_google_drive, carpeta_destino)
