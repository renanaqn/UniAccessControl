import reflex as rx

def stat_card(titulo: str, valor: int):

    return rx.card(
        rx.vstack(
            rx.text(titulo),
            rx.heading(str(valor), size="8")
        ),
        width="220px"
    )