import reflex as rx

from components.ui_components import sidebar
from states.auth_state import AuthState

def page_layout(*children):
    return rx.hstack(
        rx.cond(
            AuthState.is_authenticated,
            sidebar(),
            rx.box(display="none")
        ),

        rx.box(
            *children,
            width="100%",
            padding="2em",
        ),

        width="100%",
        min_height="100vh",
    )