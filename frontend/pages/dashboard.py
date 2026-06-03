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


def dashboard():

    return page_layout(

        rx.vstack(

            rx.heading(
                "UniAcessControl",
                size="8"
            ),

            rx.text(
                "Sistema de Controle de Acesso Universitário"
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
                    "Acessos Rejeitados Hoje",
                    DashboardState.acessos_rejeitados_hoje
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

                    rx.table.root(

                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Data/Hora"),
                                rx.table.column_header_cell("RFID"),
                                rx.table.column_header_cell("Zona"),
                                rx.table.column_header_cell("Resultado"),
                                rx.table.column_header_cell("Motivo"),
                            )
                        ),

                        rx.table.body(

                            rx.foreach(

                                DashboardState.ultimos_logs,

                                lambda log: rx.table.row(

                                    rx.table.cell(
                                        log["data_hora"]
                                    ),

                                    rx.table.cell(
                                        log["rfid_tentativa"]
                                    ),

                                    rx.table.cell(
                                        log["zona_id"]
                                    ),

                                    rx.table.cell(
                                        log["resultado"]
                                    ),

                                    rx.table.cell(
                                        log["motivo"]
                                    ),
                                )
                            )
                        ),
                    ),

                    width="100%",
                ),

                width="100%",
            ),

            width="100%",
            align="start",
            spacing="6",
        )
    )