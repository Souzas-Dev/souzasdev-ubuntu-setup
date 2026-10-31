import os
import sys
import tempfile

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from unittest.mock import patch

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from gui.services.log_service import (
    resolve_log_directory,
    list_log_files,
    read_log_file,
)

from gui.widgets.logs_page import LogsPage


def testar_diretorio():
    print("[TESTE] Resolução do diretório...")

    home = Path("/home/teste")

    assert resolve_log_directory(
        {"XDG_STATE_HOME": "/tmp/estado"},
        home,
    ) == Path("/tmp/estado/souzasdev-ubuntu-setup")

    assert resolve_log_directory(
        {"XDG_STATE_HOME": ""},
        home,
    ) == home / ".local/state/souzasdev-ubuntu-setup"


def testar_registros():
    print("[TESTE] Listagem e ordenação...")

    with tempfile.TemporaryDirectory() as temporario:
        pasta = Path(temporario)

        antigo = pasta / "setup-antigo.log"
        recente = pasta / "setup-recente.log"

        antigo.write_text("Registro antigo", encoding="utf-8")
        recente.write_text("Registro recente", encoding="utf-8")

        os.utime(antigo, (100, 100))
        os.utime(recente, (200, 200))

        arquivos = list_log_files(pasta)

        assert arquivos == [recente, antigo]

        assert read_log_file(recente) == "Registro recente"

        print("[OK] Listagem e leitura aprovadas.")


def testar_leitura_segura():
    print("[TESTE] Limites e segurança da leitura...")

    with tempfile.TemporaryDirectory() as temporario:
        pasta = Path(temporario)

        # Limite de leitura
        grande = pasta / "setup-grande.log"
        grande.write_bytes(b"0123456789ABCDEF")

        conteudo = read_log_file(grande, max_bytes=10)

        assert conteudo.startswith("[AVISO]")
        assert conteudo.endswith("6789ABCDEF")

        # UTF-8 inválido
        invalido = pasta / "setup-utf8-invalido.log"
        invalido.write_bytes(b"antes\xffdepois")

        assert read_log_file(invalido) == "antes\uFFFDdepois"

        # Arquivo inexistente
        try:
            read_log_file(pasta / "setup-ausente.log")
        except FileNotFoundError:
            pass
        else:
            raise AssertionError(
                "Arquivo inexistente deveria gerar erro."
            )

        # Limite inválido
        try:
            read_log_file(grande, max_bytes=0)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Limite zero deveria gerar erro."
            )

    print("[OK] Limites e leitura segura aprovados.")


def testar_interface(app):
    print("[TESTE] Interface de logs...")

    with tempfile.TemporaryDirectory() as temporario:
        raiz = Path(temporario)
        pasta = raiz / "logs"
        pasta.mkdir()

        antigo = pasta / "setup-antigo.log"
        recente = pasta / "setup-recente.log"

        antigo.write_text("Conteúdo antigo", encoding="utf-8")
        recente.write_text("Conteúdo recente", encoding="utf-8")

        os.utime(antigo, (100, 100))
        os.utime(recente, (200, 200))

        pagina = LogsPage(log_directory=pasta)

        assert pagina.log_list.count() == 2
        assert pagina.log_list.item(0).text() == "setup-recente.log"
        assert "Conteúdo recente" in pagina.viewer.toPlainText()

        # Atualização da lista
        novo = pasta / "setup-novo.log"
        novo.write_text("Novo registro", encoding="utf-8")
        os.utime(novo, (300, 300))

        pagina.refresh_logs()

        assert pagina.log_list.item(0).text() == "setup-novo.log"

        # Preservar registro selecionado durante atualização
        assert pagina.log_list.currentItem() is not None

        assert (
            pagina.log_list.currentItem().text()
            == "setup-recente.log"
        ), "A atualização não preservou o registro selecionado."

        # Arquivo removido após a listagem
        indice_antigo = next(
            i for i in range(pagina.log_list.count())
            if pagina.log_list.item(i).text() == "setup-antigo.log"
        )

        arquivo_removido = Path(
            pagina.log_list.item(indice_antigo).data(
                Qt.ItemDataRole.UserRole
            )
        )

        arquivo_removido.unlink()

        pagina.show_selected_log(indice_antigo)

        assert (
            "não existe mais" in pagina.viewer.toPlainText()
        ), "A interface não identificou o arquivo removido."

        # Diretório sem registros
        vazio = raiz / "vazio"
        vazio.mkdir()

        pagina_vazia = LogsPage(log_directory=vazio)

        assert "Nenhum arquivo" in pagina_vazia.status_label.text()

        # Diretório inexistente
        pagina_ausente = LogsPage(log_directory=raiz / "ausente")

        assert "não criado" in pagina_ausente.status_label.text()

        # Falha de permissão na listagem
        with patch(
            "gui.widgets.logs_page.list_log_files",
            side_effect=PermissionError("acesso negado"),
        ):
            pagina.refresh_logs()

        assert "permissão" in pagina.status_label.text().lower()

        # Falha de permissão na leitura
        pagina.refresh_logs()
        pagina.log_list.setCurrentRow(-1)

        with patch(
            "gui.widgets.logs_page.read_log_file",
            side_effect=PermissionError("acesso negado"),
        ):
            pagina.log_list.setCurrentRow(0)

        assert "permissão" in pagina.viewer.toPlainText().lower()

        pagina.close()
        pagina_vazia.close()
        pagina_ausente.close()

    print("[OK] Interface e tratamento de erros aprovados.")


if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    app = QApplication.instance() or QApplication([])

    testar_diretorio()
    testar_registros()
    testar_leitura_segura()
    testar_interface(app)

    app.quit()

    print("[OK] Todos os testes de logs passaram!")
