import reflex as rx

from components.layout import page_layout
from components.ui_components import stat_card
from components.tabelas import log_table

from states.log_state import LogState
from states.auth_state import AuthState 

def auditoria_header():
    return rx.vstack(
        rx.hstack(
            rx.badge(
                rx.icon("file-text", size=36),
                color_scheme="orange",
                variant="soft",
                radius="full",
                padding="0.65rem",
            ),
            rx.heading(
                "Auditoria de Acessos", 
                size="7", 
                margin_bottom="5"
            ),
            align="center",
            spacing="4",
        ),
        
        rx.text(
            "Consulte, filtre e acompanhe os registros de entrada no sistema.", 
            color="gray", 
            margin_bottom="5"
        ),
        rx.divider(),
        
        width="100%",
        align="center",
        spacing="4",
        wrap="wrap",
    )

def system_status_card():
    """Resumo operacional do sistema."""
    
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Status do Sistema", size="5"),
                rx.spacer(),
                rx.button(
                    rx.icon("refresh-cw", size=16),
                    "Atualizar",
                    variant="soft",
                    on_click=LogState.carregar_logs,
                ),
                width="100%",
                align="center",
            ),
            rx.divider(),
            rx.hstack(
                rx.vstack(
                    rx.text("Banco de dados", size="2", color_scheme="gray"),
                    rx.badge(
                        LogState.banco_status,
                        color_scheme=LogState.banco_cor,
                        variant="soft",
                    ),
                    align="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Última atualização", size="2", color_scheme="gray"),
                    rx.text(LogState.ultima_atualizacao, size="3", weight="medium"),
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

def filtros():
    return rx.card(

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
    )

def tabela_logs():
    return rx.card(

        rx.vstack(

            rx.heading(
                "Histórico de Auditoria",
                size="5"
            ),

            log_table(LogState.logs)
        ),

        width="100%",
    )

def paginacao():
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
    )

def logs_page():
    return rx.box(
        page_layout(

            rx.vstack(

                # =========================
                # TÍTULO
                # =========================

                auditoria_header(),
                
                system_status_card(),
                                
                rx.moment(
                    interval=5000,
                    on_change=LogState.carregar_logs,
                    display="none",
                ),

                # =========================
                # FILTROS
                # =========================

                filtros(),

                # =========================
                # TABELA
                # =========================

                tabela_logs(),

                # =========================
                # PAGINAÇÃO
                # =========================

                paginacao(),

                width="100%",
                align="start",
                spacing="5",
            ),
        )
    )   