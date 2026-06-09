import reflex as rx

from pages.dashboard import dashboard
from pages.usuarios import usuarios_page
from pages.zonas import zonas_page
from pages.logs import logs_page
from pages.simulador import simulador_page

from states.dashboard_state import DashboardState
from states.log_state import LogState


app = rx.App()

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
    simulador_page, 
    route="/simulador",
    title="Simulador"
)
