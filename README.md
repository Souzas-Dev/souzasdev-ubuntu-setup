# Souza's Dev — Ubuntu Setup

**Versão 1.0** — Primeiro projeto de automação Bash para preparar o Ubuntu após uma instalação limpa.

## O que faz

- Verifica se o sistema é Ubuntu instalado de verdade (não a sessão Live USB).
- Atualiza a lista de pacotes e aplica atualizações disponíveis.
- Instala ferramentas essenciais: Git, Curl, Wget, Python 3, venv, pip, ferramentas de compilação, cliente SSH, htop, tree, zip/unzip, jq e pciutils.
- Exibe informações básicas da GPU e do espaço em disco.
- **Não** particiona, formata, altera drivers de vídeo ou reinicia automaticamente.

## Como usar no Ubuntu instalado

Abra um terminal dentro da pasta deste projeto e execute:

```bash
bash scripts/setup-ubuntu.sh
```

Você precisará da senha do usuário para autorizar o `sudo`. É necessária conexão com a internet.

**Não execute enquanto estiver testando o Ubuntu pelo pendrive.** O script bloqueia esse uso.

## O que ficou fora da versão 1

Node.js, VS Code, autenticação no GitHub e ferramentas de jogos serão configurados e documentados em etapas próprias. Assim mantemos o script básico, previsível e fácil de estudar.

## Estrutura

```text
souzasdev-ubuntu-setup/
├── scripts/
│   └── setup-ubuntu.sh
├── docs/
│   └── guia-instalacao.md
├── .gitignore
└── README.md
```

## Segurança

Leia o script antes de executar. Não inclua senhas, tokens ou arquivos `.env` no GitHub. A automação instala pacotes com privilégios administrativos, mas não modifica os discos deliberadamente.
