<<<<<<< HEAD
# Design: Subjects Table Schema

## Context
Definição do esquema de dados da tabela `subjects` para integração com o backend Xano. Ver `proposal.md` para motivação e `specs/subjects/spec.md` para os requisitos comportamentais.
Seguindo estritamente as diretrizes de `AGENTES.md`, o escopo é restrito à definição estrutural da tabela, sem expansão para APIs, testes ou frontend.
=======
# Design

## Context

O projeto EduTrack AI utiliza o backend Xano para persistência de dados e autenticação de usuários (conforme configurado em `.xano/config.json`, branch `v1`). A interface atual em Streamlit (`app.py`) prevê uma seção de "Disciplinas", que consumirá os dados do backend. Veja `proposal.md` para o contexto geral e motivação desta mudança.
>>>>>>> e43102d (feat: insercao do banco de dados xanoscript)

## Goals / Non-Goals

**Goals:**
<<<<<<< HEAD
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
=======
- Definir formalmente a especificação técnica dos campos, tipos e restrições da tabela `subjects` no Xano.
- Estabelecer a chave estrangeira `user_id` conectada à tabela de autenticação (`user`/`users`) com índice para consultas eficientes por usuário.
- Garantir compatibilidade com os endpoints de CRUD padrão do Xano e facilitar a integração futura com a camada de visualização em Python/Streamlit.

**Non-Goals:**
- Implementação dos endpoints de API no Xano nesta etapa (será tratado em tarefas subsequentes de API/rotas).
- Desenvolvimento do código de consumo em Streamlit (`app.py`), que dependerá da tabela e das APIs criadas.
- Criação de tabelas adicionais como `tasks` ou `evaluations`.

## Decisions

### 1. Nomenclatura e Tipo dos Campos no Xano
- **Decisão**:
  - `id`: Integer, auto-increment, primary key (padrão Xano).
  - `name`: Text, não-nulo (nome oficial da matéria/disciplina).
  - `teacher`: Text, aceita nulo/vazio (nome do professor responsável).
  - `hours`: Integer, não-nulo (carga horária total em horas, valor >= 0).
  - `user_id`: Integer, table reference (Foreign Key) referenciando a tabela de autenticação `user` (ou `users`).
- **Alternativas consideradas**:
  - `workload` em vez de `hours`: `hours` foi explicitamente solicitado e é mais direto para exibição de métricas.
  - Armazenar `teacher` como uma tabela separada: Rejeitado por adicionar complexidade desnecessária para o escopo inicial do EduTrack AI.

### 2. Tratamento da Tabela de Usuários (Referência de FK)
- **Decisão**: Configurar `user_id` como referência de tabela (table reference) no Xano apontando para a entidade de usuários (`user`). O Xano normalmente cria por padrão a tabela `user`; caso a instância utilize o plural `users`, a referência é mapeada diretamente ao ID dessa entidade.
- **Alternativas consideradas**:
  - Não definir FK e usar apenas integer sem integridade referencial: Descartado, pois a integridade referencial previne registros órfãos e habilita joins automáticos (addons) no Xano.

### 3. Indexação para Filtro de Usuário
- **Decisão**: Recomendar a criação de um índice no campo `user_id` na tabela `subjects`.
- **Racional**: Como toda consulta da interface do aluno filtrará por `user_id == auth.id`, o índice garante desempenho ideal mesmo com o crescimento de dados.

## Risks / Trade-offs

- **[Divergência no nome da tabela de auth (`user` vs `users`)]** → Verificação do nome exato da tabela de autenticação existente na instância Xano antes da aplicação da foreign key.
- **[Exclusão em cascata de usuário]** → Configurar comportamento de exclusão no Xano (recomenda-se cascade delete ou restrict caso um usuário seja excluído).

## Migration Plan

1. Acessar o painel/CLI do Xano no workspace `148582` (branch `v1`).
2. Criar a tabela `subjects` com as colunas definidas (`name`, `teacher`, `hours`, `user_id`).
3. Definir a restrição de chave estrangeira em `user_id`.
4. Criar o índice na coluna `user_id`.
5. Validar a criação e persistência inserindo um registro de teste.
>>>>>>> e43102d (feat: insercao do banco de dados xanoscript)

