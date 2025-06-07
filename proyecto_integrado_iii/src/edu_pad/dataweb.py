import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_mercadolibre(url):
    print(f"--- Iniciando scraping: {url} ---")
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    productos = soup.find_all("div", class_="poly-card__content")
    print(f"Productos encontrados: {len(productos)}")

    data = []

    for prod in productos:
        try:
            marca = prod.find("span", class_="poly-component__brand").get_text(strip=True)
        except:
            marca = None

        try:
            titulo_tag = prod.find("a", class_="poly-component__title")
            titulo = titulo_tag.get_text(strip=True) if titulo_tag else None
            link = titulo_tag["href"] if titulo_tag and "href" in titulo_tag.attrs else None
        except:
            titulo, link = None, None

        def get_text_or_none(selector):
            try:
                return selector.get_text(strip=True) if selector else None
            except:
                return None

        precio_anterior = None
        precio_anterior_tags = prod.find_all("s", class_="andes-money-amount--previous")
        if precio_anterior_tags:
            # Ejemplo de obtener texto del primer span dentro del primero tag
            span_tag = precio_anterior_tags[0].find("span", class_="andes-money-amount__fraction")
            precio_anterior = get_text_or_none(span_tag)

        precio_actual_tag = prod.find("div", class_="poly-price__current")
        precio_actual = None
        if precio_actual_tag:
            span_tag = precio_actual_tag.find("span", class_="andes-money-amount__fraction")
            precio_actual = get_text_or_none(span_tag)

        descuento = get_text_or_none(prod.find("span", class_="andes-money-amount__discount"))
        cuotas = get_text_or_none(prod.find("span", class_="poly-price__installments"))
        calificacion = get_text_or_none(prod.find("span", class_="poly-reviews__rating"))
        total_resenas = get_text_or_none(prod.find("span", class_="poly-reviews__total"))

        promocionado = "Sí" if prod.find("a", class_="poly-component__ads-promotions") else "No"

        data.append({
            "Marca": marca,
            "Título": titulo,
            "Precio Anterior": precio_anterior,
            "Precio Actual": precio_actual,
            "Descuento": descuento,
            "Cuotas": cuotas,
            "Calificación": calificacion,
            "Reseñas": total_resenas,
            "URL": link,
            "Promocionado": promocionado
        })

    return data


def clean_and_transform_dataframe(df):
    if df.empty:
        return df

    def clean_price(price_str):
        if pd.isna(price_str) or price_str is None:
            return None
        cleaned = str(price_str).replace('$', '').replace('.', '').replace(',', '').strip()
        try:
            return float(cleaned)
        except ValueError:
            return None

    def clean_discount(discount_str):
        if pd.isna(discount_str) or discount_str is None:
            return None
        cleaned = str(discount_str).replace('% OFF', '').replace('%', '').strip()
        try:
            return float(cleaned)
        except ValueError:
            return None

    def clean_numeric_field(field_str):
        if pd.isna(field_str) or field_str is None:
            return None
        cleaned = str(field_str).replace('(', '').replace(')', '').strip()
        cleaned = re.sub(r'[^\d.]', '', cleaned)

        if not cleaned:
            return None
        try:
            return float(cleaned)
        except ValueError:
            return None

    df['Precio Anterior'] = df['Precio Anterior'].apply(clean_price)
    df['Precio Actual'] = df['Precio Actual'].apply(clean_price)
    df['Descuento'] = df['Descuento'].apply(clean_discount)
    df['Calificación'] = df['Calificación'].apply(clean_numeric_field)
    df['Reseñas'] = df['Reseñas'].apply(clean_numeric_field)
    df['Reseñas'] = df['Reseñas'].astype('Int64', errors='ignore')

    df = df.replace({None: pd.NA})
    return df
