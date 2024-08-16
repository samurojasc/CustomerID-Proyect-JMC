from teradataml import create_context, remove_context, TeradataMlException
import os
import json


def get_connection():
    """
    Establece una conexión con Teradata Vantage utilizando la configuración almacenada en un archivo JSON.

    Esta función realiza lo siguiente:
    1. Construye la ruta al archivo de configuración `config.json` que se encuentra en la carpeta `config`
       al nivel superior de la carpeta actual.
    2. Lee el archivo de configuración y carga los datos en un diccionario de Python.
    3. Extrae los parámetros de conexión (DSN, nombre de usuario y contraseña) del diccionario.
    4. Intenta establecer una conexión con Teradata Vantage usando los parámetros extraídos.
    5. Imprime un mensaje de éxito si la conexión se establece correctamente o maneja cualquier
       excepción específica de `teradataml` si ocurre un error.
    """
    # Construir la ruta al archivo de configuración `config.json`. Utiliza `__file__` para obtener la ruta
    # del archivo actual y luego sube un nivel en el directorio para acceder a la carpeta `config`.
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

    # Abrir el archivo `config.json` en modo lectura.
    with open(config_path, 'r') as config_file:
        # Cargar el contenido del archivo JSON en un diccionario de Python.
        config = json.load(config_file)

    # Extraer los parámetros de conexión del diccionario de configuración.
    dsn = config['dsn']
    user = config['user']
    password = config['password']

    try:
        # Intentar crear un contexto de conexión a Teradata Vantage usando los parámetros extraídos.
        create_context(host=dsn, username=user, password=password)
        print('Conexión a Teradata Vantage establecida correctamente.')

    except TeradataMlException as e:
        # Manejar cualquier excepción específica de `teradataml` e imprimir un mensaje de error.
        print(f'Error en teradataml: {str(e)}')


def close_connection():
    """
    Cierra el contexto de conexión con Teradata Vantage.

    Esta función utiliza la función `remove_context` de `teradataml` para cerrar la conexión
    con Teradata Vantage cuando ya no sea necesaria.
    """
    remove_context()
