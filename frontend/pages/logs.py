import reflex as rx

from components.layout import page_layout
from components.tabelas import log_table

from states.log_state import LogState


def auditoria_header():
    return rx.card(
        rx.hstack(
            rx.hstack(
                rx.badge(
                    rx.icon("file-search", size=36),
                    color_scheme="orange",
                    variant="soft",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.heading(
                        "Auditoria de Acessos",
                        size="7",
                    ),
                    rx.text(
                        "Consulte, filtre e acompanhe os registros de entrada no sistema.",
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

            rx.badge(
                rx.icon("shield-alert", size=16),
                "Logs do sistema",
                color_scheme="orange",
                variant="soft",
            ),

            width="100%",
            align="center",
            spacing="4",
            wrap="wrap",
        ),

        width="100%",
        variant="surface",
    )


def system_status_card():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.badge(
                        rx.icon("activity", size=18),
                        color_scheme="orange",
                        variant="soft",
                        radius="full",
                        padding="0.5rem",
                    ),
                    rx.vstack(
                        rx.heading("Monitoramento", size="5"),
                        rx.text(
                            "Status da conexão e atualização dos registros.",
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
                    rx.icon("refresh-cw", size=16),
                    "Atualizar",
                    variant="soft",
                    color_scheme="orange",
                    on_click=LogState.carregar_logs,
                ),

                width="100%",
                align="center",
                spacing="4",
                wrap="wrap",
            ),

            rx.divider(),

            rx.flex(
                status_item(
                    titulo="Banco de dados",
                    valor=LogState.banco_status,
                    icon="database",
                    color_scheme=LogState.banco_cor,
                    badge=True,
                ),
                status_item(
                    titulo="Última atualização",
                    valor=LogState.ultima_atualizacao,
                    icon="clock",
                    color_scheme="gray",
                ),
                status_item(
                    titulo="Atualização automática",
                    valor="A cada 5 segundos",
                    icon="timer-reset",
                    color_scheme="gray",
                ),

                width="100%",
                spacing="4",
                wrap="wrap",
            ),

            width="100%",
            spacing="4",
        ),
        width="100%",
        variant="surface",
    )


def status_item(
    titulo: str,
    valor,
    icon: str,
    color_scheme: str = "gray",
    badge: bool = False,
):
    return rx.card(
        rx.hstack(
            rx.badge(
                rx.icon(icon, size=16),
                color_scheme=color_scheme,
                variant="soft",
                radius="full",
                padding="0.45rem",
            ),
            rx.vstack(
                rx.text(
                    titulo,
                    size="2",
                    color_scheme="gray",
                ),
                rx.cond(
                    badge,
                    rx.badge(
                        valor,
                        color_scheme=color_scheme,
                        variant="soft",
                    ),
                    rx.text(
                        valor,
                        size="3",
                        weight="medium",
                    ),
                ),
                spacing="1",
                align="start",
            ),
            align="center",
            spacing="3",
        ),
        flex="1",
        min_width="230px",
        variant="ghost",
    )


def filtro_campo_texto():
    return rx.vstack(
        rx.text("Usuário", size="2", weight="medium", color_scheme="gray"),

        rx.box(
            rx.input(
                rx.input.slot(
                    rx.icon("user", size=16),
                ),
                placeholder="Digite o nome do usuário...",
                value=LogState.filtro_usuario,
                on_change=LogState.definir_usuario,
                width="100%",
                size="3",
            ),

            rx.cond(
                LogState.usuarios_sugeridos.length() > 0,
                rx.card(
                    rx.vstack(
                        rx.foreach(
                            LogState.usuarios_sugeridos,
                            lambda usuario: rx.button(
                                usuario,
                                variant="ghost",
                                width="100%",
                                justify="start",
                                on_click=lambda: LogState.selecionar_usuario(usuario),
                            ),
                        ),
                        width="100%",
                        align="stretch",
                        spacing="1",
                    ),
                    position="absolute",
                    top="calc(100% + 0.35rem)",
                    left="0",
                    width="100%",
                    z_index="20",
                    padding="0.5rem",
                    box_shadow="lg",
                ),
                rx.fragment(),
            ),

            width="100%",
            position="relative",
        ),

        width="100%",
        min_width="260px",
        flex="1.4",
        align="start",
        spacing="1",
    )


def filtro_select(
    label: str,
    value,
    options,
    on_change,
    icon: str,
    placeholder: str = "",
):
    return rx.vstack(
        rx.text(label, size="2", weight="medium", color_scheme="gray"),
        rx.box(
            rx.hstack(
                rx.icon(icon, size=16),
                rx.select(
                    options,
                    value=value,
                    placeholder=placeholder,
                    on_change=on_change,
                    width="100%",
                    size="3",
                ),
                width="100%",
                align="center",
                spacing="2",
            ),
            width="100%",
        ),
        width="100%",
        min_width="220px",
        flex="1",
        align="start",
        spacing="1",
    )


def filtro_data(label: str, value, on_change):
    return rx.vstack(
        rx.text(label, size="2", weight="medium", color_scheme="gray"),
        rx.input(
            rx.input.slot(
                rx.icon("calendar", size=16),
            ),
            type="date",
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


def filtros():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.badge(
                        rx.icon("sliders-horizontal", size=18),
                        color_scheme="orange",
                        variant="soft",
                        radius="full",
                        padding="0.5rem",
                    ),
                    rx.vstack(
                        rx.heading("Filtros de Auditoria", size="5"),
                        rx.text(
                            "Refine os logs por usuário, zona, resultado e período.",
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
                    on_click=LogState.limpar_filtros,
                ),

                width="100%",
                align="center",
                spacing="4",
                wrap="wrap",
            ),

            rx.divider(),

            rx.flex(
                filtro_campo_texto(),

                filtro_select(
                    label="Zona",
                    value=LogState.filtro_zona,
                    options=LogState.zonas,
                    on_change=LogState.definir_zona,
                    icon="map-pin",
                    placeholder="Todas",
                ),

                filtro_select(
                    label="Resultado",
                    value=LogState.filtro_resultado,
                    options=LogState.resultados,
                    on_change=LogState.definir_resultado,
                    icon="circle-check",
                ),

                width="100%",
                spacing="4",
                wrap="wrap",
                align="end",
            ),

            rx.flex(
                filtro_data(
                    label="Data inicial",
                    value=LogState.filtro_data_inicio,
                    on_change=LogState.definir_data_inicio,
                ),

                filtro_data(
                    label="Data final",
                    value=LogState.filtro_data_fim,
                    on_change=LogState.definir_data_fim,
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


def tabela_logs():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.badge(
                        rx.icon("scroll-text", size=18),
                        color_scheme="orange",
                        variant="soft",
                        radius="full",
                        padding="0.5rem",
                    ),
                    rx.vstack(
                        rx.heading("Histórico de Auditoria", size="5"),
                        rx.text(
                            "Registros mais recentes de tentativas de acesso.",
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

                rx.badge(
                    LogState.pagina_texto,
                    color_scheme="gray",
                    variant="soft",
                ),

                width="100%",
                align="center",
                spacing="4",
                wrap="wrap",
            ),

            rx.divider(),

            rx.box(
                log_table(LogState.logs),
                width="100%",
                overflow_x="auto",
            ),

            paginacao(),

            width="100%",
            spacing="4",
        ),
        width="100%",
        variant="surface",
    )


def paginacao():
    return rx.hstack(
        rx.button(
            rx.icon("chevron-left", size=16),
            "Anterior",
            on_click=LogState.pagina_anterior,
            disabled=~LogState.possui_pagina_anterior,
            variant="soft",
            color_scheme="gray",
        ),

        rx.spacer(),

        rx.badge(
            LogState.pagina_texto,
            color_scheme="orange",
            variant="soft",
        ),

        rx.spacer(),

        rx.button(
            "Próxima",
            rx.icon("chevron-right", size=16),
            on_click=LogState.proxima_pagina,
            disabled=~LogState.possui_proxima_pagina,
            variant="soft",
            color_scheme="gray",
        ),

        width="100%",
        spacing="4",
        align="center",
    )


def logs_page():
    return rx.box(
        page_layout(
            rx.vstack(
                auditoria_header(),

                system_status_card(),

                rx.moment(
                    interval=5000,
                    on_change=LogState.carregar_logs,
                    display="none",
                ),

                filtros(),

                tabela_logs(),

                width="100%",
                align="start",
                spacing="6",
            ),
        )
    )