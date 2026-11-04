# report-download-api Specification

## Purpose
Define a especificação da API no backend Xano para disponibilizar e permitir o download seguro do relatório de desempenho em PDF do usuário autenticado.

## Requirements

### Requirement: Authenticated report download endpoint
O sistema SHALL disponibilizar um endpoint no backend Xano protegido por autenticação de usuário (`auth = "User"`) para requisição e download do relatório de desempenho.

#### Scenario: Download de relatório por usuário autenticado
- **WHEN** um usuário autenticado envia uma requisição GET para o endpoint de download do relatório
- **THEN** o sistema valida o token de autenticação e disponibiliza o arquivo ou conteúdo binário do PDF referente ao aluno logado.

#### Scenario: Tentativa de download sem autenticação
- **WHEN** uma requisição é enviada ao endpoint de relatório sem um token de autenticação válido
- **THEN** o sistema recusa a requisição retornando status 401 Unauthorized.

### Requirement: Data isolation by authenticated user
O endpoint de download de relatório SHALL garantir isolamento rigoroso dos dados, impedindo que um usuário acesse ou baixe relatórios com dados de outros alunos.

#### Scenario: Garantia de isolamento dos dados
- **WHEN** o usuário autenticado solicita o download do seu relatório
- **THEN** o sistema utiliza estritamente o identificador `$auth.id` na consulta e entrega unicamente as informações pertinentes ao usuário logado.
