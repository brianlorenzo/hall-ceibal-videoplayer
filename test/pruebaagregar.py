import sys
import os.path
directorio_actual = os.path.dirname(os.path.abspath(__file__))
import time 

# GOOGLE DRIVE
sys.path.append(os.path.join(directorio_actual, "../DRIVE"))

from google_drive_api import *

actualizar_archivos(credentials_file, token_file, id_carpeta)