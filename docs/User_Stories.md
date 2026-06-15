## US1: Controle de Acesso às Zonas

* **Descrição:** Como usuário do sistema, quero poder me autenticar ao tentar acessar uma zona (porta/laboratório) para que o sistema verifique automaticamente se tenho permissão de acesso naquele momento. 

* **Prioridade:** Alta.

* **Estimativa:** 8 pontos.

**Critérios de Avaliação:**

1. Autenticação do usuário: Se o usuário realizar identificação na zona (RFID), então o sistema deve reconhecer o usuário corretamente.  
2. Validação de perfil: Considerando que o usuário foi identificado, quando o sistema consultar o perfil ele deve verificar se o perfil possui permissão para a zona.  
3. Validação de horário: Considerando que o perfil possui acesso a zona, o sistema deve verificar o horário atual e verificar se o acesso está dentro do horário permitido.  
4. Decisão de acesso: Se todas as regras foram satisfeitas o acesso é permitido, caso contrário o acesso é negado.  
5. Resposta do sistema: Quando o acesso for permitido a porta deve ser liberada (simulado) e quando for negado o sistema deve informar o mesmo para o usuário.  
6. Registro em auditoria: Toda tentativa de acesso deve ser registrada contendo: identificação do usuário; zona acessada; data e hora; resultado. O log não pode ser alterado posteriormente.



## US2: Cadastro de Usuário

* **Descrição:** Como administrador do sistema, eu quero poder cadastrar novos usuários com seus perfis e identificadores (RFID) para que eles possam ser reconhecidos e tenham acesso às zonas conforme suas permissões.

* **Prioridade:** Alta.

* **Estimativa:** 2 pontos.

**Critérios de Avaliação:**

1. Cadastro de dados básicos: Dado que o administrador deseja cadastrar um usuário, ele deve informar o nome, identificação e perfil do usuário, então o sistema deve salvar o usuário com sucesso.  
2. Validação de unicidade: Quando o RFID já estiver cadastrado, então o sistema deve impedir o cadastro duplicado.  
3. Confirmação de cadastro: O sistema deve exibir mensagem de confirmação após cadastro bem-sucedido.  
4. Persistência de dados: O usuário deve estar disponível para uso imediato no controle de acesso.


## US3: Consulta de Log

* **Descrição:** Como administrador ou responsável pela segurança, quero ser capaz de consultar os logs de auditoria das tentativas de acesso para que eu possa monitorar quem tentou acessar determinadas zonas e quando.

* **Prioridade:** Alta.

* **Estimativa:** 5 pontos.

**Critérios de Avaliação:**

1. Visualização dos logs: Dado que o administrador acessa a tela de auditoria, então o sistema deve exibir a lista de registro contendo: Usuário; Zona; Data e Hora; Resultado.  
2. Sistema de filtros: O administrador deve ser capaz de filtrar por usuário, zona e período.  
3. Ordenação: Os logs devem ser ordenados por data/hora.  
4. Imutabilidade dos logs: O sistema não deve permitir edição ou exclusão de registros de auditoria.

