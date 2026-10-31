from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QSplitter,
)

from gui.services.log_service import (
    list_log_files,
    read_log_file,
    resolve_log_directory,
)


class LogsPage(QWidget):

    def __init__(self, log_directory=None, parent=None):
        super().__init__(parent)

        self.log_directory = (
            Path(log_directory)
            if log_directory is not None
            else resolve_log_directory()
        )

        self.criar_interface()
        self.refresh_logs()

    def criar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        cabecalho = QHBoxLayout()

        self.status_label = QLabel("Carregando registros...")
        self.status_label.setObjectName("logsStatus")

        self.refresh_button = QPushButton("Atualizar")
        self.refresh_button.setObjectName("refreshButton")
        self.refresh_button.clicked.connect(self.refresh_logs)

        cabecalho.addWidget(self.status_label, 1)
        cabecalho.addWidget(self.refresh_button)

        layout.addLayout(cabecalho)

        divisor = QSplitter(Qt.Orientation.Horizontal)

        self.log_list = QListWidget()
        self.log_list.setMinimumWidth(230)
        self.log_list.currentRowChanged.connect(
            self.show_selected_log
        )

        self.viewer = QPlainTextEdit()
        self.viewer.setReadOnly(True)
        self.viewer.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.NoWrap
        )
        self.viewer.setPlaceholderText(
            "Selecione um registro para visualizar seu conteúdo."
        )

        divisor.addWidget(self.log_list)
        divisor.addWidget(self.viewer)
        divisor.setStretchFactor(0, 1)
        divisor.setStretchFactor(1, 3)

        layout.addWidget(divisor, 1)

    def refresh_logs(self):
        selecionado = self.log_list.currentItem()

        caminho_selecionado = (
            selecionado.data(Qt.ItemDataRole.UserRole)
            if selecionado else None
        )

        self.log_list.clear()
        self.viewer.clear()

        try:
            registros = list_log_files(self.log_directory)

        except FileNotFoundError:
            self.status_label.setText(
                "Diretório de logs ainda não criado."
            )
            return

        except PermissionError:
            self.status_label.setText(
                "Sem permissão para acessar os registros."
            )
            return

        except OSError as erro:
            self.status_label.setText(
                f"Erro ao listar registros: {erro}"
            )
            return

        if not registros:
            self.status_label.setText(
                "Nenhum arquivo de log encontrado."
            )
            return

        for arquivo in registros:
            item = QListWidgetItem(arquivo.name)
            item.setData(
                Qt.ItemDataRole.UserRole,
                str(arquivo)
            )
            self.log_list.addItem(item)

        self.status_label.setText(
            f"{len(registros)} registro(s) encontrado(s)."
        )

        indice = 0

        if caminho_selecionado:
            for i in range(self.log_list.count()):
                item = self.log_list.item(i)

                if item.data(Qt.ItemDataRole.UserRole) == caminho_selecionado:
                    indice = i
                    break

        self.log_list.setCurrentRow(indice)

    def show_selected_log(self, indice):
        if indice < 0:
            return

        item = self.log_list.item(indice)

        if item is None:
            return

        arquivo = Path(
            item.data(Qt.ItemDataRole.UserRole)
        )

        try:
            conteudo = read_log_file(arquivo)

        except FileNotFoundError:
            self.viewer.setPlainText(
                "[AVISO] O arquivo não existe mais."
            )
            self.status_label.setText(
                "O registro selecionado não foi encontrado."
            )
            return

        except PermissionError:
            self.viewer.setPlainText(
                "[ERRO] Sem permissão para ler este arquivo."
            )
            self.status_label.setText(
                "Acesso ao registro negado."
            )
            return

        except OSError as erro:
            self.viewer.setPlainText(
                f"[ERRO] Não foi possível ler o registro:\n{erro}"
            )
            self.status_label.setText(
                "Falha durante a leitura."
            )
            return

        self.viewer.setPlainText(conteudo)

        self.status_label.setText(
            f"Registro selecionado: {arquivo.name}"
        )
