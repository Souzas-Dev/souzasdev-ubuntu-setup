import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

RAIZ = Path(__file__).resolve().parent.parent

if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from gui.windows.main_window import UbuntuSetup


def main():
    app = QApplication(sys.argv)
    janela = UbuntuSetup()
    janela.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
