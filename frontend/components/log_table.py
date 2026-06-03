import reflex as rx

def log_table(logs):

    return rx.table.root(
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
                logs,
                lambda log: rx.table.row(
                    rx.table.cell(log["data_hora"]),
                    rx.table.cell(log["rfid_tentativa"]),
                    rx.table.cell(str(log["zona_id"])),
                    rx.table.cell(log["resultado"]),
                    rx.table.cell(log["motivo"]),
                )
            )
        )
    )