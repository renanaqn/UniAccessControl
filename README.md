# UniAccessControl
Repositório para o Projeto das disciplinas DCA3603 - Engenharia de Software e DCA3604 - Banco de Dados

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Como clonar ou baixar](#como-clonar-ou-baixar)  
- [Estrutura do Projeto](#estrutura-do-projeto)  
- [Licença](#licença)  

## Sobre o Projeto

### Título
UniAccessControl

### Descrição
O projeto tem como função simular um leitor facial (abstraído por RFID) e aplicar o controle de entrada e saída da pessoa nas diversas zonas dentro da instituição. Então pode-se ter tabelas de perfis (aluno, professor, chefe de dpto, reitor, motorista), zonas de acesso (laboratórios, salas) e regras de horário. Além disso, exige uma tabela de log inalterável (Auditoria) para registrar "Quem tentou abrir qual porta, quando, e se foi negado ou aceito". E aí podemos implementar no contexto de um aluno de universidade, onde é feito esse cadastro digital e ao longo da vivência dele na instituição, ele vai ganhando acesso a diferentes locais. 

### Componentes
- Israel Soares de Castro Filho
- Larissa Soares de Souza
- Pedro Felipe Costa de Albuquerque
- Pedro Rocha Di Cavalcanti
- Renan de Aquino Pereira

## Como clonar ou baixar

Você pode obter este repositório de três formas:

### Clonar via HTTPS

```bash
git clone https://github.com/renanaqn/UniAccessControl.git
```

Isso criará uma cópia local do repositório em sua máquina.

### Clonar via SSH

Se você já configurou sua chave SSH no GitHub, pode clonar usando:

```bash
git clone git@github.com:renanaqn/UniAccessControl.git
```

Isso criará uma cópia local do repositório em sua máquina.

### Baixar como ZIP

1. Acesse a página do repositório no GitHub:
   [https://github.com/renanaqn/UniAccessControl](https://github.com/renanaqn/UniAccessControl)
2. Clique no botão **Code** (verde).
3. Selecione **Download ZIP**.
4. Extraia o arquivo ZIP para o local desejado em seu computador.


## Estrutura do Projeto

> *Esta seção pode variar conforme a organização do repositório de cada grupo.*

```
UniAccessControl/
├── LICENSE
├── README.md
├── <diretório-x>/
├── <diretório-y>/
└── <diretório-z>/
```

- LICENSE: termos da licença do projeto (MIT).
- README.md: este arquivo de apresentação.
- X: descrição do diretório X.
- Y: descrição do diretório Y.
- Z: descrição do diretório Z.

## Licença

Este projeto está licenciado sob a **Licença MIT**. Veja o arquivo `LICENSE` para mais detalhes.