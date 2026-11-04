# progress-calculation Specification

## Purpose
Define o comportamento do script de cálculo de progresso acadêmico por disciplina, consumindo os endpoints CRUD do Xano e retornando a porcentagem de tarefas concluídas em formato JSON.

## Requirements

### Requirement: Calculate progress percentage for a subject
O sistema SHALL calcular a porcentagem de progresso de uma disciplina dividindo a quantidade de tarefas com status "Concluída" pela quantidade total de tarefas, multiplicando por 100.

#### Scenario: Disciplina com tarefas parcialmente concluídas
- **WHEN** a disciplina possui 4 tarefas, sendo 2 com status "Concluída"
- **THEN** o script retorna um JSON `{"percentage": 50.0}`

#### Scenario: Disciplina com todas as tarefas concluídas
- **WHEN** a disciplina possui 3 tarefas e todas têm status "Concluída"
- **THEN** o script retorna um JSON `{"percentage": 100.0}`

### Requirement: Handle zero tasks without error
O sistema SHALL retornar `{"percentage": 0}` quando a disciplina não possuir nenhuma tarefa cadastrada, evitando erro de divisão por zero.

#### Scenario: Disciplina sem tarefas
- **WHEN** a disciplina não possui tarefas acadêmicas associadas
- **THEN** o script retorna um JSON `{"percentage": 0}` sem lançar exceção

### Requirement: Consume existing CRUD endpoints
O sistema SHALL obter as tarefas acadêmicas consultando o endpoint `GET /academic_tasks` do Xano com o parâmetro `subject_id` e o token de autenticação Bearer, utilizando a URL base definida em `URL_base_ACADEMIC_TASKS` no arquivo `.env`.

#### Scenario: Consulta autenticada das tarefas
- **WHEN** o script é chamado com um `subject_id` válido e um token de autenticação
- **THEN** o script faz uma requisição GET autenticada para `/academic_tasks?subject_id=<id>` e processa a resposta

### Requirement: Return JSON output
O sistema SHALL retornar o resultado como um dicionário Python (ou JSON impresso em stdout) contendo a chave `percentage` com o valor numérico do percentual de progresso.

#### Scenario: Formato de saída
- **WHEN** o cálculo de progresso é executado com sucesso
- **THEN** o script retorna `{"percentage": <valor_numerico>}` onde o valor é um número entre 0 e 100
