import reflex as rx

from components.layout import page_layout
from components.stat_card import stat_card
from components.log_table import log_table

from states.dashboard_state import DashboardState

def logs_page():
    return rx.box(
    "Vazio",
    id="box-id",
    class_name=[
        "class-name-1",
        "class-name-2",
    ],
)