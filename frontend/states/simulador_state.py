import os
import sys
import asyncio
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
    
    leitura_id: int = 0

    def set_sim_rfid(self, v: str):
        self.sim_rfid = v

    def set_sim_zona(self, v: str):
        self.sim_zona = v
        
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
            zona_int = int(self.sim_zona)
            hora_agora = datetime.now().strftime("%H:%M:%S")

            resultado = validador.processar_leitura(
                self.sim_rfid,
                zona_int,
                hora_agora,
            )

            self.sim_status = resultado["status"]
            self.sim_visor = resultado["mensagem"]
            
            if self.sim_status == "PERMITIDO":
                self.sim_cor_status = "green"
            else:
                self.sim_cor_status = "red"
            
            self.sim_rfid = ""
            
            yield
            
            await asyncio.sleep(3)
            
            if self.leitura_id == leitura_atual:
                self.resetar_simulador()
                yield

        except ValueError:
            self.sim_status = "ERRO"
            self.sim_visor = "O ID da Zona precisa ser numérico!"
            self.sim_cor_status = "orange"
            
            yield
            
            await asyncio.sleep(3)
            
            if self.leitura_id == leitura_atual:
                self.resetar_simulador()
                yield
