"""Sidebar component for the app."""

import reflex as rx

from .. import styles
from ..backend.sidebar_state import SidebarState

def sidebar_header() -> rx.Component:
    """Sidebar header.

    Returns:
        The sidebar header component.

    """
    return rx.hstack(
        # The logo.
        rx.heading(
            "PaperHound",
            size="2",
            color=styles.accent_text_color,
            font_weight="bold",
            style={"text_transform": "uppercase"},
        ),
        rx.spacer(),
        align="center",
        width="100%",
        padding="0.35em",
        margin_bottom="1em",
    )

def sidebar_item_icon(icon: str) -> rx.Component:
    return rx.icon(icon, size=18)

def sidebar_item(text: str, url: str) -> rx.Component:
    """Sidebar item.

    Args:
        text: The text of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The sidebar item component.

    """
    # Whether the item is active.
    active = (rx.State.router.page.path == url.lower()) | (
        (rx.State.router.page.path == "/") & text == "Overview"
    )

    return rx.link(
        rx.hstack(
            rx.match(
                text,
                ("Queries", sidebar_item_icon("scan-search")),
                ("Ask about", sidebar_item_icon("message-circle-question")),
                ("Topic", sidebar_item_icon("album")),
                ("Search and process", sidebar_item_icon("circle-play")),
                ("Csv", sidebar_item_icon("settings")),
                sidebar_item_icon("layout-dashboard"),
            ),
            rx.text(text, size="3", weight="regular"),
            color=rx.cond(
                active,
                styles.accent_text_color,
                styles.text_color,
            ),
            style={
                "_hover": {
                    "background_color": rx.cond(
                        active,
                        styles.accent_bg_color,
                        styles.gray_bg_color,
                    ),
                    "color": rx.cond(
                        active,
                        styles.accent_text_color,
                        styles.text_color,
                    ),
                    "opacity": "1",
                },
                "opacity": rx.cond(
                    active,
                    "1",
                    "0.95",
                ),
            },
            align="center",
            border_radius=styles.border_radius,
            width="100%",
            spacing="2",
            padding="0.35em",
        ),
        underline="none",
        href=url,
        width="100%",
    )

def sidebar() -> rx.Component:
    """The sidebar with toggle functionality."""

    from reflex.page import get_decorated_pages

    # Lista de rutas en orden deseado
    ordered_page_routes = [
        "/",
        "/topic",
        "/csv-view",
        "/queries",
        "/questions",
        "/summary",
    ]

    pages = get_decorated_pages()

    ordered_pages = sorted(
        pages,
        key=lambda page: (
            ordered_page_routes.index(page["route"])
            if page["route"] in ordered_page_routes
            else len(ordered_page_routes)
        ),
    )

    return rx.box(
        rx.vstack(
            sidebar_header(),
            rx.vstack(
                *[
                    sidebar_item(
                        text=page.get("title", page["route"].strip("/").capitalize()),
                        url=page["route"],
                    )
                    for page in ordered_pages
                ],
                spacing="1",
                width="100%",
            ),
            rx.spacer(),
            #sidebar_footer(),
            justify="end",
            align="end",
            width="100%",
            height="100dvh",
            padding="1em",
        ),
        display=rx.cond(SidebarState.show_sidebar, "flex", "none"),  # 🔥 Controla la visibilidad
        max_width=styles.sidebar_width,
        width="auto",
        height="100%",
        position="sticky",
        justify="end",
        top="0px",
        left="0px",
        flex="1",
        bg=rx.color("gray", 2),
    )

