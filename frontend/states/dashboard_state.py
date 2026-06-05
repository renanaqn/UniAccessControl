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

    def carregar_dados(self):

        db = BancoDeDados()

        self.total_usuarios = db.total_usuarios()
        self.total_zonas = db.total_zonas()

        self.ultimos_logs = db.buscar_ultimos_logs(10)

        self.acessos_aprovados_hoje = db.acessos_permitidos_hoje()
        self.acessos_negados_hoje = db.acessos_negados_hoje()