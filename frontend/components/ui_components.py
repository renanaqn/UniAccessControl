import reflex as rx

def sidebar():
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.heading("UniAccessControl", size="6"),
                rx.badge(
                    rx.icon("shield_check", size=40),
                    color_scheme="cyan",
                    variant="soft",
                    radius="full",
                    padding="0.55rem",
                ),
                align="center"
            ),
            

            rx.divider(),

            rx.link(
                rx.button("Dashboard", width="100%"),
                href="/dashboard"
            ),

            rx.link(
                rx.button("Usuários", width="100%"),
                href="/usuarios"
            ),

            rx.link(
                rx.button("Zonas", width="100%"),
                href="/zonas"
            ),

            rx.link(
                rx.button("Logs", width="100%"),
                href="/logs"
            ),

            rx.link(
                rx.button("Simulador de Acesso", width="100%"),
                href="/simulador"
            ),

            spacing="4",
            align="stretch"
        ),

        width="250px",
        height="100vh",
        padding="1.5em",
        border_right="1px solid #ddd"
    )

def stat_card(titulo: str, valor: int):

    return rx.card(
        rx.vstack(
            rx.text(titulo),
            rx.heading(str(valor), size="8")
        ),
        width="220px"
    )