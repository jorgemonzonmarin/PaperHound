# PaperHound – Motores de Búsqueda Académica

Este repositorio contiene varios módulos Python diseñados para consultar artículos académicos desde múltiples fuentes en línea como Google Scholar, Scopus, ArXiv, OpenAlex, CrossRef y Semantic Scholar. Cada módulo implementa funciones para lanzar búsquedas por título o palabra clave, y en algunos casos, recuperar información adicional como resúmenes.

---

## Índice de Ficheros

### `filter.py`
Este módulo define un filtro común usado por todos los motores para descartar resultados no válidos.

- **Función principal**:
  - `filter_valid_results(results)`: Filtra resultados que no tienen título o tienen el título como "No disponible".

---

### `google_schoolar.py`
Conecta con Google Scholar utilizando la librería `scholarly`.

- **Funciones**:
  - `fetch_scholar_articles(query, max_results=10)`: Devuelve una lista de artículos relevantes, incluyendo título, revista (venue) y DOI (si disponible).

---

### `open_alex_api.py`
Conecta con la API pública de OpenAlex.

- **Funciones**:
  - `fetch_openalex_articles(query, max_results=10)`: Realiza una búsqueda de artículos por título y devuelve resultados relevantes.
  - `get_paper_info_openalex(title)`: Extrae el resumen del artículo (si está disponible) usando su estructura invertida de índice.

---

### `scopus_api.py`
Accede a la API de Scopus de Elsevier para recuperar metadatos de artículos científicos.

- **Funciones**:
  - `fetch_scopus_articles(query, max_results=10)`: Lanza una búsqueda por título y devuelve resultados con título y DOI.
  - `get_paper_info_scopus(title)`: Intenta recuperar la descripción (abstract) del artículo por título.

> ⚠️ Necesita una API key válida para funcionar.

---

### `arxiv.py`
Consulta la API XML de ArXiv.org para obtener artículos científicos, especialmente en áreas como física, matemáticas, e informática.

- **Funciones**:
  - `fetch_arxiv_articles(query, max_results=10)`: Recupera artículos con título y enlace permanente a su entrada en ArXiv.
  - `get_paper_info_arxiv(title)`: Obtiene el resumen del artículo indicado por su título.

---

### `cross_ref_api.py`
Utiliza la API de CrossRef para acceder a metadatos bibliográficos.

- **Funciones**:
  - `fetch_crossref_articles(query, max_results=10)`: Busca artículos usando la API de CrossRef y devuelve título y DOI.
  - `get_paper_info_crossref(title)`: Recupera el abstract de un artículo dado su título.

---

### `semantic_schoolar_api.py`
Consulta la API de Semantic Scholar para obtener información sobre artículos académicos.

- **Funciones**:
  - `get_paper_info_semantic(title)`: Extrae el resumen (abstract) del artículo con el título especificado.

---

## Formato de Resultados

Cada motor de búsqueda devuelve una lista de diccionarios con las siguientes claves comunes:

- `query`: Consulta original realizada.
- `titulo`: Título del artículo encontrado.
- `revista`: Fuente o repositorio desde el cual se obtuvo.
- `doi`: Identificador DOI o enlace permanente.

---

## Uso

Cada script puede ejecutarse de forma individual desde línea de comandos para pruebas, usando una consulta predefinida y un ejemplo de título para extraer resúmenes.

```bash
python google_schoolar.py
