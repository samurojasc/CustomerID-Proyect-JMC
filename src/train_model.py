from src import get_connection, close_connection, fetch_data_from_teradata, check_ids
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
import pandas as pd
import pickle

QUERY_VALID_FILE = '../sql/queries/valid_query.sql'
QUERY_INVALID_FILE = '../sql/queries/invalid_query.sql'
COLUMNS = ['UNIDAD DE NEGOCIO', 'ZONA', 'REGION', 'CUSTOMER_ID', 'LLAVE', 'MIN FECHA', 'MAX FECHA', 'TRANSACTIONS',
           'MONEY', 'FECHAS', 'VOLUME', 'QTY']


def load_and_process_data():
    get_connection()
    try:
        df_valid = fetch_data_from_teradata(QUERY_VALID_FILE, COLUMNS)
        df_invalid = fetch_data_from_teradata(QUERY_INVALID_FILE, COLUMNS)
    finally:
        close_connection()

    df_invalid['Category'] = 0
    df_valid['Category'] = 1
    df = pd.concat([df_invalid, df_valid])

    # Aplicar funciones de procesamiento de ID
    df[['ID_LENGTH', 'ID_HAS_REPEATED_DIGITS', 'ID_IS_ASCENDING', 'ID_IS_DESCENDING', 'ID_HAS_REPETITIVE_PATTERN']] = \
        df['CUSTOMER_ID'].apply(lambda x: pd.Series(check_ids(x)))

    # Convertir tipos de datos
    df['VOLUME'] = pd.to_numeric(df['VOLUME'], errors='coerce')
    df['QTY'] = pd.to_numeric(df['QTY'], errors='coerce')
    df['MONEY'] = pd.to_numeric(df['MONEY'], errors='coerce')
    df['MIN FECHA'] = pd.to_datetime(df['MIN FECHA'], format='%Y-%m-%d')
    df['MAX FECHA'] = pd.to_datetime(df['MAX FECHA'], format='%Y-%m-%d')

    X = df.drop(columns=['CUSTOMER_ID', 'LLAVE', 'Category'])
    y = df['Category']

    return X, y


def preprocess_data(X):
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'),
             ['UNIDAD DE NEGOCIO', 'ZONA', 'REGION', 'MIN FECHA', 'MAX FECHA']),
            ('num', StandardScaler(),
             ['TRANSACTIONS', 'MONEY', 'FECHAS', 'VOLUME', 'QTY', 'ID_LENGTH', 'ID_HAS_REPEATED_DIGITS',
              'ID_IS_ASCENDING', 'ID_IS_DESCENDING', 'ID_HAS_REPETITIVE_PATTERN'])
        ],
        remainder='passthrough'
    )
    X_processed = preprocessor.fit_transform(X)
    X_processed_df = pd.DataFrame(X_processed.toarray(), columns=preprocessor.get_feature_names_out())

    return X_processed_df, preprocessor


def train_model(X_train, y_train):
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

    model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    model.fit(X_train_smote, y_train_smote)

    return model


def save_model(model, model_path):
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
    print(f'Modelo guardado en {model_path}')


def save_preprocessor(preprocessor, preprocessor_path):
    with open(preprocessor_path, 'wb') as file:
        pickle.dump(preprocessor, file)
    print(f'Preprocesador guardado en {preprocessor_path}')


def main():
    X, y = load_and_process_data()
    X_processed, preprocessor = preprocess_data(X)
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.3, random_state=42)

    model = train_model(X_train, y_train)

    # Evaluar el modelo (opcional)
    # y_pred = model.predict(X_test)
    # print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')

    save_model(model, '../models/random_forest_model.pkl')
    save_preprocessor(preprocessor, '../models/preprocessor.pkl')


if __name__ == '__main__':
    main()
