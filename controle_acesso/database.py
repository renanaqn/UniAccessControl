import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

# Lê o arquivo .env e carrega as senhas para a memória
load_dotenv()

class BancoDeDados:
    def conectar(self):
        """Estabelece a conexão usando as variáveis de ambiente."""
        return mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

    def buscar_permissao(self, rfid_tag, zona_id):
        """Busca o usuário e as regras de horário para aquela zona."""
        # Só lembrar de rever as nomenclaturas dos atributos do banco
        query = """
            SELECT u.id as usuario_id, u.nome, r.hora_inicio, r.hora_fim
            FROM usuarios u
            JOIN regras_acesso r ON u.perfil_id = r.perfil_id
            WHERE u.rfid_tag = %s AND r.zona_id = %s
        """
        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(query, (rfid_tag, zona_id))
        resultado = cursor.fetchone()
        
        cursor.close()
        conexao.close()
        return resultado

    def registrar_log(self, usuario_id, rfid_tag, zona_id, resultado, motivo):
        """Salva a tentativa na tabela imutável de auditoria."""
        query = """
            INSERT INTO auditoria_logs (usuario_id, rfid_tentativa, zona_id, data_hora, resultado, motivo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        conexao = self.conectar()
        cursor = conexao.cursor()
        agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute(query, (usuario_id, rfid_tag, zona_id, agora, resultado, motivo))
        conexao.commit()
        
        cursor.close()
        conexao.close()