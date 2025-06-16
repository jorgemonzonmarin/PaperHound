FROM python:3.12

# Instalación de dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git unzip libstdc++6 ca-certificates procps && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Instalar Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Agrega Ollama al PATH
ENV PATH="/root/.ollama/bin:${PATH}"

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir ollama && \
    pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY ./PaperHound .

# ❗ Copiar el modelo previamente descargado
COPY ./models /root/.ollama/models

# ❌ Ya no se hace pull, porque ya copiaste el modelo
# (El servidor se iniciará al lanzar el contenedor con el modelo ya disponible)

# Exponer puertos
EXPOSE 3000
EXPOSE 11434

# Script de arranque
CMD ["bash", "/app/start.sh"]
