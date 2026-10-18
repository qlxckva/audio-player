@echo off
rem Sborka exe. Zapuskat dvojnym klikom na Windows.
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name AudioPlayer audio_player.py
echo.
echo Gotovo! Programma lezhit v papke dist\AudioPlayer.exe
pause
