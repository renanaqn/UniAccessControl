import reflex as rx

import components.layout as comp
from components.tabelas import log_table_parcial

from states.dashboard_state import DashboardState


def metric_card(
    title: str,
    value,
    subtitle: str,
    icon: str,
    color_scheme: str = "gray",
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
                rx.spacer(),
                rx.badge(
                    "Hoje" if "Hoje" in title else "Sistema",
                    color_scheme=color_scheme,
                    variant="soft",
                ),
                width="100%",
                align="center",
            ),

            rx.vstack(
                rx.text(
                    title,
                    size="2",
                    color_scheme="gray",
                    weight="medium",
                ),
                rx.heading(
                    value,
                    size="8",
                    weight="bold",
                ),
                rx.text(
                    subtitle,
                    size="2",
                    color_scheme="gray",
                ),
                align="start",
                spacing="1",
            ),

            width="100%",
            align="start",
            spacing="4",
        ),
        width="100%",
        min_width="220px",
        flex="1",
        variant="surface",
    )


def dashboard_header():
    return rx.card(
        rx.hstack(
            rx.hstack(
                rx.badge(
                    rx.icon("layout-dashboard", size=38),
                    color_scheme="sky",
                    variant="soft",
                    radius="full",
                    padding="0.75rem",
                ),
                rx.vstack(
                    rx.heading(
                        "UniAccessControl",
                        size="8",
                    ),
                    rx.text(
                        "Painel geral do sistema de controle de acesso universitário.",
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

            rx.hstack(
                rx.badge(
                    rx.icon("activity", size=16),
                    DashboardState.status_sistema,
                    color_scheme=DashboardState.status_cor,
                    variant="soft",
                ),
                rx.button(
                    rx.icon("refresh-cw", size=16),
                    "Atualizar",
                    variant="soft",
                    color_scheme="sky",
                    on_click=DashboardState.carregar_dados,
                ),
                spacing="3",
                align="center",
            ),

            width="100%",
            align="center",
            spacing="4",
            wrap="wrap",
        ),
        width="100%",
        variant="surface",
    )


def status_info_item(
    titulo: str,
    valor,
    icon: str,
    color_scheme: str = "gray",
    badge: bool = False,
):
    return rx.hstack(
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
        min_width="220px",
        flex="1",
    )


def system_status_card():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.badge(
                        rx.icon("server", size=18),
                        color_scheme="sky",
                        variant="soft",
                        radius="full",
                        padding="0.5rem",
                    ),
                    rx.vstack(
                        rx.heading("Status Operacional", size="5"),
                        rx.text(
                            "Informações de conexão e atualização do painel.",
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
                    "Auto refresh: 5s",
                    color_scheme="gray",
                    variant="soft",
                ),

                width="100%",
                align="center",
                spacing="4",
                wrap="wrap",
            ),

            rx.divider(),

            rx.flex(
                status_info_item(
                    titulo="Banco de dados",
                    valor=DashboardState.banco_status,
                    icon="database",
                    color_scheme=DashboardState.banco_cor,
                    badge=True,
                ),
                status_info_item(
                    titulo="Última atualização",
                    valor=DashboardState.ultima_atualizacao,
                    icon="clock",
                    color_scheme="gray",
                ),
                status_info_item(
                    titulo="Situação do sistema",
                    valor=DashboardState.status_sistema,
                    icon="activity",
                    color_scheme=DashboardState.status_cor,
                    badge=True,
                ),
                width="100%",
                spacing="5",
                wrap="wrap",
            ),

            width="100%",
            spacing="4",
        ),
        width="100%",
        variant="surface",
    )


def system_summary():
    return rx.flex(
        metric_card(
            "Total de Usuários",
            DashboardState.total_usuarios,
            "Usuários cadastrados no sistema",
            "users",
            "blue",
        ),
        metric_card(
            "Total de Zonas",
            DashboardState.total_zonas,
            "Áreas controladas cadastradas",
            "map-pin",
            "purple",
        ),
        metric_card(
            "Acessos Aprovados Hoje",
            DashboardState.acessos_aprovados_hoje,
            DashboardState.percentual_aprovados_label,
            "circle-check",
            "green",
        ),
        metric_card(
            "Acessos Negados Hoje",
            DashboardState.acessos_negados_hoje,
            DashboardState.percentual_negados_label,
            "circle-x",
            "red",
        ),
        wrap="wrap",
        spacing="4",
        width="100%",
    )


def access_summary_card():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.badge(
                        rx.icon("chart-pie", size=18),
                        color_scheme="sky",
                        variant="soft",
                        radius="full",
                        padding="0.5rem",
                    ),
                    rx.vstack(
                        rx.heading("Resumo de Acessos Hoje", size="5"),
                        rx.text(
                            DashboardState.total_acessos_hoje_label,
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
                    DashboardState.alerta_acessos_negados,
                    color_scheme=DashboardState.alerta_cor,
                    variant="soft",
                ),

                width="100%",
                align="center",
                spacing="4",
                wrap="wrap",
            ),

            rx.divider(),

            rx.flex(
                rx.center(
                    rx.box(
                        rx.center(
                            rx.vstack(
                                rx.heading(
                                    DashboardState.pizza_acessos_centro_label,
                                    size="7",
                                ),
                                rx.text(
                                    "aprovados",
                                    size="2",
                                    color_scheme="gray",
                                ),
                                spacing="0",
                                align="center",
                            ),
                            width="128px",
                            height="128px",
                            border_radius="50%",
                            background="var(--color-panel-solid)",
                        ),
                        width="190px",
                        height="190px",
                        border_radius="50%",
                        background=DashboardState.pizza_acessos_background,
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        flex_shrink="0",
                    ),
                    min_width="220px",
                    flex="1",
                ),

                rx.vstack(
                    resumo_linha_acesso(
                        titulo="Acessos permitidos",
                        valor=DashboardState.acessos_aprovados_hoje,
                        percentual=DashboardState.percentual_aprovados_label,
                        color_scheme="green",
                        icon="circle-check",
                    ),
                    resumo_linha_acesso(
                        titulo="Acessos negados",
                        valor=DashboardState.acessos_negados_hoje,
                        percentual=DashboardState.percentual_negados_label,
                        color_scheme="red",
                        icon="circle-x",
                    ),

                    rx.divider(),

                    rx.callout(
                        DashboardState.alerta_acessos_negados,
                        icon="info",
                        color_scheme=DashboardState.alerta_cor,
                        variant="soft",
                        width="100%",
                    ),

                    width="100%",
                    min_width="280px",
                    flex="1.5",
                    spacing="4",
                ),

                width="100%",
                spacing="6",
                wrap="wrap",
                align="center",
            ),

            width="100%",
            spacing="4",
        ),
        width="100%",
        variant="surface",
    )


def resumo_linha_acesso(
    titulo: str,
    valor,
    percentual,
    color_scheme: str,
    icon: str,
):
    return rx.card(
        rx.hstack(
            rx.badge(
                rx.icon(icon, size=18),
                color_scheme=color_scheme,
                variant="soft",
                radius="full",
                padding="0.5rem",
            ),
            rx.vstack(
                rx.text(
                    titulo,
                    size="3",
                    weight="medium",
                ),
                rx.text(
                    percentual,
                    size="2",
                    color_scheme="gray",
                ),
                spacing="0",
                align="start",
            ),
            rx.spacer(),
            rx.heading(
                valor,
                size="6",
            ),
            width="100%",
            align="center",
            spacing="3",
        ),
        width="100%",
        variant="ghost",
    )


def auditoria_coluna(
    titulo: str,
    subtitulo: str,
    logs,
    icon: str,
    color_scheme: str,
):
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(icon, size=18),
                    color_scheme=color_scheme,
                    variant="soft",
                    radius="full",
                    padding="0.5rem",
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
                width="100%",
                align="center",
                spacing="3",
            ),

            rx.divider(),

            rx.box(
                log_table_parcial(logs),
                width="100%",
                max_height="360px",
                overflow_y="auto",
                overflow_x="auto",
            ),

            width="100%",
            spacing="4",
        ),
        width="100%",
        min_width="320px",
        flex="1",
        variant="surface",
    )


def resumo_auditoria():
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
                        rx.heading("Auditoria de Acessos", size="5"),
                        rx.text(
                            "Últimos acessos permitidos e negados registrados no sistema.",
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

                rx.hstack(
                    rx.badge(
                        "Últimos 10 logs",
                        color_scheme="gray",
                        variant="soft",
                    ),
                    rx.link(
                        rx.button(
                            rx.icon("external-link", size=16),
                            "Ver auditoria completa",
                            variant="soft",
                            color_scheme="orange",
                        ),
                        href="/logs",
                    ),
                    spacing="3",
                    align="center",
                ),

                width="100%",
                align="center",
                spacing="4",
                wrap="wrap",
            ),

            rx.flex(
                auditoria_coluna(
                    titulo="Acessos Permitidos",
                    subtitulo="Entradas autorizadas pelo sistema",
                    logs=DashboardState.ultimos_permitidos,
                    icon="circle-check",
                    color_scheme="green",
                ),
                auditoria_coluna(
                    titulo="Acessos Negados",
                    subtitulo="Tentativas bloqueadas ou inválidas",
                    logs=DashboardState.ultimos_negados,
                    icon="circle-x",
                    color_scheme="red",
                ),
                width="100%",
                spacing="4",
                wrap="wrap",
                align="stretch",
            ),

            width="100%",
            spacing="4",
        ),
        width="100%",
        variant="surface",
    )


def dashboard_page():
    return rx.box(
        comp.page_layout(
            rx.vstack(
                dashboard_header(),

                rx.moment(
                    interval=5000,
                    on_change=DashboardState.carregar_dados,
                    display="none",
                ),

                system_status_card(),

                system_summary(),

                access_summary_card(),

                resumo_auditoria(),

                width="100%",
                align="start",
                spacing="6",
            )
        )
    )