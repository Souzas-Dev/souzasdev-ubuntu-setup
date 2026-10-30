#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/scripts/setup-ubuntu.sh"
TEMP_DIR="$(mktemp -d)"

trap 'rm -rf -- "$TEMP_DIR"' EXIT

echo "[TESTE] Extraindo bloco de logging..."

awk '
  /^# Preparacao segura dos registros/ { inicio=1 }
  inicio && /^info "Ubuntu / { fim=1; exit }
  inicio { print }
  END { if (!inicio || !fim) exit 1 }
' "$SCRIPT" > "$TEMP_DIR/logging.sh"

esperar_log() {
    local diretorio="$1"
    local mensagem="$2"
    local arquivo=""

    for ((i=0; i<50; i++)); do
        arquivo="$(find "$diretorio" -name "*.log" -type f -print -quit 2>/dev/null || true)"

        if [[ -n "$arquivo" ]] && grep -q "$mensagem" "$arquivo"; then
            printf '%s\n' "$arquivo"
            return 0
        fi

        sleep 0.1
    done

    echo "[ERRO] Mensagem nao encontrada no log: $mensagem" >&2
    return 1
}

echo "[TESTE] Dry-run nao deve criar logs..."

XDG_STATE_HOME="$TEMP_DIR/simulacao" bash "$SCRIPT" --dry-run >/dev/null

[[ ! -e "$TEMP_DIR/simulacao" ]]

echo "[TESTE] Criacao de log..."

XDG_STATE_HOME="$TEMP_DIR/sucesso" bash -c '
    set -Eeuo pipefail
    info() { echo "[INFO] $*"; }
    falha() { echo "[ERRO] $*" >&2; exit 1; }
    source "$1"
    echo "LOG_TEST_OK"
' _ "$TEMP_DIR/logging.sh"

LOG_OK="$(esperar_log "$TEMP_DIR/sucesso" "LOG_TEST_OK")"

echo "[TESTE] Registro de falha..."

if XDG_STATE_HOME="$TEMP_DIR/falha" bash -c '
    set -Eeuo pipefail
    info() { echo "[INFO] $*"; }
    falha() { echo "[ERRO] $*" >&2; exit 1; }
    source "$1"
    echo "LOG_TEST_FALHA"
    false
' _ "$TEMP_DIR/logging.sh"; then
    echo "[ERRO] Falha simulada retornou sucesso!" >&2
    exit 1
fi

LOG_ERRO="$(esperar_log "$TEMP_DIR/falha" "Falha na linha")"

echo "[TESTE] Verificando permissoes..."

if [[ "$(uname -s)" == Linux* ]]; then
    [[ "$(stat -c %a "$LOG_OK")" == "600" ]]
    [[ "$(stat -c %a "$(dirname "$LOG_OK")")" == "700" ]]
else
    echo "[INFO] Permissoes Unix serao verificadas no CI Linux."
fi

echo "[OK] Testes de logging aprovados!"
