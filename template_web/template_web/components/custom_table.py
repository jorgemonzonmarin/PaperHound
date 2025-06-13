import reflex as rx
import pandas as pd
import re
from typing import List, Union
from ..backend.table_state import DynamicTableState

# Función para aplicar estilos condicionales a las celdas
def styled_cell(value: str) -> rx.Component:
    """Devuelve una celda con estilo basado en el valor"""
    color = rx.cond(
        value == "Yes", "green",
        value == "No", "red",
        value == "Not Determined", "orange",
        "black"  # Color por defecto
    )
    return rx.table.cell(value, color=color, font_weight="bold")

def _badge(status: str):
    """Genera un badge estilizado basado en el estado."""
    # Normalizar el valor eliminando espacios y asegurando formato uniforme
    status = re.sub(r"\s+", " ", str(status)).strip().replace(" ", "")  # 🔹 Convierte "  Not  Determined " a "NotDetermined"
     
    status_styles = {
        "Yes": {"icon": "✔️", "text": "Yes", "color": "green", "bg": "#ECFDF5", "border": "#10B981"},
        "NotDetermined": {"icon": "⚡", "text": "Not Determined", "color": "orange", "bg": "#FFFBEB", "border": "#F59E0B"},
        "No": {"icon": "🚫", "text": "No", "color": "red", "bg": "#FEF2F2", "border": "#EF4444"},
    }
   
    style = status_styles.get(status, {"icon": "❔", "text": f"{status}", "color": "gray", "bg": "#F3F4F6", "border": "#9CA3AF"})

    return rx.box(
        rx.text(f"{style['icon']} {style['text']}",
                style={"color": style["border"], "fontWeight": "bold"}),
        style={
            "display": "inline-flex",
            "alignItems": "center",
            "gap": "4px",
            "backgroundColor": style["bg"],
            "border": f"1px solid {style['border']}",
            "borderRadius": "16px",
            "padding": "4px 12px",
            "fontSize": "14px",
            "fontWeight": "bold"
        }
    )

def status_badge(status):
    """Aplica estilos dinámicos según el valor del status usando Reflex Match."""

    

    return rx.match(
        status,
        ("Yes", _badge("Yes")),
        ("NotDetermined", _badge("NotDetermined")),  # 🔹 Ajuste para que coincida con la normalización
        ("No", _badge("No")),
        _badge(f"{status}"),  # 🔹 Valor por defecto
    )

def generate_dynamic_table() -> rx.Component:
    """Genera una tabla dinámica basada en los datos del CSV."""

    return rx.box(  # Contenedor para expandir la tabla
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.foreach(
                        DynamicTableState.columns,
                        lambda col: rx.table.column_header_cell(
                            col,
                            style={
                                "textAlign": "left",
                                "whiteSpace": "normal",  # 🔹 Permitir salto de línea
                                "wordWrap": "break-word",  # 🔹 Romper palabras largas si es necesario
                                "maxWidth": "200px",  # 🔹 Ampliado a 170px
                                "overflow": "hidden",
                            },
                        ),
                    )
                ),
            ),
            rx.table.body(
                rx.foreach(
                    DynamicTableState.get_current_page,
                    lambda row: rx.table.row(
                        rx.foreach(
                            DynamicTableState.columns,
                            lambda col: rx.table.cell(
                                status_badge(row[col]),
                                style={
                                    "padding": "8px",
                                    "whiteSpace": "normal",  # 🔹 Permitir salto de línea
                                    "wordWrap": "break-word",  # 🔹 Romper palabras largas si es necesario
                                    "maxWidth": "200px",  # 🔹 Ampliado a 170px
                                    "overflow": "hidden",
                                },
                            ),
                        )
                    )
                )
            ),
            style={
                "width": "100%",  # Expande la tabla al ancho total
                "tableLayout": "auto",
                "borderCollapse": "collapse",
            },
        ),
        style={
            "width": "100%",  
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "stretch",
            "overflowX": "auto",
        }
    )
