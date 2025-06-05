import pandas as pd
import sqlite3
import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class DatabaseMonitor:
    def __init__(self):
        self.rutadb = "src/edu_pad/static/db/mercado_analisis.db"
        self.tabla = "mercado_analisis"
        self.ruta_log = "src/edu_pad/static/logs/monitor_log.json"

    def verificar_base_datos(self):
        if not os.path.exists(self.rutadb):
            print(f"ERROR: Base de datos no encontrada en {self.rutadb}")
            return False
        try:
            conn = sqlite3.connect(self.rutadb)
            conn.close()
            print("Base de datos verificada correctamente")
            return True
        except Exception as e:
            print(f"ERROR: No se pudo conectar a la base de datos: {str(e)}")
            return False

    def contar_registros(self):
        try:
            conn = sqlite3.connect(self.rutadb)
            cursor = conn.cursor()

            cursor.execute(f"SELECT COUNT(*) FROM {self.tabla}")
            total_registros = cursor.fetchone()[0]

            cursor.execute(f"SELECT COUNT(*) FROM {self.tabla} WHERE titulo IS NULL OR precio IS NULL")
            registros_nulos = cursor.fetchone()[0]

            cursor.execute(f"SELECT MAX(fecha_update) FROM {self.tabla}")
            ultima_actualizacion = cursor.fetchone()[0]

            conn.close()

            print(f"Total de registros: {total_registros}")
            print(f"Registros con valores nulos: {registros_nulos}")
            print(f"Última actualización: {ultima_actualizacion}")

            return {
                "total_registros": total_registros,
                "registros_nulos": registros_nulos,
                "ultima_actualizacion": ultima_actualizacion,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"ERROR: No se pudo contar registros: {str(e)}")
            return None

    def analizar_precios(self):
        """Analiza la evolución del precio promedio de los productos más recientes"""
        try:
            conn = sqlite3.connect(self.rutadb)
            query = f"""
            SELECT fecha_update, precio 
            FROM {self.tabla}
            WHERE precio IS NOT NULL
            ORDER BY fecha_update DESC
            LIMIT 30
            """
            df = pd.read_sql_query(query, conn)
            conn.close()

            if len(df) < 5:
                print("No hay suficientes datos para analizar precios")
                return None

            df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
            df = df.dropna()

            df = df.sort_values("fecha_update")

            df["prom_movil_5"] = df["precio"].rolling(window=5).mean()

            ultimo_precio = df["precio"].iloc[-1]
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
            print(f"ERROR: No se pudo analizar precios: {str(e)}")
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

            print(f"Log guardado correctamente en {self.ruta_log}")
            return True
        except Exception as e:
            print(f"ERROR: No se pudo guardar el log: {str(e)}")
            return False

    def enviar_alerta(self, asunto, mensaje):
        try:
            email_emisor = os.environ.get('EMAIL_SENDER')
            email_receptor = os.environ.get('EMAIL_RECEIVER')
            email_password = os.environ.get('EMAIL_PASSWORD')
            smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.environ.get('SMTP_PORT', 587))

            if not all([email_emisor, email_receptor, email_password]):
                print("ADVERTENCIA: Faltan variables de entorno para envío de email.")
                return False

            msg = MIMEMultipart()
            msg['From'] = email_emisor
            msg['To'] = email_receptor
            msg['Subject'] = asunto
            msg.attach(MIMEText(mensaje, 'plain'))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_emisor, email_password)
            server.send_message(msg)
            server.quit()

            print(f"Correo enviado a {email_receptor}")
            return True
        except Exception as e:
            print(f"ERROR: No se pudo enviar el email: {str(e)}")
            return False

    def ejecutar_monitoreo(self):
        print("*******************************************************************")
        print(f"Inicio de monitoreo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("*******************************************************************")

        if not self.verificar_base_datos():
            self.enviar_alerta(
                "ALERTA: Base de datos no accesible",
                f"No se puede acceder a la base de datos de productos. Fecha: {datetime.now()}"
            )
            return False

        metricas = self.contar_registros()
        if not metricas:
            self.enviar_alerta(
                "ALERTA: Fallo al contar registros",
                f"No se pudo obtener métricas de la tabla {self.tabla}. Fecha: {datetime.now()}"
            )
            return False

        tendencia = self.analizar_precios()
        if tendencia:
            metricas.update(tendencia)

        self.guardar_log(metricas)

        if metricas.get("registros_nulos", 0) > 0:
            self.enviar_alerta(
                "ALERTA: Registros nulos",
                f"Se encontraron {metricas['registros_nulos']} registros incompletos en la tabla {self.tabla}."
            )

        if tendencia and tendencia.get("tendencia_precio") != "PRECIO ESTABLE":
            self.enviar_alerta(
                f"INFO: {tendencia['tendencia_precio']}",
                f"Se detectó una tendencia: {tendencia['tendencia_precio']}.\n" +
                f"Último precio: {tendencia['ultimo_precio']:.2f}\n" +
                f"Promedio móvil (5): {tendencia['promedio_movil_5']:.2f}"
            )

        print("*******************************************************************")
        print(f"Fin de monitoreo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("*******************************************************************")
        return True


if __name__ == "__main__":
    monitor = DatabaseMonitor()
    monitor.ejecutar_monitoreo()
