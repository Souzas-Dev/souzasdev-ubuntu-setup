# Guia de primeira execução — Ubuntu Setup v1.0

Este guia acompanha a **versão 1.0** do script. Antes de utilizá-lo, leia o código e faça backup dos arquivos importantes.

## 1. Prepare o ambiente

1. Termine a instalação do Ubuntu no disco e reinicie sem o pendrive de instalação.
2. Entre com um usuário comum que possa executar comandos com `sudo`.
3. Conecte-se à internet e abra o Terminal (`Ctrl+Alt+T`).
4. Instale o Git se necessário:

```bash
sudo apt-get update
sudo apt-get install -y git
```

## 2. Clone o repositório

```bash
git clone https://github.com/Souzas-Dev/souzasdev-ubuntu-setup.git
cd souzasdev-ubuntu-setup
```

> Se o repositório estiver privado, será necessário possuir acesso e autenticar-se no GitHub.

## 3. Revise antes de executar

```bash
cat scripts/setup-ubuntu.sh
```

**Atenção:** na v1.0, o script executa `sudo apt-get update`, `sudo apt-get upgrade -y` e instala os pacotes listados no README. A atualização pode alterar componentes do sistema. Ainda não existe opção `--dry-run`.

## 4. Execute a instalação

```bash
bash scripts/setup-ubuntu.sh
```

Digite sua senha quando o `sudo` solicitar. Não use `sudo bash scripts/setup-ubuntu.sh`: o script deve ser iniciado por um usuário comum.

## 5. Confira o resultado

```bash
git --version
python3 --version
df -h /
```

Se o Ubuntu recomendar reinicialização após as atualizações, reinicie manualmente.

## Observações

- Não execute na sessão Live USB, nem no Git Bash do Windows.
- O script não formata discos nem restaura backups.
- Node.js, VS Code e a autenticação GitHub não fazem parte da v1.0.
- Consulte o [README](../README.md) para limitações e próximas melhorias.
