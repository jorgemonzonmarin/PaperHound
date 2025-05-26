import reflex as rx
import pandas as pd
from ..components.custom_table import DynamicTableState
from ..templates import template

from ..backend.table_state import DynamicTableState
from ..components.custom_table import generate_dynamic_table
from ..components.sidebar import SidebarState

@template(route="/csv_view", title="CSV Viewer", on_load=DynamicTableState.load_entries)
def csv_view() -> rx.Component:
    return rx.box(  # ✅ Usamos `box` en lugar de `container` para que use todo el ancho
        rx.vstack(
            rx.heading("📊 CSV Viewer", size="7"),
            sidebar_toggle_button(),
            rx.button("Reload Data", on_click=DynamicTableState.load_entries),
            
            rx.box(  # ✅ Asegurar que la tabla ocupa el ancho completo
                generate_dynamic_table(),
                width="100%",
            ),

            rx.hstack(
                rx.button("⏮ First", on_click=DynamicTableState.first_page),
                rx.button("⬅ Prev", on_click=DynamicTableState.prev_page),
                rx.text(f"Page {DynamicTableState.page_number} of {DynamicTableState.total_pages}"),
                rx.button("Next ➡", on_click=DynamicTableState.next_page),
                rx.button("Last ⏭", on_click=DynamicTableState.last_page),
                spacing="2",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            width="100%",  # ✅ Asegurar que el vstack ocupe todo el ancho
        ),
        width="100vw",  # ✅ Ocupar todo el ancho de la ventana
        padding="4",
    )

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
