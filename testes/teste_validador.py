import unittest
from unittest.mock import MagicMock
from datetime import timedelta

from controle_acesso.validador import ValidadorAcesso


class TestValidadorAcesso(unittest.TestCase):
    def setUp(self):
        # Cria um Mock para isolar o teste do banco real.
        self.mock_db = MagicMock()
        self.validador = ValidadorAcesso(self.mock_db)

    def test_acesso_permitido_dentro_do_horario(self):
        self.mock_db.buscar_permissao.return_value = {
            "usuario_id": 5,
            "nome": "Ana Maria",
            "hora_inicio": timedelta(hours=7),
            "hora_fim": timedelta(hours=22),
        }

        resultado = self.validador.processar_leitura(
            "A1B2C3D4",
            10,
            "10:30:00",
        )

        self.assertEqual(resultado["status"], "PERMITIDO")
        self.assertEqual(resultado["mensagem"], "Bem-vindo(a), Ana Maria!")

        self.mock_db.buscar_permissao.assert_called_once_with(
            "A1B2C3D4",
            10,
        )
        self.mock_db.registrar_log.assert_called_once_with(
            5,
            "A1B2C3D4",
            10,
            "PERMITIDO",
            "Acesso autorizado",
        )

    def test_acesso_negado_tag_desconhecida_ou_sem_permissao(self):
        self.mock_db.buscar_permissao.return_value = None

        resultado = self.validador.processar_leitura(
            "TAG_FALSA",
            10,
            "10:30:00",
        )

        self.assertEqual(resultado["status"], "NEGADO")
        self.assertEqual(resultado["mensagem"], "Acesso negado para esta zona.")

        self.mock_db.buscar_permissao.assert_called_once_with(
            "TAG_FALSA",
            10,
        )
        self.mock_db.registrar_log.assert_called_once_with(
            None,
            "TAG_FALSA",
            10,
            "NEGADO",
            "Tag desconhecida ou sem permissao",
        )

    def test_acesso_negado_fora_do_horario(self):
        self.mock_db.buscar_permissao.return_value = {
            "usuario_id": 15,
            "nome": "Beatriz Souza",
            "hora_inicio": timedelta(hours=8),
            "hora_fim": timedelta(hours=21),
        }

        resultado = self.validador.processar_leitura(
            "I9J0K1L2",
            10,
            "23:30:00",
        )

        self.assertEqual(resultado["status"], "NEGADO")
        self.assertIn("Fora do horário", resultado["mensagem"])

        self.mock_db.buscar_permissao.assert_called_once_with(
            "I9J0K1L2",
            10,
        )
        self.mock_db.registrar_log.assert_called_once_with(
            15,
            "I9J0K1L2",
            10,
            "NEGADO",
            "Fora do horario",
        )

    def test_acesso_permitido_exatamente_no_horario_inicial(self):
        self.mock_db.buscar_permissao.return_value = {
            "usuario_id": 8,
            "nome": "Carlos Lima",
            "hora_inicio": timedelta(hours=8),
            "hora_fim": timedelta(hours=18),
        }

        resultado = self.validador.processar_leitura(
            "C1D2E3F4",
            2,
            "08:00:00",
        )

        self.assertEqual(resultado["status"], "PERMITIDO")
        self.assertEqual(resultado["mensagem"], "Bem-vindo(a), Carlos Lima!")
        self.mock_db.registrar_log.assert_called_once_with(
            8,
            "C1D2E3F4",
            2,
            "PERMITIDO",
            "Acesso autorizado",
        )

    def test_acesso_permitido_exatamente_no_horario_final(self):
        self.mock_db.buscar_permissao.return_value = {
            "usuario_id": 9,
            "nome": "Daniela Rocha",
            "hora_inicio": timedelta(hours=8),
            "hora_fim": timedelta(hours=18),
        }

        resultado = self.validador.processar_leitura(
            "D1E2F3G4",
            3,
            "18:00:00",
        )

        self.assertEqual(resultado["status"], "PERMITIDO")
        self.assertEqual(resultado["mensagem"], "Bem-vindo(a), Daniela Rocha!")
        self.mock_db.registrar_log.assert_called_once_with(
            9,
            "D1E2F3G4",
            3,
            "PERMITIDO",
            "Acesso autorizado",
        )

    def test_acesso_negado_um_segundo_antes_do_horario_inicial(self):
        self.mock_db.buscar_permissao.return_value = {
            "usuario_id": 10,
            "nome": "Eduardo Alves",
            "hora_inicio": timedelta(hours=8),
            "hora_fim": timedelta(hours=18),
        }

        resultado = self.validador.processar_leitura(
            "E1F2G3H4",
            4,
            "07:59:59",
        )

        self.assertEqual(resultado["status"], "NEGADO")
        self.assertIn("Fora do horário", resultado["mensagem"])
        self.mock_db.registrar_log.assert_called_once_with(
            10,
            "E1F2G3H4",
            4,
            "NEGADO",
            "Fora do horario",
        )

    def test_acesso_negado_um_segundo_depois_do_horario_final(self):
        self.mock_db.buscar_permissao.return_value = {
            "usuario_id": 11,
            "nome": "Fernanda Costa",
            "hora_inicio": timedelta(hours=8),
            "hora_fim": timedelta(hours=18),
        }

        resultado = self.validador.processar_leitura(
            "F1G2H3I4",
            5,
            "18:00:01",
        )

        self.assertEqual(resultado["status"], "NEGADO")
        self.assertIn("Fora do horário", resultado["mensagem"])
        self.mock_db.registrar_log.assert_called_once_with(
            11,
            "F1G2H3I4",
            5,
            "NEGADO",
            "Fora do horario",
        )

    def test_formato_de_hora_invalido_gera_value_error(self):
        with self.assertRaises(ValueError):
            self.validador.processar_leitura(
                "A1B2C3D4",
                10,
                "10:30",
            )

        self.mock_db.buscar_permissao.assert_not_called()
        self.mock_db.registrar_log.assert_not_called()

    def test_buscar_permissao_eh_chamado_com_rfid_e_zona_corretos(self):
        self.mock_db.buscar_permissao.return_value = None

        self.validador.processar_leitura(
            "Z9Y8X7W6",
            99,
            "12:00:00",
        )

        self.mock_db.buscar_permissao.assert_called_once_with(
            "Z9Y8X7W6",
            99,
        )


if __name__ == "__main__":
    unittest.main()
