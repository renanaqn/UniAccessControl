import reflex as rx
import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controle_acesso.database import BancoDeDados
from controle_acesso.validador import ValidadorAcesso
from datetime import datetime

class DashboardState(rx.State):

    total_usuarios: int = 0
    total_zonas: int = 0

    acessos_aprovados_hoje: int = 0
    acessos_negados_hoje: int = 0

    ultimos_logs: list[dict] = []

    zonas_lista: list[dict] = []
    perfis_lista: list[dict] = []
    
    ultima_atualizacao: str = "Aguardando atualização"
    status_sistema: str = "Carregando"
    status_cor: str = "gray"
    banco_status: str = "Não verificado"
    banco_cor: str = "gray"

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

    sim_rfid: str = ""
    sim_zona: str = ""
    sim_status: str = "AGUARDANDO LEITURA"
    sim_visor: str = "Aproxime a sua tag RFID..."
    sim_cor_status: str = "gray"
    
    # ==========================================
    # VARS CALCULADAS PARA O DASHBOARD
    # ==========================================
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

    def set_sim_rfid(self, v: str): self.sim_rfid = v
    def set_sim_zona(self, v: str): self.sim_zona = v


    def carregar_dados(self):
        """Carrega as informações utilizadas na página principal do dashboard."""

        try:
            db = BancoDeDados()

            self.total_usuarios = db.total_usuarios()
            self.total_zonas = db.total_zonas()

            self.ultimos_logs = db.buscar_ultimos_logs(10)

            self.acessos_aprovados_hoje = db.acessos_permitidos_hoje()
            self.acessos_negados_hoje = db.acessos_negados_hoje()

            self.zonas_lista = db.listar_zonas()
            self.perfis_lista = db.listar_perfis()

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

    def simular_leitura(self):
        """Atua como o microcontrolador lendo o sensor e enviando ao DB"""
        db = BancoDeDados()
        validador = ValidadorAcesso(db)
        try:
            zona_int = int(self.sim_zona)

            hora_agora = datetime.now().strftime('%H:%M:%S')
            
            resultado = validador.processar_leitura(self.sim_rfid, zona_int, hora_agora)
            
            self.sim_status = resultado['status']
            self.sim_visor = resultado['mensagem']
            
            if self.sim_status == "PERMITIDO":
                self.sim_cor_status = "green"
            else:
                self.sim_cor_status = "red"
                
            self.sim_rfid = ""
            
            # Recarrega os dados para que a aba de Logs saiba da nova entrada
            self.carregar_dados()
            
        except ValueError:
            self.sim_status = "ERRO"
            self.sim_visor = "O ID da Zona precisa ser alfanumérico!"
            self.sim_cor_status = "orange"
