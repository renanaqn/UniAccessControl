import os
from datetime import datetime
from database import BancoDeDados
from validador import ValidadorAcesso

# Inicialização
banco = BancoDeDados()
validador = ValidadorAcesso(banco)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    print("\n" + "="*50)
    print(" SISTEMA DE CONTROLE DE ACESSO - UFRN")
    print("="*50)
    print(" [1] Simular Leitura na Porta (Acesso)")
    print(" [2] [Admin] Cadastrar Novo Usuário")
    print(" [3] [Admin] Criar/Editar Regra de Acesso")
    print(" [4] [Admin] Atualizar Tag RFID")
    print(" [5] [Admin] Remover Usuário")
    print(" [6] [Admin] Ver Histórico de Logs")
    print(" [7] [Admin] Listar Zonas e Perfis")
    print(" [0] Sair do Sistema")
    print("="*50)
    
    opcao = input("Escolha uma ação: ")

    if opcao == '1':
        print("\n--- SIMULADOR DE PORTA ---")
        tag_lida = input("Aproxime a tag (Digite o RFID): ")
        try:
            print("Zonas: 1 - Lab Eletronica, 2 - Sala dos Professores, 3 - Almoxarifado, 4- Lab Informatica")
            zona_atual = int(input("ID da Zona (ex: 1 para Lab, 2 para Servidores, 3 para Almoxarifado): "))
            hora_agora = datetime.now().strftime('%H:%M:%S')
            #hora_agora = 16:30:00 # só para testes
            
            print(f"\nProcessando leitura na Zona {zona_atual}...")
            resultado = validador.processar_leitura(tag_lida, zona_atual, hora_agora)
            
            print(f"Status da Porta: {resultado['status']}")
            print(f"Visor: {resultado['mensagem']}")
        except ValueError:
            print("Erro: O ID da Zona deve ser um número inteiro!")

    elif opcao == '2':
        print("\n--- PAINEL ADMIN: NOVO USUÁRIO ---")
        try:
            id_usr = int(input("Digite um ID numérico para o usuário: "))
            nome = input("Nome Completo: ")
            rfid = input("Código da nova Tag RFID: ")
            perfil = int(input("ID do Perfil (Ex: 1=Professor, 2=Aluno): "))
            
            sucesso, mensagem = banco.cadastrar_usuario(id_usr, nome, rfid, perfil)
            print(f"\n{'SUCESSO' if sucesso else 'FALHA'}: {mensagem}")
        except ValueError:
            print("\nErro: IDs e Perfis precisam ser números!")

    elif opcao == '3':
        print("\n--- PAINEL ADMIN: REGRAS DE ACESSO ---")
        try:
            perfil_id = int(input("ID do Perfil (Ex: 1=Professor, 2=Aluno, 3=Zelador): "))
            zona_id = int(input("ID da Zona (Ex: 1=Lab, 2=Servidores, 3=Almoxarifado): "))
            hora_inicio = input("Hora de Início (HH:MM:SS): ")
            hora_fim = input("Hora de Término (HH:MM:SS): ")
            
            sucesso, mensagem = banco.criar_regra_acesso(perfil_id, zona_id, hora_inicio, hora_fim)
            print(f"\n{'SUCESSO' if sucesso else 'FALHA'}: {mensagem}")
        except ValueError:
            print("\nErro: IDs precisam ser números!")

    elif opcao == '4':
        print("\n--- PAINEL ADMIN: ATUALIZAR TAG ---")
        try:
            id_usuario = int(input("ID do Usuário: "))
            nova_tag = input("Nova Tag RFID: ")
            
            # Aqui assumimos que a função retornar True/False de forma similar
            sucesso, mensagem = banco.atualizar_tag(id_usuario, nova_tag) 
            print(f"\n{'SUCESSO' if sucesso else 'FALHA'}: {mensagem}")
        except ValueError:
            print("\nErro: O ID do Usuário precisa ser um número!")

    elif opcao == '5':
        print("\n--- PAINEL ADMIN: REMOVER USUÁRIO ---")
        try:
            id_usuario = int(input("ID do Usuário a ser removido: "))
            certeza = input(f"Tem certeza que deseja remover o usuário {id_usuario}? (S/N): ")
            
            if certeza.upper() == 'S':
                sucesso, mensagem = banco.remover_usuario(id_usuario)
                print(f"\n{'SUCESSO' if sucesso else 'FALHA'}: {mensagem}")
            else:
                print("\nOperação cancelada.")
        except ValueError:
            print("\nErro: O ID do Usuário precisa ser um número!")

    elif opcao == '6':
        print("\n--- PAINEL ADMIN: ÚLTIMOS ACESSOS ---")
        logs = banco.buscar_ultimos_logs(5)
        if not logs:
            print("Nenhum log encontrado.")
        else:
            for log in logs:
                data = log['data_hora'].strftime('%d/%m %H:%M:%S')
                print(f"[{data}] Zona: {log['zona_id']} | Tag: {log['rfid_tentativa']} | {log['resultado']} ({log['motivo']})")

    elif opcao == '7':
        print("\n--- PAINEL ADMIN: ZONAS E PERFIS ---")
        zonas = banco.listar_zonas()
        perfis = banco.listar_perfis()
        
        print("\nZONAS CADASTRADAS:")
        for z in zonas: print(f" - ID: {z['id']} | Nome: {z['nome_zona']}")
            
        print("\nPERFIS CADASTRADOS:")
        for p in perfis: print(f" - ID: {p['id']} | Nome: {p['nome_perfil']}")

    elif opcao == '0':
        print("\nDesligando sistema... Até logo!")
        break

    else:
        print("\nOpção inválida. Tente novamente.")
    
    input("\n[Pressione ENTER para voltar ao menu] ")
    limpar_tela()