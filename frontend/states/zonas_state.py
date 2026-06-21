import os
import sys

import reflex as rx
import asyncio

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controle_acesso.database import BancoDeDados


class ZonasState(rx.State):
    """Estado usado somente pela página de zonas e regras de acesso."""

    zonas_lista: list[dict] = []
    perfis_lista: list[dict] = []

    regra_perfil_id: str = ""
    regra_zona_id: str = ""
    
    regra_inicio: str = ""
    regra_fim: str = ""
    msg_regra: str = ""
    
    novo_perfil: str = ""
    nova_zona: str = ""

    msg_perfil: str = ""
    msg_zona: str = ""
    
    def set_novo_perfil(self, v: str):
        self.novo_perfil = v

    def set_nova_zona(self, v: str):
        self.nova_zona = v

    def set_regra_perfil(self, v: str):
        self.regra_perfil_id = v

    def set_regra_zona(self, v: str):
        self.regra_zona_id = v

    def set_regra_inicio(self, v: str):
        self.regra_inicio = v

    def set_regra_fim(self, v: str):
        self.regra_fim = v

    def carregar_dados(self):
        """Carrega zonas e perfis para exibição na página."""
        try:
            db = BancoDeDados()
            self.zonas_lista = db.listar_zonas()
            self.perfis_lista = db.listar_perfis()
        except Exception as erro:
            self.msg_regra = "Erro ao carregar zonas e perfis."
            print(f"Erro ao carregar dados de zonas: {erro}")
            
    async def adicionar_perfil(self):
        """Adiciona um novo perfil ao banco de dados."""
        db = BancoDeDados()

        try:
            sucesso, msg = db.cadastrar_perfil(self.novo_perfil)
            self.msg_perfil = msg

            if sucesso:
                self.novo_perfil = ""
                self.carregar_dados()
                
            yield
            
            await asyncio.sleep(3)
            
            self.msg_perfil = ""
            yield

        except Exception as erro:
            self.msg_perfil = "Erro ao cadastrar perfil."
            print(f"Erro ao cadastrar perfil: {erro}")
            
            yield
            
            await asyncio.sleep(3)
            
            self.msg_perfil = ""
            yield

    async def adicionar_zona(self):
        """Adiciona uma nova zona ao banco de dados."""
        db = BancoDeDados()

        try:
            sucesso, msg = db.cadastrar_zona(self.nova_zona)
            self.msg_zona = msg

            if sucesso:
                self.nova_zona = ""
                self.carregar_dados()
            
            yield
            
            await asyncio.sleep(3)
            
            self.msg_zona = ""
            yield

        except Exception as erro:
            self.msg_zona = "Erro ao cadastrar zona."
            print(f"Erro ao cadastrar zona: {erro}")
            
            yield
            
            await asyncio.sleep(3)
            
            self.msg_zona = ""
            yield

    def salvar_regra(self):
        db = BancoDeDados()
        try:
            sucesso, msg = db.criar_regra_acesso(
                int(self.regra_perfil_id),
                int(self.regra_zona_id),
                self.regra_inicio,
                self.regra_fim,
            )
            self.msg_regra = msg

            if sucesso:
                self.regra_perfil_id = ""
                self.regra_zona_id = ""
                self.regra_inicio = ""
                self.regra_fim = ""
                self.carregar_dados()

        except ValueError:
            self.msg_regra = "Erro: IDs precisam ser números válidos!"
