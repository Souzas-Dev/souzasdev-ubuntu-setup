<div align="center">

# 🐧 Souzas Dev — Ubuntu Setup

**Automação em Bash para preparar o Ubuntu com ferramentas essenciais de desenvolvimento e suporte técnico.**

![Versão](https://img.shields.io/badge/vers%C3%A3o-v1.1.0-2563eb?style=flat-square)
![Bash](https://img.shields.io/badge/shell-Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white)
![Ubuntu](https://img.shields.io/badge/plataforma-Ubuntu-E95420?style=flat-square&logo=ubuntu&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20evolu%C3%A7%C3%A3o-64748b?style=flat-square)

[Funcionalidades](#-funcionalidades) · [Como usar](#-como-usar) · [Segurança](#-segurança-e-limitações) · [Roadmap](#-roadmap)

</div>

---

## 📌 Sobre o projeto

O **Ubuntu Setup** é um projeto de estudo e automação criado para facilitar a preparação inicial de um Ubuntu instalado. Em vez de configurar cada ferramenta manualmente, um script Bash reúne as principais etapas de atualização, instalação e verificação do ambiente.

O foco é **praticar Linux, Bash, Git/GitHub e fundamentos de suporte técnico** com um projeto real, documentado e versionado.

> **Versão atual: v1.1.0.** Esta versão inclui o modo de simulação e testes automatizados. Os aprimoramentos serão desenvolvidos em branches e revisados por Pull Requests.

## ✨ Funcionalidades

- Confirma que o sistema identificado é Ubuntu.
- Impede a execução como usuário `root` e tenta bloquear sessões Live USB.
- Atualiza o índice APT e **executa a atualização dos pacotes instalados**.
- Instala ferramentas essenciais para desenvolvimento e diagnóstico.
- Verifica a presença de alguns programas após a instalação.
- Exibe informações sobre a placa de vídeo e o espaço livre na partição principal.
- Informa quando o sistema recomenda reinicialização, **sem reiniciar automaticamente**.

### Ferramentas instaladas

| Categoria | Pacotes |
| --- | --- |
| Versionamento e transferência | `git`, `curl`, `wget`, `ca-certificates` |
| Python | `python3`, `python3-pip`, `python3-venv` |
| Desenvolvimento | `build-essential` |
| Acesso remoto | `openssh-client` |
| Diagnóstico e utilitários | `htop`, `tree`, `jq`, `pciutils`, `zip`, `unzip` |

## 🚀 Como usar

### 1. Pré-requisitos

- Ubuntu instalado (não execute a partir de uma sessão Live USB).
- Conexão com a internet e usuário com permissão para utilizar `sudo`.
- Git instalado para clonar o repositório.
- O repositório é público e pode ser clonado sem autenticação no GitHub.

Se precisar instalar o Git no Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y git
```

### 2. Clone o projeto

```bash
git clone https://github.com/Souzas-Dev/ubuntu-workstation-setup.git
cd ubuntu-workstation-setup
```

### 3. Leia e execute o script

Confira o conteúdo antes de executar, pois ele modifica pacotes do sistema:

```bash
cat scripts/setup-ubuntu.sh
bash scripts/setup-ubuntu.sh
```

O próprio script solicitará autorização via `sudo`. **Não execute com `sudo bash scripts/setup-ubuntu.sh`**, pois ele exige que o processo seja iniciado por um usuário comum.

### Modo de simulacao (--dry-run)

Antes de instalar ferramentas, podemos visualizar os comandos que seriam executados:

```bash
bash scripts/setup-ubuntu.sh --dry-run
```

A simulacao nao solicita sudo e nao modifica pacotes do sistema.

Para visualizar as opcoes:

```bash
bash scripts/setup-ubuntu.sh --help
```

### Testes automatizados

Execute:

```bash
bash tests/test-dry-run.sh
bash tests/test-logging.sh
```

Os testes verificam sintaxe, ajuda, simulacao e argumentos invalidos. Ainda nao substituem testes de integracao em Ubuntu.

## 📂 Estrutura do projeto

```text
ubuntu-workstation-setup/
├── scripts/
│   └── setup-ubuntu.sh       # Automação principal
├── docs/
│   └── guia-instalacao.md    # Passo a passo de execução
├── .gitignore                # Arquivos excluídos do Git
└── README.md                 # Apresentação do projeto
```

📖 [Guia completo de instalação](docs/guia-instalacao.md) · [Código-fonte do script](scripts/setup-ubuntu.sh) · [Marco inicial v1.0.0](https://github.com/Souzas-Dev/ubuntu-workstation-setup/tree/v1.0.0)

## 🛡️ Segurança e limitações

- Na **v1.0**, o comando `apt-get upgrade -y` é executado automaticamente. Atualizações podem alterar pacotes importantes; faça backup e revise o script antes de rodar.
- O script **não** particiona ou formata discos, modifica drivers de vídeo deliberadamente nem reinicia a máquina.
- A instalação exige privilégios administrativos para os comandos APT.
- Não armazene senhas, tokens, chaves privadas ou arquivos `.env` no repositório.
- O projeto inclui simulação, testes Bash e logs em desenvolvimento. A instalação real ainda não possui testes de integração.
- O uso previsto é em uma instalação Ubuntu. Outros ambientes, como Windows/Git Bash, não são adequados à instalação real; compatibilidade com WSL não foi validada.

## 📝 Logs e diagnóstico (v1.2.0 em desenvolvimento)

Durante uma execução real no Ubuntu, o script registra as mensagens
do terminal em arquivos locais para facilitar o diagnóstico.

**Diretório padrão:**

`~/.local/state/souzasdev-ubuntu-setup/`

O diretório pode ser alterado pela variável `XDG_STATE_HOME`.

### Funcionalidades

- Logs com data, hora e identificador do processo.
- Registro da saída padrão e de erros com `tee`.
- Identificação de falhas por linha e código de saída.
- Permissões restritas para diretórios e arquivos.
- `--dry-run` e `--help` sem criação de logs.

### Consultando os registros

```bash
ls -la ~/.local/state/souzasdev-ubuntu-setup/
tail -n 50 ~/.local/state/souzasdev-ubuntu-setup/*.log
```

### Limitações

O sistema de logs é inicializado após as verificações do ambiente.
Falhas anteriores a essa etapa podem não ser registradas.

Os registros podem conter informações do sistema. Revise seu
conteúdo antes de compartilhá-los.

Os testes atuais não executam instalações reais com APT.

---
## 🗺️ Roadmap

As próximas melhorias serão desenvolvidas separadamente, em branches próprias, com revisão antes da integração à `main`.

- [x] Modo `--dry-run` para simular comandos com segurança.
- [ ] Registros de execução (logs) e tratamento de erros mais detalhado.
- [x] Testes automatizados de sintaxe e comportamento básico.
- [ ] Instalação modular por grupos de ferramentas.
- [ ] Configurações opcionais para ambiente de desenvolvimento.

> O objetivo é evoluir o projeto gradualmente, entendendo cada alteração em vez de apenas automatizar tudo de uma vez.

## 🎯 Aprendizados trabalhados

**Bash e automação** · **Administração Linux** · **APT e permissões** · **Git e GitHub** · **Documentação técnica** · **Troubleshooting**

---

<div align="center">

Desenvolvido como projeto de estudos por **Souzas Dev**.

</div>
