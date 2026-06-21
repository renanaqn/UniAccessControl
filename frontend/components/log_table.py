import reflex as rx

def log_table(logs):

    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Data/Hora"),
                rx.table.column_header_cell("Usuário"),
                rx.table.column_header_cell("Zona"),
                rx.table.column_header_cell("Resultado"),
                rx.table.column_header_cell("Motivo"),
            )
        ),

        rx.table.body(
            rx.foreach(
                logs,
                lambda log: rx.table.row(
                    rx.table.cell(
                        log["data_hora"]
                    ),
                    
                    rx.table.cell(
                        log["nome"]
                    ),
                    
                    rx.table.cell(
                        log["nome_zona"]
                    ),
                    
                    rx.table.cell(
                        rx.badge(
                            log["resultado"],
                            
                            color_scheme=rx.cond(
                                log["resultado"] == "PERMITIDO",
                                "green",
                                "red"
                            )
                        )
                    ),
                    
                    rx.table.cell(
                        log["motivo"]
                    ),
                )
            )
        )
    ),
    
    width="100%"
    
def log_table_parcial(logs):

    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Data/Hora"),
                rx.table.column_header_cell("Usuário"),
                rx.table.column_header_cell("Zona"),
                rx.table.column_header_cell("Resultado")
            )
        ),

        rx.table.body(
            rx.foreach(
                logs,
                lambda log: rx.table.row(
                    rx.table.cell(
                        log["data_hora"]
                    ),
                    
                    rx.table.cell(
                        log["nome"]
                    ),
                    
                    rx.table.cell(
                        log["nome_zona"]
                    ),
                    
                    rx.table.cell(
                        rx.badge(
                            log["resultado"],
                            
                            color_scheme=rx.cond(
                                log["resultado"] == "PERMITIDO",
                                "green",
                                "red"
                            )
                        )
                    ),
                )
            )
        )
    ),
    
    width="100%"