# Proposal

## Why

Atualmente, o EduTrack AI permite que os alunos acompanhem suas disciplinas e tarefas acadêmicas pelo painel, mas não oferece uma forma consolidada e exportável para visualizar o histórico e desempenho acadêmico em formato de documento. A geração de um relatório em PDF e a disponibilização de um endpoint de download no backend atendem à necessidade de emitir e baixar o comprovante/relatório de desempenho do aluno de maneira prática e padronizada.

## What Changes

- Criação de um script Python em `scripts/generate_performance_report.py` para compilar os dados de disciplinas e tarefas do aluno e gerar um documento PDF estruturado com as métricas de desempenho acadêmico.
- Criação de um endpoint no Xano (ex.: `GET /reports/performance` ou `GET /student_report/download`) sob o grupo de APIs do backend para disponibilizar e realizar o download do arquivo de relatório.

## Capabilities

### New Capabilities
- `pdf-report-generation`: Script Python para geração do relatório em formato PDF contendo os indicadores de desempenho acadêmico do aluno.
- `report-download-api`: Endpoint no backend Xano protegido por autenticação para permitir o download do arquivo de relatório gerado.

### Modified Capabilities

## Impact

- **Scripts Python**: Novo script `scripts/generate_performance_report.py` para geração do PDF de desempenho acadêmico.
- **Backend / Xano**: Novo grupo ou arquivo de endpoint de API XanoScript (ex.: `api/reports/` ou `api/student_report/`) para download do relatório.
- **Dependências**: Utilização de biblioteca para geração de PDFs em Python (como `reportlab` ou `fpdf2`).

