import os
import sys
import reflex as rx

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from PaperHound.templates import template
from PaperHound.backend.questions_state import QuestionState  # Importar la clase de estado

@template(route="/questions", title="Questions")
def settings() -> rx.Component:
    """Página para agregar y gestionar preguntas."""

    return rx.vstack(
        rx.heading("Questions page", size="5"),
        
        rx.text(
            """
            Las preguntas introducidas aquí servirán para filtrar los papers encontrados. Realiza preguntas cuya respuesta sea si/no en inglés. 
            DeepSeek se encargará de responderlas y almacenar los resultados. Al igual que en la página de queries,
            puedes introducir múltiples preguntas separándolas con punto y coma (;). Es importante que las preguntas aparezcan numeradas para identificarlas más adelante. Si la pregunta no esta numerada será ignorada. No te preocupes por el orden, las preguntas se ordenarán automáticamente.
            """,
            size="4",
        ),

        # Contenedor horizontal para el campo de entrada y el botón
        rx.hstack(
            rx.input(
                placeholder="Introduce aquí tu pregunta numerada",
                value=QuestionState.input_value,  
                on_change=QuestionState.set_input_value,  
                width="80%",  
            ),
            rx.button(
                "Add Question",
                on_click=QuestionState.add_question,  
                bg="blue",
                color="white",
                width="20%",  
            ),
            width="100%",  
            align="end",  
        ),
        
        rx.text(
            """
            Además de introducir las preguntas manualmente, puedes cargarlas desde un fichero *.txt que contenga las preguntas numeradas en cada línea. Para hacerlo, elige el fichero que quieres cargar y pulsa el botón "Cargar preguntas".
            """,
            size="4",
        ),
        
        rx.hstack(
            rx.select(
                QuestionState.file_options,
                placeholder="Selecciona un archivo de la carpeta filtro_preguntas",
                on_change=QuestionState.set_selected_file,
                width="70%",
            ),
            rx.button(
                "Cargar preguntas",
                on_click=QuestionState.load_questions_from_selected_file,
                bg="green",
                color="white",
                width="30%",
            ),
            width="100%",
        ),

        rx.button("Recargar lista de archivos", on_click=QuestionState.load_file_options),

        # Texto para separar visualmente
        rx.text("Preguntas introducidas hasta el momento:", size="4", margin_top="20px", font_weight="bold"),

        # Lista de preguntas agregadas con log
        rx.vstack(
            rx.foreach(QuestionState.questions, lambda q, idx: rx.hstack(
                rx.text(q, size="4", width="90%"),  
                rx.button(
                    "X",
                    on_click=lambda idx=idx: QuestionState.remove_question(idx),
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
            rx.text(QuestionState.questions_text, size="4", color="gray"),  # ✅ Texto más tenue
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
