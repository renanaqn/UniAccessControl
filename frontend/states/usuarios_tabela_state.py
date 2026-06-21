import os
import sys

import math
import reflex as rx

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controle_acesso.database import BancoDeDados


class UsuariosTabelaState(rx.State):
    usuarios: list[dict] = []

    pagina_atual: int = 1
    limite: int = 10
    total_registros: int = 0

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

    def carregar_usuarios(self):
        db = BancoDeDados()

        self.total_registros = db.total_usuarios()
        self.usuarios = db.listar_usuarios(
            pagina=self.pagina_atual,
            limite=self.limite,
        )

    def proxima_pagina(self):
        if self.pagina_atual < self.total_paginas:
            self.pagina_atual += 1
            self.carregar_usuarios()

    def pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.carregar_usuarios()

    def primeira_pagina(self):
        self.pagina_atual = 1
        self.carregar_usuarios()

    def ultima_pagina(self):
        self.pagina_atual = self.total_paginas
        self.carregar_usuarios()