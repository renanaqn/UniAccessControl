import reflex as rx

from components.layout import page_layout
from states.usuarios_tabela_state import UsuariosTabelaState
from states.auth_state import AuthState


def usuarios_tabela_header():
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
                    rx.heading("Usuários Cadastrados", size="7"),
                    rx.text(
                        "Consulte os usuários registrados no sistema e suas credenciais RFID.",
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
                    "Voltar a página anterior",
                    variant="soft",
                    color_scheme="purple",
                ),
                href="/usuarios",
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


def usuario_linha(usuario: dict):
    return rx.table.row(
        rx.table.cell(usuario["id"]),
        rx.table.cell(usuario["nome"]),
        rx.table.cell(usuario["rfid_tag"]),
        rx.table.cell(
            rx.badge(
                f"Perfil {usuario['perfil_id']}",
                color_scheme="green",
                variant="soft",
            )
        ),
    )


def tabela_usuarios():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Lista de Usuários", size="5"),
                rx.spacer(),
                rx.badge(
                    UsuariosTabelaState.pagina_label,
                    color_scheme="gray",
                    variant="soft",
                ),
                width="100%",
                align="center",
            ),

            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("ID"),
                            rx.table.column_header_cell("Nome"),
                            rx.table.column_header_cell("Tag RFID"),
                            rx.table.column_header_cell("Perfil"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            UsuariosTabelaState.usuarios,
                            usuario_linha,
                        )
                    ),
                    variant="surface",
                    width="100%",
                ),
                width="100%",
                overflow_x="auto",
            ),

            paginacao_usuarios(),

            width="100%",
            spacing="4",
        ),
        width="100%",
    )


def paginacao_usuarios():
    return rx.hstack(
        rx.button(
            rx.icon("chevrons-left", size=16),
            "Primeira",
            variant="soft",
            on_click=UsuariosTabelaState.primeira_pagina,
            is_disabled=~UsuariosTabelaState.tem_pagina_anterior,
        ),
        rx.button(
            rx.icon("chevron-left", size=16),
            "Anterior",
            variant="soft",
            on_click=UsuariosTabelaState.pagina_anterior,
            is_disabled=~UsuariosTabelaState.tem_pagina_anterior,
        ),

        rx.spacer(),

        rx.text(
            UsuariosTabelaState.pagina_label,
            size="2",
            color_scheme="gray",
        ),

        rx.spacer(),

        rx.button(
            "Próxima",
            rx.icon("chevron-right", size=16),
            variant="soft",
            on_click=UsuariosTabelaState.proxima_pagina,
            is_disabled=~UsuariosTabelaState.tem_proxima_pagina,
        ),
        rx.button(
            "Última",
            rx.icon("chevrons-right", size=16),
            variant="soft",
            on_click=UsuariosTabelaState.ultima_pagina,
            is_disabled=~UsuariosTabelaState.tem_proxima_pagina,
        ),

        width="100%",
        spacing="3",
        align="center",
        wrap="wrap",
    )


def usuarios_tabela_page():
    return rx.box(
        page_layout(
            rx.vstack(
                
                # =========================
                # Header
                # =========================
                
                usuarios_tabela_header(),
                
                # =========================
                # Tabela
                # =========================
                
                tabela_usuarios(),

                width="100%",
                spacing="6",
                align="start",
            )
        )
    )