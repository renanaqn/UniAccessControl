import os
import sys
from datetime import datetime

import reflex as rx

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controle_acesso.database import BancoDeDados
from controle_acesso.validador import ValidadorAcesso


class SimuladorState(rx.State):
    """Estado usado somente pela página do simulador de acesso."""

    sim_rfid: str = ""
    sim_zona: str = ""
    sim_status: str = "AGUARDANDO LEITURA"
    sim_visor: str = "Aproxime a sua tag RFID..."
    sim_cor_status: str = "gray"

    def set_sim_rfid(self, v: str):
        self.sim_rfid = v

    def set_sim_zona(self, v: str):
        self.sim_zona = v

    def simular_leitura(self):
        """Simula a leitura RFID e registra o resultado no banco."""
        db = BancoDeDados()
        validador = ValidadorAcesso(db)

        try:
            zona_int = int(self.sim_zona)
            hora_agora = datetime.now().strftime("%H:%M:%S")

            resultado = validador.processar_leitura(
                self.sim_rfid,
                zona_int,
                hora_agora,
            )

            self.sim_status = resultado["status"]
            self.sim_visor = resultado["mensagem"]
            self.sim_cor_status = "green" if self.sim_status == "PERMITIDO" else "red"
            self.sim_rfid = ""

        except ValueError:
            self.sim_status = "ERRO"
            self.sim_visor = "O ID da Zona precisa ser numérico!"
            self.sim_cor_status = "orange"
