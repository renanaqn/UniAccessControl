from database import BancoDeDados
from validador import ValidadorAcesso
import os
from dotenv import load_dotenv

# Lê o arquivo .env e carrega as senhas para a memória
load_dotenv()

config_mysql = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Inicializa as classes
banco = BancoDeDados(config_mysql)
validador = ValidadorAcesso(banco)

# Simula uma leitura de RFID
print(" ==Simulador de Leitura RFID== ")
tag_lida = input("Aproxime o cartao (Digite o RFID): ")
zona_atual = 10  # Ex: ID 10 é o Lab de Eletrônica
hora_agora = "10:30:00" # Em produção, seria datetime.now().strftime('%H:%M:%S')

# Processa a leitura
resultado = validador.processar_leitura(tag_lida, zona_atual, hora_agora)

print(f"\nResultado da Porta: {resultado['status']}")
print(f"Visor: {resultado['mensagem']}")