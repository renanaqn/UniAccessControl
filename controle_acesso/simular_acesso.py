# Esse script simula acessos contínuos no sistema para os usuários cadastrados.

import random
import time
from typing import Optional

from database import BancoDeDados
from validador import ValidadorAcesso


# Inicialização
db = BancoDeDados()
validador = ValidadorAcesso(db)


def gerar_tag_desconhecida() -> str:
    """Retorna uma tag RFID desconhecida aleatória."""

    caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    return "".join(
        random.choice(caracteres)
        for _ in range(8)
    )


def carregar_todos_usuarios(limite: int = 100):
    """
    Carrega todos os usuários do banco.

    Compatível com duas versões de database.py:
    1. listar_usuarios() sem paginação.
    2. listar_usuarios(pagina, limite, nome, rfid, perfil) com paginação/filtros.
    """

    usuarios = []

    try:
        pagina = 1

        while True:
            lote = db.listar_usuarios(
                pagina=pagina,
                limite=limite,
                nome="",
                rfid="",
                perfil="TODOS",
            )

            if not lote:
                break

            usuarios.extend(lote)

            if len(lote) < limite:
                break

            pagina += 1

        return usuarios

    except TypeError:
        # Compatibilidade com a versão antiga:
        # def listar_usuarios(self)
        return db.listar_usuarios()


def carregar_todas_regras(limite: int = 100):
    """
    Carrega todas as regras do banco.

    Compatível com duas versões de database.py:
    1. listar_regras() sem paginação.
    2. listar_regras(pagina, limite, perfil, zona, hora_inicio, hora_fim)
       com paginação/filtros.
    """

    regras = []

    try:
        pagina = 1

        while True:
            lote = db.listar_regras(
                pagina=pagina,
                limite=limite,
                perfil="TODOS",
                zona="Todas",
                hora_inicio="",
                hora_fim="",
            )

            if not lote:
                break

            regras.extend(lote)

            if len(lote) < limite:
                break

            pagina += 1

        return regras

    except TypeError:
        # Compatibilidade com a versão antiga:
        # def listar_regras(self)
        return db.listar_regras()


def criar_indice_regras(regras):
    """Agrupa as regras de acesso por perfil_id."""

    regras_por_perfil = {}

    for regra in regras:
        perfil_id = regra["perfil_id"]

        if perfil_id not in regras_por_perfil:
            regras_por_perfil[perfil_id] = []

        regras_por_perfil[perfil_id].append(regra)

    return regras_por_perfil


def usuarios_com_regras(usuarios, regras_por_perfil):
    """Retorna apenas usuários cujo perfil possui pelo menos uma regra."""

    return [
        usuario
        for usuario in usuarios
        if regras_por_perfil.get(usuario["perfil_id"])
    ]


def gerar_acesso_permitido(usuarios, regras_por_perfil):
    """
    Gera um acesso que deve ser permitido.

    Escolhe um usuário cujo perfil possui regra de acesso e escolhe uma
    zona permitida para esse perfil.
    """

    candidatos = usuarios_com_regras(usuarios, regras_por_perfil)

    if not candidatos:
        return None

    usuario = random.choice(candidatos)
    regras_usuario = regras_por_perfil[usuario["perfil_id"]]
    regra = random.choice(regras_usuario)

    return (
        usuario["rfid_tag"],
        regra["zona_id"],
        "12:00:00",
    )


def gerar_sem_permissao(usuarios, zonas, regras_por_perfil):
    """
    Gera um acesso negado por falta de permissão.

    Escolhe um usuário e tenta encontrar uma zona que não esteja permitida
    para o perfil dele.
    """

    if not usuarios or not zonas:
        return None

    usuarios_embaralhados = usuarios[:]
    random.shuffle(usuarios_embaralhados)

    for usuario in usuarios_embaralhados:
        zonas_permitidas = {
            regra["zona_id"]
            for regra in regras_por_perfil.get(usuario["perfil_id"], [])
        }

        zonas_negadas = [
            zona["id"]
            for zona in zonas
            if zona["id"] not in zonas_permitidas
        ]

        if zonas_negadas:
            zona_id = random.choice(zonas_negadas)

            return (
                usuario["rfid_tag"],
                zona_id,
                "12:00:00",
            )

    # Nenhum usuário tinha zona negada disponível.
    return None


def gerar_fora_horario(usuarios, regras_por_perfil):
    """
    Gera um acesso negado por horário.

    Escolhe uma regra válida de zona, mas utiliza um horário fora do intervalo
    esperado. Esse horário precisa estar fora das regras cadastradas para ter
    o efeito desejado.
    """

    candidatos = usuarios_com_regras(usuarios, regras_por_perfil)

    if not candidatos:
        return None

    usuario = random.choice(candidatos)
    regras_usuario = regras_por_perfil[usuario["perfil_id"]]
    regra = random.choice(regras_usuario)

    return (
        usuario["rfid_tag"],
        regra["zona_id"],
        "03:00:00",
    )


def gerar_tag_invalida(zonas):
    """Gera uma tentativa com tag RFID desconhecida."""

    if not zonas:
        return None

    return (
        gerar_tag_desconhecida(),
        random.choice(zonas)["id"],
        "12:00:00",
    )


def escolher_tentativa(usuarios, zonas, regras_por_perfil):
    """
    Escolhe uma tentativa de acesso.

    Retorna:
        tipo, rfid, zona_id, horario

    Caso a tentativa escolhida não seja possível com os dados atuais do banco,
    tenta outra categoria.
    """

    geradores = [
        ("PERMITIDO", 70, lambda: gerar_acesso_permitido(usuarios, regras_por_perfil)),
        ("SEM PERMISSAO", 20, lambda: gerar_sem_permissao(usuarios, zonas, regras_por_perfil)),
        ("FORA HORARIO", 5, lambda: gerar_fora_horario(usuarios, regras_por_perfil)),
        ("TAG INVALIDA", 5, lambda: gerar_tag_invalida(zonas)),
    ]

    # Expande a lista com pesos simples.
    tipos_ponderados = []
    for tipo, peso, gerador in geradores:
        tipos_ponderados.extend([(tipo, gerador)] * peso)

    # Tenta algumas vezes para evitar falha quando uma categoria não for possível.
    for _ in range(20):
        tipo, gerador = random.choice(tipos_ponderados)
        tentativa = gerador()

        if tentativa is not None:
            rfid, zona_id, horario = tentativa
            return tipo, rfid, zona_id, horario

    return None


def executar():
    """Realiza a simulação contínua de acessos."""

    print("Carregando usuários...")
    usuarios = carregar_todos_usuarios()

    print("Carregando zonas...")
    zonas = db.listar_zonas()

    print("Carregando regras...")
    regras = carregar_todas_regras()

    regras_por_perfil = criar_indice_regras(regras)

    print()
    print("=" * 50)
    print("SIMULADOR DE ACESSOS INICIADO")
    print(f"Usuários: {len(usuarios)}")
    print(f"Zonas: {len(zonas)}")
    print(f"Regras: {len(regras)}")
    print("=" * 50)
    print()

    if not usuarios:
        print("Nenhum usuário cadastrado. Cadastre usuários antes de iniciar a simulação.")
        return

    if not zonas:
        print("Nenhuma zona cadastrada. Cadastre zonas antes de iniciar a simulação.")
        return

    if not regras:
        print("Nenhuma regra cadastrada. A simulação continuará apenas com tentativas inválidas/negadas.")
        print()

    while True:
        tentativa = escolher_tentativa(
            usuarios,
            zonas,
            regras_por_perfil,
        )

        if tentativa is None:
            print("Não foi possível gerar uma tentativa com os dados atuais do banco.")
            time.sleep(2)
            continue

        tipo, rfid, zona_id, horario = tentativa

        resultado = validador.processar_leitura(
            rfid_tag=rfid,
            zona_id=zona_id,
            hora_atual_str=horario,
        )

        print(
            f"[{tipo}] "
            f"RFID={rfid} | "
            f"Zona={zona_id} | "
            f"Horário={horario} | "
            f"Resultado={resultado['status']} | "
            f"{resultado['mensagem']}"
        )

        time.sleep(
            random.uniform(0.5, 2.0)
        )


if __name__ == "__main__":
    executar()
