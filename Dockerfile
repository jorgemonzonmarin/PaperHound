# Usa una imagen base de Python ligera
FROM python:3.12-slim

# Instala unzip y otras dependencias necesarias
RUN apt-get update && apt-get install -y unzip curl && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos antes para aprovechar la caché
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Expone el puerto en el que correrá Reflex (por defecto 3000)
EXPOSE 3000

# Comando para iniciar la aplicación en modo producción
CMD ["reflex", "run"]
