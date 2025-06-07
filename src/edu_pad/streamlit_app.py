import streamlit as st
import pandas as pd
import altair as alt
import os


class StreamlitApp:
    def __init__(self):
        st.set_page_config(
            page_title="📊 Dashboard Productos MercadoLibre",
            page_icon="🛒",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        st.title("🛒 Dashboard de Productos - MercadoLibre")
        self.ruta_datos = "/workspaces/PAD_2025_1/proyecto_integrado_iii/src/edu_pad/static/csv/productos_mercadolibre_limpio.csv"

        if not os.path.exists(self.ruta_datos):
            st.error(f"❌ No se encontró el archivo: {self.ruta_datos}")
            self.df = pd.DataFrame()
            return

        self.df = pd.read_csv(self.ruta_datos)
        self._preparar_datos()

    def _preparar_datos(self):
        if 'fecha_update' not in self.df.columns:
            self.df['fecha_update'] = pd.Timestamp.now()

        self.df['fecha_update'] = pd.to_datetime(self.df['fecha_update'], errors='coerce')

        if 'precio' in self.df.columns:
            self.df['precio'] = pd.to_numeric(self.df['precio'], errors='coerce')
        elif 'Precio Actual' in self.df.columns:
            self.df['precio'] = pd.to_numeric(self.df['Precio Actual'], errors='coerce')
        else:
            self.df['precio'] = pd.NA

        self.df.dropna(subset=['fecha_update', 'precio'], inplace=True)

    def sidebar_filtros(self):
        with st.sidebar:
            st.title("🔍 Filtros")

            if 'categoria' in self.df.columns:
                categorias = self.df['categoria'].dropna().unique().tolist()
            else:
                categorias = []

            self.selected_categoria = st.selectbox("Seleccionar categoría", ["Todas"] + sorted(categorias))

            fechas = self.df['fecha_update'].dt.date.unique()
            fechas = sorted(fechas)

            if len(fechas) > 1 and fechas[0] != fechas[-1]:
                self.selected_fecha = st.slider(
                    "Seleccionar rango de fechas",
                    min_value=fechas[0],
                    max_value=fechas[-1],
                    value=(fechas[0], fechas[-1])
                )
            elif len(fechas) == 1:
                self.selected_fecha = st.date_input(
                    "Seleccionar fecha",
                    value=fechas[0]
                )
            else:
                self.selected_fecha = None

    def aplicar_filtros(self):
        df_filtrado = self.df.copy()

        if self.selected_categoria != "Todas" and self.selected_categoria:
            df_filtrado = df_filtrado[df_filtrado["categoria"] == self.selected_categoria]

        if self.selected_fecha:
            if isinstance(self.selected_fecha, (tuple, list)):
                start, end = self.selected_fecha
                df_filtrado = df_filtrado[
                    (df_filtrado["fecha_update"].dt.date >= start) &
                    (df_filtrado["fecha_update"].dt.date <= end)
                ]
            else:
                df_filtrado = df_filtrado[
                    df_filtrado["fecha_update"].dt.date == self.selected_fecha
                ]

        return df_filtrado

    def mostrar_graficos(self, df):
        if df.empty:
            st.warning("⚠️ No hay datos para mostrar con los filtros seleccionados.")
            return

        posibles_titulos = ["Título", "titulo", "Titulo", "name", "nombre"]
        titulo_col = None
        for col in posibles_titulos:
            if col in df.columns:
                titulo_col = col
                break

        if titulo_col is None:
            st.warning("⚠️ No se encontró columna de título en los datos.")
            titulo_col = None

        st.subheader("📈 Evolución de precios")
        tooltip_cols = []
        if titulo_col:
            tooltip_cols.append(titulo_col)
        if "precio" in df.columns:
            tooltip_cols.append("precio")
        if "fecha_update" in df.columns:
            tooltip_cols.append("fecha_update")

        line_chart = alt.Chart(df).mark_line().encode(
            x="fecha_update:T",
            y="precio:Q",
            tooltip=tooltip_cols if tooltip_cols else None
        ).properties(width=800, height=400)

        st.altair_chart(line_chart, use_container_width=True)

        st.subheader("🏷️ Productos recientes")
        cols_mostrar = []
        if titulo_col:
            cols_mostrar.append(titulo_col)
        if "precio" in df.columns:
            cols_mostrar.append("precio")
        if "fecha_update" in df.columns:
            cols_mostrar.append("fecha_update")

        if cols_mostrar:
            df_display = df.sort_values("fecha_update", ascending=False)[cols_mostrar].head(10)
            st.dataframe(df_display)
        else:
            st.info("No hay columnas disponibles para mostrar en la tabla de productos.")


if __name__ == "__main__":
    app = StreamlitApp()
    if not app.df.empty:
        app.sidebar_filtros()
        datos_filtrados = app.aplicar_filtros()
        app.mostrar_graficos(datos_filtrados)
