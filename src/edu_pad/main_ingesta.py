from database import DataBase
import pandas as pd

def main():
    ruta_csv = "/workspaces/PAD_2025_1/proyecto_integrado_iii/src/edu_pad/static/csv/productos_mercadolibre_limpio.csv"
    columnas_esperadas = ["Marca", "Título", "Precio Anterior", "Precio Actual", "Descuento", "Cuotas", "Calificación", "Reseñas", "URL", "Promocionado"]

    database = DataBase(ruta_csv, columnas_esperadas)
    df = database.cargar_df()
    # Aquí puedes procesar df si quieres
    database.guardar_df(df)
if __name__ == "__main__":
    main()
