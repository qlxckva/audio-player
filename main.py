import sys

from PySide6.QtWidgets import QApplication, QDialog

from main_window import MainWindow
from models import User
from widgets import LoginDialog


class PlayerApp:
    @staticmethod
    def run():
        app = QApplication(sys.argv)
        dialog = LoginDialog()
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        window = MainWindow(User(dialog.get_login()))
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    PlayerApp.run()
