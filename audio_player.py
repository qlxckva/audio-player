# Аудиоплеер, лабораторная/зачет по ООП
# pip install PySide6
import sys
import os
import random
from abc import ABC, abstractmethod
from datetime import datetime
from functools import total_ordering

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QListWidget, QListWidgetItem, QLineEdit,
    QComboBox, QFileDialog, QStyle, QMessageBox
)

TIME_FORMAT = "%d.%m.%Y %H:%M:%S"
if getattr(sys, "frozen", False):  # если запущено как exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_FILE = os.path.join(BASE_DIR, "report.txt")
AUDIO_EXT = (".mp3", ".wav", ".ogg", ".flac", ".m4a")


# ------------------------------------------------------------------
# Модели (сущности). Все наследуются от абстрактного класса Entity
# ------------------------------------------------------------------

@total_ordering
class Entity(ABC):
    """Абстрактный базовый класс для всех сущностей"""

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @abstractmethod
    def get_info(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self._name == other._name

    def __lt__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self._name.lower() < other._name.lower()

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return f"Entity({self._name!r})"

    def __str__(self):
        return self._name


@total_ordering
class Track(Entity):
    def __init__(self, path):
        title = os.path.splitext(os.path.basename(path))[0]
        super().__init__(title)
        self._path = path
        self._play_count = 0

    @property
    def title(self):
        return self._name

    @title.setter
    def title(self, value):
        self._name = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def play_count(self):
        return self._play_count

    @play_count.setter
    def play_count(self, value):
        if value < 0:
            value = 0
        self._play_count = value

    @staticmethod
    def is_audio(path):
        return path.lower().endswith(AUDIO_EXT)

    def get_info(self):
        return f"{self._name} | {self._path} | прослушиваний: {self._play_count}"

    # треки равны если одинаковый файл
    def __eq__(self, other):
        if not isinstance(other, Track):
            return NotImplemented
        return self._path == other._path

    def __lt__(self, other):
        if not isinstance(other, Track):
            return NotImplemented
        return self._name.lower() < other._name.lower()

    def __hash__(self):
        return hash(self._path)

    def __repr__(self):
        return f"Track(path={self._path!r}, plays={self._play_count})"

    def __str__(self):
        return self._name


@total_ordering
class Genre(Entity):
    NAMES = ["Rock", "Pop", "Jazz", "Classical", "Hip-Hop",
             "Electronic", "Metal", "Folk", "Blues", "Other"]

    def __init__(self, name):
        super().__init__(name)

    @staticmethod
    def default_genres():
        # 10 объектов жанров
        result = []
        for n in Genre.NAMES:
            result.append(Genre(n))
        return result

    def get_info(self):
        return f"Жанр: {self._name}"

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return NotImplemented
        return self._name == other._name

    def __hash__(self):
        return hash(("genre", self._name))

    def __repr__(self):
        return f"Genre({self._name!r})"

    def __str__(self):
        return self._name


@total_ordering
class User(Entity):
    def __init__(self, login):
        super().__init__(login)
        self._time_in = datetime.now()
        self._time_out = None

    @property
    def login(self):
        return self._name

    @login.setter
    def login(self, value):
        self._name = value

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self._name == other._name

    def __hash__(self):
        return hash(("user", self._name))

    def get_info(self):
        return f"Пользователь {self._name}, вошел {self._time_in.strftime(TIME_FORMAT)}"

    def __repr__(self):
        return f"User(login={self._name!r})"

    def __str__(self):
        return f"User: {self._name}"


class GenreMap:
    """Свой маппинг (вместо dict): путь к треку -> жанр"""

    def __init__(self):
        self._keys = []
        self._values = []

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, value):
        self._keys = value

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = value

    def set(self, key, value):
        if key in self._keys:
            i = self._keys.index(key)
            self._values[i] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def get(self, key):
        if key in self._keys:
            return self._values[self._keys.index(key)]
        return None

    def __len__(self):
        return len(self._keys)

    def __eq__(self, other):
        if not isinstance(other, GenreMap):
            return NotImplemented
        return self._keys == other._keys and self._values == other._values

    __hash__ = None

    def __repr__(self):
        return f"GenreMap(size={len(self._keys)})"

    def __str__(self):
        return f"GenreMap: {len(self._keys)} записей"


class SessionReport:
    """Отчет о работе приложения"""

    @staticmethod
    def write(user):
        t_in = user.time_in.strftime(TIME_FORMAT)
        t_out = user.time_out.strftime(TIME_FORMAT)
        w = max(len("login"), len(user.login))
        line = "+" + "-" * (w + 2) + "+" + "-" * 21 + "+" + "-" * 21 + "+"
        head = "| " + "login".ljust(w) + " | " + "time_in".ljust(19) + " | " + "time_out".ljust(19) + " |"
        row = "| " + user.login.ljust(w) + " | " + t_in + " | " + t_out + " |"
        sep = "|" + "-" * (w + 2) + "|" + "-" * 21 + "|" + "-" * 21 + "|"
        with open(REPORT_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n" + head + "\n" + sep + "\n" + row + "\n" + line + "\n\n")


# ------------------------------------------------------------------
# Переопределенные компоненты окна
# ------------------------------------------------------------------

class HoverButton(QPushButton):
    """Кнопка которая подсвечивается при наведении"""

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


class PlayButton(HoverButton):
    def __init__(self):
        super().__init__("▶ Играть")

    def set_playing(self, flag):
        if flag:
            self.setText("⏸ Пауза")
        else:
            self.setText("▶ Играть")


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
    """Ползунок перемотки, по клику прыгает в нужное место"""

    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setRange(0, 0)

    def mousePressEvent(self, event):
        if self.maximum() > 0:
            v = QStyle.sliderValueFromPosition(
                self.minimum(), self.maximum(), int(event.position().x()), self.width())
            self.setValue(v)
            self.sliderMoved.emit(v)
        super().mousePressEvent(event)


class VolumeSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setRange(0, 100)
        self.setValue(50)
        self.setFixedWidth(130)

    def wheelEvent(self, event):
        # колесиком меняем громкость на 5
        if event.angleDelta().y() > 0:
            self.setValue(self.value() + 5)
        else:
            self.setValue(self.value() - 5)
        event.accept()


class TimeLabel(QLabel):
    def __init__(self):
        super().__init__("00:00 / 00:00")
        self.setMinimumWidth(110)
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    @staticmethod
    def format_ms(ms):
        sec = ms // 1000
        return f"{sec // 60:02d}:{sec % 60:02d}"

    def set_times(self, pos, total):
        self.setText(TimeLabel.format_ms(pos) + " / " + TimeLabel.format_ms(total))


class TitleLabel(QLabel):
    def __init__(self):
        super().__init__("Ничего не играет")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("font-size: 16px; font-weight: bold; padding: 8px;")

    def set_track(self, track):
        self.setText("Сейчас играет: " + str(track))


class SearchEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Поиск по плейлисту... (Esc - очистить)")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.clear()
        else:
            super().keyPressEvent(event)


class GenreCombo(QComboBox):
    def __init__(self, genres):
        super().__init__()
        self.setMinimumWidth(110)
        for g in genres:
            self.addItem(str(g))
        self.setCurrentIndex(-1)
        self.setPlaceholderText("Жанр")


class PlaylistWidget(QListWidget):
    """Список треков, умеет принимать файлы перетаскиванием"""
    files_dropped = Signal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            paths = []
            for url in event.mimeData().urls():
                paths.append(url.toLocalFile())
            self.files_dropped.emit(paths)
            event.acceptProposedAction()


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setFixedSize(280, 140)

        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Введите логин")
        self.edit.setText("Student")
        self.btn = HoverButton("Войти")
        self.btn.clicked.connect(self.try_accept)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.edit)
        layout.addWidget(self.btn)

    def try_accept(self):
        if self.edit.text().strip() == "":
            QMessageBox.warning(self, "Ошибка", "Логин не может быть пустым")
            return
        self.accept()

    def get_login(self):
        return self.edit.text().strip()


# ------------------------------------------------------------------
# Главное окно
# ------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self._user = user
        self._genres = Genre.default_genres()
        self._genre_map = GenreMap()
        self._tracks = []
        self._current = -1

        self.setWindowTitle("Audio Player")
        self.resize(680, 520)

        # плеер
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.5)

        self.build_ui()
        self.connect_signals()

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, value):
        self._genres = value

    @property
    def genre_map(self):
        return self._genre_map

    @genre_map.setter
    def genre_map(self, value):
        self._genre_map = value

    @property
    def tracks(self):
        return self._tracks

    @tracks.setter
    def tracks(self, value):
        self._tracks = value

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        self._current = value

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QVBoxLayout(central)

        # верхняя строка
        top = QHBoxLayout()
        self.user_label = QLabel("Пользователь: " + self.user.login)
        self.search = SearchEdit()
        self.add_btn = HoverButton("➕ Добавить")
        self.sort_btn = HoverButton("Сортировать")
        self.shuffle_btn = HoverButton("🔀 Перемешать")
        top.addWidget(self.user_label)
        top.addWidget(self.search, 1)
        top.addWidget(self.add_btn)
        top.addWidget(self.sort_btn)
        top.addWidget(self.shuffle_btn)
        main.addLayout(top)

        # список
        self.playlist = PlaylistWidget()
        main.addWidget(self.playlist, 1)

        # название
        self.title_label = TitleLabel()
        main.addWidget(self.title_label)

        # перемотка
        seek_row = QHBoxLayout()
        self.seek = SeekSlider()
        self.time_label = TimeLabel()
        seek_row.addWidget(self.seek, 1)
        seek_row.addWidget(self.time_label)
        main.addLayout(seek_row)

        # управление
        ctrl = QHBoxLayout()
        self.prev_btn = PrevButton()
        self.play_btn = PlayButton()
        self.stop_btn = StopButton()
        self.next_btn = NextButton()
        self.volume = VolumeSlider()
        self.genre_box = GenreCombo(self.genres)
        ctrl.addWidget(self.prev_btn)
        ctrl.addWidget(self.play_btn)
        ctrl.addWidget(self.stop_btn)
        ctrl.addWidget(self.next_btn)
        ctrl.addStretch(1)
        ctrl.addWidget(QLabel("Громкость:"))
        ctrl.addWidget(self.volume)
        ctrl.addWidget(self.genre_box)
        main.addLayout(ctrl)

    def connect_signals(self):
        self.add_btn.clicked.connect(self.open_files)
        self.sort_btn.clicked.connect(self.sort_tracks)
        self.shuffle_btn.clicked.connect(self.shuffle_tracks)
        self.play_btn.clicked.connect(self.toggle_play)
        self.stop_btn.clicked.connect(self.stop_track)
        self.next_btn.clicked.connect(self.next_track)
        self.prev_btn.clicked.connect(self.prev_track)
        self.playlist.itemDoubleClicked.connect(self.on_item_double)
        self.playlist.files_dropped.connect(self.add_files)
        self.playlist.currentRowChanged.connect(self.sync_genre_box)
        self.search.textChanged.connect(self.filter_playlist)
        self.genre_box.activated.connect(self.set_genre)
        self.volume.valueChanged.connect(self.change_volume)
        self.seek.sliderMoved.connect(self.player.setPosition)
        self.player.positionChanged.connect(self.on_position)
        self.player.durationChanged.connect(self.on_duration)
        self.player.mediaStatusChanged.connect(self.on_status)

    # ---------- работа с плейлистом ----------

    def open_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Выберите аудио", "", "Audio (*.mp3 *.wav *.ogg *.flac *.m4a)")
        self.add_files(files)

    def add_files(self, paths):
        for p in paths:
            if not Track.is_audio(p):
                continue
            t = Track(p)
            if t in self.tracks:  # использует __eq__
                continue
            self.tracks.append(t)
            self.playlist.addItem(QListWidgetItem(self.item_text(t)))

    def item_text(self, track):
        g = self.genre_map.get(track.path)
        if g is None:
            return str(track)
        return f"{track}  [{g}]"

    def refresh_items(self):
        self.playlist.clear()
        for t in self.tracks:
            self.playlist.addItem(QListWidgetItem(self.item_text(t)))

    def sort_tracks(self):
        if not self.tracks:
            return
        cur_track = None
        if self.current != -1:
            cur_track = self.tracks[self.current]
        self.tracks.sort()  # работает через __lt__
        if cur_track is not None:
            self.current = self.tracks.index(cur_track)
        self.refresh_items()
        if self.current != -1:
            self.playlist.setCurrentRow(self.current)

    def shuffle_tracks(self):
        if len(self.tracks) < 2:
            return
        cur_track = None
        if self.current != -1:
            cur_track = self.tracks[self.current]
        random.shuffle(self.tracks)  # перемешиваем список
        if cur_track is not None:
            self.current = self.tracks.index(cur_track)
        self.refresh_items()
        if self.current != -1:
            self.playlist.setCurrentRow(self.current)

    def filter_playlist(self, text):
        text = text.lower()
        for i in range(self.playlist.count()):
            item = self.playlist.item(i)
            item.setHidden(text not in item.text().lower())

    def set_genre(self, index):
        row = self.playlist.currentRow()
        if row < 0 or row >= len(self.tracks):
            return
        self.genre_map.set(self.tracks[row].path, self.genres[index])
        self.playlist.item(row).setText(self.item_text(self.tracks[row]))

    def sync_genre_box(self, row):
        if row < 0 or row >= len(self.tracks):
            self.genre_box.setCurrentIndex(-1)
            return
        g = self.genre_map.get(self.tracks[row].path)
        if g is None:
            self.genre_box.setCurrentIndex(-1)
        else:
            self.genre_box.setCurrentIndex(self.genres.index(g))

    # ---------- управление воспроизведением ----------

    def on_item_double(self, item):
        self.play_index(self.playlist.row(item))

    def play_index(self, i):
        if i < 0 or i >= len(self.tracks):
            return
        self.current = i
        track = self.tracks[i]
        track.play_count += 1
        self.player.setSource(QUrl.fromLocalFile(track.path))
        self.player.play()
        self.title_label.set_track(track)
        self.playlist.setCurrentRow(i)
        self.play_btn.set_playing(True)

    def toggle_play(self):
        if not self.tracks:
            QMessageBox.information(self, "Плеер", "Сначала добавьте треки")
            return
        if self.current == -1:
            self.play_index(max(self.playlist.currentRow(), 0))
        elif self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.play_btn.set_playing(False)
        else:
            self.player.play()
            self.play_btn.set_playing(True)

    def stop_track(self):
        self.player.stop()
        self.play_btn.set_playing(False)

    def next_track(self):
        if self.tracks:
            self.play_index((self.current + 1) % len(self.tracks))

    def prev_track(self):
        if self.tracks:
            self.play_index((self.current - 1) % len(self.tracks))

    def change_volume(self, value):
        self.audio.setVolume(value / 100)

    def on_position(self, pos):
        if not self.seek.isSliderDown():
            self.seek.setValue(pos)
        self.time_label.set_times(pos, self.player.duration())

    def on_duration(self, dur):
        self.seek.setRange(0, dur)

    def on_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.next_track()

    # ---------- закрытие ----------

    def closeEvent(self, event):
        self.player.stop()
        self.user.time_out = datetime.now()
        SessionReport.write(self.user)
        event.accept()


class PlayerApp:
    """Запуск приложения (вся логика внутри класса)"""

    @staticmethod
    def run():
        app = QApplication(sys.argv)

        dialog = LoginDialog()
        if dialog.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)

        user = User(dialog.get_login())
        window = MainWindow(user)
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    PlayerApp.run()
