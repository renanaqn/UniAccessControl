import reflex as rx
import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controle_acesso.database import BancoDeDados

class UsuarioState(rx.State):
    # Vazio