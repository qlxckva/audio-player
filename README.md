# Audio Player

Десктопное приложение — аудиоплеер на Python и PySide6.
Учебный проект по дисциплине «ООП».

**Автор:** Волошин Денис Артемович, 201 группа

## Возможности

- Вход по логину
- Плейлист: добавление файлов кнопкой или перетаскиванием, дубликаты не добавляются
- Воспроизведение: play / пауза, стоп, следующий и предыдущий трек, перемотка, громкость
- Сортировка плейлиста по названию и случайное перемешивание
- Поиск по плейлисту
- Жанры для треков
- Отчёт о работе: при закрытии приложения в `report.txt` дописывается строка
  `login | time_in | time_out`

## Скриншоты
[Окно входа]
<img width="274" height="164" alt="image" src="https://github.com/user-attachments/assets/e9af31f8-0686-4bae-8c66-f52a4c0a09ba" />

[Главное окно]
<img width="679" height="546" alt="image" src="https://github.com/user-attachments/assets/bc9f1e9c-4d90-441a-8156-359ce9fc03a7" />

[Отчёт] 
<img width="598" height="644" alt="image" src="https://github.com/user-attachments/assets/09e8c830-7971-490e-b4de-12494b088e88" />


## Запуск из исходного кода

```
pip install -r requirements.txt
python audio_player.py
```

Нужен Python 3.9 или новее.

## Запуск готовой программы (Windows)

Скачайте `AudioPlayer.exe` из раздела **Releases** и запустите. Python не нужен.

## Сборка exe самостоятельно

Запустите `build.bat` (или выполните команды из него вручную).
Готовый файл появится в папке `dist`.

## Структура кода

| Класс | Назначение |
|---|---|
| `Entity` (абстрактный) | базовый класс сущностей |
| `Track`, `Genre`, `User` | модели данных |
| `GenreMap` | собственный маппинг вместо `dict` |
| `SessionReport` | запись отчёта о работе |
| `HoverButton`, `PlayButton`, `StopButton`, `NextButton`, `PrevButton`, `SeekSlider`, `VolumeSlider`, `TimeLabel`, `TitleLabel`, `SearchEdit`, `GenreCombo`, `PlaylistWidget`, `LoginDialog` | переопределённые компоненты Qt |
| `MainWindow` | главное окно |
| `PlayerApp` | запуск приложения |
