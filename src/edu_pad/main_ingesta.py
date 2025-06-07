from edu_pad.database import DataBase
import pandas as pd
import os

def main():
    ruta_csv = "/app/static/csv/productos_mercadolibre_limpio.csv"
    columnas_esperadas = ["Marca", "Título", "Precio Anterior", "Precio Actual", "Descuento", "Cuotas", "Calificación", "Reseñas", "URL", "Promocionado"]

    os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)

    database = DataBase(ruta_csv, columnas_esperadas)
    df = database.cargar_df()
    database.guardar_df(df)

if __name__ == "__main__":
    main()
