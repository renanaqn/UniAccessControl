import reflex as rx

from states.auth_state import AuthState


def login_brand_panel():
    return rx.box(
        rx.vstack(
            rx.image(
                src="/logos/log branco-04.png",
                width="360px",
                max_width="80%",
                object_fit="contain",
            ),

            rx.heading(
                "Controle de Acesso Inteligente",
                size="7",
                color="white",
                text_align="center",
                margin_top="2rem",
            ),

            rx.text(
                "Gerencie usuários, zonas, permissões e registros de auditoria em uma única plataforma.",
                color="rgba(255,255,255,0.75)",
                size="3",
                text_align="center",
                max_width="520px",
                line_height="1.6",
            ),

            rx.hstack(
                rx.badge(
                    rx.icon("shield-check", size=16),
                    "Seguro",
                    color_scheme="blue",
                    variant="soft",
                ),
                rx.badge(
                    rx.icon("file-search", size=16),
                    "Auditável",
                    color_scheme="blue",
                    variant="soft",
                ),
                rx.badge(
                    rx.icon("scan-line", size=16),
                    "RFID",
                    color_scheme="blue",
                    variant="soft",
                ),
                spacing="3",
                wrap="wrap",
                justify="center",
                margin_top="1rem",
            ),

            align="center",
            justify="center",
            spacing="5",
            width="100%",
            height="100%",
            padding="3rem",
        ),

        width=["0%", "0%", "50%"],
        display=["none", "none", "flex"],
        min_height="100vh",
        background=(
            "linear-gradient(135deg, "
            "#081826 0%, "
            "#102f45 45%, "
            "#173d59 100%)"
        ),
        position="relative",
        overflow="hidden",
    )


def login_header():
    return rx.vstack(

        rx.heading(
            "Bem-vindo de volta",
            size="6",
            text_align="center",
        ),

        rx.text(
            "Faça login para acessar o UniAccessControl.",
            color_scheme="gray",
            size="3",
            text_align="center",
        ),

        width="100%",
        align="center",
        spacing="2",
    )


def usuario_senha():
    return rx.vstack(
        rx.vstack(
            rx.text("Usuário", size="2", weight="medium"),
            rx.input(
                rx.input.slot(
                    rx.icon("user", size=18),
                ),
                placeholder="Digite seu usuário",
                value=AuthState.login_user,
                on_change=AuthState.set_login_user,
                width="100%",
                size="3",
            ),
            width="100%",
            align="start",
            spacing="1",
        ),

        rx.vstack(
            rx.text("Senha", size="2", weight="medium"),
            rx.input(
                rx.input.slot(
                    rx.icon("lock-keyhole", size=18),
                ),
                placeholder="Digite sua senha",
                type="password",
                value=AuthState.login_pass,
                on_change=AuthState.set_login_pass,
                width="100%",
                size="3",
            ),
            width="100%",
            align="start",
            spacing="1",
        ),

        width="100%",
        spacing="4",
    )


def entrar():
    return rx.vstack(
        rx.button(
            rx.icon("log-in", size=18),
            "Entrar no sistema",
            on_click=AuthState.fazer_login,
            color_scheme="blue",
            width="100%",
            size="3",
            margin_top="1rem",
        ),

        rx.cond(
            AuthState.erro_login != "",
            rx.callout(
                AuthState.erro_login,
                icon="triangle-alert",
                color_scheme="red",
                variant="soft",
                width="100%",
                margin_top="0.75rem",
            ),
            rx.fragment(),
        ),

        width="100%",
        align="center",
    )


def login_card():
    return rx.card(
        rx.vstack(
            login_header(),

            rx.divider(margin_y="1rem"),

            usuario_senha(),

            entrar(),

            rx.text(
                "Acesso restrito a usuários autorizados.",
                color_scheme="gray",
                size="1",
                text_align="center",
                margin_top="1rem",
            ),

            width="100%",
            spacing="4",
        ),

        width="100%",
        max_width="430px",
        padding="2.5rem",
        border_radius="1rem",
        box_shadow="0 20px 60px rgba(0, 0, 0, 0.18)",
        background="var(--color-panel-solid)",
    )


def login_form_panel():
    return rx.box(
        rx.center(
            login_card(),
            width="100%",
            height="100%",
            padding="2rem",
        ),

        width=["100%", "100%", "50%"],
        min_height="100vh",
        background=(
            "linear-gradient(180deg, "
            "var(--gray-1) 0%, "
            "var(--gray-3) 100%)"
        ),
    )


def login_page():
    return rx.flex(
        login_brand_panel(),
        login_form_panel(),
        width="100%",
        min_height="100vh",
    )