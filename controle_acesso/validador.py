from datetime import datetime

class ValidadorAcesso:
    def __init__(self, banco_de_dados):
        # Recebe a classe de banco de dados
        self.db = banco_de_dados

    def processar_leitura(self, rfid_tag: str, zona_id: int, hora_atual_str: str) -> dict:
        """
        Função principal que avalia as USs e decide se a porta abre ou não.
        Retorna um dicionário com o status e a mensagem.
        """
        hora_atual = datetime.strptime(hora_atual_str, '%H:%M:%S').time()
        
        # Busca os dados no banco
        permissao = self.db.buscar_permissao(rfid_tag, zona_id)

        # Valida se a tag existe e tem permissão para a zona
        if not permissao:
            self.db.registrar_log(None, rfid_tag, zona_id, "NEGADO", "Tag desconhecida ou sem permissao")
            return {"status": "NEGADO", "mensagem": "Acesso negado para esta zona."}

        # Valida a janela de horário
        # Transforma os timedeltas do MySQL em objetos time do Python
        hora_inicio = (datetime.min + permissao['hora_inicio']).time()
        hora_fim = (datetime.min + permissao['hora_fim']).time()

        if not (hora_inicio <= hora_atual <= hora_fim):
            self.db.registrar_log(permissao['usuario_id'], rfid_tag, zona_id, "NEGADO", "Fora do horario")
            return {"status": "NEGADO", "mensagem": f"Fora do horário permitido ({hora_inicio} as {hora_fim})."}

        # Acesso Permitido
        self.db.registrar_log(permissao['usuario_id'], rfid_tag, zona_id, "PERMITIDO", "Acesso autorizado")
        return {"status": "PERMITIDO", "mensagem": f"Bem-vindo(a), {permissao['nome']}!"}