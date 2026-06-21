import os
import sys

import math
import reflex as rx

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controle_acesso.database import BancoDeDados


class RegrasState(rx.State):
    regras: list[dict] = []

    pagina_atual: int = 1
    limite: int = 10
    total_registros: int = 0
    
    filtro_perfil: str = "TODOS"
    filtro_zona: str = "Todas"
    filtro_hora_inicio: str = ""
    filtro_hora_fim: str = ""

    perfis: list[str] = ["TODOS"]
    zonas: list[str] = ["Todas"]

    def carregar_pagina(self):
        self.carregar_filtros()
        self.carregar_regras()

    def carregar_filtros(self):
        db = BancoDeDados()

        self.perfis = ["TODOS"] + [
            perfil["nome_perfil"]
            for perfil in db.listar_perfis()
        ]

        self.zonas = ["Todas"] + [
            zona["nome_zona"]
            for zona in db.listar_zonas()
        ]
    
    def normalizar_hora(self, hora: str) -> str:
        if hora and len(hora) == 5:
            return f"{hora}:00"
        return hora

    def carregar_regras(self):
        db = BancoDeDados()

        self.regras = db.listar_regras(
            pagina=self.pagina_atual,
            limite=self.limite,
            perfil=self.filtro_perfil,
            zona=self.filtro_zona,
            hora_inicio=self.normalizar_hora(self.filtro_hora_inicio),
            hora_fim=self.normalizar_hora(self.filtro_hora_fim),
        )

        self.total_registros = db.contar_regras_filtradas(
            perfil=self.filtro_perfil,
            zona=self.filtro_zona,
            hora_inicio=self.filtro_hora_inicio,
            hora_fim=self.filtro_hora_fim,
        )

    def aplicar_filtros(self):
        self.pagina_atual = 1
        self.carregar_regras()

    def limpar_filtros(self):
        self.filtro_perfil = "TODOS"
        self.filtro_zona = "Todas"
        self.filtro_hora_inicio = ""
        self.filtro_hora_fim = ""

        self.pagina_atual = 1
        self.carregar_regras()

    def definir_perfil(self, valor: str):
        self.filtro_perfil = valor
        self.aplicar_filtros()

    def definir_zona(self, valor: str):
        self.filtro_zona = valor
        self.aplicar_filtros()

    def definir_hora_inicio(self, valor: str):
        self.filtro_hora_inicio = valor
        self.aplicar_filtros()

    def definir_hora_fim(self, valor: str):
        self.filtro_hora_fim = valor
        self.aplicar_filtros()

    @rx.var
    def total_paginas(self) -> int:
        if self.total_registros == 0:
            return 1
        return math.ceil(self.total_registros / self.limite)

    @rx.var
    def pagina_label(self) -> str:
        return f"Página {self.pagina_atual} de {self.total_paginas}"

    @rx.var
    def tem_pagina_anterior(self) -> bool:
        return self.pagina_atual > 1

    @rx.var
    def tem_proxima_pagina(self) -> bool:
        return self.pagina_atual < self.total_paginas

    def proxima_pagina(self):
        if self.pagina_atual < self.total_paginas:
            self.pagina_atual += 1
            self.carregar_regras()

    def pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.carregar_regras()

    def primeira_pagina(self):
        self.pagina_atual = 1
        self.carregar_regras()

    def ultima_pagina(self):
        self.pagina_atual = self.total_paginas
        self.carregar_regras()