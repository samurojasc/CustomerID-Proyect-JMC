# Clasificación de IDs Válidos para el proyecto de CustomerID en JMC

Este proyecto tiene como objetivo clasificar IDs en válidos 
o no válidos utilizando un modelo de Random Forest. 
Los datos se extraen de las bases de datos de Teradata y 
se procesan en lotes debido al gran tamaño del conjunto de datos.

## Estructura del Proyecto

```plaintext
project-root/
│
├── notebooks/
│   └── random_forest_id_classification.ipynb
│
├── src/
│   ├── check_ids.py
│   ├── get_connection.py
│   ├── close_connection.py
│   ├── insert_query.py
│   └── teradata_query_batches.py
│
├── models/
│   ├── preprocessor.pkl
│   └── random_forest_model.pkl
│
├── sql/
│   └── queries/
│       └── customerid_query.sql
│
├── data/
│   └── outputs/
│
├── requirements.txt
└── README.md
```


## Descripción del Flujo de Trabajo

1. **Conexión a la base de datos**: Se establece una conexión a Teradata utilizando funciones definidas en `src/get_connection.py`.

2. **Carga del modelo y preprocesador**: El preprocesador y el modelo de Random Forest preentrenado se cargan desde archivos `.pkl` almacenados en la carpeta `models`.

3. **Extracción de datos en lotes**:
   - Se cuenta el total de registros en la tabla `COL_MKT.INFO_PER_CUSTOMER`.
   - Los datos se extraen en lotes de tamaño definido (`batch_size`) utilizando una consulta SQL almacenada en `sql/queries/customerid_query.sql`.

4. **Preprocesamiento y predicción**:
   - Los datos extraídos se preprocesan para convertirlos al formato esperado por el modelo.
   - El modelo predice si cada ID es válido o no.

5. **Almacenamiento de resultados**:
   - Los resultados se cargan en una tabla auxiliar en Teradata usando `fastload`.
   - Luego, los resultados se insertan en la tabla final `COL_MKT.CUSTOMER_PREDICTIONS`.

6. **Gestión de errores**: El script incluye manejo de errores para garantizar que, en caso de fallos durante la ejecución de la consulta, el proceso continúe con el siguiente lote.

## Requisitos

- Python 3.8 o superior.
- Librerías necesarias (especificadas en `requirements.txt`):
  - pandas
  - teradataml
  - joblib
  - scikit-learn

## Instrucciones de Ejecución

1. Clona el repositorio en tu entorno local.
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
    ```
3. Instala las dependencias:
   ```bash
    pip install -r requirements.txt
    ```
4. Inicia Jupyter Notebook:
   ```bash
    jupyter notebook
    ```
5. Abre y ejecuta el notebook `random_forest_id_classification.ipynb` ubicado en la carpeta notebooks

## Notas

- Asegúrate de tener acceso a la base de datos en Teradata y de que las credenciales necesarias estén configuradas en el archivo `config.json` en la carpeta config.
- La carpeta `data/outputs/` se utiliza para almacenar los resultados locales si es necesario.

