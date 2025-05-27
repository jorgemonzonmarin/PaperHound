"""The dashboard page."""

import reflex as rx

from ..backend.table_state import TableState
from ..templates import template
from ..views.table import main_table


@template(route="/", title="Inicio", on_load=TableState.load_entries)
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.

    """
    return rx.vstack(
        rx.heading("Introducción a PaperHound", size="5"),
        
        rx.text(
            """Paper Hound es una herramienta diseñada para facilitar la revisión sistemática de literatura científica. Permite a los usuarios buscar y filtrar articulos de manera eficiente.
            En primer lugar, es necesario introducir las queries que se van a emplear para la búsqueda de artículos. Son empleadas para buscar en las siguientes bases de datos: scopus, arXiv, 
            openalex, crossref, semantic y Google Scholar. A continuación, se debe introducir el topic de la revisión, que describe la temática en la que se centra la revisión bibliográfica. 
            Posteriormente, se deben agregar las preguntas que empleará DeepSeek para filtrar los articulos más relevantes relacionados con la temática del paper. Finalmente, Paper Hound 
            generará un resumen de los resultados obtenidos.
            """,
            size="4",
            margin_bottom="20px",
        ),
    )
