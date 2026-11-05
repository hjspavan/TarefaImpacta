# Design

## Context

Atualmente, as páginas `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py` e `pages/3_👤_Perfil.py` implementam funções próprias (ex.: `get_base_url()`, `get_env_url()`, `get_auth_url()`) que abrem e leem manualmente o arquivo `.env` linha a linha.
O Streamlit disponibiliza a estrutura nativa `st.secrets`, que carrega automaticamente as configurações do arquivo local `.streamlit/secrets.toml` e, em produção, das configurações de secrets do servidor em nuvem.
A mudança substitui a leitura de arquivo manual pela consulta a `st.secrets`, mantendo compatibilidade resiliente.

Veja `proposal.md` para a motivação detalhada da mudança.

## Goals / Non-Goals

**Goals:**
- Substituir o parsing manual de `.env` nas páginas Streamlit pelo acesso direto via `st.secrets`.
- Manter fallback para `os.environ` caso a aplicação seja executada em ambientes onde variáveis de sistema são injetadas diretamente.
- Corrigir a sintaxe de `.streamlit/secrets.toml` (remoção de aspas duplicadas).
- Assegurar que o arquivo `.streamlit/` permaneça protegido no `.gitignore`.

**Non-Goals:**
- Não alterar a lógica de negócio das páginas nem endpoints do Xano.
- Não remover os scripts em `scripts/` (que operam fora do contexto Streamlit e podem continuar usando `os.environ` ou seus helpers).
- Não fazer push/deploy de arquivos para o Xano ou outros serviços remotos.

## Decisions

### Decisão 1: Helper reutilizável ou acesso direto a st.secrets
- **Decisão**: Criar uma função padronizada `get_config_url(key)` em cada página (ou método direto) que consulta `st.secrets.get(key)` e faz fallback para `os.environ.get(key)`.
- **Racional**: Garante que se o Streamlit Secrets estiver ativo, ele terá precedência; se não estiver presente ou a página rodar em outro contexto, o sistema não quebra com `KeyError`.

### Decisão 2: Formatação do .streamlit/secrets.toml
- **Decisão**: Manter as chaves em formato padrão TOML:
  ```toml
  URL_base_AUTH = "https://x8ki-letl-twmt.n7.xano.io/api:0rf1eKTV"
  URL_base_SUBJECTS = "https://x8ki-letl-twmt.n7.xano.io/api:rfrl5MWM"
  URL_base_ACADEMIC_TASKS = "https://x8ki-letl-twmt.n7.xano.io/api:TphVlUn-"
  ```
- **Racional**: Corrige a linha malformada existente com aspas extras em `URL_base_SUBJECTS`.

## Risks / Trade-offs

- **[Risco] Arquivo secrets.toml ausente**: Se o desenvolvedor clonar o repositório em outra máquina sem criar o `.streamlit/secrets.toml`, o Streamlit avisará sobre a ausência.
  - *Mitigação*: Mensagem explicativa em `st.error` instruindo a configurar o arquivo `.streamlit/secrets.toml`.

## Migration Plan

1. Corrigir o arquivo `.streamlit/secrets.toml` para garantir TOML válido.
2. Atualizar `pages/1_📚_Disciplinas.py` para usar `st.secrets`.
3. Atualizar `pages/2_📝_Tarefas.py` para usar `st.secrets`.
4. Atualizar `pages/3_👤_Perfil.py` para usar `st.secrets`.
5. Verificar se `.gitignore` contém `.streamlit/`.

