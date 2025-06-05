# Workflow de ETL para Datos del Dólar con GitHub Actions

Workflow de ETL para Productos de Mercado Libre con GitHub Actions
Este proyecto implementa un flujo completo de ETL (Extracción, Transformación y Carga) para el monitoreo de productos de Mercado Libre usando GitHub Actions como orquestador de CI/CD.

⚙️ Estructura del Flujo de Trabajo
El proceso está dividido en cuatro workflows de GitHub Actions:

Setup Environment (0-Setup-Environment.yml)

Prepara el entorno de ejecución y dependencias con setup.py

Se ejecuta automáticamente al hacer push al branch principal o de forma manual

Data Extraction (1-Data-Extraction.yml)

Extrae información de productos desde Mercado Libre (precios, títulos, fechas, etc.)

Guarda los datos en formato CSV temporal

Se ejecuta cada 12 horas o manualmente

Si falla la extracción, detiene el pipeline

Data Ingestion (2-Data-Ingestion.yml)

Inserta los datos del CSV en una base de datos SQLite para consultas y monitoreo

Elimina el CSV después de la ingesta

Se ejecuta automáticamente tras una extracción exitosa

Data Monitoring (3-Data-Monitoring.yml)

Revisa la integridad de la base de datos

Analiza tendencias de precios en productos monitoreados

Genera logs en JSON y envía alertas por correo si se detectan anomalías

Se ejecuta cada 6 horas o manualmente

🔐 Requisitos de Configuración
Para que este flujo funcione correctamente, debes definir los siguientes secrets en GitHub:

EMAIL_SENDER: Correo electrónico emisor

EMAIL_RECEIVER: Correo electrónico destinatario

EMAIL_PASSWORD: Contraseña del emisor o token de aplicación

SMTP_SERVER: Servidor SMTP (por defecto: smtp.gmail.com)

SMTP_PORT: Puerto SMTP (por defecto: 587)



## Estructura del Proyecto

```
proyecto/
├── .github/
│   └── workflows/
│       ├── 0-Setup-Environment.yml
│       ├── 1-Data-Extraction.yml
│       ├── 2-Data-Ingestion.yml
│       └── 3-Data-Monitoring.yml
├── src/
│   └── edu_pad/
│       ├── database.py
│       ├── dataweb.py
│       ├── main_extractor.py
│       ├── main_ingesta.py
│       ├── monitor.py
│       ├── streamlit_app.py
│       └── static/
│           ├── csv/
│           ├── db/
│           ├── logs/
│           └── html/
├── setup.py
└── README.md
