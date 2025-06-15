import os 
import sys
import reflex as rx

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from PaperHound.templates import template
from PaperHound.components.sidebar import SidebarState
from PaperHound.backend.table_state import DynamicTableState
from PaperHound.components.select_file import select_example3
from PaperHound.components.custom_table import DynamicTableState

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
