import pandas as pd
from teradataml import execute_sql


def fetch_data_from_teradata(query, columns):
    """
    Ejecuta una consulta SQL en Teradata y devuelve los resultados en un DataFrame de Pandas.

    Esta función realiza las siguientes acciones:
    1. Ejecuta la consulta SQL proporcionada utilizando `execute_sql` de `teradataml`.
    2. Crea un DataFrame de Pandas con los resultados de la consulta.
    3. Asigna los nombres de las columnas al DataFrame usando la lista `columns` proporcionada.
    4. Devuelve el DataFrame con los datos recuperados de Teradata.

    Args:
        query (str): Consulta SQL que se ejecutará en la base de datos Teradata.
        columns (list): Lista de nombres de columnas para el DataFrame.

    Returns:
        pd.DataFrame: DataFrame que contiene los resultados de la consulta SQL.
    """
    # Ejecutar la consulta SQL en Teradata y recuperar los resultados.
    # La función `execute_sql` devuelve los resultados de la consulta como una lista de tuplas o una estructura similar.
    with open(query, 'r') as file:
        query_template = file.read()
    result_set = execute_sql(query_template)

    # Crear un DataFrame de Pandas a partir del resultado de la consulta.
    # `columns` se usa para nombrar las columnas del DataFrame.
    df = pd.DataFrame(result_set, columns=columns)

    # Devolver el DataFrame con los resultados.
    return df
