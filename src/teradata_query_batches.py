import pandas as pd
from teradataml import execute_sql
import math


def fetch_data_in_batches(query_file, batch_size, columns):
    """
    Ejecuta la consulta SQL en lotes y devuelve un DataFrame concatenado.

    Args:
    query_file (str): Ruta al archivo SQL.
    Batch_size (int): Número de registros por lote.
    Connection: Objeto de conexión a la base de datos.

    Returns:
    pd.DataFrame: DataFrame concatenado con los resultados de todas las consultas.
    """
    all_data = pd.DataFrame()

    # Leer la consulta SQL desde el archivo
    with open(query_file, 'r') as file:
        query_template = file.read()

    # Consulta preliminar para obtener el número total de registros
    count_query = """
        SELECT COUNT(*) AS total_records
        FROM COL_MKT.INFO_PER_CUSTOMER
        WHERE CUSTOMER_ID IS NOT NULL
        """

    # Ejecutar la consulta de conteo
    total_records = pd.DataFrame(execute_sql(count_query))[0][0]
    total_batches = math.ceil(total_records / batch_size)

    for batch in range(total_batches):
        start = batch * batch_size + 1
        end = start + batch_size - 1

        # Crear la consulta SQL para el lote actual
        query = query_template.format(start=start, end=end)
        # Ejecutar la consulta
        try:
            result = execute_sql(query)
            batch_df = pd.DataFrame(result, columns=columns)

            all_data = pd.concat([all_data, batch_df], ignore_index=True)
        except Exception as e:
            print(f'Error al ejecutar la consulta para el lote {batch}: {e}')

    return all_data
