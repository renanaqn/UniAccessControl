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

    def buscar_ultimos_logs(self, limite=10):
        """Retorna as últimas tentativas de acesso para o Admin visualizar."""
        query = """        
            SELECT * 
            FROM registro
            ORDER BY data_hora DESC
            LIMIT %s
        """
        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)
        
        try:
            cursor.execute(query, (limite,))
            return cursor.fetchall()

        finally:
            cursor.close()
            conexao.close()
    
    def buscar_usuarios_por_nome(self, texto):
        """
        Buscar usuários por nome parcial
        """
        
        query = """
            SELECT *
            FROM usuarios
            WHERE nome LIKE %s
            ORDER BY nome
            LIMIT 10
        """
        
        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)
        
        cursor.execute(
            query,
            (f"%{texto}%",)
        )
        
        resultado = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        
        return [
            usuario["nome"]
            for usuario in resultado
        ]
    
    def buscar_logs(self,
                    pagina=1,
                    limite=25,
                    usuario=None,
                    zona=None,
                    resultado=None,
                    data_inicio=None,
                    data_fim=None):
        """
        Busca logs com filtros e paginação
        """
        
        offset = (pagina - 1) * limite
        
        query = """
            SELECT *
            FROM registro
            WHERE 1=1
        """
        
        parametros = []
        
        if usuario:
            query += " AND nome LIKE %s"
            parametros.append(f"%{usuario}%")
            
        if zona and zona != "Todas":
            query += " AND nome_zona = %s"
            parametros.append(zona)
            
        if resultado and resultado != "TODOS":
            query += " AND resultado = %s"
            parametros.append(resultado)
        
        if data_inicio:
            query += " AND DATE(data_hora) >= %s"
            parametros.append(data_inicio)
        
        if data_fim:
            query += " AND DATE(data_hora) <= %s"
            parametros.append(data_fim)
        
        query += """
            ORDER BY data_hora DESC
            LIMIT %s OFFSET %s
        """
        
        parametros.extend([limite, offset])
        
        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)
        
        try:
            cursor.execute(query, parametros)
            return cursor.fetchall()
        except Exception as err:
            print(f"Erro ao buscar logs: {err}")
            return []
        finally:
            cursor.close()
            conexao.close()
    
    def contar_logs(self,
                    usuario=None,
                    zona=None,
                    resultado=None,
                    data_inicio=None,
                    data_fim=None):
        """
        Retorna a quantidade total de logs, considerando os filtros ativos
        """
        
        query = """
            SELECT COUNT(*) AS total
            FROM registro
            WHERE 1=1
        """
        
        parametros = []
        
        if usuario:
            query += " AND nome LIKE %s"
            parametros.append(f"%{usuario}%")
        
        if zona and zona != "Todas":
            query += " AND zona = %s"
            parametros.append(zona)
            
        if resultado and resultado != "TODOS":
            query += " AND resultado = %s"
            parametros.append(resultado)
        
        if data_inicio:
            query += " AND DATE(data_hora) >= %s"
            parametros.append(data_inicio)
        
        if data_fim:
            query += " AND DATE(data_hora) <= %s"
            parametros.append(data_fim)
        
        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)
        
        try:
            cursor.execute(query, parametros)
            return cursor.fetchone()["total"]
        except Exception as err:
            print(f"Erro ao contar logs: {err}")
            return 0
        finally:
            cursor.close()
            conexao.close()  
    
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
    
    def listar_usuarios(self):
        """Retorna todos os usuarios cadastrados."""
        query = """
            SELECT id, nome, rfid_tag, perfil_id
            FROM usuarios
        """
        
        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)
        
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    
    def listar_regras(self):
        """Retorna as regras de acesso"""
        
        query = """
            SELECT
                perfil_id,
                zona_id,
                hora_inicio,
                hora_fim
            FROM regras_acesso
        """
        
        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)
        
        try:
            cursor.execute(query)
            return cursor.fetchall()
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
    
    
    def _contar_registros(self, tabela):
        """Retorna a quantidade total de items em certa tabela"""
        query = f"SELECT COUNT(*) AS total FROM {tabela}"

        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(query)
            resultado = cursor.fetchone()
            return resultado["total"]

        except Exception as err:
            print(f"Erro ao contar registros de {tabela}: {err}")
            return 0

        finally:
            cursor.close()
            conexao.close()
    
    def total_usuarios(self):
        return self._contar_registros("usuarios")

    def total_perfis(self):
        return self._contar_registros("perfis")

    def total_zonas(self):
        return self._contar_registros("zonas")
    
    def acessos_permitidos_hoje(self):

        query = """
            SELECT COUNT(*) AS total
            FROM auditoria_logs
            WHERE DATE(data_hora) = CURDATE()
            AND resultado = 'PERMITIDO'
        """

        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(query)
            return cursor.fetchone()["total"]
        except Exception as err:
            print(f"Erro ao contar acessos permitidos: {err}")
            return 0
        finally:
            cursor.close()
            conexao.close()
    
    def acessos_negados_hoje(self):

        query = """
            SELECT COUNT(*) AS total
            FROM auditoria_logs
            WHERE DATE(data_hora) = CURDATE()
            AND resultado = 'NEGADO'
        """

        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(query)
            return cursor.fetchone()["total"]
        except Exception as err:
            print(f"Erro ao contar acessos permitidos: {err}")
            return 0
        finally:
            cursor.close()
            conexao.close()

        return total