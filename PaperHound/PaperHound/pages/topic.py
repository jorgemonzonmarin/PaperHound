"""The settings page."""
import os
import sys
import reflex as rx

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from PaperHound.templates import template
from PaperHound.backend.topic_state import TopicState  # Importar la clase de estado

@template(route="/topic", title="Topic")
def settings() -> rx.Component:
    """Página para agregar y gestionar preguntas."""

    return rx.vstack(
        rx.heading("Topic page", size="5"),
        
        rx.text(
            "A la hora de analizar y filtrar los papers encontrados, es necesario describir la temática en la que se centra la revisión bibliográfica. Esto se lleva a cabo mediante el topic. Introduce el topic en ingles a continuación.",
            size="4",
            margin_bottom="20px",
        ),

        # Contenedor horizontal para el campo de entrada y el botón
        rx.hstack(
            rx.input(
                placeholder="Enter your topic here...",
                value=TopicState.input_value,  
                on_change=TopicState.set_input_value,  
                width="80%",  
            ),
            rx.button(
                "Añadir topic",
                on_click=TopicState.add_question,  
                bg="blue",
                color="white",
                width="20%",  
            ),
            width="100%",  
            align="end",  
        ),

        # Texto para separar visualmente
        rx.text("Topic introducido:", size="4", margin_top="20px", font_weight="bold"),

        # Lista de preguntas agregadas con log
        rx.vstack(
            rx.foreach(TopicState.topic, lambda q, idx: rx.hstack(
                rx.text(q, size="4", width="90%"),  
                rx.button(
                    "X",
                    on_click=lambda idx=idx: TopicState.remove_question(idx),
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
            rx.text(TopicState.topic_text, size="4", color="gray"),  # ✅ Texto más tenue
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
