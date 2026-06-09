import reflex as rx

from components.layout import page_layout
from states.dashboard_state import DashboardState

def simulador_page():
    return page_layout(
        # deixa simulador no meio da tela
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading("Simulador de Leitor RFID", size="5", text_align="center"),
                    rx.text("Interface de testes do hardware da porta.", color="gray", margin_bottom="4"),
                    
                    # Painel Visor (Muda de cor dinamicamente)
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
                    
                    # Inputs do Sensor
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
                padding="6"
            ),
            width="100%",
            padding_top="10vh"
        )
    )