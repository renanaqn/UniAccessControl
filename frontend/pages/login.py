import reflex as rx

from states.auth_state import AuthState

def login_page():
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("UniAccessControl", size="6", margin_bottom="2"),
                rx.text("Faça login para acessar o sistema", color="gray", margin_bottom="4"),
                
                rx.input(
                    placeholder="Usuário", 
                    value=AuthState.login_user, 
                    on_change=AuthState.set_login_user,
                    width="100%"
                ),
                rx.input(
                    placeholder="Senha", 
                    type="password", 
                    value=AuthState.login_pass, 
                    on_change=AuthState.set_login_pass,
                    width="100%"
                ),
                
                rx.button(
                    "Entrar", 
                    on_click=AuthState.fazer_login, 
                    color_scheme="blue", 
                    width="100%",
                    margin_top="4"
                ),
                rx.text(AuthState.erro_login, color="red", size="2", margin_top="2"),
            ),
            padding="8",
            width="100%",
            max_width="400px",
            box_shadow="lg"
        ),
        width="100%",
        height="100vh"
    )