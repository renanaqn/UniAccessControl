import reflex as rx

from components.layout import page_layout
from states.zonas_state import ZonasState


def zonas_header():
    return rx.card(
        rx.hstack(
            rx.hstack(
                rx.badge(
                    rx.icon("map-pin", size=36),
                    color_scheme="purple",
                    variant="soft",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.heading("Zonas e Permissões", size="7"),
                    rx.text(
                        "Defina regras de acesso, horários permitidos e permissões por perfil.",
                        color_scheme="gray",
                        size="3",
                    ),
                    spacing="1",
                    align="start",
                ),
                align="center",
                spacing="4",
            ),

            rx.spacer(),

            rx.link(
                rx.button(
                    rx.icon("table", size=16),
                    "Ver regras cadastradas",
                    variant="soft",
                    color_scheme="purple",
                ),
                href="/zonas/regras",
            ),

            width="100%",
            align="center",
            spacing="4",
            wrap="wrap",
        ),

        width="100%",
        variant="surface",
    )


def campo_regra(label: str, placeholder: str, value, on_change, icon: str):
    return rx.vstack(
        rx.text(
            label,
            size="2",
            weight="medium",
            color_scheme="gray",
        ),
        rx.input(
            rx.input.slot(
                rx.icon(icon, size=16),
            ),
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            width="100%",
            size="3",
        ),
        width="100%",
        align="start",
        spacing="1",
    )


def feedback_regra():
    return rx.cond(
        ZonasState.msg_regra != "",
        rx.callout(
            ZonasState.msg_regra,
            icon="info",
            color_scheme="indigo",
            variant="soft",
            width="100%",
            margin_top="0.5rem",
        ),
        rx.fragment(),
    )


def regras_horario():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon("clock", size=20),
                    color_scheme="indigo",
                    variant="soft",
                    radius="full",
                    padding="0.55rem",
                ),
                rx.vstack(
                    rx.heading(
                        "Controle de Regras de Horário",
                        size="5",
                    ),
                    rx.text(
                        "Associe um perfil a uma zona e defina o intervalo permitido.",
                        size="2",
                        color_scheme="gray",
                    ),
                    spacing="0",
                    align="start",
                ),
                align="center",
                spacing="3",
                width="100%",
            ),

            rx.divider(),

            rx.callout(
                "Inserir uma regra já existente pode atualizar os horários configurados.",
                icon="info",
                color_scheme="indigo",
                variant="soft",
                width="100%",
            ),

            campo_regra(
                label="Perfil",
                placeholder="ID do perfil, ex: 1",
                value=ZonasState.regra_perfil_id,
                on_change=ZonasState.set_regra_perfil,
                icon="shield-check",
            ),

            campo_regra(
                label="Zona",
                placeholder="ID da zona, ex: 10",
                value=ZonasState.regra_zona_id,
                on_change=ZonasState.set_regra_zona,
                icon="map-pin",
            ),

            rx.flex(
                campo_regra(
                    label="Horário inicial",
                    placeholder="HH:MM:SS",
                    value=ZonasState.regra_inicio,
                    on_change=ZonasState.set_regra_inicio,
                    icon="clock-3",
                ),
                campo_regra(
                    label="Horário final",
                    placeholder="HH:MM:SS",
                    value=ZonasState.regra_fim,
                    on_change=ZonasState.set_regra_fim,
                    icon="clock-9",
                ),
                spacing="3",
                width="100%",
                wrap="wrap",
            ),

            rx.button(
                rx.icon("save", size=16),
                "Salvar regra de acesso",
                on_click=ZonasState.salvar_regra,
                color_scheme="indigo",
                width="100%",
                size="3",
                margin_top="0.5rem",
            ),

            feedback_regra(),

            width="100%",
            spacing="4",
        ),
        width="100%",
        min_width="320px",
        max_width="520px",
        flex="1.4",
        variant="surface",
    )


def mostrar_zona(zona: dict):
    return rx.hstack(
        rx.badge(
            rx.icon("door-open", size=14),
            color_scheme="purple",
            variant="soft",
            radius="full",
        ),
        rx.vstack(
            rx.text(
                zona["nome_zona"],
                size="3",
                weight="medium",
            ),
            rx.text(
                f"ID da zona: {zona['id']}",
                size="1",
                color_scheme="gray",
            ),
            spacing="0",
            align="start",
        ),
        width="100%",
        align="center",
        spacing="3",
        padding="0.65rem",
        border_radius="0.75rem",
        _hover={
            "background": "var(--gray-3)",
        },
    )


def mostrar_perfil(perfil: dict):
    return rx.hstack(
        rx.badge(
            rx.icon("user-check", size=14),
            color_scheme="green",
            variant="soft",
            radius="full",
        ),
        rx.vstack(
            rx.text(
                perfil["nome_perfil"],
                size="3",
                weight="medium",
            ),
            rx.text(
                f"ID do perfil: {perfil['id']}",
                size="1",
                color_scheme="gray",
            ),
            spacing="0",
            align="start",
        ),
        width="100%",
        align="center",
        spacing="3",
        padding="0.65rem",
        border_radius="0.75rem",
        _hover={
            "background": "var(--gray-3)",
        },
    )


def lista_card(
    titulo: str,
    subtitulo: str,
    icon: str,
    color_scheme: str,
    conteudo,
):
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(icon, size=20),
                    color_scheme=color_scheme,
                    variant="soft",
                    radius="full",
                    padding="0.55rem",
                ),
                rx.vstack(
                    rx.heading(titulo, size="5"),
                    rx.text(
                        subtitulo,
                        size="2",
                        color_scheme="gray",
                    ),
                    spacing="0",
                    align="start",
                ),
                width="100%",
                align="center",
                spacing="3",
            ),

            rx.divider(),

            rx.box(
                conteudo,
                width="100%",
                max_height="360px",
                overflow_y="auto",
                padding_right="0.25rem",
            ),

            width="100%",
            spacing="4",
        ),
        width="100%",
        min_width="260px",
        flex="1",
        variant="surface",
    )


def zonas_cadastradas():
    return lista_card(
        titulo="Zonas Cadastradas",
        subtitulo="Áreas controladas pelo sistema.",
        icon="map",
        color_scheme="purple",
        conteudo=rx.vstack(
            rx.foreach(ZonasState.zonas_lista, mostrar_zona),
            width="100%",
            align="stretch",
            spacing="1",
        ),
    )


def perfis_existentes():
    return lista_card(
        titulo="Perfis Existentes",
        subtitulo="Grupos usados nas regras de acesso.",
        icon="users",
        color_scheme="green",
        conteudo=rx.vstack(
            rx.foreach(ZonasState.perfis_lista, mostrar_perfil),
            width="100%",
            align="stretch",
            spacing="1",
        ),
    )


def zonas_page():
    return rx.box(
        page_layout(
            rx.vstack(
                
                # =========================
                # Header
                # =========================
                
                zonas_header(),

                rx.flex(
                    
                    # =========================
                    # Regras
                    # =========================
                    
                    regras_horario(),
                    rx.vstack(
                        
                        # =========================
                        # Zonas/Perfis Cadastrados
                        # =========================
                        
                        perfis_existentes(),
                        zonas_cadastradas(),
                        
                        width="100%",
                        min_width="300px",
                        flex="1",
                        spacing="5",
                    ),

                    spacing="5",
                    wrap="wrap",
                    width="100%",
                    align="stretch",
                ),

                width="100%",
                spacing="6",
                align="start",
            )
        )
    )