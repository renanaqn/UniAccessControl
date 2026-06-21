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
    
    def buscar_usuarios_com_rfid_por_nome(self, texto):
        """
        Busca usuários por nome parcial e retorna nome, RFID e perfil.
        Usado no simulador para exibir 'Nome | Perfil',
        mas validar internamente pela tag RFID.
        """

        query = """
            SELECT 
                u.id,
                u.nome,
                u.rfid_tag,
                u.perfil_id,
                p.nome_perfil
            FROM usuarios u
            JOIN perfis p ON p.id = u.perfil_id
            WHERE u.nome LIKE %s
            ORDER BY u.nome
            LIMIT 10
        """

        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(query, (f"%{texto}%",))
            return cursor.fetchall()

        except Exception as err:
            print(f"Erro ao buscar usuários com RFID: {err}")
            return []

        finally:
            cursor.close()
            conexao.close()
    
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
    
    def contar_usuarios_filtrados(
        self,
        nome="",
        rfid="",
        perfil="TODOS",
    ):
        """
        Conta a quantidade total de usuários cadastrados,
        considerando os filtros de nome, RFID e perfil.
        """

        query = """
            SELECT COUNT(*) AS total
            FROM usuarios u
            JOIN perfis p ON p.id = u.perfil_id
            WHERE 1=1
        """

        parametros = []

        if nome:
            query += " AND u.nome LIKE %s"
            parametros.append(f"%{nome}%")

        if rfid:
            query += " AND u.rfid_tag LIKE %s"
            parametros.append(f"%{rfid}%")

        if perfil and perfil != "TODOS":
            query += " AND p.nome_perfil = %s"
            parametros.append(perfil)

        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(query, parametros)
            resultado = cursor.fetchone()

            return resultado["total"]

        except Exception as err:
            print(f"Erro ao contar usuários filtrados: {err}")
            return 0

        finally:
            cursor.close()
            conexao.close()
    
    def contar_regras_filtradas(
        self,
        perfil="TODOS",
        zona="Todas",
        hora_inicio="",
        hora_fim="",
    ):
        """
        Conta a quantidade total de regras de acesso,
        considerando os filtros ativos.
        """

        query = """
            SELECT COUNT(*) AS total
            FROM regras_acesso r
            JOIN perfis p ON p.id = r.perfil_id
            JOIN zonas z ON z.id = r.zona_id
            WHERE 1=1
        """

        parametros = []

        if perfil and perfil != "TODOS":
            query += " AND p.nome_perfil = %s"
            parametros.append(perfil)

        if zona and zona != "Todas":
            query += " AND z.nome_zona = %s"
            parametros.append(zona)

        if hora_inicio:
            query += " AND r.hora_inicio >= %s"
            parametros.append(hora_inicio)

        if hora_fim:
            query += " AND r.hora_fim <= %s"
            parametros.append(hora_fim)

        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(query, parametros)
            resultado = cursor.fetchone()

            return resultado["total"]

        except Exception as err:
            print(f"Erro ao contar regras filtradas: {err}")
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
    
    def listar_usuarios(
        self,
        pagina=1,
        limite=5,
        nome="",
        rfid="",
        perfil="TODOS",
    ):
        """Retorna os usuários cadastrados com filtros e paginação."""

        query = """
            SELECT 
                u.id,
                u.nome,
                u.rfid_tag,
                u.perfil_id,
                p.nome_perfil
            FROM usuarios u
            JOIN perfis p ON p.id = u.perfil_id
            WHERE 1=1
        """

        parametros = []

        if nome:
            query += " AND u.nome LIKE %s"
            parametros.append(f"%{nome}%")

        if rfid:
            query += " AND u.rfid_tag LIKE %s"
            parametros.append(f"%{rfid}%")

        if perfil and perfil != "TODOS":
            query += " AND p.nome_perfil = %s"
            parametros.append(perfil)

        query += """
            ORDER BY u.nome
            LIMIT %s OFFSET %s
        """

        offset = (pagina - 1) * limite
        parametros.extend([limite, offset])

        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(query, parametros)
            return cursor.fetchall()

        except Exception as err:
            print(f"Erro ao listar usuários: {err}")
            return []

        finally:
            cursor.close()
            conexao.close()

    def listar_regras(
        self,
        pagina=1,
        limite=5,
        perfil="TODOS",
        zona="Todas",
        hora_inicio="",
        hora_fim="",
    ):
        """
        Retorna as regras de acesso com filtros e paginação.
        """

        offset = (pagina - 1) * limite

        query = """
            SELECT
                r.perfil_id,
                p.nome_perfil,
                r.zona_id,
                z.nome_zona,
                r.hora_inicio,
                r.hora_fim
            FROM regras_acesso r
            JOIN perfis p ON p.id = r.perfil_id
            JOIN zonas z ON z.id = r.zona_id
            WHERE 1=1
        """

        parametros = []

        if perfil and perfil != "TODOS":
            query += " AND p.nome_perfil = %s"
            parametros.append(perfil)

        if zona and zona != "Todas":
            query += " AND z.nome_zona = %s"
            parametros.append(zona)

        if hora_inicio:
            query += " AND r.hora_inicio >= %s"
            parametros.append(hora_inicio)

        if hora_fim:
            query += " AND r.hora_fim <= %s"
            parametros.append(hora_fim)

        query += """
            ORDER BY p.nome_perfil, z.nome_zona
            LIMIT %s OFFSET %s
        """

        parametros.extend([limite, offset])

        conexao = self.conectar()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(query, parametros)
            return cursor.fetchall()

        except Exception as err:
            print(f"Erro ao listar regras de acesso: {err}")
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
    
    def cadastrar_perfil(self, nome_perfil):
        """
        Cadastra um novo perfil no sistema.
        Exemplo: Aluno, Professor, Técnico, Administrador.
        """

        if not nome_perfil or nome_perfil.strip() == "":
            return False, "Erro: o nome do perfil não pode estar vazio."

        query = """
            INSERT INTO perfis (nome_perfil)
            VALUES (%s)
        """

        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(query, (nome_perfil.strip(),))
            conexao.commit()

            return True, "Perfil cadastrado com sucesso!"

        except mysql.connector.IntegrityError:
            return False, "Erro: já existe um perfil com esse nome."

        except Exception as err:
            return False, f"Erro ao cadastrar perfil: {err}"

        finally:
            cursor.close()
            conexao.close()
            
    def cadastrar_zona(self, nome_zona):
        """
        Cadastra uma nova zona de acesso no sistema.
        Exemplo: Laboratório, Biblioteca, Sala dos Professores.
        """

        if not nome_zona or nome_zona.strip() == "":
            return False, "Erro: o nome da zona não pode estar vazio."

        query = """
            INSERT INTO zonas (nome_zona)
            VALUES (%s)
        """

        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(query, (nome_zona.strip(),))
            conexao.commit()

            return True, "Zona cadastrada com sucesso!"

        except mysql.connector.IntegrityError:
            return False, "Erro: já existe uma zona com esse nome."

        except Exception as err:
            return False, f"Erro ao cadastrar zona: {err}"

        finally:
            cursor.close()
            conexao.close()

    def remover_perfil(self, perfil_id):
        """
        Remove um perfil pelo ID.

        Observação:
        Se existirem usuários ou regras de acesso vinculados ao perfil,
        o banco pode impedir a remoção por causa das chaves estrangeiras.
        """

        query = """
            DELETE FROM perfis
            WHERE id = %s
        """

        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(query, (perfil_id,))
            conexao.commit()

            if cursor.rowcount == 0:
                return False, "Nenhum perfil encontrado com esse ID."

            return True, "Perfil removido com sucesso!"

        except mysql.connector.IntegrityError:
            return (
                False,
                "Não foi possível remover o perfil. Existem usuários ou regras de acesso vinculados a ele."
            )

        except Exception as err:
            return False, f"Erro ao remover perfil: {err}"

        finally:
            cursor.close()
            conexao.close()

    def remover_zona(self, zona_id):
        """
        Remove uma zona pelo ID.

        Observação:
        Se existirem regras de acesso ou logs vinculados à zona,
        o banco pode impedir a remoção por causa das chaves estrangeiras.
        """

        query = """
            DELETE FROM zonas
            WHERE id = %s
        """

        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(query, (zona_id,))
            conexao.commit()

            if cursor.rowcount == 0:
                return False, "Nenhuma zona encontrada com esse ID."

            return True, "Zona removida com sucesso!"

        except mysql.connector.IntegrityError:
            return (
                False,
                "Não foi possível remover a zona. Existem regras de acesso ou logs vinculados a ela."
            )

        except Exception as err:
            return False, f"Erro ao remover zona: {err}"

        finally:
            cursor.close()
            conexao.close()