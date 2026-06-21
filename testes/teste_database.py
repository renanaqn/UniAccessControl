import unittest
from unittest.mock import patch, MagicMock
import mysql.connector

from controle_acesso.database import BancoDeDados


class TestBancoDeDados(unittest.TestCase):

    def criar_mock_banco(self, mock_connect):
        """
        Cria conexão e cursor falsos para evitar acesso ao MySQL real.
        """
        mock_conexao = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_conexao
        mock_conexao.cursor.return_value = mock_cursor

        return mock_conexao, mock_cursor

    # ============================================================
    # Permissões e logs
    # ============================================================

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_buscar_permissao(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchone.return_value = {
            "usuario_id": 1,
            "nome": "Ana Maria",
            "hora_inicio": "08:00:00",
            "hora_fim": "18:00:00",
        }

        db = BancoDeDados()
        resultado = db.buscar_permissao("A1B2C3D4", 1)

        self.assertEqual(resultado["usuario_id"], 1)
        self.assertEqual(resultado["nome"], "Ana Maria")

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conexao.close.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_registrar_log(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        db = BancoDeDados()
        db.registrar_log(
            usuario_id=1,
            rfid_tag="A1B2C3D4",
            zona_id=2,
            resultado="PERMITIDO",
            motivo="Acesso autorizado",
        )

        mock_cursor.execute.assert_called_once()
        mock_conexao.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conexao.close.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_buscar_ultimos_logs(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchall.return_value = [
            {
                "data_hora": "2026-01-01 10:00:00",
                "nome": "Ana Maria",
                "nome_zona": "Lab. Eletronica",
                "resultado": "PERMITIDO",
                "motivo": "Acesso autorizado",
            }
        ]

        db = BancoDeDados()
        logs = db.buscar_ultimos_logs(10)

        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["resultado"], "PERMITIDO")

        mock_cursor.execute.assert_called_once()

    # ============================================================
    # Usuários
    # ============================================================

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_cadastrar_usuario_sucesso(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        db = BancoDeDados()
        sucesso, msg = db.cadastrar_usuario("João Silva", "TAG12345", 1)

        self.assertTrue(sucesso)
        self.assertEqual(msg, "Usuário cadastrado com sucesso!")

        mock_cursor.execute.assert_called_once()
        mock_conexao.commit.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_cadastrar_usuario_erro_banco(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.execute.side_effect = mysql.connector.Error(
            msg="Duplicate entry"
        )

        db = BancoDeDados()
        sucesso, msg = db.cadastrar_usuario("Maria", "TAG_DUPLICADA", 2)

        self.assertFalse(sucesso)
        self.assertIn("Erro do Banco", msg)

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_buscar_usuarios_por_nome(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchall.return_value = [
            {"id": 1, "nome": "Ana Maria", "rfid_tag": "A1B2C3D4"},
            {"id": 2, "nome": "Ana Clara", "rfid_tag": "E5F6G7H8"},
        ]

        db = BancoDeDados()
        usuarios = db.buscar_usuarios_por_nome("Ana")

        self.assertEqual(usuarios, ["Ana Maria", "Ana Clara"])
        mock_cursor.execute.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_buscar_usuarios_com_rfid_por_nome(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchall.return_value = [
            {
                "id": 1,
                "nome": "Ana Maria",
                "rfid_tag": "A1B2C3D4",
                "perfil_id": 1,
                "nome_perfil": "Aluna",
            }
        ]

        db = BancoDeDados()
        usuarios = db.buscar_usuarios_com_rfid_por_nome("Ana")

        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0]["nome"], "Ana Maria")
        self.assertEqual(usuarios[0]["nome_perfil"], "Aluna")
        self.assertEqual(usuarios[0]["rfid_tag"], "A1B2C3D4")

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_listar_usuarios_com_filtros(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchall.return_value = [
            {
                "id": 1,
                "nome": "Ana Maria",
                "rfid_tag": "A1B2C3D4",
                "perfil_id": 1,
                "nome_perfil": "Aluna",
            }
        ]

        db = BancoDeDados()
        usuarios = db.listar_usuarios(
            pagina=1,
            limite=5,
            nome="Ana",
            rfid="A1",
            perfil="Aluna",
        )

        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0]["nome_perfil"], "Aluna")
        mock_cursor.execute.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_contar_usuarios_filtrados(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchone.return_value = {"total": 3}

        db = BancoDeDados()
        total = db.contar_usuarios_filtrados(
            nome="Ana",
            rfid="A1",
            perfil="Aluna",
        )

        self.assertEqual(total, 3)
        mock_cursor.execute.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_atualizar_tag(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        db = BancoDeDados()
        sucesso, msg = db.atualizar_tag(1, "NOVA_TAG")

        self.assertTrue(sucesso)
        self.assertEqual(msg, "Tag RFID atualizada com sucesso!")
        mock_conexao.commit.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_remover_usuario(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        db = BancoDeDados()
        sucesso, msg = db.remover_usuario(1)

        self.assertTrue(sucesso)
        self.assertEqual(msg, "Usuário removido com sucesso!")
        mock_conexao.commit.assert_called_once()

    # ============================================================
    # Logs e auditoria
    # ============================================================

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_buscar_logs_com_filtros(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchall.return_value = [
            {
                "data_hora": "2026-01-01 10:00:00",
                "nome": "Ana Maria",
                "nome_zona": "Lab. Eletronica",
                "resultado": "PERMITIDO",
                "motivo": "Acesso autorizado",
            }
        ]

        db = BancoDeDados()
        logs = db.buscar_logs(
            pagina=1,
            limite=25,
            usuario="Ana",
            zona="Lab. Eletronica",
            resultado="PERMITIDO",
            data_inicio="2026-01-01",
            data_fim="2026-01-31",
        )

        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["nome_zona"], "Lab. Eletronica")
        mock_cursor.execute.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_contar_logs_com_filtros(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchone.return_value = {"total": 7}

        db = BancoDeDados()
        total = db.contar_logs(
            usuario="Ana",
            zona="Lab. Eletronica",
            resultado="NEGADO",
            data_inicio="2026-01-01",
            data_fim="2026-01-31",
        )

        self.assertEqual(total, 7)
        mock_cursor.execute.assert_called_once()

    # ============================================================
    # Zonas e perfis
    # ============================================================

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_listar_zonas(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchall.return_value = [
            {"id": 1, "nome_zona": "Lab. Eletronica"},
            {"id": 2, "nome_zona": "Biblioteca"},
        ]

        db = BancoDeDados()
        zonas = db.listar_zonas()

        self.assertEqual(len(zonas), 2)
        self.assertEqual(zonas[0]["nome_zona"], "Lab. Eletronica")

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_listar_perfis(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchall.return_value = [
            {"id": 1, "nome_perfil": "Aluna"},
            {"id": 2, "nome_perfil": "Professor"},
        ]

        db = BancoDeDados()
        perfis = db.listar_perfis()

        self.assertEqual(len(perfis), 2)
        self.assertEqual(perfis[0]["nome_perfil"], "Aluna")

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_cadastrar_perfil_sucesso(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        db = BancoDeDados()
        sucesso, msg = db.cadastrar_perfil("Aluna")

        self.assertTrue(sucesso)
        self.assertEqual(msg, "Perfil cadastrado com sucesso!")
        mock_conexao.commit.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_cadastrar_perfil_vazio(self, mock_connect):
        db = BancoDeDados()
        sucesso, msg = db.cadastrar_perfil("")

        self.assertFalse(sucesso)
        self.assertIn("não pode estar vazio", msg)
        mock_connect.assert_not_called()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_cadastrar_perfil_duplicado(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.execute.side_effect = mysql.connector.IntegrityError()

        db = BancoDeDados()
        sucesso, msg = db.cadastrar_perfil("Aluna")

        self.assertFalse(sucesso)
        self.assertIn("já existe", msg)

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_cadastrar_zona_sucesso(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        db = BancoDeDados()
        sucesso, msg = db.cadastrar_zona("Lab. Eletronica")

        self.assertTrue(sucesso)
        self.assertEqual(msg, "Zona cadastrada com sucesso!")
        mock_conexao.commit.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_cadastrar_zona_vazia(self, mock_connect):
        db = BancoDeDados()
        sucesso, msg = db.cadastrar_zona("")

        self.assertFalse(sucesso)
        self.assertIn("não pode estar vazio", msg)
        mock_connect.assert_not_called()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_cadastrar_zona_duplicada(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.execute.side_effect = mysql.connector.IntegrityError()

        db = BancoDeDados()
        sucesso, msg = db.cadastrar_zona("Lab. Eletronica")

        self.assertFalse(sucesso)
        self.assertIn("já existe", msg)

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_remover_perfil_sucesso(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)
        mock_cursor.rowcount = 1

        db = BancoDeDados()
        sucesso, msg = db.remover_perfil(1)

        self.assertTrue(sucesso)
        self.assertEqual(msg, "Perfil removido com sucesso!")
        mock_conexao.commit.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_remover_perfil_inexistente(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)
        mock_cursor.rowcount = 0

        db = BancoDeDados()
        sucesso, msg = db.remover_perfil(999)

        self.assertFalse(sucesso)
        self.assertIn("Nenhum perfil", msg)

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_remover_perfil_com_dependencias(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)
        mock_cursor.execute.side_effect = mysql.connector.IntegrityError()

        db = BancoDeDados()
        sucesso, msg = db.remover_perfil(1)

        self.assertFalse(sucesso)
        self.assertIn("vinculados", msg)

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_remover_zona_sucesso(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)
        mock_cursor.rowcount = 1

        db = BancoDeDados()
        sucesso, msg = db.remover_zona(1)

        self.assertTrue(sucesso)
        self.assertEqual(msg, "Zona removida com sucesso!")
        mock_conexao.commit.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_remover_zona_inexistente(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)
        mock_cursor.rowcount = 0

        db = BancoDeDados()
        sucesso, msg = db.remover_zona(999)

        self.assertFalse(sucesso)
        self.assertIn("Nenhuma zona", msg)

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_remover_zona_com_dependencias(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)
        mock_cursor.execute.side_effect = mysql.connector.IntegrityError()

        db = BancoDeDados()
        sucesso, msg = db.remover_zona(1)

        self.assertFalse(sucesso)
        self.assertIn("vinculados", msg)

    # ============================================================
    # Regras de acesso
    # ============================================================

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_criar_regra_acesso_sucesso(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        db = BancoDeDados()
        sucesso, msg = db.criar_regra_acesso(
            perfil_id=1,
            zona_id=1,
            hora_inicio="08:00:00",
            hora_fim="18:00:00",
        )

        self.assertTrue(sucesso)
        self.assertEqual(msg, "Regra de acesso salva com sucesso!")
        mock_conexao.commit.assert_called_once()

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_criar_regra_acesso_erro(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.execute.side_effect = Exception("Erro simulado")

        db = BancoDeDados()
        sucesso, msg = db.criar_regra_acesso(
            perfil_id=1,
            zona_id=1,
            hora_inicio="08:00:00",
            hora_fim="18:00:00",
        )

        self.assertFalse(sucesso)
        self.assertIn("Erro", msg)

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_listar_regras_com_filtros(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchall.return_value = [
            {
                "perfil_id": 1,
                "nome_perfil": "Aluna",
                "zona_id": 1,
                "nome_zona": "Lab. Eletronica",
                "hora_inicio": "08:00:00",
                "hora_fim": "18:00:00",
            }
        ]

        db = BancoDeDados()
        regras = db.listar_regras(
            pagina=1,
            limite=5,
            perfil="Aluna",
            zona="Lab. Eletronica",
            hora_inicio="08:00:00",
            hora_fim="18:00:00",
        )

        self.assertEqual(len(regras), 1)
        self.assertEqual(regras[0]["nome_perfil"], "Aluna")
        self.assertEqual(regras[0]["nome_zona"], "Lab. Eletronica")

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_contar_regras_filtradas(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchone.return_value = {"total": 4}

        db = BancoDeDados()
        total = db.contar_regras_filtradas(
            perfil="Aluna",
            zona="Lab. Eletronica",
            hora_inicio="08:00:00",
            hora_fim="18:00:00",
        )

        self.assertEqual(total, 4)

    # ============================================================
    # Dashboard e contagens gerais
    # ============================================================

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_total_usuarios(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchone.return_value = {"total": 10}

        db = BancoDeDados()
        total = db.total_usuarios()

        self.assertEqual(total, 10)

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_total_perfis(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchone.return_value = {"total": 3}

        db = BancoDeDados()
        total = db.total_perfis()

        self.assertEqual(total, 3)

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_total_zonas(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchone.return_value = {"total": 5}

        db = BancoDeDados()
        total = db.total_zonas()

        self.assertEqual(total, 5)

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_acessos_permitidos_hoje(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchone.return_value = {"total": 12}

        db = BancoDeDados()
        total = db.acessos_permitidos_hoje()

        self.assertEqual(total, 12)

    @patch("controle_acesso.database.mysql.connector.connect")
    def test_acessos_negados_hoje(self, mock_connect):
        mock_conexao, mock_cursor = self.criar_mock_banco(mock_connect)

        mock_cursor.fetchone.return_value = {"total": 6}

        db = BancoDeDados()
        total = db.acessos_negados_hoje()

        self.assertEqual(total, 6)


if __name__ == "__main__":
    unittest.main()