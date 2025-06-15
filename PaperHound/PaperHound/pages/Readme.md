# PaperHound UI – Páginas de Usuario

Este módulo define las distintas páginas navegables de la aplicación **PaperHound**, organizadas en torno al flujo de una revisión sistemática: desde la introducción de queries y tópicos hasta el procesamiento y visualización de resultados en formato tabla.

---

## Índice de Páginas

### `dashboard.py`
Página de inicio de la aplicación.

- **Ruta**: `/`
- **Descripción**:
  Introduce el propósito de PaperHound, su funcionamiento general y cómo interactúan las diferentes etapas del sistema (queries → topic → preguntas → procesamiento).
- **Componentes**:
  - Encabezado, texto introductorio y logo visual:contentReference[oaicite:0]{index=0}.

---

### `queries.py`
Gestor visual para introducir queries de búsqueda.

- **Ruta**: `/queries`
- **Funcionalidad**:
  - Añadir queries compuestas usando operadores booleanos (AND, OR, NOT).
  - Visualizar y eliminar queries introducidas.
  - Explicación detallada de cómo estructurar una query académica.
- **Estado vinculado**: `QueryState`:contentReference[oaicite:1]{index=1}.

---

### `topic.py`
Permite al usuario definir el **tópico** de revisión bibliográfica.

- **Ruta**: `/topic`
- **Funcionalidad**:
  - Entrada de texto para definir el tema central de la revisión.
  - Eliminación, visualización y mantenimiento del estado.
- **Estado vinculado**: `TopicState`:contentReference[oaicite:2]{index=2}.

---

### `questions.py`
Gestión de las preguntas de evaluación (usadas por LLM para filtrar papers).

- **Ruta**: `/questions`
- **Funcionalidad**:
  - Entrada de preguntas tipo sí/no numeradas.
  - Soporte para carga desde ficheros `.txt` o `.csv` en `assets/filtro_preguntas`.
  - Visualización de la lista cargada y campo de vista previa final.
- **Estado vinculado**: `QuestionState`:contentReference[oaicite:3]{index=3}.

---

### `summary.py`
Resumen final de revisión antes de iniciar el procesamiento.

- **Ruta**: `/summary`
- **Componentes**:
  - Visualización de:
    - Tópico
    - Queries
    - Preguntas
  - Botón de inicio para ejecutar la búsqueda, análisis y filtrado.
  - Texto de estado dinámico con la fase actual (Processing, Completed, etc).
- **Estado vinculado**: `TopicState`, `QueryState`, `QuestionState`, `ProcessingState`:contentReference[oaicite:4]{index=4}.

---

### `csv_view.py`
Visualizador interactivo de resultados filtrados.

- **Ruta**: `/csv_view`
- **Componentes**:
  - Selector de archivo `.csv` desde `assets/papers_filtrados`.
  - Botón para cargar tabla.
  - Tabla interactiva con paginación, filtros y colores por respuesta.
- **Estado vinculado**: `DynamicTableState`
- **Componente usado**: `select_example3()` de `select_file.py`:contentReference[oaicite:5]{index=5}.

---

## Flujo Completo del Usuario

```text
1. Dashboard (/)
2. Queries (/queries)
3. Topic (/topic)
4. Questions (/questions)
5. Summary (/summary)
6. Visualización (/csv_view)
