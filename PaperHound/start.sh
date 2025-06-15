#!/bin/bash

# Iniciar Ollama
ollama serve &

# Esperar a que esté disponible
until curl -s http://localhost:11434/ > /dev/null; do
  echo "Esperando a que Ollama esté listo..."
  sleep 1
done

echo "Ollama está listo. Ejecutando la aplicación..."

# Lanzar tu app (por ejemplo, Reflex)
reflex run
