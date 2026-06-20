import reflex as rx

import components.layout as comp
from components.log_table import log_table

from states.dashboard_state import DashboardState
from states.auth_state import AuthState 

def metric_card(
    title: str,
    value,
    subtitle: str,
    icon: str,
    color_scheme: str = 'gray',
):
    """Card reutilizável para indicadores principais do dashboard"""
    
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(icon, size=18),
                    color_scheme=color_scheme,
                    variant="soft",
                    radius="full",
                    padding="0.55rem",
                ),
                rx.text(
                    title,
                    size="3",
                    weight="medium",
                    color_scheme="gray",
                ),
                width="100%",
                align="center",
                spacing="3",
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
            spacing="2",
        ),
        width="100%",
        min_width="220px",
        flex="1",
    )
    
def system_status_card():
    """Resumo operacional do sistema."""
    
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Status do Sistema", size="5"),
                rx.spacer(),
                rx.badge(
                    DashboardState.status_sistema,
                    color_scheme=DashboardState.status_cor,
                    variant="soft",
                ),
                width="100%",
                align="center",
            ),
            rx.divider(),
            rx.hstack(
                rx.vstack(
                    rx.text("Banco de dados", size="2", color_scheme="gray"),
                    rx.badge(
                        DashboardState.banco_status,
                        color_scheme=DashboardState.banco_cor,
                        variant="soft",
                    ),
                    align="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Última atualização", size="2", color_scheme="gray"),
                    rx.text(DashboardState.ultima_atualizacao, size="3", weight="medium"),
                    align="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Atualização automática", size="2", color_scheme="gray"),
                    rx.text("A cada 5 segundos", size="3", weight="medium"),
                    align="start",
                    spacing="1",
                ),
                width="100%",
                spacing="6",
                wrap="wrap",
            ),
            width="100%",
            align="start",
            spacing="4",
        ),
        width="100%",
    )

def access_summary_card():
    """Resumo visual dos acessos permitidos e negados no dia"""
    
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Resumo de Acessos Hoje", size="5"),
                rx.spacer(),
                rx.text(
                    DashboardState.total_acessos_hoje_label,
                    size="2",
                    color_scheme="gray",
                ),
                width="100%",
                align="center",
            ),

            rx.divider(),

            rx.vstack(
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                DashboardState.pizza_acessos_centro_label,
                                size="6",
                            ),
                            rx.text(
                                "aprovados",
                                size="2",
                                color_scheme="gray",
                            ),
                            spacing="0",
                            align="center",
                        ),
                        width="120px",
                        height="120px",
                        border_radius="50%",
                        background="var(--color-panel-solid)",
                    ),
                    width="170px",
                    height="170px",
                    border_radius="50%",
                    background=DashboardState.pizza_acessos_background,
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),

                rx.vstack(
                    rx.hstack(
                        rx.box(
                            width="12px",
                            height="12px",
                            border_radius="50%",
                            background="var(--green-9)",
                        ),
                        rx.text("Aprovados", size="3", weight="medium"),
                        rx.spacer(),
                        rx.text(
                            DashboardState.percentual_aprovados_label,
                            size="3",
                            color_scheme="gray",
                        ),
                        width="100%",
                        align="center",
                    ),

                    rx.hstack(
                        rx.box(
                            width="12px",
                            height="12px",
                            border_radius="50%",
                            background="var(--red-9)",
                        ),
                        rx.text("Negados", size="3", weight="medium"),
                        rx.spacer(),
                        rx.text(
                            DashboardState.percentual_negados_label,
                            size="3",
                            color_scheme="gray",
                        ),
                        width="100%",
                        align="center",
                    ),

                    rx.divider(),

                    rx.text(
                        DashboardState.alerta_acessos_negados,
                        size="2",
                        color_scheme=DashboardState.alerta_cor,
                    ),

                    width="100%",
                    align="center",
                    spacing="3",
                ),

                width="100%",
                spacing="6",
                align="center",
                wrap="wrap",
            ),

            width="100%",
            align="start",
            spacing="4",
        ),
        width="100%",
    )

def dashboard_header():
    """Cabeçalho principal do dashboard."""

    return rx.hstack(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon("shield_check", size=40),
                    color_scheme="cyan",
                    variant="soft",
                    radius="full",
                    padding="0.55rem",
                ),
                rx.heading(
                    "UniAccessControl",
                    size="8",
                ),
                align="center"
            ),
            
            rx.text(
                "Sistema de Controle de Acesso Universitário",
                color_scheme="gray",
            ),
            align="start",
            spacing="1",
        ),
        rx.spacer(),
        rx.button(
            rx.icon("refresh-cw", size=16),
            "Atualizar",
            variant="soft",
            on_click=DashboardState.carregar_dados,
        ),
        width="100%",
        align="center",
        spacing="4",
        wrap="wrap",
    )

def system_summary():
    return rx.flex(
        metric_card(
            "Total de Usuários",
            DashboardState.total_usuarios,
            "Usuários Cadastrados",
            "users",
            "blue",
        ),
        metric_card(
            "Total de Zonas",
            DashboardState.total_zonas,
            "Áreas Cadastradas",
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

def dashboard_page():
    return rx.box(
        comp.page_layout(
            rx.vstack(
                dashboard_header(),

                # Atualiza os dados periodicamente, sem sobrecarregar o banco a cada 1 segundo.
                rx.moment(
                    interval=5000,
                    on_change=DashboardState.carregar_dados,
                    display="none",
                ),

                rx.divider(),

                system_status_card(),

                system_summary(),

                access_summary_card(),

                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.heading(
                                "Últimos 10 Logs",
                                size="5",
                            ),
                            rx.spacer(),
                            rx.badge(
                                "Auditoria resumida",
                                color_scheme="gray",
                                variant="soft",
                            ),
                            width="100%",
                            align="center",
                        ),
                        log_table(DashboardState.ultimos_logs),
                        width="100%",
                        spacing="4",
                    ),
                    width="100%",
                ),

                width="100%",
                align="start",
                spacing="6",
                on_mount=DashboardState.carregar_dados,
            )
        ),
        on_mount=AuthState.verificar_acesso,
    )