# Workflow de ETL para Datos del Dólar con GitHub Actions

Este proyecto implementa un flujo completo de ETL (Extracción, Transformación y Carga) para datos del dólar usando GitHub Actions como orquestador de CI/CD.

## Estructura del Flujo de Trabajo

El proceso está dividido en cuatro workflows de GitHub Actions:

1. **Setup Environment** (`0-Setup-Environment.yml`)
   - Prepara el entorno y la estructura del proyecto
   - Instala dependencias usando `setup.py`
   - Se ejecuta al hacer push al branch principal o manualmente

2. **Data Extraction** (`1-Data-Extraction.yml`)
   - Extrae datos del dólar desde Yahoo Finance
   - Guarda los datos en un archivo CSV
   - Se ejecuta cada 12 horas o manualmente
   - Si la extracción falla, detiene el pipeline

3. **Data Ingestion** (`2-Data-Ingestion.yml`)
   - Carga los datos del CSV en una base de datos SQLite
   - Elimina el CSV temporal después de la ingesta
   - Se ejecuta automáticamente después de una extracción exitosa

4. **Data Monitoring** (`3-Data-Monitoring.yml`)
   - Monitorea la base de datos SQLite verificando integridad y tendencias
   - Genera logs y envía alertas si es necesario
   - Se ejecuta después de una ingesta exitosa, cada 6 horas o manualmente

## Requisitos para la Configuración

Para que este workflow funcione correctamente, necesitas configurar los siguientes secretos en GitHub:

1. Para el envío de alertas por correo electrónico:
   - `EMAIL_SENDER`: Dirección de correo del remitente
   - `EMAIL_RECEIVER`: Dirección de correo del destinatario
   - `EMAIL_PASSWORD`: Contraseña o token de la cuenta del remitente
   - `SMTP_SERVER`: Servidor SMTP (valor predeterminado: smtp.gmail.com)
   - `SMTP_PORT`: Puerto SMTP (valor predeterminado: 587)

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
│       └── static/
│           ├── csv/
│           ├── db/
│           └── logs/
├── setup.py
└── README.md
```

## Instalación

1. Clona este repositorio
2. Configura los secretos en GitHub
3. Los workflows se ejecutarán automáticamente según lo programado o puedes iniciarlos manualmente

## Características Principales

- **Modular**: Cada fase del ETL está en su propio archivo YAML
- **Condicional**: Los jobs dependen del éxito de los anteriores
- **Monitoreo automatizado**: Análisis de tendencias y detección de anomalías
- **Alertas**: Notificaciones por correo cuando hay problemas o cambios importantes
- **Persistencia de artefactos**: Los datos y logs se conservan entre ejecuciones
- **Instalación simplificada**: Utiliza setup.py para gestionar dependencias

## Personalización

Para adaptar este workflow a tus necesidades:

1. Modifica `dataweb.py` para extraer datos de otras fuentes
2. Ajusta la frecuencia de ejecución modificando las expresiones cron en los archivos YAML
3. Añade más análisis o transformaciones en la clase `DatabaseMonitor`
4. Actualiza `setup.py` si necesitas instalar paquetes adicionales

---

Creado para la formacion de analitica de datos utilizando GitHub Actions y Python