import reflex as rx

from components.layout import page_layout
from states.regras_state import RegrasState
from states.auth_state import AuthState


def regras_header():
    return rx.card(
        rx.hstack(
            rx.hstack(
                rx.badge(
                    rx.icon("shield-check", size=36),
                    color_scheme="purple",
                    variant="soft",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.heading("Regras de Acesso", size="7"),
                    rx.text(
                        "Consulte as permissões configuradas por perfil, zona e horário.",
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
                href="/zonas",
            ),

            width="100%",
            align="center",
            spacing="4",
            wrap="wrap",
        ),
        width="100%",
        variant="surface",
    )


def regra_linha(regra: dict):
    return rx.table.row(
        rx.table.cell(
            rx.badge(
                regra["nome_perfil"],
                color_scheme="green",
                variant="soft",
            )
        ),
        rx.table.cell(
            rx.badge(
                regra["nome_zona"],
                color_scheme="purple",
                variant="soft",
            )
        ),
        rx.table.cell(regra["hora_inicio"]),
        rx.table.cell(regra["hora_fim"]),
    )


def tabela_regras():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Lista de Regras", size="5"),
                rx.spacer(),
                rx.badge(
                    RegrasState.pagina_label,
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
                            rx.table.column_header_cell("Perfil"),
                            rx.table.column_header_cell("Zona"),
                            rx.table.column_header_cell("Início"),
                            rx.table.column_header_cell("Fim"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            RegrasState.regras,
                            regra_linha,
                        )
                    ),
                    variant="surface",
                    width="100%",
                ),
                width="100%",
                overflow_x="auto",
            ),

            paginacao_regras(),

            width="100%",
            spacing="4",
        ),
        width="100%",
    )


def paginacao_regras():
    return rx.hstack(
        rx.button(
            rx.icon("chevrons-left", size=16),
            "Primeira",
            variant="soft",
            on_click=RegrasState.primeira_pagina,
            is_disabled=~RegrasState.tem_pagina_anterior,
        ),
        rx.button(
            rx.icon("chevron-left", size=16),
            "Anterior",
            variant="soft",
            on_click=RegrasState.pagina_anterior,
            is_disabled=~RegrasState.tem_pagina_anterior,
        ),

        rx.spacer(),

        rx.text(
            RegrasState.pagina_label,
            size="2",
            color_scheme="gray",
        ),

        rx.spacer(),

        rx.button(
            "Próxima",
            rx.icon("chevron-right", size=16),
            variant="soft",
            on_click=RegrasState.proxima_pagina,
            is_disabled=~RegrasState.tem_proxima_pagina,
        ),
        rx.button(
            "Última",
            rx.icon("chevrons-right", size=16),
            variant="soft",
            on_click=RegrasState.ultima_pagina,
            is_disabled=~RegrasState.tem_proxima_pagina,
        ),

        width="100%",
        spacing="3",
        align="center",
        wrap="wrap",
    )


def regras_page():
    return rx.box(
        page_layout(
            rx.vstack(
                
                # =========================
                # Header
                # =========================
                
                regras_header(),
                
                # =========================
                # Tabela
                # =========================
                
                tabela_regras(),

                width="100%",
                spacing="6",
                align="start",
            )
        )
    )