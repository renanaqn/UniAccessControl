import os
import sys
from datetime import datetime

import reflex as rx

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controle_acesso.database import BancoDeDados


class DashboardState(rx.State):
    """Estado usado pela página principal do dashboard."""

    total_usuarios: int = 0
    total_zonas: int = 0

    acessos_aprovados_hoje: int = 0
    acessos_negados_hoje: int = 0

    ultimos_logs: list[dict] = []

    ultima_atualizacao: str = "Aguardando atualização"
    status_sistema: str = "Carregando"
    status_cor: str = "gray"
    banco_status: str = "Não verificado"
    banco_cor: str = "gray"

    @rx.var
    def total_acessos_hoje(self) -> int:
        return self.acessos_aprovados_hoje + self.acessos_negados_hoje

    @rx.var
    def total_acessos_hoje_label(self) -> str:
        total = self.total_acessos_hoje
        if total == 1:
            return "1 acesso registrado hoje"
        return f"{total} acessos registrados hoje"

    @rx.var
    def percentual_aprovados(self) -> int:
        total = self.total_acessos_hoje
        if total == 0:
            return 0
        return round((self.acessos_aprovados_hoje / total) * 100)

    @rx.var
    def percentual_negados(self) -> int:
        total = self.total_acessos_hoje
        if total == 0:
            return 0
        return round((self.acessos_negados_hoje / total) * 100)

    @rx.var
    def percentual_aprovados_label(self) -> str:
        return f"{self.percentual_aprovados}% dos acessos de hoje"

    @rx.var
    def percentual_negados_label(self) -> str:
        return f"{self.percentual_negados}% dos acessos de hoje"

    @rx.var
    def alerta_acessos_negados(self) -> str:
        if self.total_acessos_hoje == 0:
            return "Nenhum acesso registrado hoje."
        if self.percentual_negados >= 40:
            return "Atenção: há uma quantidade elevada de acessos negados hoje."
        if self.acessos_negados_hoje > 0:
            return "Existem acessos negados registrados hoje. Verifique a aba de auditoria se necessário."
        return "Nenhum acesso negado registrado hoje."

    @rx.var
    def alerta_cor(self) -> str:
        if self.total_acessos_hoje == 0:
            return "gray"
        if self.percentual_negados >= 40:
            return "red"
        if self.acessos_negados_hoje > 0:
            return "orange"
        return "green"

    @rx.var
    def pizza_acessos_background(self) -> str:
        if self.total_acessos_hoje == 0:
            return "conic-gradient(var(--gray-6) 0% 100%)"

        return (
            "conic-gradient("
            f"var(--green-9) 0% {self.percentual_aprovados}%, "
            f"var(--red-9) {self.percentual_aprovados}% 100%"
            ")"
        )

    @rx.var
    def pizza_acessos_centro_label(self) -> str:
        if self.total_acessos_hoje == 0:
            return "0%"
        return f"{self.percentual_aprovados}%"

    def carregar_dados(self):
        """Carrega as informações utilizadas na página principal do dashboard."""
        try:
            db = BancoDeDados()

            self.total_usuarios = db.total_usuarios()
            self.total_zonas = db.total_zonas()
            self.ultimos_logs = db.buscar_ultimos_logs(10)
            self.acessos_aprovados_hoje = db.acessos_permitidos_hoje()
            self.acessos_negados_hoje = db.acessos_negados_hoje()

            self.ultima_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.status_sistema = "Online"
            self.status_cor = "green"
            self.banco_status = "Conectado"
            self.banco_cor = "green"

        except Exception as erro:
            self.status_sistema = "Erro"
            self.status_cor = "red"
            self.banco_status = "Falha na conexão"
            self.banco_cor = "red"
            self.ultima_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"Erro ao carregar dados do dashboard: {erro}")
