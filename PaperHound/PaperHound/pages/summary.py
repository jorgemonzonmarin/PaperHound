import reflex as rx
from ..templates import template
from ..backend.questions_state import QuestionState
from ..backend.query_state import QueryState
from ..backend.topic_state import TopicState
from ..backend.processing_state import ProcessingState  # Importamos el estado de procesamiento

@template(route="/summary", title="Summary of Review")
def summary_page() -> rx.Component:
    """Página de resumen con Topic, Queries y Preguntas."""
    
    return rx.vstack(
        rx.heading("Summary of Review", size="5"),

        # 📌 Topic de la revisión
        rx.text("Topic de la revisión:", size="4", font_weight="bold", margin_top="20px"),
        rx.box(
            rx.text(TopicState.topic_text, size="4", color="gray"),  
            width="100%",
            height="100px",
            bg="#f5f5f5",
            padding="10px",
            border_radius="5px",
            border="1px solid #ccc",
            cursor="not-allowed",
        ),

        # 📌 Queries de búsqueda
        rx.text("Queries de búsqueda:", size="4", font_weight="bold", margin_top="20px"),
        rx.box(
            rx.text(QueryState.queries_text, size="4", color="gray"),
            width="100%",
            height="100px",
            bg="#f5f5f5",
            padding="10px",
            border_radius="5px",
            border="1px solid #ccc",
            cursor="not-allowed",
        ),

        # 📌 Preguntas de la revisión
        rx.text("Preguntas de la revisión:", size="4", font_weight="bold", margin_top="20px"),
        rx.box(
            rx.text(QuestionState.questions_text, size="4", color="gray"),
            width="100%",
            height="200px",
            bg="#f5f5f5",
            padding="10px",
            border_radius="5px",
            border="1px solid #ccc",
            cursor="not-allowed",
        ),

        # 🚀 Botón para ejecutar el procesamiento
        rx.button(
            "Start Processing",
            on_click=ProcessingState.start_processing,
            bg="blue",
            color="white",
            margin_top="20px",
        ),

        # 📢 Estado del procesamiento
        rx.text(
            ProcessingState.status,
            size="4",
            color="black",
            font_weight="bold",
            margin_top="10px",
        ),

        spacing="7",
        width="100%",
    )
