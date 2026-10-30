import os
import sys
from pathlib import Path

# Permite testar a GUI sem abrir uma janela
os.environ["QT_QPA_PLATFORM"] = "offscreen"

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from PySide6.QtCore import QEventLoop, QProcess, QTimer
from PySide6.QtWidgets import QApplication

from gui.main import UbuntuSetup


def testar_interface():
    print("[TESTE] Inicializando interface...")

    app = QApplication.instance() or QApplication([])
    janela = UbuntuSetup()

    assert "Ubuntu Workstation Setup" in janela.windowTitle()
    assert janela.console.isReadOnly()
    assert janela.paginas.count() == 4

    for indice, botao in enumerate(janela.menu_botoes):
        botao.click()
        assert janela.paginas.currentIndex() == indice

    print("[TESTE] Executando simulacao Bash...")

    loop = QEventLoop()

    janela.processo.finished.connect(
        lambda *_: loop.quit()
    )
    janela.processo.errorOccurred.connect(
        lambda *_: loop.quit()
    )

    janela.botao.click()

    QTimer.singleShot(15000, loop.quit)
    loop.exec()

    assert (
        janela.processo.state()
        == QProcess.ProcessState.NotRunning
    ), "Processo nao terminou dentro do limite."

    assert janela.processo.exitCode() == 0, (
        "Simulacao Bash falhou."
    )

    saida = janela.console.toPlainText()

    assert "[SIMULAÇÃO SEGURA]" in saida
    assert "sudo apt-get update" in saida
    assert "sudo apt-get install -y" in saida
    assert "[OK] Simulação concluída." in saida
    assert janela.botao.isEnabled()

    janela.close()
    app.quit()

    print("[OK] Teste da interface aprovado!")


if __name__ == "__main__":
    testar_interface()
