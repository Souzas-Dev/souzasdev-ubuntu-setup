#!/usr/bin/env bash
# Souza's Dev — Ubuntu Setup v1.0
# Instala ferramentas essenciais APOS a instalacao definitiva do Ubuntu.
set -Eeuo pipefail

info() { printf '\n[Souzas Dev] %s\n' "$*"; }
falha() { printf '\n[ERRO] %s\n' "$*" >&2; exit 1; }

PACOTES=(
    ca-certificates curl wget git
    python3 python3-pip python3-venv
    build-essential openssh-client
    htop tree unzip zip jq pciutils
)

MODO_SIMULACAO=false

while (($# > 0)); do
    case "$1" in
        --dry-run)
            MODO_SIMULACAO=true
            ;;
        -h|--help)
            echo "Uso: bash scripts/setup-ubuntu.sh [--dry-run]"
            exit 0
            ;;
        *)
            falha "Opcao desconhecida: $1"
            ;;
    esac
    shift
done

if "$MODO_SIMULACAO"; then
    info "Modo simulacao ativado"
    printf '  sudo apt-get update\n'
    printf '  sudo apt-get upgrade -y\n'
    printf '  sudo apt-get install -y'
    printf ' %q' "${PACOTES[@]}"
    printf '\n'
    exit 0
fi

if [[ $EUID -eq 0 ]]; then
    falha "Execute como usuario normal (bash scripts/setup-ubuntu.sh), nao com sudo."
fi

if [[ ! -f /etc/os-release ]]; then
    falha "Nao foi possivel identificar o sistema operacional."
fi
# shellcheck source=/dev/null
source /etc/os-release
if [[ "${ID:-}" != "ubuntu" ]]; then
    falha "Este script foi preparado apenas para Ubuntu. Sistema detectado: ${ID:-desconhecido}."
fi

# Na sessao Live USB, a instalacao de programas nao sobrevive ao reboot.
if [[ -d /rofs ]] || grep -Eq '(/casper/vmlinuz|boot=casper)' /proc/cmdline; then
    falha "Voce esta no Ubuntu Live USB. Reinicie e execute no Ubuntu instalado no SSD."
fi

command -v apt-get >/dev/null 2>&1 || falha "apt-get nao encontrado."
command -v sudo >/dev/null 2>&1 || falha "sudo nao encontrado."

# Preparacao segura dos registros
command -v tee >/dev/null 2>&1 || falha "tee nao encontrado."

umask 077
LOG_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/souzasdev-ubuntu-setup"

mkdir -p -- "$LOG_DIR"
chmod 700 -- "$LOG_DIR"

LOG_FILE="$LOG_DIR/setup-$(date +%Y%m%d-%H%M%S)-$$.log"

# Tratamento de falhas
on_error() {
    local status="$1"
    local linha="$2"

    trap - ERR
    printf '\n[ERRO] Falha na linha %s (codigo %s).\n' "$linha" "$status" >&2
    printf '[ERRO] Consulte o log: %s\n' "$LOG_FILE" >&2

    exit "$status"
}

# Registra a saida no terminal e no arquivo
exec > >(tee -a "$LOG_FILE") 2>&1

trap 'on_error "$?" "$LINENO"' ERR

info "Log desta execucao: $LOG_FILE"

info "Ubuntu ${VERSION_ID:-} | Usuario: ${USER:-desconhecido}"
info "Pedindo permissao de administrador (sudo)..."
sudo -v

info "Atualizando a lista de pacotes..."
sudo apt-get update

info "Instalando atualizacoes disponiveis..."
sudo apt-get upgrade -y

info "Instalando ferramentas essenciais de desenvolvimento e suporte..."
sudo apt-get install -y "${PACOTES[@]}"

info "Verificando instalacoes..."
for programa in git python3 curl wget jq; do
    if command -v "$programa" >/dev/null 2>&1; then
        printf '  [OK] %s: %s\n' "$programa" "$(command -v "$programa")"
    else
        printf '  [ATENCAO] %s nao encontrado\n' "$programa"
    fi
done

info "Hardware de video (somente leitura):"
lspci | grep -Ei 'VGA|3D|Display' || true

info "Espaco livre no sistema:"
df -h /

if [[ -f /var/run/reboot-required ]]; then
    info "Reinicializacao recomendada para concluir as atualizacoes."
fi

info "Configuracao basica concluida!"
info "Proximos passos: configurar Git/GitHub e instalar Node.js / VS Code separadamente."
