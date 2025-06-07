import pandas as pd

class DataBase:
    def __init__(self, filename, expected_columns=None):
        self.filename = filename
        self.expected_columns = expected_columns or []

    def guardar_df(self, df):
        try:
            df.to_csv(self.filename, index=False, encoding="utf-8")
            print(f"✅ CSV guardado exitosamente en '{self.filename}'.")
        except Exception as e:
            print(f"❌ Error al guardar CSV: {e}")

    def cargar_df(self):
        try:
            df = pd.read_csv(self.filename)
            print(f"✅ Archivo '{self.filename}' cargado exitosamente.")
            return df
        except FileNotFoundError:
            print(f"❌ Archivo '{self.filename}' no encontrado. Creando DataFrame vacío.")
            return pd.DataFrame(columns=self.expected_columns)
        except Exception as e:
            print(f"❌ Error al cargar CSV: {e}")
            return pd.DataFrame(columns=self.expected_columns)
