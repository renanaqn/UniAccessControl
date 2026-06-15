import reflex as rx

from components.layout import page_layout
from components.stat_card import stat_card
from components.log_table import log_table

from states.dashboard_state import DashboardState
from states.auth_state import AuthState

def usuarios_page():
    return rx.box(
            page_layout(
                rx.vstack(
                    rx.heading("Gestão de Usuários", size="7", margin_bottom="5"),
                    rx.text("Cadastre novos indivíduos, atualize credenciais perdidas ou revogue acessos.", color="gray", margin_bottom="5"),
                    
                    rx.flex(
                        rx.card(
                            rx.heading("Novo Usuário", size="4", margin_bottom="4"),
                            rx.vstack(
                                rx.input(placeholder="Nome Completo", value=DashboardState.novo_nome, on_change=DashboardState.set_novo_nome),
                                rx.input(placeholder="Código da Tag RFID", value=DashboardState.novo_rfid, on_change=DashboardState.set_novo_rfid),
                                rx.input(placeholder="ID Perfil (1=Prof, 2=Aluno)", value=DashboardState.novo_perfil_id, on_change=DashboardState.set_novo_perfil_id),
                                rx.button("Cadastrar", on_click=DashboardState.registrar_usuario, color_scheme="blue", width="100%"),
                                rx.text(DashboardState.msg_cadastro, color="blue", size="2"),
                            ),
                            width="100%", max_width="350px"
                        ),
                        
                        rx.card(
                            rx.heading("Atualizar Credencial", size="4", margin_bottom="4"),
                            rx.vstack(
                                rx.input(placeholder="ID do Usuário", value=DashboardState.update_id, on_change=DashboardState.set_update_id),
                                rx.input(placeholder="Nova Tag RFID", value=DashboardState.update_rfid, on_change=DashboardState.set_update_rfid),
                                rx.button("Atualizar Tag", on_click=DashboardState.atualizar_tag, color_scheme="orange", width="100%"),
                                rx.text(DashboardState.msg_update, color="orange", size="2"),
                            ),
                            width="100%", max_width="350px"
                        ),
                        
                        rx.card(
                            rx.heading("Revogar Acesso", size="4", margin_bottom="4"),
                            rx.vstack(
                                rx.input(placeholder="ID a remover", value=DashboardState.delete_id, on_change=DashboardState.set_delete_id),
                                rx.button("Remover do Sistema", on_click=DashboardState.remover_usuario, color_scheme="red", width="100%"),
                                rx.text(DashboardState.msg_delete, color="red", size="2"),
                            ),
                            width="100%", max_width="350px"
                        ),
                        spacing="5",
                        wrap="wrap",
                        width="100%"
                    ),
                    width="100%"
                )
            ),
        on_mount=AuthState.verificar_acesso
    )
