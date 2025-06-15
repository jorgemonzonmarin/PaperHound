import os
import sys
import reflex as rx

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from PaperHound.templates import template

@template(route="/", title="Inicio")
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.

    """
    return rx.hstack(
        # Columna izquierda con el texto
        rx.vstack(
            rx.heading("Introducción a PaperHound", size="5"),
            rx.text(
                """Paper Hound es una herramienta diseñada para facilitar la revisión sistemática de literatura científica. Permite a los usuarios buscar y filtrar artículos de manera eficiente.
    En primer lugar, es necesario introducir las queries que se van a emplear para la búsqueda de artículos. Son empleadas para buscar en las siguientes bases de datos: scopus, arXiv, 
    openalex, crossref, semantic y Google Scholar. A continuación, se debe introducir el topic de la revisión, que describe la temática en la que se centra la revisión bibliográfica. 
    Posteriormente, se deben agregar las preguntas que empleará DeepSeek para filtrar los artículos más relevantes relacionados con la temática del paper. Finalmente, Paper Hound 
    generará un resumen de los resultados obtenidos.""",
                size="4",
                margin_bottom="20px",
            ),
            width="60%",
            padding_right="5%",
        ),

        # Columna derecha con la imagen
        rx.image(
            src="/Logo.png",  # Esta es la ruta correcta dado que el archivo está en template_web/assets
            alt="Logo PaperHound",
            max_width="300px",
            height="auto",
            border_radius="10px",
            box_shadow="lg",
        ),

        width="100%",
        spacing="6",
        align="start",
    )


