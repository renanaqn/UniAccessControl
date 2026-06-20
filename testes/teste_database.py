import unittest
from unittest.mock import patch, MagicMock
from controle_acesso.database import BancoDeDados
import mysql.connector

class TestBancoDeDados(unittest.TestCase):
    
    # o decorador @patch vai interceptar a biblioteca mysql.connector e impede que ela acesse o banco real
    @patch('controle_acesso.database.mysql.connector.connect')
    def test_cadastrar_usuario_sucesso(self, mock_connect):
        # Prepara a conexão (setup do Mock)
        mock_conexao = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conexao
        mock_conexao.cursor.return_value = mock_cursor
        
        # Executa a função do código
        db = BancoDeDados()
        sucesso, msg = db.cadastrar_usuario("João Silva", "TAG_NOVA_123", 1)
        
        # Verificação
        self.assertTrue(sucesso)
        self.assertEqual(msg, "Usuário cadastrado com sucesso!")
        
        # Garante que o comando INSERT foi chamado e o COMMIT foi feito
        mock_cursor.execute.assert_called()
        mock_conexao.commit.assert_called_once()

    @patch('controle_acesso.database.mysql.connector.connect')
    def test_cadastrar_usuario_erro_banco(self, mock_connect):
        # Prepara simulando um erro (ex: Tag já existe)
        mock_conexao = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conexao
        mock_conexao.cursor.return_value = mock_cursor
        
        # Força o execute a gerar uma Exception genérica
        mock_cursor.execute.side_effect = mysql.connector.Error(msg="Duplicate entry 'TAG_DUPLICADA'")
        
        # Ação
        db = BancoDeDados()
        sucesso, msg = db.cadastrar_usuario("Maria", "TAG_DUPLICADA", 2)
        
        # Verificação
        self.assertFalse(sucesso)


    @patch('controle_acesso.database.mysql.connector.connect')
    def test_listar_zonas_e_perfis(self, mock_connect):
        # Preparação
        mock_conexao = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conexao
        mock_conexao.cursor.return_value = mock_cursor
        
        # Simulando o retorno do banco para as listas
        mock_cursor.fetchall.return_value = [{'id': 1, 'nome': 'Teste'}]
        
        # Ação
        db = BancoDeDados()
        zonas = db.listar_zonas()
        perfis = db.listar_perfis()
        ultimos_logs = db.buscar_ultimos_logs(10)
        
        # Verificação
        self.assertTrue(len(zonas) > 0)
        self.assertTrue(len(perfis) > 0)
        self.assertTrue(len(ultimos_logs) > 0)
        self.assertEqual(mock_cursor.execute.call_count, 3)

    @patch('controle_acesso.database.mysql.connector.connect')
    def test_estatisticas_dashboard(self, mock_connect):
        mock_conexao = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conexao
        mock_conexao.cursor.return_value = mock_cursor
        
        # Simulando o retorno de funções COUNT (ex: 15 usuários)
        mock_cursor.fetchone.return_value = {'total': 15, 'COUNT(*)': 15, 'count': 15}
        
        db = BancoDeDados()
        # Chama essas funções para já pontuar linhas como "cobertas" no relatório
        db.total_usuarios()
        db.total_zonas()
        db.acessos_permitidos_hoje()
        db.acessos_negados_hoje()
        
        self.assertEqual(mock_cursor.execute.call_count, 4)

    @patch('controle_acesso.database.mysql.connector.connect')
    def test_atualizar_e_remover(self, mock_connect):
        mock_conexao = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conexao
        mock_conexao.cursor.return_value = mock_cursor
        
        db = BancoDeDados()
        sucesso_rm, _ = db.remover_usuario(1)
        sucesso_up, _ = db.atualizar_tag(1, "NOVA_TAG_777")
        sucesso_regra, _ = db.criar_regra_acesso(1, 1, '08:00:00', '18:00:00')
        
        # Verifica se as operações de escrita retornaram sucesso e deram commit
        self.assertTrue(sucesso_rm)
        self.assertTrue(sucesso_up)
        self.assertTrue(sucesso_regra)
        self.assertEqual(mock_conexao.commit.call_count, 3)


if __name__ == '__main__':
    unittest.main()