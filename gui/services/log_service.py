import os
from pathlib import Path
from collections.abc import Mapping

LOG_DIRECTORY = "souzasdev-ubuntu-setup"
MAX_LOG_BYTES = 1_000_000


def resolve_log_directory(
    environ: Mapping[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    env = os.environ if environ is None else environ

    xdg_state_home = env.get("XDG_STATE_HOME")

    if xdg_state_home:
        state_home = Path(xdg_state_home).expanduser()
    else:
        home_dir = Path(home) if home is not None else Path.home()
        state_home = home_dir / ".local" / "state"

    return state_home / LOG_DIRECTORY


def list_log_files(directory: Path | str | None = None) -> list[Path]:
    target = Path(directory) if directory is not None else resolve_log_directory()

    registros = []

    with os.scandir(target) as arquivos:
        for arquivo in arquivos:
            if not (
                arquivo.name.startswith("setup-")
                and arquivo.name.endswith(".log")
            ):
                continue

            try:
                if not arquivo.is_file(follow_symlinks=False):
                    continue

                metadata = arquivo.stat(follow_symlinks=False)

            except FileNotFoundError:
                continue

            registros.append(
                (metadata.st_mtime_ns, arquivo.name, Path(arquivo.path))
            )

    registros.sort(key=lambda item: (item[0], item[1]), reverse=True)

    return [item[2] for item in registros]


def read_log_file(
    path: Path | str,
    max_bytes: int = MAX_LOG_BYTES,
) -> str:
    if max_bytes < 1:
        raise ValueError("max_bytes deve ser maior que zero.")

    arquivo = Path(path)

    with arquivo.open("rb") as stream:
        stream.seek(0, os.SEEK_END)
        tamanho = stream.tell()

        truncado = tamanho > max_bytes

        if truncado:
            stream.seek(-max_bytes, os.SEEK_END)
        else:
            stream.seek(0)

        conteudo = stream.read(max_bytes)

    texto = conteudo.decode("utf-8", errors="replace")

    if truncado:
        texto = (
            "[AVISO] Exibindo somente a parte final do arquivo.\n\n"
            + texto
        )

    return texto
