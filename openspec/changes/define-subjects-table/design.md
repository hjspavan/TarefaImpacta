# Design: Subjects Table Schema

## Context
Definição do esquema de dados da tabela `subjects` para integração com o backend Xano. Ver `proposal.md` para motivação e `specs/subjects/spec.md` para os requisitos comportamentais.
Seguindo estritamente as diretrizes de `AGENTES.md`, o escopo é restrito à definição estrutural da tabela, sem expansão para APIs, testes ou frontend.

## Goals / Non-Goals

**Goals:**
- Definir a estrutura formal de dados da tabela `subjects` no Xano.
- Especificar os 5 campos solicitados: `id` (auto), `name` (text), `teacher` (text), `hours` (int), e `user_id` (FK).
- Estabelecer a relação de chave estrangeira entre `subjects.user_id` e a tabela de usuários (`user`/`users`).

**Non-Goals:**
- Criação de endpoints de API CRUD para a tabela `subjects` (fora de escopo conforme `AGENTES.md`).
- Criação de interfaces de usuário ou componentes de frontend.
- Criação de testes unitários ou de integração automatizados.
- Sincronização, push ou deploy automatizado para a instância do Xano (conforme `AGENTES.md`, push é de responsabilidade manual do desenvolvedor).

## Decisions

### Decisão 1: Mapeamento de Tipos e Campos no Xano
- **Campos definidos**:
  - `id`: Tipo `id` / `integer` (auto-increment primary key gerado automaticamente pelo Xano).
  - `name`: Tipo `text` (nome da disciplina/matéria).
  - `teacher`: Tipo `text` (nome do professor responsável).
  - `hours`: Tipo `integer` (carga horária da matéria).
  - `user_id`: Tipo `integer` com referência / Foreign Key configurada para a tabela de autenticação (`user` ou `users`).
- **Rationale**: Mapeamento direto e semântico dos tipos suportados pelo Xano, garantindo integridade referencial com os usuários autenticados.
- **Alternativas consideradas**:
  - Adição de timestamps (`created_at`) ou campos de controle: Descartado para manter estritamente os campos pedidos pelo usuário.

### Decisão 2: Conformidade com AGENTES.md
- **Rationale**: `AGENTES.md` estabelece que a solicitação "criar tabela X" não deve incluir CRUD, testes ou frontend, e a responsabilidade da IA termina na geração dos arquivos sem tentar fazer push/deploy para o Xano.
- **Alternativas consideradas**:
  - Gerar endpoints REST para matérias: Rejeitado por violar a regra crítica de `AGENTES.md`.

## Risks / Trade-offs

- [Nome da tabela de autenticação variar entre `user` e `users` no Xano] → Configurar a referência de chave estrangeira explicitando ambas as nomenclaturas habituais do Xano Auth para que o desenvolvedor conecte à tabela existente em seu workspace.
- [Necessidade de migração manual no Xano] → O desenvolvedor aplicará as definições manualmente no console do Xano ou via arquivo de exportação/schema.

