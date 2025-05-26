import reflex as rx

class SidebarState(rx.State):
    """Estado global para controlar la visibilidad del sidebar."""
    show_sidebar: bool = True  # Inicialmente visible

    def toggle_sidebar(self):
        """Alterna la visibilidad del sidebar."""
        self.show_sidebar = not self.show_sidebar
