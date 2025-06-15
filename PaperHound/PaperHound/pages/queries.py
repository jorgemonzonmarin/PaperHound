"""The settings page."""
import os
import sys
import reflex as rx

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from PaperHound.templates import template
from PaperHound.backend.query_state import QueryState  # Importar la clase de estado

@template(route="/queries", title="Queries")
def settings() -> rx.Component:
    """Página para agregar y gestionar preguntas."""

    return rx.vstack(
        rx.heading("Queries page", size="5"),
        
        rx.text(
            """
            Esta página te permite agregar y gestionar las queries o consultas que se utilizarán para realizar búsquedas bibliográficas de forma sistemática. 
            Estas queries están diseñadas para encontrar artículos relevantes mediante el uso de combinaciones de términos clave, sinónimos y operadores lógicos, 
            siguiendo las buenas prácticas de búsqueda académica en bases de datos como Scopus, Web of Science o IEEE Xplore. Las queries se componen de los siguientes elementos:
            """,
            margin_bottom="1px",
        ),
        rx.text("Operadores booleanos:", margin_bottom="1px"),
        rx.list.unordered(
            rx.list.item("AND: Requiere que todos los términos estén presentes. Restringe la búsqueda."),
            rx.list.item("OR: Acepta que cualquiera de los términos esté presente. Amplía la búsqueda."),
            rx.list.item("NOT: Excluye resultados que contengan un término específico. Se usa con precaución."),
            rx.list.item('Comillas " ": Encapsulan expresiones compuestas por varias palabras, garantizando que se busquen como frase exacta y no por separado.'),
            rx.list.item("Paréntesis (): Agrupan sinónimos o términos equivalentes para combinarse con otros bloques."),
        ),
        rx.text("Truncamientos y comodines:", margin_bottom="1px"),    
        rx.list.unordered(
            rx.list.item('*: Sustituye cualquier número de caracteres. Ej.: detect* recupera "detect", "detection", "detecting", etc.'),
            rx.list.item('?: Sustituye un solo carácter. Ej.: analy?e encuentra tanto "analyze" como "analyse".'),
        ),
        rx.text("Ejemplo explicado paso a paso", margin_bottom="1px"),
        rx.code(
            """
            ("foam detection" OR "bubble detection" OR "foam sensing") AND ("ultrasonic sensor" OR "ultrasound sensor")
            """
        ),
        rx.text("¿Qué hace esta query?", margin_bottom="1px"),
        rx.list.unordered(
            rx.list.item('"foam detection" OR "bubble detection" OR "foam sensing": Encuentra artículos que mencionan cualquiera de estas formas de referirse a la detección de espuma.'),
            rx.list.item('"ultrasonic sensor" OR "ultrasound sensor": Incluye dos formas comunes de referirse a sensores por ultrasonidos.'),
            rx.list.item('AND: Solo se devolverán resultados que contengan al menos un término de cada bloque.'),
        ),        
        rx.text("De esta forma, se asegura que los artículos estén relacionados tanto con sensores ultrasónicos como con la detección de espuma, sin importar la variación terminológica empleada por los autores.", margin_bottom="1px"),
        rx.text("Es posible introducir múltiples queries de forma simultanea separando cada una de ellas con un punto y coma (;) entre una y otra.", margin_bottom="1px"),

        # Contenedor horizontal para el campo de entrada y el botón
        rx.hstack(
            rx.input(
                placeholder="Introduce aquí tu query...",
                value=QueryState.input_value,  
                on_change=QueryState.set_input_value,  
                width="80%",  
            ),
            rx.button(
                "Añadir queries",
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
            border_radius="1px",  
        ),

        # Visualización del resultado final de preguntas (diseño diferenciado)
        rx.box(
            rx.text(QueryState.queries_text, size="4", color="gray"),  # ✅ Texto más tenue
            width="100%",  
            height="150px",  
            bg="#f5f5f5",  # ✅ Fondo gris claro
            padding="10px",
            margin_top="10px",
            border_radius="1px",  
            cursor="not-allowed",  # ✅ Bloquea interacción con el mouse
            border="1px solid #ccc",  
        ),

        spacing="7",
        width="100%",
    )
