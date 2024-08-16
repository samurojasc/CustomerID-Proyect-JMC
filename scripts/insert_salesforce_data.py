from src import get_connection, insert_query, load_data
import pandas as pd

df = load_data("SF_julio.xlsx")
df = df[['CUSTOMER_ID', 'Tipo de documento']]
df = df.dropna()
df = df.replace('', 'CC')
insert_query('COL_MKT', 'SalesForce', 'Customer_ID', df)
