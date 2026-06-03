import reflex as rx

from components.sidebar import sidebar

def page_layout(*children):

    return rx.hstack(

        sidebar(),

        rx.box(
            *children,
            width="100%",
            padding="2em",
        ),

        width="100%",
        min_height="100vh",
    )