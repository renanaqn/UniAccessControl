import reflex as rx

from components.layout import page_layout
from states.usuarios_state import UsuariosState
from states.auth_state import AuthState


def usuarios_header():
    return rx.vstack(
        rx.hstack(
            rx.hstack(
                rx.badge(
                    rx.icon("users", size=36),
                    color_scheme="green",
                    variant="soft",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.heading(
                        "Gestão de Usuários",
                        size="7",
                    ),
                    rx.text(
                        "Cadastre usuários, atualize credenciais RFID e revogue acessos quando necessário.",
                        color_scheme="gray",
                        size="3",
                    ),
                    spacing="1",
                    align="start",
                ),
                align="center",
                spacing="4",
            ),
            
            rx.spacer(),
            rx.link(
                rx.button(
                    rx.icon("table", size=16),
                    "Ver usuários cadastradas",
                    variant="soft",
                    color_scheme="purple",
                ),
                href="/usuarios/lista",
            ),
            
            width="100%",
            align="center",
            spacing="4",
            wrap="wrap",
        ),
        
        rx.divider(),

        width="100%",
        align="start",
        spacing="4",
    )


def form_field(label: str, placeholder: str, value, on_change, icon: str, input_type: str = "text"):
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
            type=input_type,
            width="100%",
            size="3",
        ),
        width="100%",
        spacing="1",
        align="start",
    )


def feedback_message(message, color_scheme: str):
    return rx.cond(
        message != "",
        rx.callout(
            message,
            icon="info",
            color_scheme=color_scheme,
            variant="soft",
            width="100%",
            margin_top="0.5rem",
        ),
        rx.fragment(),
    )


def usuario_action_card(
    titulo: str,
    subtitulo: str,
    icon: str,
    color_scheme: str,
    children,
):
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(icon, size=20),
                    color_scheme=color_scheme,
                    variant="soft",
                    radius="full",
                    padding="0.55rem",
                ),
                rx.vstack(
                    rx.heading(titulo, size="4"),
                    rx.text(
                        subtitulo,
                        size="2",
                        color_scheme="gray",
                    ),
                    spacing="0",
                    align="start",
                ),
                align="center",
                spacing="3",
                width="100%",
            ),

            rx.divider(),

            children,

            width="100%",
            spacing="4",
        ),
        width="100%",
        min_width="280px",
        max_width="380px",
        flex="1",
        variant="surface",
    )


def novo_usuario():
    return usuario_action_card(
        titulo="Novo Usuário",
        subtitulo="Cadastre uma nova pessoa no sistema.",
        icon="user-plus",
        color_scheme="blue",
        children=rx.vstack(
            form_field(
                label="Nome completo",
                placeholder="Ex: João Silva",
                value=UsuariosState.novo_nome,
                on_change=UsuariosState.set_novo_nome,
                icon="user",
            ),

            form_field(
                label="Tag RFID",
                placeholder="Ex: A1B2C3D4",
                value=UsuariosState.novo_rfid,
                on_change=UsuariosState.set_novo_rfid,
                icon="badge",
            ),

            form_field(
                label="Perfil",
                placeholder="ID do perfil, ex: 1",
                value=UsuariosState.novo_perfil_id,
                on_change=UsuariosState.set_novo_perfil_id,
                icon="shield-check",
            ),

            rx.button(
                rx.icon("plus", size=16),
                "Cadastrar usuário",
                on_click=UsuariosState.registrar_usuario,
                color_scheme="blue",
                width="100%",
                size="3",
            ),

            feedback_message(
                UsuariosState.msg_cadastro,
                "blue",
            ),

            width="100%",
            spacing="3",
        ),
    )


def atualizar_credencial():
    return usuario_action_card(
        titulo="Atualizar Credencial",
        subtitulo="Substitua uma tag RFID perdida ou danificada.",
        icon="refresh-cw",
        color_scheme="orange",
        children=rx.vstack(
            form_field(
                label="ID do usuário",
                placeholder="Ex: 12",
                value=UsuariosState.update_id,
                on_change=UsuariosState.set_update_id,
                icon="hash",
            ),

            form_field(
                label="Nova tag RFID",
                placeholder="Ex: D4C3B2A1",
                value=UsuariosState.update_rfid,
                on_change=UsuariosState.set_update_rfid,
                icon="badge",
            ),

            rx.button(
                rx.icon("refresh-cw", size=16),
                "Atualizar tag",
                on_click=UsuariosState.atualizar_tag,
                color_scheme="orange",
                width="100%",
                size="3",
            ),

            feedback_message(
                UsuariosState.msg_update,
                "orange",
            ),

            width="100%",
            spacing="3",
        ),
    )


def revogar_acesso():
    return usuario_action_card(
        titulo="Revogar Acesso",
        subtitulo="Remova um usuário do sistema de controle.",
        icon="user-x",
        color_scheme="red",
        children=rx.vstack(
            rx.callout(
                "Essa ação remove o usuário cadastrado. Confirme o ID antes de continuar.",
                icon="triangle-alert",
                color_scheme="red",
                variant="soft",
                width="100%",
            ),

            form_field(
                label="ID do usuário",
                placeholder="Ex: 12",
                value=UsuariosState.delete_id,
                on_change=UsuariosState.set_delete_id,
                icon="hash",
            ),

            rx.button(
                rx.icon("trash-2", size=16),
                "Remover usuário",
                on_click=UsuariosState.remover_usuario,
                color_scheme="red",
                width="100%",
                size="3",
            ),

            feedback_message(
                UsuariosState.msg_delete,
                "red",
            ),

            width="100%",
            spacing="3",
        ),
    )


def usuarios_page():
    return rx.box(
        page_layout(
            rx.vstack(
                
                # =========================
                # Header
                # =========================
                
                usuarios_header(),

                rx.flex(
                    
                    # =========================
                    # Gestão de Usuários
                    # =========================
                    
                    novo_usuario(),
                    atualizar_credencial(),
                    revogar_acesso(),

                    spacing="5",
                    wrap="wrap",
                    width="100%",
                    align="stretch",
                ),

                width="100%",
                spacing="6",
                align="start",
            )
        )
    )