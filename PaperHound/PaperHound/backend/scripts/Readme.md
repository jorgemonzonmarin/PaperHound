# PaperHound – Búsqueda, Almacenamiento y Evaluación de Artículos Científicos

Este módulo amplía la funcionalidad de búsqueda con herramientas para guardar automáticamente los resultados en CSV y analizar la relevancia de los artículos mediante un modelo de lenguaje natural.

---

## Índice de Ficheros

### `search_papers.py`
Módulo principal para lanzar búsquedas académicas simultáneamente en múltiples fuentes.

- **Fuentes soportadas**:
  - Scopus
  - Google Scholar
  - OpenAlex
  - ArXiv
  - CrossRef

- **Funciones**:
  - `search_papers(queries, max_results=10)`: Devuelve una lista combinada de resultados obtenidos desde las fuentes anteriores, cada uno con:
    - `titulo`
    - `doi`
    - `revista`
    - `query` original usada:contentReference[oaicite:0]{index=0}.

---

### `search_and_save_papers.py`
Extiende `search_papers.py` agregando la lógica para guardar los resultados en un archivo CSV y obtener el abstract de cada artículo.

- **Funciones**:
  - `search_and_save_papers(queries=QUERIES)`: Lanza una búsqueda por cada query definida en la lista `QUERIES`, obtiene los abstracts a través de varias fuentes (en orden de preferencia) y guarda los resultados en un archivo CSV dentro de `assets/papers_encontrados`.

- **Lógica adicional**:
  - `get_valid_abstract(title)`: Prueba múltiples fuentes para recuperar el abstract más completo.
  - `save_to_csv(file_path, data)`: Guarda datos en CSV con codificación UTF-8 y manejo correcto de campos con comas.
  - `generate_filename(base_name)`: Evita sobrescribir archivos existentes generando nombres únicos basados en la fecha:contentReference[oaicite:1]{index=1}.

---

### `procesar_papers.py`
Procesa los resultados guardados (CSV) usando un modelo LLM para analizar sistemáticamente cada artículo con base en una serie de 13 preguntas.

- **Funciones principales**:
  - `procesar_articulos(csv_path, output_path)`: 
    - Carga un CSV con artículos previamente descargados.
    - Crea prompts usando el título y abstract.
    - Envía los prompts a un modelo de lenguaje (como `ollama` con `deepseek-r1:8b`) para analizar cada paper.
    - Estructura las respuestas en listas explicadas y resumidas.
    - Guarda el resultado en un nuevo CSV.
  
  - `verificar_y_reprocesar(output_path, threshold=0.2)`: Reanaliza artículos cuyo porcentaje de respuestas `NaN` en las columnas tipo `summary` supera un umbral, para asegurar calidad del análisis.

- **Utilidades**:
  - `crea_prompt(...)`: Crea un prompt muy estructurado para obtener respuestas en formato rígido.
  - `process_text(...)`: Extrae de la respuesta del modelo las respuestas explicadas y resumidas y las inserta en un `DataFrame`.
  - `sort_by_yes_count(...)`: Ordena los artículos por número de respuestas "Yes" en las columnas `summary`, para priorizar los más relevantes.

- **Columnas en el CSV de salida**:
  - Título, DOI, Revista, Abstract
  - 13 columnas `n. explained` con justificación
  - 13 columnas `n. summary` con respuestas sintéticas
  - Columna `Respuesta` con todo el output generado por el modelo:contentReference[oaicite:2]{index=2}.

---

## Requisitos

- Python 3.x
- Bibliotecas:
  - `pandas`
  - `ollama` (para conexión con modelos LLM locales o remotos)
  - `logging`, `re`, `csv`
  - Fuentes externas: conexión a Internet y claves API donde aplique

---

## Ejecución

```bash
# Buscar y guardar artículos
python search_and_save_papers.py

# Analizar artículos previamente guardados
python procesar_papers.py
