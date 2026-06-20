import reflex as rx

from states.dashboard_state import DashboardState
from components.layout import page_layout

def simulador_page():
    return rx.box(
        page_layout(
            rx.center(
                rx.vstack(
                    rx.card(
                        rx.vstack(
                            rx.heading("Porta Física", size="5", text_align="center"),
                            rx.text("Simulador de Leitura RFID", color="gray", margin_bottom="4", text_align="center"),
                            
                            rx.box(
                                rx.vstack(
                                    rx.heading(DashboardState.sim_status, size="6", color="white"),
                                    rx.text(DashboardState.sim_visor, color="white", size="3"),
                                    align_items="center",
                                    justify_content="center",
                                    text_align="center"
                                ),
                                bg=DashboardState.sim_cor_status,
                                padding="6",
                                border_radius="md",
                                width="100%",
                                margin_bottom="4"
                            ),
                            
                            rx.input(placeholder="ID da Zona (Ex: 1 - Lab Eletrônica)", value=DashboardState.sim_zona, on_change=DashboardState.set_sim_zona, size="3"),
                            rx.input(placeholder="Código Lido na Tag", value=DashboardState.sim_rfid, on_change=DashboardState.set_sim_rfid, size="3"),
                            
                            rx.button(
                                "Simular Passagem do Cartão", 
                                on_click=DashboardState.simular_leitura, 
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
        )
    )