# 📦 Requisitos e Dependências do Projeto

Esta pasta contém a relação de bibliotecas Python necessárias para executar o projeto **EduTrack AI** em qualquer máquina.

---

## 📄 Arquivos Disponíveis

- **`requirements.txt`**: Dependências principais e recomendadas para instalação em uma nova máquina (com versões compatíveis).
- **`freeze.txt`**: Espelho exato (freeze) de todas as bibliotecas e versões instaladas no ambiente de desenvolvimento original.

---

## 🚀 Como Configurar e Rodar em Outra Máquina

### 1. Clonar ou Baixar o Projeto
Certifique-se de ter o Python 3.10 ou superior instalado na máquina.

### 2. Criar e Ativar o Ambiente Virtual (`.venv`)

**No Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

*(Se houver erro de permissão de scripts no PowerShell, execute `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` ou utilize o Prompt de Comando: `.venv\Scripts\activate.bat`)*

**No Linux / macOS (Bash/Zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements/requirements.txt
```

*(Ou utilize o arquivo da raiz do projeto: `pip install -r requirements.txt`)*

---

### 4. Configurar as Variáveis de Ambiente (`.env`)

Crie um arquivo `.env` na raiz do projeto com a URL base dos endpoints do Xano:

```env
URL_base_AUTH=https://x8ki-letl-twmt.n7.xano.io/api:0rf1eKTV
```

---

### 5. Executar a Aplicação Streamlit

```bash
streamlit run app.py
```
