import reflex as rx
import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controle_acesso.database import BancoDeDados

class DashboardState(rx.State):

    total_usuarios: int = 0
    total_zonas: int = 0

    acessos_aprovados_hoje: int = 0
    acessos_negados_hoje: int = 0

    ultimos_logs: list[dict] = []

    zonas_lista: list[dict] = []
    perfis_lista: list[dict] = []

    novo_nome: str = ""
    novo_rfid: str = ""
    novo_perfil_id: str = ""
    msg_cadastro: str = ""

    update_id: str = ""
    update_rfid: str = ""
    msg_update: str = ""

    delete_id: str = ""
    msg_delete: str = ""

    regra_perfil_id: str = ""
    regra_zona_id: str = ""
    regra_inicio: str = ""
    regra_fim: str = ""
    msg_regra: str = ""


    # ==========================================
    # SETTERS EXPLÍCITOS (Evita o erro do Python 3.13)
    # ==========================================
    def set_novo_nome(self, v: str): self.novo_nome = v
    def set_novo_rfid(self, v: str): self.novo_rfid = v
    def set_novo_perfil_id(self, v: str): self.novo_perfil_id = v
    
    def set_update_id(self, v: str): self.update_id = v
    def set_update_rfid(self, v: str): self.update_rfid = v
    
    def set_delete_id(self, v: str): self.delete_id = v
    
    def set_regra_perfil(self, v: str): self.regra_perfil_id = v
    def set_regra_zona(self, v: str): self.regra_zona_id = v
    def set_regra_inicio(self, v: str): self.regra_inicio = v
    def set_regra_fim(self, v: str): self.regra_fim = v
    # ==========================================


    def carregar_dados(self):

        db = BancoDeDados()

        self.total_usuarios = db.total_usuarios()
        self.total_zonas = db.total_zonas()

        self.ultimos_logs = db.buscar_ultimos_logs(10)

        self.acessos_aprovados_hoje = db.acessos_permitidos_hoje()
        self.acessos_negados_hoje = db.acessos_negados_hoje()

        self.zonas_lista = db.listar_zonas()
        self.perfis_lista = db.listar_perfis()

    def registrar_usuario(self):
        db = BancoDeDados()
        try:
            sucesso, msg = db.cadastrar_usuario(self.novo_nome, self.novo_rfid, int(self.novo_perfil_id))
            self.msg_cadastro = msg
            if sucesso:
                self.novo_nome = self.novo_rfid = self.novo_perfil_id = ""
                self.carregar_dados()
        except ValueError:
            self.msg_cadastro = "Erro: ID e Perfil precisam ser números!"
    
    def atualizar_tag(self):
        db = BancoDeDados()
        try:
            sucesso, msg = db.atualizar_tag(int(self.update_id), self.update_rfid)
            self.msg_update = msg
            if sucesso: self.update_id = self.update_rfid = ""
        except ValueError:
            self.msg_update = "Erro: ID precisa ser um número!"

    def remover_usuario(self):
        db = BancoDeDados()
        try:
            sucesso, msg = db.remover_usuario(int(self.delete_id))
            self.msg_delete = msg
            if sucesso:
                self.delete_id = ""
                self.carregar_dados()
        except ValueError:
            self.msg_delete = "Erro: ID precisa ser um número!"

    def salvar_regra(self):
        db = BancoDeDados()
        try:
            sucesso, msg = db.criar_regra_acesso(int(self.regra_perfil_id), int(self.regra_zona_id), self.regra_inicio, self.regra_fim)
            self.msg_regra = msg
            if sucesso:
                self.regra_perfil_id = self.regra_zona_id = self.regra_inicio = self.regra_fim = ""
        except ValueError:
            self.msg_regra = "Erro: IDs precisam ser números válidos!"

