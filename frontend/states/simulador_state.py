import os
import sys
import asyncio
from datetime import datetime

import reflex as rx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controle_acesso.database import BancoDeDados
from controle_acesso.validador import ValidadorAcesso


class SimuladorState(rx.State):
    """Estado usado somente pela página do simulador de acesso."""

    # Usuário visual
    sim_usuario_nome: str = ""
    usuarios_sugeridos: list[dict] = []

    # RFID usada internamente pelo validador
    sim_rfid: str = ""

    # Zona visual
    sim_zona_nome: str = ""
    zonas_lista: list[dict] = []
    zonas_opcoes: list[str] = []

    sim_status: str = "AGUARDANDO LEITURA"
    sim_visor: str = "Aproxime a sua tag RFID..."
    sim_cor_status: str = "gray"

    leitura_id: int = 0

    def carregar_dados(self):
        """Carrega as zonas disponíveis para o menu drop-down."""
        try:
            db = BancoDeDados()

            self.zonas_lista = db.listar_zonas()
            self.zonas_opcoes = [
                zona["nome_zona"]
                for zona in self.zonas_lista
            ]

        except Exception as erro:
            self.sim_status = "ERRO"
            self.sim_visor = "Erro ao carregar dados do simulador."
            self.sim_cor_status = "orange"
            print(f"Erro ao carregar dados no simulador: {erro}")

    def set_sim_zona_nome(self, v: str):
        self.sim_zona_nome = v

    def definir_usuario(self, nome: str):
        """
        Gera sugestões de usuários a partir do nome parcial.
        """

        self.sim_usuario_nome = nome
        self.sim_rfid = ""

        if nome.strip() == "":
            self.usuarios_sugeridos = []
            return

        if len(nome) < 2:
            self.usuarios_sugeridos = []
            return

        db = BancoDeDados()
        self.usuarios_sugeridos = db.buscar_usuarios_com_rfid_por_nome(nome)

    def selecionar_usuario(self, nome: str, rfid_tag: str, nome_perfil: str):
        self.sim_usuario_nome = f"{nome} | {nome_perfil}"
        self.sim_rfid = rfid_tag
        self.usuarios_sugeridos = []

    def obter_zona_id_selecionada(self):
        """Retorna o ID da zona selecionada pelo nome."""

        for zona in self.zonas_lista:
            if zona["nome_zona"] == self.sim_zona_nome:
                return zona["id"]

        return None

    def resetar_simulador(self):
        self.sim_status = "AGUARDANDO LEITURA"
        self.sim_visor = "Aproxime a sua tag RFID..."
        self.sim_cor_status = "gray"

    async def simular_leitura(self):
        """Simula a leitura RFID e registra o resultado no banco."""
        db = BancoDeDados()
        validador = ValidadorAcesso(db)

        self.leitura_id += 1
        leitura_atual = self.leitura_id

        try:
            zona_id = self.obter_zona_id_selecionada()

            if zona_id is None:
                self.sim_status = "ERRO"
                self.sim_visor = "Selecione uma zona válida."
                self.sim_cor_status = "orange"

                yield
                await asyncio.sleep(3)

                if self.leitura_id == leitura_atual:
                    self.resetar_simulador()
                    yield

                return

            if not self.sim_rfid:
                self.sim_status = "ERRO"
                self.sim_visor = "Selecione um usuário válido."
                self.sim_cor_status = "orange"

                yield
                await asyncio.sleep(3)

                if self.leitura_id == leitura_atual:
                    self.resetar_simulador()
                    yield

                return

            hora_agora = datetime.now().strftime("%H:%M:%S")

            resultado = validador.processar_leitura(
                self.sim_rfid,
                int(zona_id),
                hora_agora,
            )

            self.sim_status = resultado["status"]
            self.sim_visor = resultado["mensagem"]

            if self.sim_status == "PERMITIDO":
                self.sim_cor_status = "green"
            else:
                self.sim_cor_status = "red"

            self.sim_usuario_nome = ""
            self.sim_rfid = ""

            yield
            await asyncio.sleep(3)

            if self.leitura_id == leitura_atual:
                self.resetar_simulador()
                yield

        except Exception as erro:
            self.sim_status = "ERRO"
            self.sim_visor = "Erro ao processar a leitura."
            self.sim_cor_status = "orange"
            print(f"Erro no simulador: {erro}")

            yield
            await asyncio.sleep(3)

            if self.leitura_id == leitura_atual:
                self.resetar_simulador()
                yield