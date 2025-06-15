import os
import sys
import reflex as rx

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from PaperHound.components.viewer_content import viewer_content
from PaperHound.components.custom_table import DynamicTableState

class SelectState3(rx.State):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    papers_path = os.path.join(current_dir, "..", "..", "assets", "papers_filtrados")
    values: list[str] = [ f for f in os.listdir(papers_path) if f.endswith(".csv")]


    value: str = values[0]
    show_content: bool = False  # ⬅ nueva variable

    @rx.event
    def change_value(self, value: str):
        self.value = value

    @rx.event
    def show_viewer(self):
        print(f"📂 Archivo seleccionado: {self.value}")
        self.show_content = True
        yield DynamicTableState.set_selected_file(self.value)
        yield DynamicTableState.load_entries()

def select_example3():
    return rx.vstack(
        rx.heading("📊 Resumen de artículos filtrados", size="7"),
        rx.select(
            SelectState3.values,
            value=SelectState3.value,
            on_change=SelectState3.set_value,
        ),
        rx.button(
            "Mostrar resultados",
            on_click=SelectState3.show_viewer,
        ),
        rx.cond(
            SelectState3.show_content,
            viewer_content(),
            rx.box(height="400px")  # ⬅ contenido en blanco por defecto
        ),
    )
 