import reflex as rx

from components.layout import page_layout
from components.stat_card import stat_card
from components.log_table import log_table

from states.dashboard_state import DashboardState
from states.auth_state import AuthState 

def mostrar_zona(zona: dict):
    return rx.text(
        f"ID {zona['id']} - {zona['nome_zona']}", 
        margin_bottom="2", 
        size="2" 
    )

def mostrar_perfil (perfil: dict):
    return rx.text(
        f"ID {perfil['id']} - {perfil['nome_perfil']}", 
        margin_bottom="2", 
        size="2"
    )

def zonas_page():
    return rx.box(
        page_layout(
            rx.vstack(
                rx.heading("Zonas e Permissões", size="7", margin_bottom="5"),
                rx.text("Defina as regras de controle de acesso para as zonas.", color="gray", margin_bottom="5"),
                
                rx.flex(
                    rx.card(
                        rx.heading("Controle de Regras de Horário", size="4", margin_bottom="2"),
                        rx.text("Dica: Inserir uma regra existente atualizará os seus horários.", size="2", color="gray", margin_bottom="4"),
                        rx.vstack(
                            rx.input(placeholder="ID do Perfil (Ex: 1 - Prof)", value=DashboardState.regra_perfil_id, on_change=DashboardState.set_regra_perfil),
                            rx.input(placeholder="ID da Zona (Ex: 10 - Lab)", value=DashboardState.regra_zona_id, on_change=DashboardState.set_regra_zona),
                            rx.flex(
                                rx.input(placeholder="Início (HH:MM:SS)", value=DashboardState.regra_inicio, on_change=DashboardState.set_regra_inicio),
                                rx.input(placeholder="Fim (HH:MM:SS)", value=DashboardState.regra_fim, on_change=DashboardState.set_regra_fim),
                                spacing="2", width="100%"
                            ),
                            rx.button("Salvar Regra de Acesso", on_click=DashboardState.salvar_regra, color_scheme="indigo", width="100%"),
                            rx.text(DashboardState.msg_regra, color="indigo", size="2"),
                        ),
                        width="100%", max_width="450px"
                    ),
                    
                    rx.card(
                        rx.heading("Zonas Cadastradas", size="4", margin_bottom="4"),
                        rx.vstack(
                            # Puxa a função 'mostrar_zona' para cada item na lista do DB
                            rx.foreach(DashboardState.zonas_lista, mostrar_zona),
                            align_items="start"
                        ),
                        width="100%", max_width="250px", bg="rgba(0,0,0,0.1)"
                    ),

                    rx.card(
                        rx.heading("Perfis Existentes", size="4", margin_bottom="4"),
                        rx.vstack(
                            # Puxa a função 'mostrar_perfil' para cada item na lista do DB
                            rx.foreach(DashboardState.perfis_lista, mostrar_perfil),
                            align_items="start"
                        ),
                        width="100%", max_width="250px", bg="rgba(0,0,0,0.1)"
                    ),
                    
                    spacing="5",
                    wrap="wrap",
                    width="100%",
                    align_items="stretch"

                ),
                width="100%"
            )
        ),
        on_mount=AuthState.verificar_acesso
    )

