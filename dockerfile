# Usa una imagen base ligera con Python 3.9
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el contenido del proyecto al contenedor
COPY . .

# Crea las carpetas necesarias para CSV y base de datos
RUN mkdir -p src/edu_pad/static/csv src/edu_pad/static/db

# Instala las dependencias del proyecto
RUN pip install --upgrade pip \
    && pip install -e . \
    && rm -rf /root/.cache/pip

# Establece la raíz del módulo Python
ENV PYTHONPATH=/app/src

# Punto de entrada del contenedor: ejecuta un módulo Python
ENTRYPOINT ["python", "-m"]

# Comando por defecto si no se especifica otro
CMD ["edu_pad.main_extractor"]
