import reflex as rx

from states.simulador_state import SimuladorState
from components.layout import page_layout


def simulador_header():
    return rx.vstack(
        rx.hstack(
            rx.badge(
                rx.icon("scan-line", size=36),
                color_scheme="blue",
                variant="soft",
                radius="full",
                padding="0.65rem",
            ),
            rx.vstack(
                rx.heading(
                    "Simulador de Acessos",
                    size="7",
                ),
                rx.text(
                    "Simule leituras RFID e valide permissões de entrada em zonas controladas.",
                    color_scheme="gray",
                    size="3",
                ),
                spacing="1",
                align="start",
            ),
            align="center",
            spacing="4",
        ),

        rx.divider(),

        width="100%",
        align="start",
        spacing="4",
    )


def status_porta_card():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon("door-open", size=20),
                    color_scheme="blue",
                    variant="soft",
                    radius="full",
                    padding="0.55rem",
                ),
                rx.vstack(
                    rx.heading("Porta Física", size="5"),
                    rx.text(
                        "Estado atual da tentativa de acesso.",
                        size="2",
                        color_scheme="gray",
                    ),
                    spacing="0",
                    align="start",
                ),
                width="100%",
                align="center",
                spacing="3",
            ),

            rx.divider(),

            rx.box(
                rx.vstack(
                    rx.badge(
                        SimuladorState.sim_status,
                        color_scheme=SimuladorState.sim_cor_status,
                        variant="solid",
                        size="3",
                    ),

                    rx.icon(
                        "radio-tower",
                        size=54,
                        color="white",
                    ),

                    rx.text(
                        SimuladorState.sim_visor,
                        color="white",
                        size="4",
                        weight="medium",
                        text_align="center",
                        max_width="320px",
                    ),

                    spacing="4",
                    align="center",
                    justify="center",
                    min_height="230px",
                ),
                width="100%",
                border_radius="1rem",
                padding="2rem",
                background=(
                    f"linear-gradient(135deg, "
                    f"var(--{SimuladorState.sim_cor_status}-9), "
                    f"var(--{SimuladorState.sim_cor_status}-11))"
                ),
                box_shadow="0 16px 40px rgba(0, 0, 0, 0.18)",
            ),

            rx.hstack(
                rx.badge(
                    rx.icon("shield-check", size=14),
                    "Validação em tempo real",
                    color_scheme="blue",
                    variant="soft",
                ),
                rx.badge(
                    rx.icon("database", size=14),
                    "Registro no banco",
                    color_scheme="gray",
                    variant="soft",
                ),
                spacing="2",
                wrap="wrap",
            ),

            width="100%",
            spacing="4",
        ),
        width="100%",
        min_width="320px",
        flex="1",
        variant="surface",
    )


def campo_simulador(label: str, placeholder: str, value, on_change, icon: str):
    return rx.vstack(
        rx.text(
            label,
            size="2",
            weight="medium",
            color_scheme="gray",
        ),
        rx.input(
            rx.input.slot(
                rx.icon(icon, size=16),
            ),
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            width="100%",
            size="3",
        ),
        width="100%",
        align="start",
        spacing="1",
    )


def formulario_simulador_card():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon("badge-check", size=20),
                    color_scheme="blue",
                    variant="soft",
                    radius="full",
                    padding="0.55rem",
                ),
                rx.vstack(
                    rx.heading("Leitura RFID", size="5"),
                    rx.text(
                        "Informe a zona e o código da tag para simular uma passagem.",
                        size="2",
                        color_scheme="gray",
                    ),
                    spacing="0",
                    align="start",
                ),
                width="100%",
                align="center",
                spacing="3",
            ),

            rx.divider(),

            campo_simulador(
                label="Zona de acesso",
                placeholder="Ex: 1",
                value=SimuladorState.sim_zona,
                on_change=SimuladorState.set_sim_zona,
                icon="map-pin",
            ),

            campo_simulador(
                label="Tag RFID",
                placeholder="Ex: A1B2C3D4",
                value=SimuladorState.sim_rfid,
                on_change=SimuladorState.set_sim_rfid,
                icon="scan-line",
            ),

            rx.button(
                rx.icon("send", size=16),
                "Simular passagem do cartão",
                on_click=SimuladorState.simular_leitura,
                color_scheme="blue",
                size="3",
                width="100%",
                margin_top="0.5rem",
            ),

            rx.callout(
                "A tentativa será validada com base nas regras cadastradas para a zona e o perfil do usuário.",
                icon="info",
                color_scheme="blue",
                variant="soft",
                width="100%",
            ),

            width="100%",
            spacing="4",
        ),
        width="100%",
        min_width="320px",
        max_width="480px",
        flex="1",
        variant="surface",
    )


def simulacao():
    return rx.flex(
        status_porta_card(),
        formulario_simulador_card(),

        width="100%",
        spacing="5",
        wrap="wrap",
        align="stretch",
    )


def simulador_page():
    return rx.box(
        page_layout(
            rx.vstack(
                
                # =========================
                # Header
                # =========================
                
                simulador_header(),
                
                # =========================
                # Simulador
                # =========================
                
                simulacao(),

                width="100%",
                spacing="6",
                align="start",
            )
        )
    )