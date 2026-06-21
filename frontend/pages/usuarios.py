import reflex as rx

from components.layout import page_layout
from states.usuarios_state import UsuariosState
from states.auth_state import AuthState

def usuarios_header():
    return rx.vstack(
        rx.hstack(
            rx.badge(
                rx.icon("users", size=36),
                color_scheme="green",
                variant="soft",
                radius="full",
                padding="0.65rem",
            ),
            rx.heading(
                "Gestão de Usuários", 
                size="7", 
                margin_bottom="5"
            ),
            align="center",
            spacing="4",
        ),
        
        rx.text(
            "Cadastre novos indivíduos, atualize credenciais perdidas ou revogue acessos.", 
            color="gray", 
            margin_bottom="5"
        ),
        rx.divider(),
        
        width="100%",
        align="center",
        spacing="4",
        wrap="wrap",
    )

def usuarios_page():
    return rx.box(
            page_layout(
                rx.vstack(
                    usuarios_header(),                    
                    rx.flex(
                        rx.card(
                            rx.heading("Novo Usuário", size="4", margin_bottom="4"),
                            rx.vstack(
                                rx.input(placeholder="Nome Completo", value=UsuariosState.novo_nome, on_change=UsuariosState.set_novo_nome),
                                rx.input(placeholder="Código da Tag RFID", value=UsuariosState.novo_rfid, on_change=UsuariosState.set_novo_rfid),
                                rx.input(placeholder="ID Perfil (1=Prof, 2=Aluno)", value=UsuariosState.novo_perfil_id, on_change=UsuariosState.set_novo_perfil_id),
                                rx.button("Cadastrar", on_click=UsuariosState.registrar_usuario, color_scheme="blue", width="100%"),
                                rx.text(UsuariosState.msg_cadastro, color="blue", size="2"),
                            ),
                            width="100%", max_width="350px"
                        ),
                        
                        rx.card(
                            rx.heading("Atualizar Credencial", size="4", margin_bottom="4"),
                            rx.vstack(
                                rx.input(placeholder="ID do Usuário", value=UsuariosState.update_id, on_change=UsuariosState.set_update_id),
                                rx.input(placeholder="Nova Tag RFID", value=UsuariosState.update_rfid, on_change=UsuariosState.set_update_rfid),
                                rx.button("Atualizar Tag", on_click=UsuariosState.atualizar_tag, color_scheme="orange", width="100%"),
                                rx.text(UsuariosState.msg_update, color="orange", size="2"),
                            ),
                            width="100%", max_width="350px"
                        ),
                        
                        rx.card(
                            rx.heading("Revogar Acesso", size="4", margin_bottom="4"),
                            rx.vstack(
                                rx.input(placeholder="ID a remover", value=UsuariosState.delete_id, on_change=UsuariosState.set_delete_id),
                                rx.button("Remover do Sistema", on_click=UsuariosState.remover_usuario, color_scheme="red", width="100%"),
                                rx.text(UsuariosState.msg_delete, color="red", size="2"),
                            ),
                            width="100%", max_width="350px"
                        ),
                        spacing="5",
                        wrap="wrap",
                        width="100%"
                    ),
                    width="100%"
                )
            )
    )
