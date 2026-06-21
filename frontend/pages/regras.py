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
                href="/permissoes",
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


def filtro_select_regras(
    label: str,
    value,
    options,
    on_change,
    icon: str,
):
    return rx.vstack(
        rx.text(label, size="2", weight="medium", color_scheme="gray"),
        rx.hstack(
            rx.icon(icon, size=16),
            rx.select(
                options,
                value=value,
                on_change=on_change,
                width="100%",
                size="3",
            ),
            width="100%",
            align="center",
            spacing="2",
        ),
        width="100%",
        min_width="220px",
        flex="1",
        align="start",
        spacing="1",
    )


def filtro_hora_regras(label: str, value, on_change, icon: str):
    return rx.vstack(
        rx.text(label, size="2", weight="medium", color_scheme="gray"),
        rx.input(
            rx.input.slot(
                rx.icon(icon, size=16),
            ),
            type="time",
            value=value,
            on_change=on_change,
            width="100%",
            size="3",
        ),
        width="100%",
        min_width="180px",
        flex="1",
        align="start",
        spacing="1",
    )


def filtros_regras():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.badge(
                        rx.icon("sliders-horizontal", size=18),
                        color_scheme="purple",
                        variant="soft",
                        radius="full",
                        padding="0.5rem",
                    ),
                    rx.vstack(
                        rx.heading("Filtros de Regras", size="5"),
                        rx.text(
                            "Filtre permissões por perfil, zona e intervalo de horário.",
                            size="2",
                            color_scheme="gray",
                        ),
                        spacing="0",
                        align="start",
                    ),
                    align="center",
                    spacing="3",
                ),

                rx.spacer(),

                rx.button(
                    rx.icon("x", size=16),
                    "Limpar filtros",
                    variant="soft",
                    color_scheme="gray",
                    on_click=RegrasState.limpar_filtros,
                ),

                width="100%",
                align="center",
                spacing="4",
                wrap="wrap",
            ),

            rx.divider(),

            rx.flex(
                filtro_select_regras(
                    label="Perfil",
                    value=RegrasState.filtro_perfil,
                    options=RegrasState.perfis,
                    on_change=RegrasState.definir_perfil,
                    icon="users",
                ),

                filtro_select_regras(
                    label="Zona",
                    value=RegrasState.filtro_zona,
                    options=RegrasState.zonas,
                    on_change=RegrasState.definir_zona,
                    icon="map-pin",
                ),

                filtro_hora_regras(
                    label="Horário inicial",
                    value=RegrasState.filtro_hora_inicio,
                    on_change=RegrasState.definir_hora_inicio,
                    icon="clock-3",
                ),

                filtro_hora_regras(
                    label="Horário final",
                    value=RegrasState.filtro_hora_fim,
                    on_change=RegrasState.definir_hora_fim,
                    icon="clock-9",
                ),

                width="100%",
                spacing="4",
                wrap="wrap",
                align="end",
            ),

            width="100%",
            spacing="4",
        ),
        width="100%",
        variant="surface",
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
                # Filtros
                # =========================
                
                filtros_regras(),
                
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