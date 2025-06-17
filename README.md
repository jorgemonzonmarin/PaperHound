# 📚 PaperHound – Sistema Inteligente para Revisión Sistemática de Literatura Científica

<div style="display: flex; align-items: center; gap: 20px;">
  <img src="PaperHound/assets/Logo.png" alt="PaperHound Logo" width="140"/>
  <p>
    <strong>PaperHound</strong> es una herramienta web desarrollada en Python con Reflex que automatiza, organiza y acelera el proceso de revisión sistemática de literatura científica. Está diseñada para investigadores, doctorandos, ingenieros y equipos de I+D que buscan eficiencia, trazabilidad y rigor metodológico en sus revisiones bibliográficas.
  </p>
</div>



---

## 🎯 Objetivo del Proyecto

El objetivo de PaperHound es **automatizar la búsqueda, clasificación y análisis de artículos científicos** mediante el uso de consultas complejas (queries), preguntas de revisión y modelos de lenguaje como DeepSeek. El sistema extrae artículos desde múltiples bases de datos, los filtra usando criterios definidos por el usuario y genera una tabla resumen priorizada y justificable.

---

## 🧩 Problemas que resuelve

| Problema | Cómo lo soluciona PaperHound |
|---------|-------------------------------|
| 🔍 La búsqueda manual de artículos es tediosa y propensa a omisiones | Permite definir queries complejas en lenguaje booleano para realizar búsquedas automáticas en Scopus, arXiv, OpenAlex, CrossRef, Semantic Scholar y Google Scholar |
| 📂 Es difícil mantener trazabilidad de queries y criterios de inclusión/exclusión | Almacena y muestra de forma estructurada el tópico, las queries y las preguntas en un panel resumen reproducible |
| ✅ El filtrado de papers es subjetivo y consume mucho tiempo | Utiliza un modelo LLM (DeepSeek vía Ollama) para responder preguntas dicotómicas sobre cada artículo y justificar cada decisión |
| 📊 No hay forma sencilla de priorizar artículos relevantes | Genera automáticamente un CSV ordenado por número de respuestas positivas a los criterios establecidos |
| ⚙️ El proceso no es fácilmente reutilizable o desplegable | Todo el sistema es portable vía Docker y puede ejecutarse de forma local o remota sin configuración manual |

---

## 🛠️ Estructura General

```text
PaperHound/
├── backend/                # Lógica de estado (queries, preguntas, topic, procesamiento)
├── components/             # Componentes visuales (tablas, selectores, navegación)
├── templates/              # Decoradores para definir páginas
├── assets/ 
│   ├── filtro_preguntas/   # Preguntas predefinidas en txt o csv
│   ├── papers_encontrados/ # Resultados de los papers encontrados de las bbdd
│   └── papers_filtrados/   # Resultados generados por el sistema
├── start.sh                # Script de arranque (opcional)
├── Dockerfile              # Imagen para ejecución aislada
├── requirements.txt        # Dependencias
└── README.md               # (Este documento)
```

---

## 🔄 Flujo del Usuario

1. **Introducción** – En la página de inicio se presenta el propósito del sistema.
2. **Definir Queries** – Se introducen consultas complejas para búsqueda de artículos.
3. **Definir Topic** – Se especifica el objetivo o temática central de la revisión.
4. **Añadir Preguntas** – Se redactan preguntas de decisión (tipo sí/no) que serán evaluadas por deepseek.
5. **Resumen** – Se muestra todo lo definido antes de lanzar el análisis.
6. **Procesamiento** – Se buscan artículos, se extraen abstracts y se analizan uno por uno mediante un modelo LLM.
7. **Visualización** – Se muestra una tabla con los artículos filtrados, ordenados por relevancia, con paginación y color semántico.

---

## ⚙️ Tecnologías utilizadas

- **Python 3.12**
- **Reflex** (framework web en Python)
- **Ollama** para ejecutar modelos LLM localmente (por ejemplo, `deepseek`)
- **APIs científicas**:
  - Scopus
  - ArXiv
  - CrossRef
  - OpenAlex
  - Semantic Scholar
  - Google Scholar (vía `scholarly`)
- **Docker** para ejecución multiplataforma

---

## 🧠 Lógica de Procesamiento Inteligente

El análisis semántico se realiza mediante un modelo LLM local (DeepSeek) que responde a cada pregunta definida por el usuario, generando:
- Lista justificada (`1. explained Yes - ...`)
- Lista resumida (`1. summary Yes`)

Esto permite un filtrado trazable y objetivo de los artículos.

---

## 🚀 Ejecución con Docker

El `Dockerfile`:
- Instala Python, dependencias y Ollama.
- Añade la app y los modelos.
- Expone los puertos necesarios (`3000`, `11434`).

### Build y ejecución

```bash
docker build -t paperhound .
docker run -e SCOPUS_API_KEY=valor -v <ruta_local>:/app/assets -p 3000:3000 -p 11434:11434 paperhound
```
---

# 📧 Contacto
Jorge Monzón Marín – jorgemonzonmarin@gmail.com