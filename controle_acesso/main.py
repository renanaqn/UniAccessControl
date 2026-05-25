from database import BancoDeDados
from validador import ValidadorAcesso

# Inicializa as classes
banco = BancoDeDados()
validador = ValidadorAcesso(banco)

print("== Teste de Integração com o Banco de Dados ==")
# Usando a tag da Professora Ana Maria
tag_lida = input("Digite a tag RFID (ex: A1B2C3D4): ") 
zona_atual = 10  # ID do Laboratório de Eletrônica
hora_agora = "10:30:00" # Simulando às 10h30 da manhã

print(f"\n[Processando leitura da tag {tag_lida} no Lab de Eletrônica às {hora_agora}]")

# Processa a leitura
resultado = validador.processar_leitura(tag_lida, zona_atual, hora_agora)

print(f"\nResultado da Porta: {resultado['status']}")
print(f"Visor: {resultado['mensagem']}")