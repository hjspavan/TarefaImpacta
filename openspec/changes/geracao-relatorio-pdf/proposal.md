# Proposal

## Why

Atualmente, o EduTrack AI permite que os alunos acompanhem suas disciplinas e tarefas acadêmicas pelo painel, mas faz-se necessário consolidar a emissão de comprovante e relatório formal em documento exportável. A geração de um relatório em PDF estruturado com indicadores de desempenho e a disponibilização de um endpoint de download no backend Xano atendem a essa necessidade de forma prática, segura e padronizada.

## What Changes

- Implementação do script Python `scripts/generate_performance_report.py` para consolidar os dados acadêmicos (disciplinas, tarefas concluídas, percentual de progresso) e gerar o relatório em formato PDF.
- Criação do endpoint no Xano `GET /reports/performance` (sob o grupo `api/reports/`) protegido por autenticação (`auth = "User"`) para consulta e download do relatório de desempenho do aluno autenticado.

## Capabilities

### New Capabilities

### Modified Capabilities
- `pdf-report-generation`: Consolidação e geração do relatório em formato PDF contendo os indicadores de desempenho acadêmico do aluno.
- `report-download-api`: Endpoint no backend Xano protegido por autenticação para permitir o download do arquivo de relatório gerado.

## Impact

- **Scripts Python**: Arquivo `scripts/generate_performance_report.py` para geração do PDF de desempenho acadêmico.
- **Backend / Xano**: Arquivos de endpoint e grupo de APIs XanoScript (`api/reports/reports.xs` e `api/reports/performance_GET.xs`).
- **Segurança**: Endpoint protegido por autenticação JWT (`auth = "User"`), garantindo isolamento total por `$auth.id`.

