# streamlit-secrets Specification

## Purpose

Define a especificação para leitura e gerenciamento de configurações e variáveis de ambiente nas páginas do frontend Streamlit através do mecanismo nativo `st.secrets`.

## Requirements

### Requirement: Reading API Base URLs from Streamlit Secrets
As páginas do frontend Streamlit SHALL obter as URLs base dos serviços do Xano (`URL_base_AUTH`, `URL_base_SUBJECTS`, `URL_base_ACADEMIC_TASKS`) consultando prioritariamente o dicionário nativo `st.secrets`.

#### Scenario: Leitura bem-sucedida a partir de st.secrets
- **WHEN** a página Streamlit for carregada e as variáveis estiverem configuradas em `st.secrets`
- **THEN** o sistema recupera os valores de URL a partir de `st.secrets` e estabelece a comunicação com os endpoints da API.

#### Scenario: Fallback para variáveis de ambiente
- **WHEN** a chave solicitada não for encontrada em `st.secrets` mas estiver definida no ambiente (`os.environ`)
- **THEN** o sistema utiliza o valor presente em `os.environ` como contingência para manter o funcionamento.

### Requirement: Missing configuration handling
As páginas do frontend Streamlit SHALL exibir mensagem de erro amigável na interface e interromper a execução da página (`st.stop()`) caso uma URL obrigatória não seja encontrada em `st.secrets` nem em variáveis de ambiente.

#### Scenario: URL obrigatória ausente
- **WHEN** uma URL base requerida pela página não estiver definida em `st.secrets` nem no ambiente
- **THEN** a página exibe mensagem de alerta informando a chave ausente e instruindo a configuração em `.streamlit/secrets.toml`.

### Requirement: Secure local secrets configuration
O arquivo de configuração local `.streamlit/secrets.toml` SHALL conter as definições de variáveis em formato TOML válido e deve permanecer devidamente ignorado pelo controle de versão Git.

#### Scenario: Proteção de segredos no repositório
- **WHEN** o status do repositório Git for verificado
- **THEN** o arquivo `.streamlit/secrets.toml` permanece ignorado pelas regras do `.gitignore`, prevenindo vazamento de credenciais.

