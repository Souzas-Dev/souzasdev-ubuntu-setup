#!/usr/bin/env bash
set -euo pipefail

SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/scripts/setup-ubuntu.sh"

echo "[TESTE] Verificando sintaxe..."
bash -n "$SCRIPT"

echo "[TESTE] Verificando ajuda..."
AJUDA="$(bash "$SCRIPT" --help)"
[[ "$AJUDA" == *"--dry-run"* ]]

echo "[TESTE] Verificando simulacao..."
SAIDA="$(bash "$SCRIPT" --dry-run)"

[[ "$SAIDA" == *"sudo apt-get update"* ]]
[[ "$SAIDA" == *"sudo apt-get upgrade -y"* ]]
[[ "$SAIDA" == *"sudo apt-get install -y"* ]]
[[ "$SAIDA" == *"git python3"* ]]

echo "[TESTE] Verificando argumentos invalidos..."
if bash "$SCRIPT" --invalido > /dev/null 2>&1; then
    echo "[ERRO] Argumento invalido foi aceito!"
    exit 1
fi

echo "[OK] Todos os testes passaram!"
