import reflex as rx

from pages.dashboard import dashboard_page
from pages.usuarios import usuarios_page
from pages.zonas import zonas_page
from pages.logs import logs_page
from pages.simulador import simulador_page
from pages.login import login_page

from states.dashboard_state import DashboardState
from states.log_state import LogState
from states.auth_state import AuthState


app = rx.App()

app.add_page(
    login_page,
    route="/",
    title="Login | UniAccessControl"
)

app.add_page(
    dashboard_page, 
    route="/dashboard", 
    title="Dashboard | UniAccessControl",
    on_load=[AuthState.verificar_acesso, DashboardState.carregar_dados]
)

app.add_page(
    logs_page, 
    route="/logs", 
    title="Auditoria | UniAccessControl",
    on_load=[AuthState.verificar_acesso, LogState.carregar_pagina]
)

app.add_page(
    usuarios_page,
    route="/usuarios",
    title="Usuários",
    on_load=[AuthState.verificar_acesso]
)

app.add_page(
    zonas_page,
    route="/zonas",
    title="Zonas",
    on_load=[AuthState.verificar_acesso]
)

app.add_page(
    simulador_page, 
    route="/simulador",
    title="Terminal Porta | UniAccessControl",
    on_load=[AuthState.verificar_acesso, DashboardState.carregar_dados]
)
