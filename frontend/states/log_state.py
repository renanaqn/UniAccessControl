import reflex as rx
import sys
import os
from datetime import datetime

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controle_acesso.database import BancoDeDados

class LogState(rx.State):
    # =====================
    # Dados exibidos na tabela
    # =====================
    
    logs: list[dict] = []
    
    # =====================
    # Paginacao
    # =====================
    
    pagina: int = 1
    limite: int = 25
    total_paginas: int = 1
    
    # =====================
    # Filtros
    # =====================
    
    filtro_usuario: str = ""
    filtro_zona: str = "Todas"
    filtro_resultado: str = "TODOS"
    
    filtro_data_inicio: str = ""
    filtro_data_fim: str = ""
    
    ultima_atualizacao: str = "Aguardando atualização"
    banco_status: str = "Não verificado"
    banco_cor: str = "gray"
    
    # =====================
    # Opções de Filtros
    # =====================
    
    zonas: list[str] = []
    resultados: list[str] = [
        "TODOS",
        "PERMITIDO",
        "NEGADO"
    ]
    usuarios_sugeridos: list[str] = []
    
    # =====================
    # Inicialização
    # =====================
    
    def carregar_pagina(self):
        """
        Executado quando a página é aberta.
        """
        
        self.carregar_filtros()
        self.carregar_logs()
    
    def carregar_filtros(self):
        db = BancoDeDados()
        
        self.zonas = ["Todas"] + [
            zona["nome_zona"]
            for zona in db.listar_zonas()
        ]
    
    # =====================    
    # Busca de Logs
    # =====================
    
    def carregar_logs(self):
        """
        Carrega os logs utilizando os filtros atuais
        """
        
        db = BancoDeDados()
        
        try:
            self.logs = db.buscar_logs(
                pagina=self.pagina,
                limite=self.limite,
                usuario=self.filtro_usuario,
                zona=self.filtro_zona,
                resultado=self.filtro_resultado,
                data_inicio=self.filtro_data_inicio or None,
                data_fim=self.filtro_data_fim or None,
            )
            
            total = db.contar_logs(
                usuario=self.filtro_usuario,
                zona=self.filtro_zona,
                resultado=self.filtro_resultado,
                data_inicio=self.filtro_data_inicio or None,
                data_fim=self.filtro_data_fim or None,
            )
            
            self.total_paginas = max(
                1,
                (total + self.limite - 1) // self.limite
            )
            
            self.zonas = ["Todas"] + [
                zona["nome_zona"] 
                for zona in db.listar_zonas()
            ]
            
            self.ultima_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.banco_status = "Conectado"
            self.banco_cor = "green"
        
        except Exception as erro:
            self.banco_status = "Falha na conexão"
            self.banco_cor = "red"
            self.ultima_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"Erro ao carregar logs de auditoria: {erro}")
    
    # =====================
    # Filtros
    # =====================
    
    def aplicar_filtros(self):
        """
        Reinicia para primira página e reaplica os filtros.
        """
        
        self.pagina = 1
        
        self.carregar_logs()
    
    def limpar_filtros(self):
        """
        Remove todos os filtros
        """
        
        self.filtro_usuario = ""
        self.filtro_zona = "Todas"
        self.filtro_resultado = "TODOS"
        
        self.filtro_data_inicio = ""
        self.filtro_data_fim = ""
        
        self.pagina = 1
        
        self.carregar_logs()
        
    # =====================
    # Usuário (autocomplete)
    # =====================
    
    def definir_usuario(self, nome: str):
        """
        Gera os usuários apartir do nome parcial
        """
        
        self.filtro_usuario = nome
        
        if nome.strip() == "":
            self.usuarios_sugeridos = []
            self.aplicar_filtros()
            return
        
        if len(nome) < 2:
            self.usuarios_sugeridos = []
            return
        
        db = BancoDeDados()
        
        self.usuarios_sugeridos = (
            db.buscar_usuarios_por_nome(nome)
        )
    
    def selecionar_usuario(self, nome: str):
        """
        Seleciona um usuário do dropdown
        """
        
        self.filtro_usuario = nome

        self.usuarios_sugeridos = []

        self.aplicar_filtros()
        
    # =====================
    # Zona
    # =====================
    
    def definir_zona(self, valor: str):
        self.filtro_zona = valor
        
        self.aplicar_filtros()
        
    # =====================
    # Resultado
    # =====================
    
    def definir_resultado(self, valor: str):
        self.filtro_resultado = valor
        
        self.aplicar_filtros()
    
    # =====================
    # Datas
    # =====================
    
    def definir_data_inicio(self, valor: str):
        self.filtro_data_inicio = valor
        
        self.aplicar_filtros()
    
    def definir_data_fim(self, valor: str):
        self.filtro_data_fim = valor
        
        self.aplicar_filtros()
    
    # =====================
    # Paginação
    # =====================
    
    def proxima_pagina(self):
        """
        Avança para próxima página.
        """
        
        if self.pagina < self.total_paginas:
            self.pagina += 1
            self.carregar_logs()
    
    def pagina_anterior(self):
        """
        Volta para página anterior.
        """
        
        if self.pagina > 1:
            self.pagina -= 1
            self.carregar_logs()
            
    # =====================
    # Propriedades
    # =====================

    @rx.var
    def pagina_texto(self) -> str:
        return f"Página {self.pagina} de {self.total_paginas}"
    
    @rx.var
    def possui_proxima_pagina(self) -> bool:
        return self.pagina < self.total_paginas
    
    @rx.var
    def possui_pagina_anterior(self) -> bool:
        return self.pagina > 1