import pandas as pd
import os
import json
from datetime import datetime

class DatabaseMonitor:
    def __init__(self, ruta_csv, ruta_log="src/edu_pad/static/logs/monitor_log.json"):
        self.ruta_csv = ruta_csv
        self.ruta_log = ruta_log

    def verificar_archivo(self):
        if not os.path.exists(self.ruta_csv):
            print(f"ERROR: Archivo no encontrado en {self.ruta_csv}")
            return False
        print("Archivo CSV verificado correctamente")
        return True

    def contar_registros(self):
        try:
            df = pd.read_csv(self.ruta_csv)
            total_registros = len(df)
            registros_nulos = df.isnull().sum().sum()  # total valores nulos en todo el df
            ultima_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # o si tienes fecha en df, toma max
            
            print(f"Total registros: {total_registros}")
            print(f"Valores nulos totales: {registros_nulos}")
            print(f"Última actualización (monitor): {ultima_actualizacion}")

            return {
                "total_registros": total_registros,
                "registros_nulos": registros_nulos,
                "ultima_actualizacion": ultima_actualizacion,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"ERROR al contar registros: {str(e)}")
            return None

    def analizar_precios(self):
        try:
            df = pd.read_csv(self.ruta_csv)
            if "Precio Actual" not in df.columns:
                print("No hay columna 'Precio Actual' para analizar precios")
                return None
            df = df.dropna(subset=["Precio Actual"])
            if len(df) < 5:
                print("No hay suficientes datos para analizar precios")
                return None
            df = df.sort_index()  # Asumimos orden cronológico por índice o una columna fecha si la tienes

            df["prom_movil_5"] = df["Precio Actual"].rolling(window=5).mean()
            ultimo_precio = df["Precio Actual"].iloc[-1]
            promedio_movil = df["prom_movil_5"].iloc[-1]

            if ultimo_precio > promedio_movil * 1.05:
                tendencia = "PRECIO EN AUMENTO"
            elif ultimo_precio < promedio_movil * 0.95:
                tendencia = "PRECIO EN BAJA"
            else:
                tendencia = "PRECIO ESTABLE"

            print(f"Tendencia de precios: {tendencia}")

            return {
                "ultimo_precio": ultimo_precio,
                "promedio_movil_5": promedio_movil,
                "tendencia_precio": tendencia
            }
        except Exception as e:
            print(f"ERROR al analizar precios: {str(e)}")
            return None

    def guardar_log(self, metricas):
        try:
            os.makedirs(os.path.dirname(self.ruta_log), exist_ok=True)
            if os.path.exists(self.ruta_log):
                with open(self.ruta_log, 'r') as f:
                    try:
                        logs = json.load(f)
                    except:
                        logs = {"registros": []}
            else:
                logs = {"registros": []}

            logs["registros"].append(metricas)
            if len(logs["registros"]) > 30:
                logs["registros"] = logs["registros"][-30:]

            with open(self.ruta_log, 'w') as f:
                json.dump(logs, f, indent=2)

            print(f"Log guardado en {self.ruta_log}")
            return True
        except Exception as e:
            print(f"ERROR al guardar log: {str(e)}")
            return False

    def ejecutar_monitoreo(self):
        print(f"Inicio monitoreo: {datetime.now()}")
        if not self.verificar_archivo():
            return False

        metricas = self.contar_registros()
        if not metricas:
            return False

        tendencia = self.analizar_precios()
        if tendencia:
            metricas.update(tendencia)

        self.guardar_log(metricas)

        # Aquí podrías añadir alertas con print o emails si quieres (adaptar función de correo)
        if metricas.get("registros_nulos", 0) > 0:
            print(f"ALERTA: Hay {metricas['registros_nulos']} valores nulos en el CSV")

        if tendencia and tendencia.get("tendencia_precio") != "PRECIO ESTABLE":
            print(f"INFO: Tendencia detectada: {tendencia['tendencia_precio']}")

        print(f"Fin monitoreo: {datetime.now()}")
        return True
