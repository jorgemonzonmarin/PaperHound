import reflex as rx
from ..components.custom_table import DynamicTableState, generate_dynamic_table
from ..backend.sidebar_state import SidebarState

def viewer_content():
    return rx.box(
        rx.vstack(  
            rx.button("Ocultar/mostrar barra lateral", on_click=SidebarState.toggle_sidebar),
            rx.hstack(
                rx.button("⏮ First", on_click=DynamicTableState.first_page),
                rx.button("⬅ Prev", on_click=DynamicTableState.prev_page),
                rx.text(
                    rx.cond(
                        DynamicTableState.total_pages > 0,
                        f"Page {DynamicTableState.page_number} of {DynamicTableState.total_pages}",
                        "No data"
                    )
                ),
                rx.button("Next ➡", on_click=DynamicTableState.next_page),
                rx.button("Last ⏭", on_click=DynamicTableState.last_page),
                spacing="2",
            ),
            rx.box(
                generate_dynamic_table(),
                width="100%",
            ),
            rx.hstack(
                rx.button("⏮ First", on_click=DynamicTableState.first_page),
                rx.button("⬅ Prev", on_click=DynamicTableState.prev_page),
                rx.text(
                    rx.cond(
                        DynamicTableState.total_pages > 0,
                        f"Page {DynamicTableState.page_number} of {DynamicTableState.total_pages}",
                        "No data"
                    )
                ),
                rx.button("Next ➡", on_click=DynamicTableState.next_page),
                rx.button("Last ⏭", on_click=DynamicTableState.last_page),
                spacing="2",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            width="100%",
        ),
        width="100vw",
        padding="4",
    )
