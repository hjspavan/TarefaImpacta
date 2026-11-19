# 🎓 EduTrack AI

### Sua vida acadêmica organizada com inteligência artificial.

O **EduTrack AI** é uma aplicação web desenvolvida em Python com Streamlit, criada para ajudar estudantes a organizar sua rotina acadêmica, acompanhar disciplinas, gerenciar tarefas e analisar seu desempenho.

Com uma interface intuitiva e recursos de inteligência artificial, o projeto reúne ferramentas importantes para tornar o acompanhamento da vida acadêmica mais simples e eficiente.

---

## 🚀 Funcionalidades

### 👤 Cadastro e autenticação
- Cadastro de novos usuários.
- Login na plataforma.
- Gerenciamento de sessão do usuário.

### 📚 Gerenciamento de disciplinas
- Visualização das disciplinas cadastradas.
- Cadastro de novas disciplinas.
- Organização das informações acadêmicas.

### 📝 Gerenciamento de tarefas
- Visualização das tarefas acadêmicas.
- Consulta de tarefas por disciplina.
- Acompanhamento das atividades cadastradas.

### 📄 Relatórios acadêmicos
- Geração de relatórios em PDF.
- Apresentação de indicadores e gráficos de desempenho.
- Recomendações para acompanhamento acadêmico.

### 🤖 Assistente Acadêmico com IA
- Assistente integrado ao Gemini.
- Apoio na análise das informações acadêmicas.
- Respostas e orientações relacionadas à rotina de estudos.
- Alternativa de análise local quando a integração com IA não está disponível.

### 🎨 Interface personalizada
- Tema visual claro e escuro.
- Componentes e telas com identidade visual padronizada.
- Navegação organizada e intuitiva.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Streamlit | Desenvolvimento da aplicação web |
| Xano | Backend, banco de dados e APIs |
| Google Gemini | Assistente de inteligência artificial |
| Pandas | Manipulação e análise de dados |
| Requests | Comunicação com APIs |
| Git e GitHub | Controle de versão |

---

## 🏗️ Estrutura do projeto

```text
EduTrack-AI/
│
├── app.py
│
├── pages/
│   ├── 1_📚_Disciplinas.py
│   ├── 2_📝_Tarefas.py
│   ├── 3_👤_Perfil.py
│   ├── 4_📄_Relatórios.py
│   └── 5_🤖_Assistente.py
│
├── api/
│
├── components/
│   └── theme.py
│
├── scripts/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/hjspavan/TarefaImpacta.git
```

### 2. Acesse a pasta

```bash
cd TarefaImpacta
```

### 3. Crie o ambiente virtual

```bash
python -m venv .venv
```

### 4. Ative o ambiente virtual

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate
```

**Linux ou macOS:**

```bash
source .venv/bin/activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Configure as integrações

Configure as credenciais necessárias para acessar os serviços do Xano e, caso utilize o assistente com inteligência artificial, a chave de API do Google Gemini.

Não compartilhe chaves de API ou credenciais no repositório.

### 7. Execute a aplicação

```bash
streamlit run app.py
```

A aplicação estará disponível em:

```text
http://localhost:8501
```

---

## 🔗 Integrações

**Xano:** responsável pelo backend, armazenamento de dados e disponibilização dos endpoints utilizados pela aplicação.

**Google Gemini:** utilizado pelo Assistente Acadêmico para oferecer recursos de inteligência artificial.

---

## 🎯 Objetivo do projeto

O EduTrack AI tem como objetivo centralizar o gerenciamento da rotina acadêmica em uma única plataforma, permitindo que estudantes organizem suas disciplinas, acompanhem tarefas e obtenham informações sobre seu desempenho.

O projeto também representa a aplicação prática de conhecimentos de desenvolvimento Python, integração com APIs, gerenciamento de dados, inteligência artificial e controle de versão.

---

## 👨‍💻 Desenvolvimento

Projeto desenvolvido como parte das atividades acadêmicas da **UNIMPACTA**, com foco na aplicação prática de tecnologias e conceitos de Engenharia de Software.

**Repositório:** [EduTrack AI — GitHub](https://github.com/hjspavan/TarefaImpacta)

---

⭐ Se você gostou do projeto, considere deixar uma estrela no repositório!
