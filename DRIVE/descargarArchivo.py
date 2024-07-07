import io
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']

def obtener_credenciales(credentials_file='credentials.json', token_file='token.json'):
    """Obtiene las credenciales del usuario para acceder a la API de Google Drive.
    Si no existen o no son válidas, inicia el flujo de autenticación.

    Args:
        credentials_file (str): Nombre del archivo de credenciales JSON.
        token_file (str): Nombre del archivo token JSON.

    Returns:
        Credentials: Objeto de credenciales de Google Drive.
    """
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return creds

def listar_archivos_en_carpeta(service, id_carpeta):
    """Lista todos los archivos en una carpeta específica de Google Drive.

    Args:
        service: El servicio de la API de Drive.
        id_carpeta: El ID de la carpeta en Google Drive.

    Returns:
        list: Una lista de diccionarios con los archivos encontrados, cada uno con su id y nombre.
    """
    results = service.files().list(
        q=f"'{id_carpeta}' in parents",
        fields='nextPageToken, files(id, name)'
    ).execute()
    return results.get('files', [])

def descargar_archivo(service, file_id, filename):
    """Descarga un archivo de Google Drive.

    Args:
        service: El servicio de la API de Drive.
        file_id: El ID del archivo que se va a descargar.
        filename: El nombre del archivo para guardar.
    """
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f'Descarga {int(status.progress() * 100)}% completada.')

    with open(filename, 'wb') as f:
        f.write(fh.getvalue())

def actualizar_archivos(credentials_file, token_file, id_carpeta):
    """Actualiza todos los archivos de una carpeta específica de Google Drive.

    Args:
        credentials_file (str): Nombre del archivo de credenciales JSON.
        token_file (str): Nombre del archivo token JSON.
        id_carpeta (str): El ID de la carpeta en Google Drive.
    """
    # Definir el path de descarga
    download_path = '../videos/'
    
    # Verifica si la carpeta de destino existe, si no, la crea
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Obtener las credenciales
    creds = obtener_credenciales(credentials_file, token_file)
    # Construir el servicio de la API de Drive
    service = build('drive', 'v3', credentials=creds)

    # Listar los archivos en la carpeta
    items = listar_archivos_en_carpeta(service, id_carpeta)

    if not items:
        print('No se encontraron archivos en la carpeta.')
    else:
        print('Archivos:')
        for item in items:
            file_path = os.path.join(download_path, item['name'])
            print(f'Descargando {item["name"]} ({item["id"]}) a {file_path}')
            try:
                descargar_archivo(service, item['id'], file_path)
            except Exception as e:
                print(f'Error descargando {item["name"]}: {e}')


def construir_servicio_drive():
    """Construye el servicio de la API de Google Drive.

    Returns:
        Resource: Objeto del servicio de la API de Google Drive.
    """
    creds = obtener_credenciales()
    service = build('drive', 'v3', credentials=creds)
    return service


def subir_archivo(service, file_path, id_carpeta):
    """Sube un archivo a Google Drive en una carpeta específica.

    Args:
        service: Servicio de la API de Google Drive.
        file_path (str): Ruta del archivo que se va a subir.
        id_carpeta (str): ID de la carpeta de destino en Google Drive.

    Returns:
        dict: Metadata del archivo subido.
    """
    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [id_carpeta]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print(f'Archivo "{file_name}" subido correctamente con ID: {file.get("id")}')

    return file

# Llamar a la función actualizar_archivos al final del script
if __name__ == "__main__":
    credentials_file = 'credentials.json'
    token_file = 'token.json'
    id_carpeta = "17hpy0N-HCGaTHFvdjn5dcKNqSb1MRxIF"
    
    # Construir el servicio de Google Drive
    service = construir_servicio_drive()
    
   #actualizar_archivos(credentials_file, token_file, id_carpeta)

    # Ruta del archivo que deseas subir
    archivo_a_subir = 'hola.txt'

    # Subir el archivo a Google Drive
    subir_archivo(service, archivo_a_subir, id_carpeta)
