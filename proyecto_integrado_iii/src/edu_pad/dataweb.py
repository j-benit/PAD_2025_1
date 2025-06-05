import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class DataWeb:
    def __init__(self):
        self.base_url = "https://listado.mercadolibre.com.co/"
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def obtener_datos(self, producto="laptop"):
        """
        Obtiene una lista de productos de Mercado Libre Colombia para el término dado

        Parámetros:
        producto (str): Nombre del producto a buscar (ej. "laptop", "celular")

        Retorna:
        pd.DataFrame: DataFrame con columnas: titulo, precio, url, fecha_scraping
        """
        url = f"{self.base_url}{producto.replace(' ', '-')}"
        try:
            respuesta = requests.get(url, headers=self.headers)
            if respuesta.status_code != 200:
                print(f"Error al acceder a la URL: {url}")
                return pd.DataFrame()

            soup = BeautifulSoup(respuesta.text, 'html.parser')
            items = soup.select("li.ui-search-layout__item")

            productos = []
            for item in items:
                titulo = item.select_one("h2.ui-search-item__title")
                precio = item.select_one("span.price-tag-fraction")
                enlace = item.select_one("a.ui-search-link")

                if titulo and precio and enlace:
                    productos.append({
                        "titulo": titulo.text.strip(),
                        "precio": self._limpiar_precio(precio.text),
                        "url": enlace.get("href"),
                        "fecha_scraping": datetime.today().strftime("%Y-%m-%d"),
                        "producto_consultado": producto
                    })

            df = pd.DataFrame(productos)
            print(f"{len(df)} productos obtenidos para '{producto}'.")
            return df

        except Exception as e:
            print(f"Error al obtener datos del producto '{producto}': {e}")
            return pd.DataFrame()

    def _limpiar_precio(self, texto_precio):
        """
        Limpia el texto del precio, eliminando puntos y convirtiéndolo a float
        """
        try:
            texto_limpio = texto_precio.replace(".", "").replace(",", ".")
            return float(texto_limpio)
        except:
            return None

    def obtener_multiples_productos(self, productos=["laptop", "celular"]):
        """
        Procesa varios productos y concatena sus DataFrames

        Retorna:
        pd.DataFrame: DataFrame combinado con resultados de todos los productos
        """
        df_total = pd.DataFrame()
        for prod in productos:
            df = self.obtener_datos(prod)
            if not df.empty:
                df_total = pd.concat([df_total, df], ignore_index=True)
        return df_total


# # Ejemplo de uso
# if __name__ == "__main__":
#     dw = DataWeb()
#     df_laptops = dw.obtener_datos("laptop")
#     print(df_laptops.head())
#     df_varios = dw.obtener_multiples_productos(["laptop", "monitor"])
#     print(df_varios.head())
