import platform
from pathlib import Path

from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QIcon, QPixmap, QTextCursor
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from gui.widgets.logs_page import LogsPage


class UbuntuSetup(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Souzas Dev | Ubuntu Workstation Setup"
        )
        assets = Path(__file__).resolve().parent.parent / "assets"
        self.setWindowIcon(
            QIcon(str(assets / "souzas-dev-icon.png"))
        )
        self.resize(1000, 620)
        self.setMinimumSize(850, 520)

        self.menu_botoes = []
        self.paginas = QStackedWidget()

        self.criar_estrutura()
        self.configurar_processo()
        self.aplicar_estilo()
        self.abrir_pagina(0)

    def criar_estrutura(self):
        central = QWidget()
        self.setCentralWidget(central)

        estrutura = QHBoxLayout(central)
        estrutura.setContentsMargins(0, 0, 0, 0)
        estrutura.setSpacing(0)

        lateral = QFrame()
        lateral.setObjectName("sidebar")
        lateral.setFixedWidth(230)

        menu = QVBoxLayout(lateral)
        menu.setContentsMargins(18, 28, 18, 24)
        menu.setSpacing(10)

        marca = QLabel()
        logo = Path(__file__).resolve().parent.parent / "assets" / "souzas-dev-logo.png"
        imagem = QPixmap(str(logo))
        marca.setPixmap(
            imagem.scaledToWidth(
                180, Qt.TransformationMode.SmoothTransformation
            )
        )
        menu.addWidget(marca)

        produto = QLabel("Ubuntu Workstation Setup")
        produto.setObjectName("subtitulo")
        produto.setWordWrap(True)
        menu.addWidget(produto)

        menu.addSpacing(30)

        nomes = (
            "Visão geral",
            "Ferramentas",
            "Execução",
            "Logs",
        )

        for indice, nome in enumerate(nomes):
            botao = QPushButton(nome)
            botao.setObjectName("navButton")
            botao.setCheckable(True)

            botao.clicked.connect(
                lambda checked=False, i=indice:
                self.abrir_pagina(i)
            )

            menu.addWidget(botao)
            self.menu_botoes.append(botao)

        menu.addStretch()

        versao = QLabel("Protótipo | Modo seguro")
        versao.setObjectName("subtitulo")
        menu.addWidget(versao)

        estrutura.addWidget(lateral)
        estrutura.addWidget(self.paginas, 1)

        self.criar_dashboard()
        self.criar_ferramentas()
        self.criar_execucao()
        self.criar_logs()

    def pagina_base(self, titulo, descricao):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)

        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        cabecalho = QLabel(titulo)
        cabecalho.setObjectName("titulo")
        layout.addWidget(cabecalho)

        detalhe = QLabel(descricao)
        detalhe.setObjectName("subtitulo")
        detalhe.setWordWrap(True)
        layout.addWidget(detalhe)

        layout.addSpacing(12)
        self.paginas.addWidget(pagina)

        return layout

    def cartao(self, titulo, descricao):
        caixa = QFrame()
        caixa.setObjectName("card")

        layout = QVBoxLayout(caixa)
        layout.setContentsMargins(20, 18, 20, 18)

        nome = QLabel(titulo)
        nome.setObjectName("cartaoTitulo")

        detalhe = QLabel(descricao)
        detalhe.setObjectName("subtitulo")
        detalhe.setWordWrap(True)

        layout.addWidget(nome)
        layout.addWidget(detalhe)

        return caixa

    def criar_dashboard(self):
        layout = self.pagina_base(
            "Visão geral",
            "Acompanhe o ambiente e o estado da aplicação."
        )

        layout.addWidget(
            self.cartao(
                "Sistema detectado",
                platform.system()
            )
        )

        layout.addWidget(
            self.cartao(
                "Modo de operação",
                "Simulação segura | Nenhuma instalação real"
            )
        )

        layout.addWidget(
            self.cartao(
                "Motor de automação",
                "Bash | setup-ubuntu.sh"
            )
        )

        layout.addStretch()

    def criar_ferramentas(self):
        layout = self.pagina_base(
            "Ferramentas",
            "Pacotes utilizados pelo instalador Ubuntu."
        )

        layout.addWidget(
            self.cartao(
                "Desenvolvimento",
                "git, python3, python3-pip, build-essential"
            )
        )

        layout.addWidget(
            self.cartao(
                "Rede e diagnóstico",
                "curl, wget, openssh-client, pciutils"
            )
        )

        layout.addWidget(
            self.cartao(
                "Utilitários",
                "htop, tree, jq, unzip, zip"
            )
        )

        layout.addWidget(
            QLabel(
                "Lista informativa. A seleção de pacotes "
                "será implementada posteriormente."
            )
        )

        layout.addStretch()

    def criar_execucao(self):
        layout = self.pagina_base(
            "Execução",
            "Visualize a simulação real do script Bash."
        )

        self.botao = QPushButton("Visualizar simulação")
        self.botao.setObjectName("runButton")
        self.botao.clicked.connect(self.simular)

        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setPlaceholderText(
            "A saída do Bash aparecerá aqui."
        )

        layout.addWidget(self.botao)
        layout.addWidget(self.console, 1)

    def criar_logs(self):
        layout = self.pagina_base(
            "Logs",
            "Histórico de execuções e informações de diagnóstico."
        )

        self.logs_viewer = LogsPage()
        layout.addWidget(self.logs_viewer, 1)

    def configurar_processo(self):
        raiz = Path(__file__).resolve().parents[2]

        self.processo = QProcess(self)
        self.processo.setWorkingDirectory(str(raiz))

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

    def abrir_pagina(self, indice):
        self.paginas.setCurrentIndex(indice)

        for i, botao in enumerate(self.menu_botoes):
            botao.setChecked(i == indice)

    def simular(self):
        if self.processo.state() != QProcess.ProcessState.NotRunning:
            return

        raiz = Path(__file__).resolve().parents[2]
        script = raiz / "scripts" / "setup-ubuntu.sh"

        if not script.is_file():
            self.console.setPlainText(
                "[ERRO] Script Bash não encontrado."
            )
            return

        if platform.system() == "Windows":
            bash = Path(r"C:\Program Files\Git\bin\bash.exe")

            if not bash.is_file():
                self.console.setPlainText(
                    "[ERRO] Git Bash não encontrado."
                )
                return

            executavel = str(bash)
        else:
            executavel = "bash"

        self.abrir_pagina(2)

        self.console.setPlainText(
            "[SIMULAÇÃO SEGURA]\n"
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

        self.console.moveCursor(
            QTextCursor.MoveOperation.End
        )

        self.console.insertPlainText(
            dados.decode("utf-8", errors="replace")
        )

    def finalizar(self, codigo, estado):
        self.botao.setEnabled(True)

        if codigo == 0:
            self.console.appendPlainText(
                "\n[OK] Simulação concluída."
            )
        else:
            self.console.appendPlainText(
                f"\n[ERRO] Processo encerrado: {codigo}"
            )

    def erro_processo(self, erro):
        if erro == QProcess.ProcessError.FailedToStart:
            self.botao.setEnabled(True)
            self.console.appendPlainText(
                "\n[ERRO] Não foi possível iniciar o Bash."
            )

    def aplicar_estilo(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #141c2b;
                color: #e9eef6;
                font-size: 14px;
            }
            QLabel {
                background-color: transparent;
            }
            QFrame#sidebar {
                background-color: #0c1422;
                border-right: 1px solid #253249;
            }
            QLabel#marca {
                color: #60a5fa;
                font-size: 19px;
                font-weight: bold;
            }
            QLabel#titulo {
                font-size: 26px;
                font-weight: bold;
            }
            QLabel#subtitulo {
                color: #9eafc7;
            }
            QLabel#cartaoTitulo {
                font-size: 17px;
                font-weight: bold;
            }
            QFrame#card {
                background-color: #1d293b;
                border: 1px solid #34445b;
                border-radius: 10px;
            }
            QPushButton#navButton {
                text-align: left;
                background-color: transparent;
                border: none;
                border-radius: 8px;
                padding: 14px;
            }
            QPushButton#navButton:hover {
                background-color: #253550;
            }
            QPushButton#navButton:checked {
                background-color: #2563eb;
                font-weight: bold;
            }
            QPushButton#runButton {
                background-color: #2563eb;
                border-radius: 8px;
                padding: 13px;
                font-weight: bold;
            }
            QPushButton#runButton:hover {
                background-color: #3b82f6;
            }
            QPushButton#runButton:disabled {
                background-color: #475569;
            }
            QListWidget {
                background-color: #0b1220;
                border: 1px solid #34445b;
                border-radius: 8px;
                padding: 6px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 6px;
            }
            QListWidget::item:selected {
                background-color: #2563eb;
            }
            QPushButton#refreshButton {
                background-color: #2563eb;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: bold;
            }
            QPushButton#refreshButton:hover {
                background-color: #3b82f6;
            }
            QPlainTextEdit {
                background-color: #0b1220;
                border: 1px solid #34445b;
                border-radius: 8px;
                padding: 12px;
                font-family: Consolas, monospace;
            }
        """)
