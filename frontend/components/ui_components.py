import reflex as rx


def sidebar_item(
    label: str,
    icon: str,
    href: str,
):
    return rx.link(
        rx.hstack(
            rx.icon(
                icon,
                size=18,
                color="rgba(255,255,255,0.9)",
            ),
            rx.text(
                label,
                color="rgba(255,255,255,0.9)",
                size="2",
                weight="medium",
            ),
            align="center",
            spacing="3",
            padding="0.8rem",
            border_radius="0.75rem",
            width="100%",
            transition="all 0.2s ease",
            _hover={
                "background": "rgba(255,255,255,0.12)",
                "transform": "translateX(4px)",
            },
        ),
        href=href,
        width="100%",
        _hover={"textDecoration": "none"},
    )


def sidebar_section_title(title: str):
    return rx.text(
        title,
        size="1",
        weight="bold",
        color="rgba(255,255,255,0.45)",
        letter_spacing="0.08em",
        text_transform="uppercase",
        padding_x="0.75rem",
        padding_top="0.75rem",
        padding_bottom="0.25rem",
    )


def sidebar_user_card():
    return rx.box(
        rx.hstack(
            rx.avatar(
                name="Admin",
                size="3",
                radius="full",
                fallback="A",
            ),
            rx.vstack(
                rx.text(
                    "Admin",
                    size="2",
                    weight="bold",
                    color="white",
                ),
                rx.text(
                    "Administrador",
                    size="1",
                    color="rgba(255,255,255,0.65)",
                ),
                spacing="0",
                align="start",
            ),
            rx.spacer(),
            rx.icon(
                "chevron-right",
                size=16,
                color="rgba(255,255,255,0.45)",
            ),
            width="100%",
            align="center",
            spacing="3",
        ),
        width="100%",
        padding="0.8rem",
        border_radius="0.9rem",
        background="rgba(255,255,255,0.08)",
        border="1px solid rgba(255,255,255,0.08)",
    )


def sidebar():
    return rx.box(
        rx.vstack(
            # =========================
            # Header
            # =========================

            rx.vstack(
                rx.hstack(

                    rx.image(
                        src="/logos/logo security-02.png",
                        width="36px",
                        height="36px",
                        object_fit="contain",
                    ),


                    rx.vstack(
                        rx.heading(
                            "UniAccess",
                            size="5",
                            color="white",
                        ),
                        rx.text(
                            "Control",
                            size="1",
                            color="rgba(255,255,255,0.65)",
                            letter_spacing="0.12em",
                            text_transform="uppercase",
                        ),
                        spacing="0",
                        align="start",
                    ),

                    align="center",
                    spacing="3",
                    width="100%",
                ),

                rx.text(
                    "Sistema de controle de acesso",
                    size="1",
                    color="rgba(255,255,255,0.55)",
                    padding_left="0.25rem",
                ),

                width="100%",
                align="start",
                spacing="3",
            ),

            rx.divider(
                border_color="rgba(255,255,255,0.12)",
                margin_y="1rem",
            ),

            # =========================
            # Navegação principal
            # =========================

            rx.vstack(
                sidebar_section_title("Principal"),

                sidebar_item(
                    label="Dashboard",
                    icon="layout-dashboard",
                    href="/dashboard",
                ),

                sidebar_item(
                    label="Usuários",
                    icon="users",
                    href="/usuarios",
                ),

                sidebar_item(
                    label="Permissões",
                    icon="map-pin",
                    href="/permissoes",
                ),

                sidebar_item(
                    label="Auditoria",
                    icon="file-search",
                    href="/logs",
                ),

                sidebar_item(
                    label="Simulador",
                    icon="scan-line",
                    href="/simulador",
                ),

                spacing="1",
                width="100%",
                align="stretch",
            ),

            rx.spacer(),

            # =========================
            # Rodapé
            # =========================

            rx.vstack(
                rx.divider(
                    border_color="rgba(255,255,255,0.12)",
                    margin_bottom="0.5rem",
                ),

                sidebar_section_title("Usuário"),

                sidebar_user_card(),

                spacing="2",
                width="100%",
                align="stretch",
            ),

            spacing="0",
            align="stretch",
            width="100%",
            height="100%",
            padding="1.25rem",
        ),

        width="270px",
        height="100vh",
        position="sticky",
        top="0",
        background=(
            "linear-gradient(180deg, "
            "#0b1f2f 0%, "
            "#12334a 45%, "
            "#1a3a52 100%)"
        ),
        color="white",
        overflow_y="auto",
        flex_shrink="0",
        box_sizing="border-box",
        border_right="1px solid rgba(255,255,255,0.08)",
        box_shadow="8px 0 30px rgba(0,0,0,0.18)",
    )

def stat_card(titulo: str, valor: int):

    return rx.card(
        rx.vstack(
            rx.text(titulo),
            rx.heading(str(valor), size="8")
        ),
        width="220px"
    )