import reflex as rx
import pandas as pd
from ..components.custom_table import DynamicTableState
from ..templates import template

from ..backend.table_state import DynamicTableState
from ..components.custom_table import generate_dynamic_table
from ..components.sidebar import SidebarState

from ..components.select_file import select_example3

@template(route="/csv_view", title="CSV Viewer", on_load=DynamicTableState.load_entries)
def csv_view() -> rx.Component:
    
    return select_example3()

def sidebar_toggle_button() -> rx.Component:
    """Botón para mostrar/ocultar la barra lateral."""
    return rx.button(
        rx.icon("menu"),  # Icono tipo "hamburguesa"
        on_click=SidebarState.toggle_sidebar,  # 🔥 Alternar sidebar al hacer clic
        position="fixed",
        top="1em",
        left="1em",
        z_index="1000",  # Asegura que esté por encima de otros elementos
        bg="gray.700",
        color="white",
        border_radius="md",
        padding="0.5em",
        box_shadow="md",
    )
