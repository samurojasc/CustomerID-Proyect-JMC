import os
import pandas as pd


def load_data(file_name):
    """
    Carga un archivo de datos desde la carpeta 'data/raw'.

    Args:
        file_name (str): Nombre del archivo de datos a cargar.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados.
    """
    # Construir la ruta al archivo en la carpeta 'data/raw'
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', file_name)

    # Leer el archivo usando pandas (ejemplo para archivos Excel)
    df = pd.read_excel(file_path)

    return df
