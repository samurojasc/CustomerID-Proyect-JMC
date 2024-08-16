import pandas as pd
from teradataml import TeradataMlException
from teradataml.dataframe.copy_to import copy_to_sql


def insert_query(schema, table, primary_index, df):
    """
    Inserta datos desde un archivo Excel en una tabla de Teradata Vantage utilizando la función `copy_to_sql`.

    Esta función realiza las siguientes acciones:
    1. Lee el archivo Excel especificado en un DataFrame de Pandas.
    2. Intenta copiar el DataFrame a una tabla en Teradata Vantage.
    3. Imprime un mensaje de éxito si la inserción es correcta o maneja cualquier excepción específica
       de `teradataml` si ocurre un error.

    Args:
        schema (str): Nombre del esquema en Teradata donde se encuentra la tabla.
        table (str): Nombre de la tabla en Teradata donde se insertarán los datos.
        primary_index (str): Nombre del índice primario para la tabla en Teradata.
        df (dataframe): Dataframe para insertar
    """
    # Leer el archivo Excel especificado y cargarlo en un DataFrame de Pandas.

    try:
        # Intentar copiar el DataFrame a la tabla en Teradata Vantage usando `copy_to_sql`.
        # - `schema_name`: Nombre del esquema en Teradata.
        # - `table_name`: Nombre de la tabla en Teradata.
        # - `primary_index`: Índice primario para la tabla en Teradata.
        # - `if_exists="replace"`: Reemplaza la tabla en Teradata si ya existe.
        copy_to_sql(df=df, schema_name=schema, table_name=table, primary_index=primary_index, if_exists="replace")

        # Imprimir un mensaje de éxito si la inserción se realiza correctamente.
        print(f'Inserción hecha correctamente en {schema}.{table}.')

    except TeradataMlException as e:
        # Manejar cualquier excepción específica de `teradataml` e imprimir un mensaje de error.
        print(f'Error en teradataml: {str(e)}')



