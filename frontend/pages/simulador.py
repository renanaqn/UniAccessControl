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
            rx.heading(
                "Simulador de Acessos",
                size="7",
                margin_bottom="5",
            ),
            align="center",
            spacing="4",
        ),

        rx.text(
            "Simule leituras RFID e valide permissões de entrada em zonas controladas.",
            color="gray",
            margin_bottom="5",
        ),

        rx.divider(),

        width="100%",
        align="center",
        spacing="4",
        wrap="wrap",
    )

def simulacao():
    return rx.center(
        rx.vstack(
            rx.card(
                rx.vstack(
                    rx.heading("Porta Física", size="5", text_align="center"),
                    rx.text("Simulador de Leitura RFID", color="gray", margin_bottom="4", text_align="center"),
                    
                    rx.box(
                        rx.vstack(
                            rx.heading(SimuladorState.sim_status, size="6", color="white"),
                            rx.text(SimuladorState.sim_visor, color="white", size="3"),
                            align_items="center",
                            justify_content="center",
                            text_align="center"
                        ),
                        bg=SimuladorState.sim_cor_status,
                        padding="6",
                        border_radius="md",
                        width="100%",
                        margin_bottom="4"
                    ),
                    
                    rx.input(placeholder="ID da Zona (Ex: 1 - Lab Eletrônica)", value=SimuladorState.sim_zona, on_change=SimuladorState.set_sim_zona, size="3"),
                    rx.input(placeholder="Código Lido na Tag", value=SimuladorState.sim_rfid, on_change=SimuladorState.set_sim_rfid, size="3"),
                    
                    rx.button(
                        "Simular Passagem do Cartão", 
                        on_click=SimuladorState.simular_leitura, 
                        color_scheme="blue", 
                        size="3", 
                        width="100%", 
                        margin_top="2"
                    ),
                    width="100%",
                ),
                width="100%",
                max_width="450px",
                padding="6",
                box_shadow="lg"
            ),
            rx.link(
                rx.button("Acessar Painel Administrativo", variant="ghost", color_scheme="gray", margin_top="4"),
                href="/"
            ),
            align_items="center"
        ),
        width="100%",
        height="100vh",
        bg="rgba(0,0,0,0.2)"
    )

def simulador_page():
    return rx.box(
        page_layout(
            
            # =========================
            # Header
            # =========================
            
            simulador_header(),
            
            # =========================
            # Simulador
            # =========================
            
            simulacao(),
        )
    )