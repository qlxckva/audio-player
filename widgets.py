from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QPushButton, QSlider, QLabel, QLineEdit, QComboBox, QStyle,
    QDialog, QVBoxLayout, QMessageBox
)


class HoverButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setMinimumHeight(36)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        self.setStyleSheet("background-color: #cfe3ff;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("")
        super().leaveEvent(event)


# Небольшие классы кнопок оставлены, чтобы каждой кнопке задать свою надпись.
class PlayButton(HoverButton):
    def __init__(self):
        super().__init__("▶ Играть")

    def set_playing(self, playing):
        self.setText("⏸ Пауза" if playing else "▶ Играть")


class StopButton(HoverButton):
    def __init__(self):
        super().__init__("⏹ Стоп")


class NextButton(HoverButton):
    def __init__(self):
        super().__init__("⏭ Далее")


class PrevButton(HoverButton):
    def __init__(self):
        super().__init__("⏮ Назад")


class SeekSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setRange(0, 0)

    def mousePressEvent(self, event):
        if self.maximum() > 0:
            value = QStyle.sliderValueFromPosition(
                self.minimum(), self.maximum(), int(event.position().x()), self.width())
            self.setValue(value)
            self.sliderMoved.emit(value)
        super().mousePressEvent(event)


class VolumeSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setRange(0, 100)
        self.setValue(50)
        self.setFixedWidth(130)

    def wheelEvent(self, event):
        step = 5 if event.angleDelta().y() > 0 else -5
        self.setValue(self.value() + step)
        event.accept()


class TimeLabel(QLabel):
    def __init__(self):
        super().__init__("00:00 / 00:00")
        self.setMinimumWidth(110)
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    @staticmethod
    def format_ms(ms):
        seconds = ms // 1000
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def set_times(self, position, total):
        self.setText(f"{self.format_ms(position)} / {self.format_ms(total)}")


class TitleLabel(QLabel):
    def __init__(self):
        super().__init__("Ничего не играет")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("font-size: 16px; font-weight: bold; padding: 8px;")

    def set_track(self, track):
        self.setText(f"Сейчас играет: {track}")


class GenreCombo(QComboBox):
    def __init__(self, genres):
        super().__init__()
        self.setMinimumWidth(110)
        for genre in genres:
            self.addItem(str(genre))
        self.setCurrentIndex(-1)
        self.setPlaceholderText("Жанр")


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setFixedSize(280, 140)
        self.edit = QLineEdit("Student")
        self.edit.setPlaceholderText("Введите логин")
        self.button = HoverButton("Войти")
        self.button.clicked.connect(self.try_accept)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

    def try_accept(self):
        if not self.edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Логин не может быть пустым")
        else:
            self.accept()

    def get_login(self):
        return self.edit.text().strip()



