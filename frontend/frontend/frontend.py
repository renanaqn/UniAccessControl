import reflex as rx

from pages.dashboard import dashboard
from pages.usuarios import usuarios_page
from pages.zonas import zonas_page
from pages.logs import logs_page
from states.dashboard_state import DashboardState

app = rx.App()

app.add_page(
    dashboard,
    route="/",
    title="UniAcessControl",
    on_load=DashboardState.carregar_dados
)

app.add_page(
    usuarios_page,
    route="/usuarios",
    title="Usuários"
)

app.add_page(
    zonas_page,
    route="/zonas",
    title="Zonas"
)

app.add_page(
    logs_page,
    route="/logs",
    title="Logs"
)