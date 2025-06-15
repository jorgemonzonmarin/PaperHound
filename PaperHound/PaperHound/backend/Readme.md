# PaperHound UI – Lógica de Estado y Procesamiento en Reflex

Este módulo contiene la lógica de backend y estado de la interfaz web desarrollada con [Reflex](https://reflex.dev). Integra funcionalidades de búsqueda, procesamiento, filtrado y visualización de artículos académicos.

---

## Índice de Ficheros

### `topic_state.py`
Gestor de estado para el *tópico* de investigación que guía el análisis de relevancia.

- **Atributos**:
  - `topic`: Lista de cadenas (preguntas o enunciados).
  - `input_value`: Valor actual del campo de entrada.

- **Funciones clave**:
  - `add_question()`: Añade una pregunta a `topic`.
  - `remove_question(index)`: Elimina una pregunta por índice.
  - `topic_text`: Devuelve el texto combinado del tópico:contentReference[oaicite:0]{index=0}.

---

### `query_state.py`
Gestiona la lista de *consultas* (queries) para búsqueda de artículos.

- **Atributos**:
  - `queries`: Lista de cadenas de consulta.
  - `input_value`: Texto en el input para agregar nuevas queries.

- **Funciones clave**:
  - `add_question()`: Añade múltiples queries separadas por `;`.
  - `queries_text`: Devuelve todas las queries concatenadas.
  - `remove_question(index)`: Elimina una consulta por índice:contentReference[oaicite:1]{index=1}.

---

### `questions_state.py`
Administra el conjunto de preguntas de análisis que se aplican a cada artículo.

- **Atributos**:
  - `questions`: Lista de preguntas numeradas.
  - `selected_file`: Archivo CSV o TXT seleccionado desde el frontend.
  - `_file_options`: Lista interna de archivos disponibles.

- **Funciones clave**:
  - `add_question()`: Agrega nuevas preguntas numeradas automáticamente.
  - `load_file_options()`: Carga archivos disponibles desde `assets/filtro_preguntas`.
  - `load_questions_from_selected_file()`: Carga preguntas desde un archivo.
  - `questions_text`: Devuelve las preguntas en formato texto:contentReference[oaicite:2]{index=2}.

---

### `processing_state.py`
Orquesta todo el flujo de procesamiento: búsqueda → análisis → filtrado.

- **Atributos**:
  - `status`: Estado textual del proceso.
  - `papers_filepath`: Ruta al CSV con los papers encontrados.

- **Flujo principal**:
  1. Obtiene las queries desde `QueryState`.
  2. Ejecuta `search_and_save_papers`.
  3. Obtiene el tópico y preguntas desde `TopicState` y `QuestionState`.
  4. Ejecuta `procesar_articulos` y `verificar_y_reprocesar` en segundo plano mediante `threading` y `asyncio`.
  5. Actualiza el estado para reflejar el progreso:contentReference[oaicite:3]{index=3}.

---

### `run_in_thread.py`
Función utilitaria para ejecutar funciones bloqueantes en segundo plano sin bloquear el bucle de eventos de Reflex.

- **Función**:
  - `run_in_thread(func)`: Ejecuta una función sincrónica dentro de un hilo, usando `run_in_executor`:contentReference[oaicite:4]{index=4}.

---

### `rx_procesar_papers.py`
Script experimental que prueba la ejecución del procesamiento y reprocesamiento en `background` con Reflex.

- **Clases**:
  - `TaskInfo`: Información de una tarea individual.
  - `RunInThreadState`: Contiene eventos para correr tareas asincrónicas:
    - `run_quick_task`
    - `run_procesar_articulos`
    - `run_verificar_y_reprocesar`
  - Utiliza `rx.run_in_thread` y `asyncio.wait_for` con timeout:contentReference[oaicite:5]{index=5}.

---

### `sidebar_state.py`
Maneja el estado de visibilidad del panel lateral de navegación.

- **Atributos**:
  - `show_sidebar`: Booleano que indica si el sidebar está visible.

- **Métodos**:
  - `toggle_sidebar()`: Cambia el estado.
  - `close_sidebar()`: Lo oculta directamente:contentReference[oaicite:6]{index=6}.

---

### `table_state.py`
Permite cargar y visualizar un CSV en una tabla con paginación, ordenación y filtrado dinámico.

- **Atributos**:
  - `items`: Lista de diccionarios (filas del CSV).
  - `columns`: Lista de nombres de columna detectados.
  - `selected_file`: Archivo CSV seleccionado.
  - `search_value`, `sort_value`, `limit`, `offset`: Control de navegación.

- **Funciones clave**:
  - `load_entries()`: Carga y filtra columnas del CSV desde `assets/papers_filtrados`.
  - `filtered_sorted_items`: Devuelve ítems filtrados y ordenados.
  - `get_current_page`: Devuelve la página activa.
  - Métodos de navegación: `next_page`, `prev_page`, `first_page`, `last_page`:contentReference[oaicite:7]{index=7}.

---

## Dependencias

- [Reflex](https://reflex.dev) (antes Pynecone)
- `asyncio`, `threading`, `dataclasses`, `re`, `csv`
- Estructura de carpetas esperada:
  - `assets/filtro_preguntas/*.txt`
  - `assets/papers_encontrados/*.csv`
  - `assets/papers_filtrados/*.csv`

---

## Licencia

Este módulo forma parte del sistema PaperHound y está sujeto a la licencia de uso interna o de código abierto que se defina en el proyecto principal.
