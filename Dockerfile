# Usa una imagen base de Python
FROM python:3.10

# Instalar dependencias del sistema necesarias para aplicaciones gráficas
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Configura el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos de la carpeta actual al contenedor
COPY . /app

# Crea un entorno virtual e instala las dependencias
RUN python -m venv --copies /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Añade el entorno virtual al PATH para que se use por defecto
ENV PATH="/opt/venv/bin:$PATH"

# Copia y prepara el script de inicio
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["./start.sh"]




