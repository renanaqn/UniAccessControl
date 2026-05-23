import unittest
from unittest.mock import MagicMock
from datetime import timedelta
from validador import ValidadorAcesso

class TestValidadorAcesso(unittest.TestCase):
    def setUp(self):
        # Cria um Mock para isolar o teste
        self.mock_db = MagicMock()
        # Injeta o banco falso no validador
        self.validador = ValidadorAcesso(self.mock_db)

    def test_acesso_permitido_dentro_do_horario(self):
        # Prepara o mock para simular o banco retornando a Ana Maria
        self.mock_db.buscar_permissao.return_value = {
            'usuario_id': 5,
            'nome': 'Ana Maria',
            'hora_inicio': timedelta(hours=7),
            'hora_fim': timedelta(hours=22)
        }
        
        # Executa a ação
        resultado = self.validador.processar_leitura('A1B2C3D4', 10, '10:30:00')
        
        # Verifica se o resultado foi o esperado
        self.assertEqual(resultado['status'], 'PERMITIDO')
        self.assertIn('Bem-vindo', resultado['mensagem'])
        
        # Verifica se o sistema gravou o log corretamente na auditoria
        self.mock_db.registrar_log.assert_called_once_with(
            5, 'A1B2C3D4', 10, 'PERMITIDO', 'Acesso autorizado'
        )

    def test_acesso_negado_tag_desconhecida(self):
        # Prepara o mock para simular que não achou a tag no banco
        self.mock_db.buscar_permissao.return_value = None
        
        resultado = self.validador.processar_leitura('TAG_FALSA', 10, '10:30:00')
        
        self.assertEqual(resultado['status'], 'NEGADO')
        self.mock_db.registrar_log.assert_called_once_with(
            None, 'TAG_FALSA', 10, 'NEGADO', 'Tag desconhecida ou sem permissao'
        )

    def test_acesso_negado_fora_do_horario(self):
        # Prepara o mock simulando um aluno tentando entrar 23:30
        self.mock_db.buscar_permissao.return_value = {
            'usuario_id': 15,
            'nome': 'Beatriz Souza',
            'hora_inicio': timedelta(hours=8),
            'hora_fim': timedelta(hours=21)
        }
        
        resultado = self.validador.processar_leitura('I9J0K1L2', 10, '23:30:00')
        
        self.assertEqual(resultado['status'], 'NEGADO')
        self.assertIn('Fora do horário', resultado['mensagem'])
        self.mock_db.registrar_log.assert_called_once_with(
            15, 'I9J0K1L2', 10, 'NEGADO', 'Fora do horario'
        )

if __name__ == '__main__':
    unittest.main()