from datetime import datetime

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidgetItem,
    QFileDialog, QMessageBox, QListWidget
)

from models import Genre, GenreMap, Track
from report import SessionReport
from widgets import (
    PlayButton, StopButton, NextButton, PrevButton, SeekSlider, VolumeSlider,
    TimeLabel, TitleLabel, GenreCombo, HoverButton
)


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.genres = Genre.default_genres()  # Здесь создаются 10 объектов жанров.
        self.genre_map = GenreMap()
        self.tracks = []
        self.current = -1

        self.setWindowTitle("Аудиоплеер")
        self.resize(680, 520)
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.5)

        self.build_ui()
        self.connect_signals()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QVBoxLayout(central)

        top = QHBoxLayout()
        self.user_label = QLabel("Пользователь: " + self.user.login)
        self.add_btn = HoverButton("Добавить")
        self.sort_btn = HoverButton("Сортировать")
        for widget in (self.user_label, self.add_btn, self.sort_btn):
            top.addWidget(widget)
        main.addLayout(top)

        self.playlist = QListWidget()
        main.addWidget(self.playlist, 1)
        self.title_label = TitleLabel()
        main.addWidget(self.title_label)

        seek_row = QHBoxLayout()
        self.seek = SeekSlider()
        self.time_label = TimeLabel()
        seek_row.addWidget(self.seek, 1)
        seek_row.addWidget(self.time_label)
        main.addLayout(seek_row)

        controls = QHBoxLayout()
        self.prev_btn = PrevButton()
        self.play_btn = PlayButton()
        self.stop_btn = StopButton()
        self.next_btn = NextButton()
        self.volume = VolumeSlider()
        self.genre_box = GenreCombo(self.genres)
        for widget in (self.prev_btn, self.play_btn, self.stop_btn, self.next_btn):
            controls.addWidget(widget)
        controls.addStretch(1)
        controls.addWidget(QLabel("Громкость:"))
        controls.addWidget(self.volume)
        controls.addWidget(self.genre_box)
        main.addLayout(controls)

    def connect_signals(self):
        self.add_btn.clicked.connect(self.open_files)
        self.sort_btn.clicked.connect(self.sort_tracks)
        self.play_btn.clicked.connect(self.toggle_play)
        self.stop_btn.clicked.connect(self.stop_track)
        self.next_btn.clicked.connect(self.next_track)
        self.prev_btn.clicked.connect(self.prev_track)
        self.playlist.itemDoubleClicked.connect(self.play_item)
        self.playlist.currentRowChanged.connect(self.sync_genre_box)
        self.genre_box.activated.connect(self.set_genre)
        self.volume.valueChanged.connect(self.change_volume)
        self.seek.sliderMoved.connect(self.player.setPosition)
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(lambda duration: self.seek.setRange(0, duration))
        self.player.mediaStatusChanged.connect(self.on_status)

    def open_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Выберите аудио", "",
            "Audio (*.mp3 *.wav *.ogg *.flac *.m4a)")
        self.add_files(paths)

    def add_files(self, paths):
        for path in paths:
            if Track.is_audio(path):
                track = Track(path)
                if track not in self.tracks:
                    self.tracks.append(track)
                    self.playlist.addItem(QListWidgetItem(self.item_text(track)))

    def item_text(self, track):
        genre = self.genre_map.get(track.path)
        return str(track) if genre is None else f"{track} [{genre}]"

    def refresh_playlist(self):
        self.playlist.clear()
        for track in self.tracks:
            self.playlist.addItem(self.item_text(track))

    def sort_tracks(self):
        current_track = self.tracks[self.current] if self.current >= 0 else None
        self.tracks.sort()
        self.refresh_playlist()
        if current_track is not None:
            self.current = self.tracks.index(current_track)
            self.playlist.setCurrentRow(self.current)

    def set_genre(self, index):
        row = self.playlist.currentRow()
        if 0 <= row < len(self.tracks):
            self.genre_map.set(self.tracks[row].path, self.genres[index])
            self.playlist.item(row).setText(self.item_text(self.tracks[row]))

    def sync_genre_box(self, row):
        if 0 <= row < len(self.tracks):
            genre = self.genre_map.get(self.tracks[row].path)
            self.genre_box.setCurrentIndex(
                self.genres.index(genre) if genre in self.genres else -1)
        else:
            self.genre_box.setCurrentIndex(-1)

    def play_item(self, item):
        self.play_track(self.playlist.row(item))

    def play_track(self, index):
        if not 0 <= index < len(self.tracks):
            return
        self.current = index
        track = self.tracks[index]
        track.play_count += 1
        self.player.setSource(QUrl.fromLocalFile(track.path))
        self.player.play()
        self.title_label.set_track(track)
        self.playlist.setCurrentRow(index)
        self.play_btn.set_playing(True)

    def toggle_play(self):
        if not self.tracks:
            QMessageBox.information(self, "Плеер", "Сначала добавьте треки")
        elif self.current == -1:
            self.play_track(max(self.playlist.currentRow(), 0))
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
            self.play_track((self.current + 1) % len(self.tracks))

    def prev_track(self):
        if self.tracks:
            self.play_track((self.current - 1) % len(self.tracks))

    def change_volume(self, value):
        self.audio.setVolume(value / 100)

    def update_position(self, position):
        if not self.seek.isSliderDown():
            self.seek.setValue(position)
        self.time_label.set_times(position, self.player.duration())

    def on_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.next_track()

    def closeEvent(self, event):
        self.player.stop()
        self.user.time_out = datetime.now()
        SessionReport.write(self.user)
        event.accept()



