import reflex as rx

from components.layout import page_layout
from components.stat_card import stat_card
from components.log_table import log_table

from states.dashboard_state import DashboardState

def metric_card(title: str, value):

    return rx.card(

        rx.vstack(

            rx.text(
                title,
                size="3",
                color_scheme="gray"
            ),

            rx.heading(
                value,
                size="8"
            ),

            align="start",
            spacing="1",
        ),

        width="250px",
    )

@rx.page(
    route="/",
    title="UniAcessControl",
    on_load=DashboardState.carregar_dados
)
def dashboard():

    return page_layout(

        rx.vstack(

            rx.heading(
                "UniAccessControl",
                size="8"
            ),

            rx.text(
                "Sistema de Controle de Acesso Universitário"
            ),
            
            rx.moment(
                interval=1000,
                on_change=DashboardState.carregar_dados
            ),

            rx.divider(),

            rx.flex(

                metric_card(
                    "Total de Usuários",
                    DashboardState.total_usuarios
                ),

                metric_card(
                    "Total de Zonas",
                    DashboardState.total_zonas
                ),

                metric_card(
                    "Acessos Aprovados Hoje",
                    DashboardState.acessos_aprovados_hoje
                ),

                metric_card(
                    "Acessos Negados Hoje",
                    DashboardState.acessos_negados_hoje
                ),

                wrap="wrap",
                spacing="4",
                width="100%",
            ),

            rx.card(

                rx.vstack(

                    rx.heading(
                        "Últimos 10 Logs",
                        size="5"
                    ),

                    log_table(DashboardState.ultimos_logs)
                ),

                width="100%",
            ),

            width="100%",
            align="start",
            spacing="6",
        )
    )