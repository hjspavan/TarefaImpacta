# 📚 Aula de Git

Este repositório foi criado para acompanhar as aulas de **Git e GitHub**, apresentando os principais comandos e conceitos utilizados no controle de versão.

## 🎯 Objetivos

- Compreender o funcionamento do Git.
- Aprender os principais comandos do Git.
- Criar e gerenciar repositórios locais.
- Trabalhar com repositórios remotos no GitHub.
- Utilizar branches para desenvolvimento.
- Realizar merge e resolver conflitos.
- Compartilhar código utilizando GitHub.

## 🛠️ Pré-requisitos

Antes de começar, você precisa ter instalado:

- Git
- Uma conta no GitHub
- Um editor de código (VS Code, por exemplo)

Verifique se o Git está instalado:

```bash
git --version
```

## 🚀 Principais Comandos

### Configuração inicial

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### Criar um repositório

```bash
git init
```

### Verificar status

```bash
git status
```

### Adicionar arquivos

Adicionar um arquivo específico:

```bash
git add arquivo.txt
```

Adicionar todos os arquivos:

```bash
git add .
```

### Criar um commit

```bash
git commit -m "Mensagem do commit"
```

### Visualizar histórico

```bash
git log
```

Versão resumida:

```bash
git log --oneline
```

### Trabalhando com repositórios remotos

Adicionar um repositório remoto:

```bash
git remote add origin https://github.com/usuario/repositorio.git
```

Enviar alterações:

```bash
git push -u origin main
```

Baixar alterações:

```bash
git pull
```

Clonar um repositório:

```bash
git clone https://github.com/usuario/repositorio.git
```

## 🌿 Branches

Criar uma branch:

```bash
git branch nova-branch
```

Trocar de branch:

```bash
git checkout nova-branch
```

Criar e trocar ao mesmo tempo:

```bash
git checkout -b nova-branch
```

Listar branches:

```bash
git branch
```

Mesclar uma branch:

```bash
git merge nova-branch
```

## 📂 Estrutura do Repositório

```text
.
├── README.md
├── exemplos/
├── exercicios/
└── arquivos/
```

## 📖 Conteúdo da Aula

- Introdução ao Git
- Controle de versão
- Repositórios locais
- Commits
- Histórico de versões
- Branches
- Merge
- GitHub
- Clone, Push e Pull
- Boas práticas com Git

## 💡 Boas Práticas

- Faça commits pequenos e frequentes.
- Escreva mensagens de commit descritivas.
- Utilize branches para novas funcionalidades.
- Sempre sincronize o repositório antes de enviar alterações.
- Evite enviar arquivos desnecessários.

## 📚 Referências

- Documentação oficial do Git: https://git-scm.com/docs
- GitHub Docs: https://docs.github.com

## 👨‍🏫 Autor

Material desenvolvido para fins didáticos durante as aulas de Git e GitHub.