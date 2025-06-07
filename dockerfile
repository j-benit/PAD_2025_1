FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todo el contenido del proyecto al contenedor
COPY . .

# Asegura que existan las carpetas necesarias
RUN mkdir -p src/edu_pad/static/csv src/edu_pad/static/db

# Instala dependencias del proyecto
RUN pip install --upgrade pip \
    && pip install -e . \
    && rm -rf /root/.cache/pip

# Define la raíz de los módulos de Python
ENV PYTHONPATH=/app/src

# Define el punto de entrada (ejecuta un módulo)
ENTRYPOINT ["python", "-m"]

# Comando por defecto: módulo extractor
CMD ["edu_pad.main_extractor"]
