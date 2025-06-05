from src.edu_pad.dataweb import DataWeb
import pandas as pd
import os


def main():
    dataweb = DataWeb()
    
    # Lista de productos a consultar en Mercado Libre
    lista_productos = ["laptop", "celular", "monitor"]
    
    # Ruta de salida para guardar los datos extraídos
    ruta_salida = "src/edu_pad/static/csv/data_productos.csv"

    # Si el archivo ya existe, lo eliminamos para evitar duplicados (opcional)
    if os.path.exists(ruta_salida):
        os.remove(ruta_salida)

    # Iteramos sobre cada producto y guardamos los resultados
    for producto in lista_productos:
        df = dataweb.obtener_datos(producto)
        if not df.empty:
            df.to_csv(ruta_salida, index=False, mode="a", header=not os.path.exists(ruta_salida))


if __name__ == "__main__":
    main()
