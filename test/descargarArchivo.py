import os
import gdown

def check_and_download_file(file_name, file_url):
    if os.path.isfile(file_name):
        print("El archivo ya existe en la carpeta actual.")
    else:
        print("Descargando el archivo...")
        gdown.download(file_url, file_name)
        print("Descarga completada.")

# Especifica el nombre del archivo y el enlace de Google Drive
nombre_archivo = "olimpiada(1080).mp4"
enlace_google_drive = "https://drive.google.com/file/d/1K_k2YGBj2BdTZeEzOxg0tmFKhzWbS5t2/view?usp=drive_link"

# Llama a la función para verificar y descargar el archivo si es necesario
check_and_download_file(nombre_archivo, enlace_google_drive)
