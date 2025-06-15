import reflex as rx

class SidebarState(rx.State):
    show_sidebar: bool = True

    def toggle_sidebar(self):
        self.show_sidebar = not self.show_sidebar

    def close_sidebar(self):
        self.show_sidebar = False
