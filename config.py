from pathlib import Path

TIME_FORMAT = "%d.%m.%Y %H:%M:%S"
BASE_DIR = Path(__file__).resolve().parent
REPORT_FILE = BASE_DIR / "report.txt"
AUDIO_EXT = (".mp3", ".wav", ".ogg", ".flac", ".m4a")
