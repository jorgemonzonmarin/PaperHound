# PaperHound UI – Componentes Visuales en Reflex

Este módulo define la interfaz visual de la aplicación **PaperHound**, centrada en el análisis y filtrado de artículos científicos. Está diseñada con [Reflex](https://reflex.dev), integrando navegación, visualización de datos tabulares y control de flujo desde la UI.

---

## Índice de Componentes

### `sidebar.py`
Contiene la barra lateral izquierda que permite navegar entre secciones clave del proyecto.

- **Funciones**:
  - `sidebar()`: Genera el contenedor con botones de navegación y visibilidad condicional.
  - `sidebar_item()`: Crea un ítem clicable con íconos dinámicos según el texto.
  - `sidebar_header()`: Encabezado con el título de la aplicación:contentReference[oaicite:0]{index=0}.

---

### `navbar.py`
Barra superior con menú tipo *drawer* para pantallas pequeñas.

- **Funciones**:
  - `navbar()`: Define la barra superior completa.
  - `menu_button()`: Genera menú dinámico con enlaces a todas las páginas registradas.
  - `menu_item()`: Componente para cada opción del menú.
  - `navbar_footer()`: Enlaces adicionales (Docs, Blog) y botón de modo oscuro:contentReference[oaicite:1]{index=1}.

---

### `status_badge.py`
Componente visual reutilizable para mostrar un badge de estado.

- **Funciones**:
  - `_badge(status)`: Mapea el estado (`Completed`, `Pending`, `Canceled`) a color e ícono.
  - `status_badge(status)`: Usa `rx.match` para retornar el componente adecuado según el estado:contentReference[oaicite:2]{index=2}.

---

### `custom_table.py`
Componente que renderiza una tabla dinámica con colores e íconos según valores (`Yes`, `No`, `Not Determined`).

- **Funciones**:
  - `generate_dynamic_table()`: Construye tabla basada en `DynamicTableState`, con encabezados y celdas estilizadas.
  - `status_badge(status)`: Aplica estilos visuales semánticos a cada celda según su valor.
  - `styled_cell(value)`: Alternativa para aplicar estilos directos (no utilizada directamente aquí):contentReference[oaicite:3]{index=3}.

---

### `viewer_content.py`
Define el área central de visualización de artículos filtrados en formato tabla, con botones de paginación.

- **Funciones**:
  - `viewer_content()`: Componente completo que combina el selector de página y la tabla dinámica. Integra navegación por páginas y toggle del sidebar:contentReference[oaicite:4]{index=4}.

---

### `select_file.py`
Permite al usuario seleccionar un archivo CSV con resultados filtrados y visualizarlo dinámicamente.

- **Clases**:
  - `SelectState3`: 
    - `values`: Lista de archivos `.csv` en `assets/papers_filtrados`.
    - `show_viewer()`: Activa la visualización y carga la tabla correspondiente.
  - **Componente**:
    - `select_example3()`: Renderiza el dropdown, botón de mostrar y el contenido dinámico:contentReference[oaicite:5]{index=5}.

---

## Estilo y Convenciones

- Todos los componentes están diseñados con enfoque responsivo y minimalista.
- Se emplea una estructura modular con separación entre lógica (`State`) y visual (`Component`).
- Se usan íconos y colores personalizados para mejorar la semántica visual.

---

## Dependencias

- Reflex >= 0.4.0
- Archivos de datos `.csv` generados por el backend (`papers_filtrados`)
- Definiciones de estilo importadas desde `PaperHound.styles` (no incluidas aquí)
