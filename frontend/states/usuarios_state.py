import os
import sys

import reflex as rx

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controle_acesso.database import BancoDeDados


class UsuariosState(rx.State):
    """Estado usado somente pela página de gestão de usuários."""

    novo_nome: str = ""
    novo_rfid: str = ""
    novo_perfil_id: str = ""
    msg_cadastro: str = ""

    update_id: str = ""
    update_rfid: str = ""
    msg_update: str = ""

    delete_id: str = ""
    msg_delete: str = ""

    def set_novo_nome(self, v: str):
        self.novo_nome = v

    def set_novo_rfid(self, v: str):
        self.novo_rfid = v

    def set_novo_perfil_id(self, v: str):
        self.novo_perfil_id = v

    def set_update_id(self, v: str):
        self.update_id = v

    def set_update_rfid(self, v: str):
        self.update_rfid = v

    def set_delete_id(self, v: str):
        self.delete_id = v

    def registrar_usuario(self):
        db = BancoDeDados()
        try:
            sucesso, msg = db.cadastrar_usuario(
                self.novo_nome,
                self.novo_rfid,
                int(self.novo_perfil_id),
            )
            self.msg_cadastro = msg

            if sucesso:
                self.novo_nome = ""
                self.novo_rfid = ""
                self.novo_perfil_id = ""

        except ValueError:
            self.msg_cadastro = "Erro: o ID do perfil precisa ser um número!"

    def atualizar_tag(self):
        db = BancoDeDados()
        try:
            sucesso, msg = db.atualizar_tag(int(self.update_id), self.update_rfid)
            self.msg_update = msg

            if sucesso:
                self.update_id = ""
                self.update_rfid = ""

        except ValueError:
            self.msg_update = "Erro: ID precisa ser um número!"

    def remover_usuario(self):
        db = BancoDeDados()
        try:
            sucesso, msg = db.remover_usuario(int(self.delete_id))
            self.msg_delete = msg

            if sucesso:
                self.delete_id = ""

        except ValueError:
            self.msg_delete = "Erro: ID precisa ser um número!"
