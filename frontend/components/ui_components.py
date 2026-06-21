import reflex as rx

def sidebar():
    return rx.box(
        rx.vstack(
            # Header com logo
            rx.hstack(
                rx.icon("shield_check", size=24, color="white"),
                rx.heading("UniAccessControl", size="5", color="white"),
                align="center",
                spacing="3",
                width="100%"
            ),
            
            rx.divider(),

            # Menu Principal
            rx.vstack(
                rx.link(
                    rx.hstack(
                        rx.icon("home", size=18),
                        rx.text("Dashboard", color="white"),
                        align="center",
                        spacing="3",
                        padding="0.75rem",
                        border_radius="0.5rem",
                        _hover={"bg": "rgba(255,255,255,0.1)"},
                        width="100%",
                    ),
                    href="/dashboard",
                    _hover={"textDecoration": "none"},
                ),

                rx.link(
                    rx.hstack(
                        rx.icon("users", size=18),
                        rx.text("Usuários", color="white"),
                        align="center",
                        spacing="3",
                        padding="0.75rem",
                        border_radius="0.5rem",
                        _hover={"bg": "rgba(255,255,255,0.1)"},
                        width="100%",
                    ),
                    href="/usuarios",
                    _hover={"textDecoration": "none"},
                ),

                rx.link(
                    rx.hstack(
                        rx.icon("map-pin", size=18),
                        rx.text("Zonas", color="white"),
                        align="center",
                        spacing="3",
                        padding="0.75rem",
                        border_radius="0.5rem",
                        _hover={"bg": "rgba(255,255,255,0.1)"},
                        width="100%",
                    ),
                    href="/zonas",
                    _hover={"textDecoration": "none"},
                ),

                rx.link(
                    rx.hstack(
                        rx.icon("file-text", size=18),
                        rx.text("Logs (Auditoria)", color="white"),
                        align="center",
                        spacing="3",
                        padding="0.75rem",
                        border_radius="0.5rem",
                        _hover={"bg": "rgba(255,255,255,0.1)"},
                        width="100%",
                    ),
                    href="/logs",
                    _hover={"textDecoration": "none"},
                ),

                rx.link(
                    rx.hstack(
                        rx.icon("scan-line", size=18),
                        rx.text("Simulação de Acesso", color="white"),
                        align="center",
                        spacing="3",
                        padding="0.75rem",
                        border_radius="0.5rem",
                        _hover={"bg": "rgba(255,255,255,0.1)"},
                        width="100%",
                    ),
                    href="/simulador",
                    _hover={"textDecoration": "none"},
                ),

                spacing="2",
                width="100%",
                padding_top="2",
            ),

            rx.spacer(),

            # Configurações e Usuário
            rx.vstack(
                rx.divider(border_color="rgba(255,255,255,0.1)"),
                
                rx.link(
                    rx.hstack(
                        rx.icon("settings", size=18),
                        rx.text("Configurações", color="white"),
                        align="center",
                        spacing="3",
                        padding="0.75rem",
                        border_radius="0.5rem",
                        _hover={"bg": "rgba(255,255,255,0.1)"},
                        width="100%",
                    ),
                    href="#",
                    _hover={"textDecoration": "none"},
                ),

                rx.hstack(
                    rx.avatar(name="Admin", size="3"),
                    rx.vstack(
                        rx.text("Admin", size="2", weight="bold", color="white"),
                        rx.text("Administrador", size="1", color="rgba(255,255,255,0.7)"),
                        spacing="0",
                    ),
                    width="100%",
                    padding="0.75rem",
                ),

                spacing="2",
                width="100%",
                padding_top="2",
            ),

            spacing="0",
            align="stretch",
            width="100%",
            height="100%",
            padding="1.5em",
        ),

        width="250px",
        height="100vh",
        position="sticky",
        top=0,
        background="#1a3a52",  # Navy/Dark blue
        color="white",
        overflow_y="auto",
        flex_shrink="0",
        box_sizing="border-box",
    )

def stat_card(titulo: str, valor: int):

    return rx.card(
        rx.vstack(
            rx.text(titulo),
            rx.heading(str(valor), size="8")
        ),
        width="220px"
    )