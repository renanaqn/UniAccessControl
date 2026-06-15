import reflex as rx

from components.layout import page_layout
from components.stat_card import stat_card
from components.log_table import log_table

from states.log_state import LogState
from states.auth_state import AuthState 


def logs_page():
    return rx.box(
        page_layout(

            rx.vstack(

                # =========================
                # TÍTULO
                # =========================

                rx.heading(
                    "Registros de Acesso",
                    size="8"
                ),
                
                rx.moment(
                    interval=1000,
                    on_change=LogState.carregar_logs
                ),

                rx.divider(),

                # =========================
                # FILTROS
                # =========================

                rx.card(

                    rx.vstack(

                        rx.heading(
                            "Filtros",
                            size="5"
                        ),

                        rx.flex(

                            # -------------------
                            # Usuário
                            # -------------------

                            rx.vstack(

                                rx.text("Usuário"),

                                rx.input(
                                    placeholder="Digite o nome do usuário...",
                                    value=LogState.filtro_usuario,
                                    on_change=LogState.definir_usuario,
                                    width="300px"
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
                                                    on_click=lambda: LogState.selecionar_usuario(usuario)
                                                )
                                            ),

                                            width="100%",
                                            align="start",
                                        ),

                                        width="300px",
                                    ),
                                ),

                                align="start",
                            ),

                            # -------------------
                            # Zona
                            # -------------------

                            rx.vstack(

                                rx.text("Zona"),

                                rx.select(
                                    LogState.zonas,
                                    value=LogState.filtro_zona,
                                    placeholder="Todas",
                                    on_change=LogState.definir_zona,
                                    width="250px"
                                ),

                                align="start",
                            ),

                            # -------------------
                            # Resultado
                            # -------------------

                            rx.vstack(

                                rx.text("Resultado"),

                                rx.select(
                                    LogState.resultados,
                                    value=LogState.filtro_resultado,
                                    on_change=LogState.definir_resultado,
                                    width="200px"
                                ),

                                align="start",
                            ),

                            wrap="wrap",
                            spacing="5",
                        ),

                        # =====================
                        # DATAS
                        # =====================

                        rx.flex(

                            rx.vstack(

                                rx.text("Data Inicial"),

                                rx.input(
                                    type="date",
                                    value=LogState.filtro_data_inicio,
                                    on_change=LogState.definir_data_inicio,
                                ),

                                align="start"
                            ),

                            rx.vstack(

                                rx.text("Data Final"),

                                rx.input(
                                    type="date",
                                    value=LogState.filtro_data_fim,
                                    on_change=LogState.definir_data_fim,
                                ),

                                align="start"
                            ),

                            spacing="5",
                        ),

                        # =====================
                        # BOTÕES
                        # =====================

                        rx.button(
                            "Limpar",
                            variant="outline",
                            on_click=LogState.limpar_filtros
                        ),

                        width="100%",
                        align="start",
                        spacing="4",
                    ),

                    width="100%",
                ),

                # =========================
                # TABELA
                # =========================

                rx.card(

                    rx.vstack(

                        rx.heading(
                            "Histórico de Auditoria",
                            size="5"
                        ),

                        log_table(LogState.logs)
                    ),

                    width="100%",
                ),

                # =========================
                # PAGINAÇÃO
                # =========================

                rx.hstack(

                    rx.button(
                        "Anterior",
                        on_click=LogState.pagina_anterior,
                        disabled=~LogState.possui_pagina_anterior
                    ),

                    rx.text(
                        LogState.pagina_texto
                    ),

                    rx.button(
                        "Próxima",
                        on_click=LogState.proxima_pagina,
                        disabled=~LogState.possui_proxima_pagina
                    ),

                    justify="center",
                    width="100%",
                    spacing="4"
                ),

                width="100%",
                align="start",
                spacing="5",
            ),
        ), 
        on_mount=AuthState.verificar_acesso
    )   