# Workflow de Extracción e Ingesta de Datos de Laptops desde Mercado Libre con Docker y GitHub Actions

Este proyecto implementa un flujo automatizado para la extracción e ingesta de datos de productos (laptops) disponibles en Mercado Libre Colombia. Se utilizan herramientas como Docker y GitHub Actions para orquestar un proceso reproducible de integración y entrega continua (CI/CD).

## Estructura del Flujo de Trabajo

El flujo automatizado se realiza mediante un único workflow de GitHub Actions (`accionables.yml`) con los siguientes pasos:

1. **Checkout del Repositorio**
   - Clona el repositorio al runner de GitHub Actions.

2. **Autenticación en Docker Hub**
   - Se realiza login utilizando secretos `DOCKER_USERNAME` y `DOCKER_TOKEN`.

3. **Construcción de Imagen Docker**
   - Se crea una imagen con todas las dependencias necesarias para ejecutar los scripts de scraping e ingesta.

4. **Ejecución de la Extracción**
   - Se corre el script `main_extractor.py` dentro del contenedor para extraer información estructurada de laptops publicadas en Mercado Libre.

5. **Ejecución de la Ingesta**
   - Se ejecuta `main_ingesta.py` para almacenar los datos extraídos en un archivo o base de datos.

## Estructura del Proyecto

proyecto/
├── .github/
│ └── workflows/
│ └── docker.yml
├── src/
│ └── edu_pad/
│ ├── database.py
│ ├── dataweb.py
│ ├── main_extractor.py
│ ├── main_ingesta.py
│ └── static/
│ ├── csv/
│ └── db/
├── Dockerfile
├── requirements.txt
└── README.md


## Requisitos de Configuración

Para la correcta ejecución del pipeline, deben definirse los siguientes secretos en GitHub:

- `DOCKER_USERNAME`: Usuario de Docker Hub.
- `DOCKER_TOKEN`: Token de acceso a Docker Hub.

## Características Principales

- **Automatización CI/CD**: El flujo se ejecuta automáticamente al hacer `push` a la rama principal.
- **Reproducibilidad**: Uso de Docker para estandarizar el entorno de ejecución.
- **Extracción web dinámica**: Uso de Selenium para manejar el contenido cargado dinámicamente desde Mercado Libre.
- **Persistencia**: Los datos se almacenan en carpetas compartidas (volúmenes) entre host y contenedor.

## Cómo Ejecutar Localmente

1. **Construir imagen Docker:**

```bash
docker build -t contenedor .

