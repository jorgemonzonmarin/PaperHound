"""The settings page."""

import reflex as rx

from ..templates import template
from ..views.color_picker import primary_color_picker, secondary_color_picker
from ..views.radius_picker import radius_picker
from ..views.scaling_picker import scaling_picker
from ..backend.query_state import QueryState  # Importar la clase de estado

@template(route="/queries", title="Queries")
def settings() -> rx.Component:
    """Página para agregar y gestionar preguntas."""

    return rx.vstack(
        rx.heading("Queries page", size="5"),
        
        rx.text(
            "Esta página te permite agregar y gestionar las queries que se van a emplear para la búsqueda de articulos.",
            size="4",
            margin_bottom="20px",
        ),

        # Contenedor horizontal para el campo de entrada y el botón
        rx.hstack(
            rx.input(
                placeholder="Introduce aquí tu query...",
                value=QueryState.input_value,  
                on_change=QueryState.set_input_value,  
                width="80%",  
            ),
            rx.button(
                "Añadir pregunta",
                on_click=QueryState.add_question,  
                bg="blue",
                color="white",
                width="20%",  
            ),
            width="100%",  
            align="end",  
        ),

        # Texto para separar visualmente
        rx.text("Queries introducidas hasta el momento:", size="4", margin_top="20px", font_weight="bold"),

        # Lista de preguntas agregadas con log
        rx.vstack(
            rx.foreach(QueryState.queries, lambda q, idx: rx.hstack(
                rx.text(q, size="4", width="90%"),  
                rx.button(
                    "X",
                    on_click=lambda idx=idx: QueryState.remove_question(idx),
                    bg="red",
                    color="white"
                ),
                align="center",
            )),
            spacing="4",
            width="100%",
            border="1px solid #ddd",  
            padding="10px",
            border_radius="5px",  
        ),

        # Visualización del resultado final de preguntas (diseño diferenciado)
        rx.box(
            rx.text(QueryState.queries_text, size="4", color="gray"),  # ✅ Texto más tenue
            width="100%",  
            height="150px",  
            bg="#f5f5f5",  # ✅ Fondo gris claro
            padding="10px",
            margin_top="10px",
            border_radius="5px",  
            cursor="not-allowed",  # ✅ Bloquea interacción con el mouse
            border="1px solid #ccc",  
        ),

        spacing="7",
        width="100%",
    )
