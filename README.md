# UniAccessControl
> Repositório para o Projeto das disciplinas DCA3603 - Engenharia de Software e DCA3604 - Banco de Dados

O **UniAccessControl** é um sistema completo de controle de acesso físico, projetado para gerenciar a entrada e saída de indivíduos em zonas restritas de uma instituição. O projeto simula a integração de um hardware de leitura na ponta (como um totem RFID) com um painel de controle administrativo web.

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Equipe](#equipe)
- [Instalação](#instalação) 
- [Como Executar o Projeto](#como-executar-o-projeto) 
- [Estrutura do Projeto](#estrutura-do-projeto)  
- [Licença](#licença)  

## Sobre o Projeto

### Descrição
O projeto resolve o problema de gestão de acessos em ambientes institucionais. Ele aplica regras de negócio baseadas em **Perfis** (ex: aluno, professor, técnico), **Zonas de Acesso** (ex: laboratórios, almoxarifado) e **Políticas de Horário**. 

A solução proposta neste MVP (*Minimum Viable Product*) é composta por duas frentes:
1. **Painel Administrativo Web:** Interface protegida por autenticação para gestão de usuários, cadastro de tags RFID, configuração de permissões e visualização de relatórios.
2. **Endpoint de Hardware (Simulador):** Uma interface pública que atua como o microcontrolador da porta física, lendo as tags e despachando os dados para o validador no backend.

Como requisito de segurança e auditoria, o sistema conta com uma tabela de logs inalterável, registrando o histórico de *"Quem tentou abrir qual porta, quando, e se o acesso foi negado ou aceito"*.



## Tecnologias Utilizadas

- **Linguagem Principal:** Python 3
- **Frontend / Fullstack Framework:** Reflex (Interface Web e reatividade)
- **Banco de Dados:** MySQL (Persistência, Relacionamentos N↔M e Logs)
- **Controle de Versão:** Git/GitHub


## Equipe
- Israel Soares de Castro Filho
- Larissa Soares de Souza
- Pedro Felipe Costa de Albuquerque
- Pedro Rocha Di Cavalcanti
- Renan de Aquino Pereira

## Instalação

Antes de começar, certifique-se de ter o **Python (3.10 ou superior)** e o **MySQL Server** instalados na sua máquina.


Você pode obter este repositório de três formas:

### 1. Clone o repositório

```bash
git clone https://github.com/renanaqn/UniAccessControl.git
```

### 2. Configure o Banco de Dados:

1. Abra o seu cliente MySQL (MySQL Workbench, DBeaver ou terminal).
2. Execute o script de inicialização localizado em `database/init_db.sql` e database/`incremento_db.sql` para criar o schema, as tabelas e popular os dados iniciais necessários para testes.
3. Atualize as credenciais de acesso ao banco (usuário e senha) no arquivo `controle_acesso/database.py` caso o seu ambiente local exija.

### 3. Instale as dependências do Python:

```bash
pip install -r requirements.txt
```

## Como executar o projeto

Com o banco de dados rodando e as dependências instaladas, inicie o servidor da aplicação web:
```bash
# Entre na pasta do frontend
cd frontend

# Execute o Reflex
reflex run
```

A aplicação estará disponível no seu navegador em http://localhost:3000.

Credenciais de Teste (Administrador):

- Usuário: admin

- Senha: admin123


## Estrutura do Projeto

A arquitetura do projeto aplica o princípio de Separation of Concerns (Separação de Responsabilidades), dividindo o banco de dados, as regras de negócio e a interface do usuário.

```
UniAccessControl/
├── controle_acesso/        # Camada de Regras de Negócio e Persistência
│   ├── database.py         # Conexão com MySQL e queries (CRUD)
│   ├── validador.py        # Validação de horários, perfis e permissões
│   └── main.py             # Script de teste em terminal (CLI)
├── database/               # Camada de Dados
│   ├── init_db.sql         # Script DDL/DML de inicialização
│   └── incremento_db.sql   # Script DDL/DML de incremento de dados     
├── docs/                   # Documentação do Projeto
│   └── User_Stories.md     # Levantamento de Requisitos e Histórias de Usuário
├── frontend/               # Camada de Apresentação (Reflex App)
│   ├── components/         # Componentes visuais reaproveitáveis (Ex: Sidebar)
│   ├── pages/              # Telas do sistema (Login, Dashboard, Simulador, etc.)
│   ├── states/             # Gerenciamento de Estado (Auth, Variáveis de Tela)
│   └── frontend.py         # Arquivo principal do reflex
├── testes/                 # Suíte de Testes Automatizados
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação principal
```

## Licença

Este projeto está licenciado sob a **Licença MIT**. Veja o arquivo `LICENSE` para mais detalhes.