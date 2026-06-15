# Esse Script tem o objetivo de Simular acessos contínuos no sistema para os usuários cadastrados.

import random
import time
from datetime import datetime

from database import BancoDeDados
from validador import ValidadorAcesso

# Inicialização
db = BancoDeDados()
validador = ValidadorAcesso(db)

def gerar_tag_desconhecida():
    """
    Retorna uma tag desconhecida aleatória
    """
    
    caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    return "".join(
        random.choice(caracteres)
        for _ in range(8)
    )

def criar_indice_regras(regras):
    regras_por_perfil = {}

    for regra in regras:
        perfil = regra["perfil_id"]
        
        if perfil not in regras_por_perfil:
            regras_por_perfil[perfil] = []
        
        regras_por_perfil[perfil].append(regra)
    
    return regras_por_perfil

def gerar_acesso_permitido(usuarios, regras_por_perfil):
    usuario = random.choice(usuarios)
    
    regras_usuario = regras_por_perfil.get(
        usuario["perfil_id"],
        []
    )
    
    regra = random.choice(regras_usuario)
    
    return (
        usuario["rfid_tag"],
        regra["zona_id"],
        "12:00:00"
    )

def gerar_sem_permissao(usuarios, zonas, regras_por_perfil):
    while True:
        usuario = random.choice(usuarios)
        
        zonas_permitidas = {
            regra["zona_id"]
            for regra in regras_por_perfil.get(
                usuario["perfil_id"],
                []
            )
        }
        
        zonas_negadas = [
            zona["id"]
            for zona in zonas
            if zona["id"] not in zonas_permitidas
        ]
        
        if zonas_negadas:
            zona = random.choice(zonas_negadas)
        
        return (
            usuario["rfid_tag"],
            zona,
            "12:00:00"
        )

def gerar_fora_horario(usuarios, regras_por_perfil):
    usuario = random.choice(usuarios)
    
    regras_usuario = regras_por_perfil.get(
        usuario["perfil_id"],
        []
    )
    
    regra = random.choice(regras_usuario)
    
    return (
        usuario["rfid_tag"],
        regra["zona_id"],
        "03:00:00"
    )
    
def gerar_tag_invalida(zonas):
    return (
        gerar_tag_desconhecida(),
        random.choice(zonas)["id"],
        "12:00:00"
    )

def executar():
    """
    Realiza simulação contínua de acesso
    """
    
    print("Carregando usuários...")
    usuarios = db.listar_usuarios()
    
    print("Carregando zonas...")
    zonas = db.listar_zonas()
    
    print("Carregando Regras...")
    regras = db.listar_regras()
    
    regras_por_perfil = criar_indice_regras(regras)
    
    print()
    print("=" * 50)
    print("SIMULADOR DE ACESSOS INICIADO")
    print(f"Usuários: {len(usuarios)}")
    print(f"Zonas: {len(zonas)}")
    print(f"Regras: {len(regras)}")
    print("=" * 50)
    print()
    
    while True:

        sorteio = random.randint(1, 100)

        # 70%
        if sorteio <= 70:

            tipo = "PERMITIDO"

            rfid, zona, horario = (
                gerar_acesso_permitido(
                    usuarios,
                    regras_por_perfil
                )
            )

        # 20%
        elif sorteio <= 90:

            tipo = "SEM PERMISSAO"

            rfid, zona, horario = (
                gerar_sem_permissao(
                    usuarios,
                    zonas,
                    regras_por_perfil
                )
            )

        # 5%
        elif sorteio <= 95:

            tipo = "FORA HORARIO"

            rfid, zona, horario = (
                gerar_fora_horario(
                    usuarios,
                    regras_por_perfil
                )
            )

        # 5%
        else:

            tipo = "TAG INVALIDA"

            rfid, zona, horario = (
                gerar_tag_invalida(
                    zonas
                )
            )

        resultado = validador.processar_leitura(
            rfid_tag=rfid,
            zona_id=zona,
            hora_atual_str=horario
        )

        print(
            f"[{tipo}] "
            f"RFID={rfid} | "
            f"Zona={zona} | "
            f"Resultado={resultado['status']} | "
            f"{resultado['mensagem']}"
        )

        time.sleep(
            random.uniform(0.5, 2.0)
        )

if __name__ == "__main__":   
    executar()