import sys
import platform
from pathlib import Path
from PySide6.QtCore import QProcess
from PySide6.QtGui import QTextCursor

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QPlainTextEdit,
)

class UbuntuSetup(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Souzas Dev | Ubuntu Workstation Setup")
        self.resize(800, 520)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(18)
        layout.setContentsMargins(30, 30, 30, 30)

        titulo = QLabel("Ubuntu Workstation Setup")
        titulo.setObjectName("titulo")

        subtitulo = QLabel("Souzas Dev | Assistente de configuracao")
        subtitulo.setObjectName("subtitulo")

        sistema = QLabel(
            f"Ambiente detectado: {platform.system()}"
        )

        descricao = QLabel(
            "Primeiro prototipo da interface grafica. "
            "Nenhum pacote sera instalado."
        )
        descricao.setWordWrap(True)

        botao = QPushButton("Visualizar simulacao")

        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setPlaceholderText(
            "Os comandos simulados aparecerao aqui."
        )

        self.botao = botao

        self.processo = QProcess(self)
        self.processo.setWorkingDirectory(
            str(Path(__file__).resolve().parent.parent)
        )
        self.processo.setProcessChannelMode(
            QProcess.ProcessChannelMode.MergedChannels
        )
        self.processo.readyReadStandardOutput.connect(
            self.ler_saida
        )
        self.processo.finished.connect(
            self.finalizar
        )
        self.processo.errorOccurred.connect(
            self.erro_processo
        )

        botao.clicked.connect(self.simular)

        for item in (
            titulo, subtitulo, sistema,
            descricao, botao, self.console
        ):
            layout.addWidget(item)

        self.setCentralWidget(container)

        self.setStyleSheet("""
            QWidget {
                background-color: #151d2b;
                color: #e9eef6;
                font-size: 14px;
            }
            QLabel#titulo {
                font-size: 25px;
                font-weight: bold;
            }
            QLabel#subtitulo {
                color: #9aacc3;
            }
            QPushButton {
                background-color: #2563eb;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3b82f6;
            }
            QPlainTextEdit {
                background-color: #0c1320;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 12px;
                font-family: Consolas, monospace;
            }
        """)

    def simular(self):
        raiz = Path(__file__).resolve().parent.parent
        script = raiz / "scripts" / "setup-ubuntu.sh"

        if not script.is_file():
            self.console.setPlainText(
                "[ERRO] Script Bash nao encontrado."
            )
            return

        if platform.system() == "Windows":
            bash = Path(r"C:\Program Files\Git\bin\bash.exe")

            if not bash.is_file():
                self.console.setPlainText(
                    "[ERRO] Git Bash nao encontrado."
                )
                return

            executavel = str(bash)
        else:
            executavel = "bash"

        self.console.setPlainText(
            "[SIMULACAO SEGURA]\n"
            "Executando o modo --dry-run...\n\n"
        )

        self.botao.setEnabled(False)

        self.processo.start(
            executavel,
            ["scripts/setup-ubuntu.sh", "--dry-run"]
        )

    def ler_saida(self):
        dados = bytes(
            self.processo.readAllStandardOutput()
        )

        self.console.moveCursor(QTextCursor.MoveOperation.End)
        self.console.insertPlainText(
            dados.decode("utf-8", errors="replace")
        )

    def finalizar(self, codigo, estado):
        self.botao.setEnabled(True)

        if codigo == 0:
            self.console.appendPlainText(
                "\n[OK] Simulacao concluida."
            )
        else:
            self.console.appendPlainText(
                f"\n[ERRO] Processo encerrado: {codigo}"
            )

    def erro_processo(self, erro):
        if erro == QProcess.ProcessError.FailedToStart:
            self.botao.setEnabled(True)
            self.console.appendPlainText(
                "\n[ERRO] Nao foi possivel iniciar o Bash."
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = UbuntuSetup()
    janela.show()
    sys.exit(app.exec())
