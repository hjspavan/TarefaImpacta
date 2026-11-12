# Design

## Context

O EduTrack AI já possui estrutura de dados para usuários, disciplinas (`subjects`) e tarefas acadêmicas (`academic_tasks`), com endpoints CRUD autenticados e rotina de cálculo de progresso. Para viabilizar a entrega formal de dados acadêmicos ao aluno, faz-se necessária a geração de um relatório em documento PDF e um endpoint no backend Xano que possibilite o download desse arquivo.

Veja `proposal.md` para a motivação detalhada da mudança.

## Goals / Non-Goals

**Goals:**
- Projetar o script Python `scripts/generate_performance_report.py` capaz de consultar dados acadêmicos do aluno e compilar um arquivo PDF de desempenho formatado.
- Definir o endpoint REST no XanoScript (`api/reports/performance_GET.xs` e respectivo `api/reports/reports.xs`) com `auth = "User"` para download do relatório referente ao usuário autenticado.
- Garantir que cada aluno acesse e baixe unicamente os dados atrelados ao seu próprio `$auth.id`.

**Non-Goals:**
- Não criar componentes de interface visual no Streamlit nesta mudança (não solicitado na demanda).
- Não alterar as tabelas ou esquemas existentes no banco de dados.
- Não executar comandos de push/deploy para o Xano remoto (em estrita conformidade com a Regra Nº 2 de `AGENTS.md`).

## Decisions

### Decisão 1: Geração de PDF em Python
- **Decisão**: Utilizar gerador de PDF compatível com padrão PDF 1.4 no script `scripts/generate_performance_report.py`.
- **Racional**: Permite a renderização direta de layout estruturado (cabeçalho, dados do estudante, resumo geral de progresso e detalhamento de disciplinas e tarefas) sem depender de bibliotecas de sistema pesado externas.

### Decisão 2: Organização do Grupo de API de Relatórios no Xano
- **Decisão**: Criar o grupo `api/reports/reports.xs` e o endpoint `api/reports/performance_GET.xs` com `auth = "User"`.
- **Racional**: Mantém a modularidade e consistência arquitetural observada em `api/subjects/`, `api/academic_tasks/` e `api/auth/`.

### Decisão 3: Isolamento e segurança no download do relatório
- **Decisão**: O endpoint no Xano obriga autenticação JWT (`auth = "User"`) e baseia todo o retorno no identificador `$auth.id`.
- **Racional**: Previne vulnerabilidades de vazamento de informações (BOLA/IDOR), garantindo que um aluno jamais receba o relatório de outro.

## Risks / Trade-offs

- **[Risco] Aluno sem tarefas ou disciplinas**: Geração de documento em branco ou erro de cálculo.
  - *Mitigação*: Tratamento condicional no script para gerar mensagem indicando ausência de registros acadêmicos no momento da emissão sem interromper com exceção não tratada.

## Migration Plan

1. Criar/verificar o script Python `scripts/generate_performance_report.py`.
2. Criar a especificação do grupo de API `api/reports/reports.xs`.
3. Criar a especificação do endpoint XanoScript `api/reports/performance_GET.xs`.
4. Os arquivos serão gerados localmente e disponibilizados para revisão manual pelo desenvolvedor.

