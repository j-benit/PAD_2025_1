import pandas as pd
import os


from edu_pad.dataweb import scrape_mercadolibre
import re
from tabulate import tabulate  # <-- Importar aquí

# Funciones para limpiar el DataFrame
def limpiar_cuotas(texto_cuotas):
    if not isinstance(texto_cuotas, str) or texto_cuotas.strip() == '':
        return None
    num_cuotas = re.search(r'(\d+)\s*cuotas', texto_cuotas)
    valor_cuota = re.search(r'\$\s*([\d\.]+)', texto_cuotas)
    cuotas = int(num_cuotas.group(1)) if num_cuotas else None
    valor = valor_cuota.group(1).replace('.', '') if valor_cuota else None
    valor = float(valor) if valor else None
    if cuotas and valor:
        return f"{cuotas} cuotas de ${valor:,.0f}".replace(',', '.')
    return None

def limpiar_precios(precio):
    if isinstance(precio, str):
        precio = precio.replace('.', '').replace(',', '.').strip()
        try:
            return float(precio)
        except:
            return None
    return precio

def limpiar_dataframe(df):
    df['Precio Anterior'] = df['Precio Anterior'].apply(limpiar_precios)
    df['Precio Actual'] = df['Precio Actual'].apply(limpiar_precios)
    df['Cuotas'] = df['Cuotas'].apply(limpiar_cuotas)
    df['Calificación'] = pd.to_numeric(df['Calificación'], errors='coerce')
    df['Reseñas'] = pd.to_numeric(df['Reseñas'], errors='coerce')
    return df

if __name__ == "__main__":
    url = "https://listado.mercadolibre.com.co/portatiles"
    print(f"--- Iniciando scraping: {url} ---")

    # Scrapeamos los datos
    productos = scrape_mercadolibre(url)

    # Convertimos a DataFrame
    df = pd.DataFrame(productos)

    print(f"Productos encontrados: {len(df)}")

    # Limpiamos el DataFrame
    df_limpio = limpiar_dataframe(df)

    # Mostrar tabla legible en consola
    print("\n--- Datos limpios en tabla ---")
    print(tabulate(df_limpio, headers='keys', tablefmt='psql', showindex=False))

    # Definir ruta donde guardar CSV (cambia según tu proyecto)
    ruta_guardado = "/workspaces/PAD_2025_1/proyecto_integrado_iii/src/edu_pad/static/csv"

    # Crear directorio padre si no existe
    os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

    # Guardamos CSV limpio
    df_limpio.to_csv(ruta_guardado, index=False, encoding='utf-8')

    print(f"\n✅ CSV limpio guardado en '{ruta_guardado}'.")
