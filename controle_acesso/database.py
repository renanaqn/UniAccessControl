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
    
    def cadastrar_usuario(self, nome, rfid_tag, perfil_id):
        """Salva um novo usuário no banco."""
        query = "INSERT INTO usuarios (nome, rfid_tag, perfil_id) VALUES (%s, %s, %s)"
        conexao = self.conectar()
        cursor = conexao.cursor()
        try:
            cursor.execute(query, (nome, rfid_tag, perfil_id))
            conexao.commit()
            return True, "Usuário cadastrado com sucesso!"
        except mysql.connector.Error as err:
            return False, f"Erro do Banco: {err}"
        finally:
            cursor.close()
            conexao.close()

    def buscar_ultimos_logs(self, limite=5):
        """Retorna as últimas tentativas de acesso para o Admin visualizar."""
        query = """
            SELECT data_hora, rfid_tentativa, zona_id, resultado, motivo 
            FROM auditoria_logs 
            ORDER BY data_hora DESC LIMIT %s
        """
        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(query, (limite,))
        resultados = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        return resultados
    
    def criar_regra_acesso(self, perfil_id, zona_id, hora_inicio, hora_fim):
        """Define o horário permitido para um perfil em uma zona."""
        query = """
            INSERT INTO regras_acesso (perfil_id, zona_id, hora_inicio, hora_fim) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            hora_inicio = VALUES(hora_inicio), hora_fim = VALUES(hora_fim)
        """
        # o parâmetro "ON DUPLICATE KEY" permite que essa função sirva tanto 
        # para criar uma regra nova quanto para editar o horário de uma existente!
        conexao = self.conectar()
        cursor = conexao.cursor()
        try:
            cursor.execute(query, (perfil_id, zona_id, hora_inicio, hora_fim))
            conexao.commit()
            return True, "Regra de acesso salva com sucesso!"
        except Exception as err:
            return False, f"Erro: {err}"
        finally:
            cursor.close()
            conexao.close()

    def atualizar_tag(self, id_usuario, nova_rfid_tag):
        """Substitui o cartão de um usuário existente."""
        query = "UPDATE usuarios SET rfid_tag = %s WHERE id = %s"
        conexao = self.conectar()
        cursor = conexao.cursor()
        try:
            cursor.execute(query, (nova_rfid_tag, id_usuario))
            conexao.commit()
            return True, "Tag RFID atualizada com sucesso!"
        except Exception as err:
            return False, f"Erro: {err}"
        finally:
            cursor.close()
            conexao.close()


    def listar_zonas(self):
        """Retorna todas as zonas para preencher menus dropdown no frontend."""
        query = "SELECT id, nome_zona FROM zonas"
        conexao = self.conectar()
        
        # O dictionary=True é essencial aqui para que o retorno seja
        # [{'id': 1, 'nome_zona': 'Lab'}] ao invés de tuplas [(1, 'Lab')]
        cursor = conexao.cursor(dictionary=True) 
        try:
            cursor.execute(query)
            resultados = cursor.fetchall()
            return resultados
        except Exception as err:
            print(f"Erro ao buscar zonas: {err}")
            return []
        finally:
            cursor.close()
            conexao.close()
        
    def listar_perfis(self):
        """Retorna todos os perfis cadastrados."""
        query = "SELECT id, nome_perfil FROM perfis"
        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute(query)
            resultados = cursor.fetchall()
            return resultados
        except Exception as err:
            print(f"Erro ao buscar perfis: {err}")
            return []
        finally:
            cursor.close()
            conexao.close()

    def remover_usuario(self, id_usuario):
        """Deleta um usuário do sistema, revogando seu acesso."""
        query = "DELETE FROM usuarios WHERE id = %s"
        conexao = self.conectar()
        cursor = conexao.cursor()
        try:
            cursor.execute(query, (id_usuario,))
            conexao.commit() 
            return True, "Usuário removido com sucesso!"
        except Exception as err:
            return False, f"Erro: {err}"
        finally:
            cursor.close()
            conexao.close()