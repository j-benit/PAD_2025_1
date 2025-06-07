import streamlit as st
import pandas as pd
import altair as alt
import os

class StreamlitApp:
    def __init__(self, ruta_datos="/workspaces/PAD_2025_1/proyecto_integrado_iii/src/edu_pad/static/csv/productos_mercadolibre_limpio.csv"):
        st.set_page_config(
            page_title="📊 Dashboard Productos MercadoLibre",
            page_icon="🛒",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        st.title("🛒 Dashboard de Productos - MercadoLibre")
        self.ruta_datos = ruta_datos

        if not os.path.exists(self.ruta_datos):
            st.error(f"❌ No se encontró el archivo: {self.ruta_datos}")
            self.df = pd.DataFrame()
            return

        self.df = pd.read_csv(self.ruta_datos)
        self._preparar_datos()

    def _preparar_datos(self):
        # Asegura que las columnas de fecha y precio estén limpias y en el formato correcto
        self.df['fecha_update'] = pd.to_datetime(self.df['fecha_update'], errors='coerce')
        self.df['precio'] = pd.to_numeric(self.df['precio'], errors='coerce')
        self.df.dropna(subset=['fecha_update', 'precio'], inplace=True)

    def sidebar_filtros(self):
        with st.sidebar:
            st.title("🔍 Filtros")

            categorias = self.df['categoria'].dropna().unique().tolist() if 'categoria' in self.df.columns else []
            self.selected_categoria = st.selectbox("Seleccionar categoría", ["Todas"] + sorted(categorias))

            fechas = self.df['fecha_update'].dt.date.unique() if 'fecha_update' in self.df.columns else []
            if len(fechas) > 0:
                self.selected_fecha = st.slider(
                    "Seleccionar rango de fechas",
                    min_value=min(fechas),
                    max_value=max(fechas),
                    value=(min(fechas), max(fechas))
                )
            else:
                self.selected_fecha = None

    def aplicar_filtros(self):
        df_filtrado = self.df.copy()

        if hasattr(self, 'selected_categoria') and self.selected_categoria != "Todas":
            df_filtrado = df_filtrado[df_filtrado["categoria"] == self.selected_categoria]

        if hasattr(self, 'selected_fecha') and self.selected_fecha:
            start, end = self.selected_fecha
            df_filtrado = df_filtrado[
                (df_filtrado["fecha_update"].dt.date >= start) &
                (df_filtrado["fecha_update"].dt.date <= end)
            ]

        return df_filtrado

    def mostrar_graficos(self, df):
        if df.empty:
            st.warning("⚠️ No hay datos para mostrar con los filtros seleccionados.")
            return

        st.subheader("📈 Evolución de precios")
        line_chart = alt.Chart(df).mark_line().encode(
            x="fecha_update:T",
            y="precio:Q",
            tooltip=["titulo", "precio", "fecha_update"]
        ).properties(width=800, height=400)

        st.altair_chart(line_chart, use_container_width=True)

        st.subheader("🏷️ Productos recientes")
        st.dataframe(df.sort_values("fecha_update", ascending=False)[["titulo", "precio", "fecha_update"]].head(10))


if __name__ == "__main__":
    app = StreamlitApp()
    if not app.df.empty:
        app.sidebar_filtros()
        datos_filtrados = app.aplicar_filtros()
        app.mostrar_graficos(datos_filtrados)
